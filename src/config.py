"""Configuración y constantes del DAM v3.2 (Imágenes + Vídeo)."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Sales Layer API ---
SL_API_URL = os.getenv("SL_API_URL", "https://api.saleslayer.com/")
SL_CONNECTOR_ID = os.getenv("SL_CONNECTOR_ID")
SL_SECRET_KEY = os.getenv("SL_SECRET_KEY")

# --- Mapping: sufijo de archivo -> field ID en Sales Layer ---
# Tabla PRODUCTOS (Models)
PRODUCT_FIELDS = {
    # Imágenes
    "PK":   "img_pk",
    "KV":   "img_kv",
    "KVV":  "img_kvv",
    "FM":   "img_fm",
    "FMD":  "img_fmd",
    "FT":   "img_ft",
    "LF":   "img_lf",
    # Vídeos
    "VMK":  "vid_mk",
    "VINS": "vid_ins",
    "VCN":  "vid_cn",
    "VCF":  "vid_cf",
    "VTR":  "vid_tr",
}

# Tabla VARIANTES (SKUs) — solo imágenes, sin vídeo
VARIANT_FIELDS = {
    "PK":  "img_pk",
    "2PK": "img_2pk",
    "3PK": "img_3pk",
}

# Tabla TEMAS_MARKETING
THEME_FIELDS = {
    # Imágenes
    "KV":   "img_kv",
    "LF":   "img_lf",
    "FM":   "img_fm",
    "FMD":  "img_fmd",
    "FT":   "img_ft",
    # Vídeos
    "VMK":  "vid_mk",
    "VINS": "vid_ins",
    "VCN":  "vid_cn",
    "VCF":  "vid_cf",
    "VTR":  "vid_tr",
}

# --- Metadata auxiliar ---
# Sufijo -> (dam_type, dam_context)
METADATA_MAP = {
    # Imágenes
    "PK":   ("Packshot",    "Standard"),
    "2PK":  ("Packshot",    "Packaging Box"),
    "3PK":  ("Packshot",    "Combo"),
    "KV":   ("Marketing",   "Hero"),
    "KVV":  ("Marketing",   "Hero Vertical"),
    "LF":   ("Lifestyle",   "Standard"),
    "FM":   ("Infographic", "Mosaic"),
    "FMD":  ("Infographic", "Decomposed"),
    "FT":   ("Detail",      "Feature"),
    # Vídeos
    "VMK":  ("Marketing",   "Demo / Hero"),
    "VINS": ("Technical",   "Installation"),
    "VCN":  ("Technical",   "Pairing / IoT"),
    "VCF":  ("Technical",   "App Usage"),
    "VTR":  ("Support",     "Troubleshooting"),
}

# --- Legacy: traducción de sufijos antiguos (solo imágenes) ---
LEGACY_MAP = {
    "A": ("PK", "01"),   # _A -> _PK_01
    "5": ("LF", "01"),   # _5 -> _LF_01
    "4": ("FT", "01"),   # _4 -> _FT_01
}

# Extensiones válidas por tipo de media
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}
VALID_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
