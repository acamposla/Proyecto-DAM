"""DAM Ingest - Script principal de clasificación automática de imágenes.

Lee archivos de un directorio, parsea sus nombres según nomenclatura v3.1,
y los sube al campo correspondiente en Sales Layer.

Uso:
    python -m src.dam_ingest <directorio_imagenes>
"""

import sys
from pathlib import Path

from .config import PRODUCT_FIELDS, VARIANT_FIELDS, THEME_FIELDS
from .parser import parse_filename, ParsedAsset


# Mapping: target -> campos válidos por tabla
TARGET_FIELD_MAP = {
    "product": PRODUCT_FIELDS,
    "variant": VARIANT_FIELDS,
    "theme":   THEME_FIELDS,
}


def get_field_id(asset: ParsedAsset) -> str | None:
    """Devuelve el field ID de Sales Layer para un asset parseado."""
    fields = TARGET_FIELD_MAP.get(asset.target)
    if not fields:
        return None
    return fields.get(asset.type_code)


def process_directory(directory: Path) -> None:
    """Procesa todos los archivos de imagen en un directorio."""
    files = sorted(directory.iterdir())
    ok, skip, error = 0, 0, 0

    for filepath in files:
        if not filepath.is_file():
            continue

        asset = parse_filename(filepath.name)

        if asset is None:
            print(f"  SKIP  {filepath.name} (nombre no reconocido)")
            skip += 1
            continue

        field_id = get_field_id(asset)

        if field_id is None:
            print(
                f"  ERROR {filepath.name} -> "
                f"{asset.target}.{asset.type_code} no tiene campo asignado"
            )
            error += 1
            continue

        legacy_tag = " [LEGACY]" if asset.is_legacy else ""
        print(
            f"  OK    {filepath.name} -> "
            f"{asset.target}/{asset.identifier}.{field_id} "
            f"(serie:{asset.series}, type:{asset.dam_type}, "
            f"context:{asset.dam_context}){legacy_tag}"
        )
        ok += 1

        # TODO: Subir imagen a Sales Layer
        # client.upload_image(asset.target, asset.identifier, field_id, filepath)
        # client.set_metadata(asset.target, asset.identifier, asset.dam_type, asset.dam_context)

    print(f"\nResultado: {ok} OK / {skip} SKIP / {error} ERROR")


def main():
    if len(sys.argv) < 2:
        print("Uso: python -m src.dam_ingest <directorio_imagenes>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Error: {directory} no es un directorio válido")
        sys.exit(1)

    print(f"DAM Ingest v3.1 - Procesando: {directory}\n")
    process_directory(directory)


if __name__ == "__main__":
    main()
