"""Parser de nombres de archivo según nomenclatura DAM v3.2.

Fórmula: IDENTIFICADOR_TIPO_SERIE.ext
Ejemplos: 401275_PK_01.jpg, SOLAR_KV_02.jpg, 401275_VCN_01.mp4
"""

import os
import re
from dataclasses import dataclass

from .config import (
    IMAGE_EXTENSIONS,
    LEGACY_MAP,
    METADATA_MAP,
    VALID_EXTENSIONS,
    VIDEO_EXTENSIONS,
)


@dataclass
class ParsedAsset:
    """Resultado del parsing de un nombre de archivo."""
    identifier: str      # ID de producto/variante/tema (ej: "401275", "SOLAR")
    type_code: str       # Código de tipo (ej: "PK", "KV", "VMK")
    series: str          # Número de serie (ej: "01", "02")
    extension: str       # Extensión del archivo (ej: ".jpg", ".mp4")
    original_name: str   # Nombre original completo
    is_legacy: bool      # True si se tradujo desde nomenclatura legacy
    target: str          # "product", "variant" o "theme"
    media_type: str      # "image" o "video"
    dam_type: str        # Metadata TYPE (ej: "Packshot", "Marketing")
    dam_context: str     # Metadata CONTEXT (ej: "Standard", "Hero")


def classify_identifier(identifier: str) -> str:
    """Determina si un identificador corresponde a producto/variante o tema.

    - Numérico puro -> "variant" (SKU / referencia)
    - Alfabético o alfanumérico -> se resuelve contra Sales Layer
    - Full mayúsculas sin números -> "theme" (SOLAR, WIFI, SMART)
    """
    if identifier.isdigit():
        return "variant"
    if re.match(r"^[A-Z]+$", identifier):
        return "theme"
    # Alfanumérico (ej: G401275) -> producto/modelo
    return "product"


def _detect_media_type(ext: str) -> str:
    """Devuelve 'image' o 'video' según la extensión."""
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return "unknown"


def parse_filename(filename: str) -> ParsedAsset | None:
    """Parsea un nombre de archivo y devuelve un ParsedAsset o None si es inválido.

    Soporta:
    - v3.2: IDENTIFICADOR_TIPO_SERIE.ext (ej: 401275_PK_01.jpg, 401275_VCN_01.mp4)
    - Legacy: IDENTIFICADOR_SUFIJO.ext (ej: 401275_A.jpg) — solo imágenes
    """
    name, ext = os.path.splitext(filename)
    ext_lower = ext.lower()

    if ext_lower not in VALID_EXTENSIONS:
        return None

    media_type = _detect_media_type(ext_lower)
    parts = name.split("_")

    if len(parts) < 2:
        return None

    # Intentar formato v3.2: ID_TIPO_SERIE
    if len(parts) >= 3:
        identifier = "_".join(parts[:-2])  # Soporta IDs con _ internos
        type_code = parts[-2].upper()
        series = parts[-1]

        if type_code in METADATA_MAP and re.match(r"^\d{2}$", series):
            dam_type, dam_context = METADATA_MAP[type_code]
            target = classify_identifier(identifier)
            return ParsedAsset(
                identifier=identifier,
                type_code=type_code,
                series=series,
                extension=ext_lower,
                original_name=filename,
                is_legacy=False,
                target=target,
                media_type=media_type,
                dam_type=dam_type,
                dam_context=dam_context,
            )

    # Intentar formato legacy: ID_SUFIJO (solo imágenes)
    if media_type != "image":
        return None

    identifier = "_".join(parts[:-1])
    legacy_suffix = parts[-1]

    if legacy_suffix in LEGACY_MAP:
        type_code, series = LEGACY_MAP[legacy_suffix]
        dam_type, dam_context = METADATA_MAP[type_code]
        target = classify_identifier(identifier)
        return ParsedAsset(
            identifier=identifier,
            type_code=type_code,
            series=series,
            extension=ext_lower,
            original_name=filename,
            is_legacy=True,
            target=target,
            media_type=media_type,
            dam_type=dam_type,
            dam_context=dam_context,
        )

    return None
