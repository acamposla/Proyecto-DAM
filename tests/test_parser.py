"""Tests para el parser de nomenclatura DAM v3.2 (imágenes + vídeo)."""

import pytest
from src.parser import parse_filename, classify_identifier


class TestClassifyIdentifier:
    def test_numeric_is_variant(self):
        assert classify_identifier("401275") == "variant"

    def test_uppercase_alpha_is_theme(self):
        assert classify_identifier("SOLAR") == "theme"
        assert classify_identifier("WIFI") == "theme"

    def test_mixed_alphanumeric_is_product(self):
        assert classify_identifier("G401") == "product"

    def test_pure_alpha_is_theme(self):
        # Pure alpha mayúsculas -> tema por defecto
        # DALIA vs SOLAR son indistinguibles sin consultar Sales Layer.
        assert classify_identifier("DALIA") == "theme"


# --- Imágenes v3.2 ---

class TestParseImages:
    def test_packshot_product(self):
        asset = parse_filename("401275_PK_01.jpg")
        assert asset is not None
        assert asset.identifier == "401275"
        assert asset.type_code == "PK"
        assert asset.series == "01"
        assert asset.target == "variant"
        assert asset.media_type == "image"
        assert asset.dam_type == "Packshot"
        assert asset.is_legacy is False

    def test_key_visual_theme(self):
        asset = parse_filename("SOLAR_KV_02.jpg")
        assert asset is not None
        assert asset.identifier == "SOLAR"
        assert asset.type_code == "KV"
        assert asset.series == "02"
        assert asset.target == "theme"
        assert asset.media_type == "image"
        assert asset.dam_type == "Marketing"
        assert asset.dam_context == "Hero"

    def test_mosaic_decomposed(self):
        asset = parse_filename("DALIA_FMD_04.jpg")
        assert asset is not None
        assert asset.type_code == "FMD"
        assert asset.media_type == "image"
        assert asset.dam_type == "Infographic"
        assert asset.dam_context == "Decomposed"

    def test_packaging_box(self):
        asset = parse_filename("401275_2PK_01.png")
        assert asset is not None
        assert asset.type_code == "2PK"
        assert asset.media_type == "image"
        assert asset.dam_context == "Packaging Box"

    def test_key_visual_vertical(self):
        asset = parse_filename("DALIA_KVV_01.webp")
        assert asset is not None
        assert asset.type_code == "KVV"
        assert asset.media_type == "image"
        assert asset.dam_context == "Hero Vertical"


# --- Vídeos v3.2 ---

class TestParseVideos:
    def test_video_marketing(self):
        asset = parse_filename("401275_VMK_01.mp4")
        assert asset is not None
        assert asset.identifier == "401275"
        assert asset.type_code == "VMK"
        assert asset.series == "01"
        assert asset.media_type == "video"
        assert asset.dam_type == "Marketing"
        assert asset.dam_context == "Demo / Hero"

    def test_video_installation(self):
        asset = parse_filename("401275_VINS_01.mp4")
        assert asset is not None
        assert asset.type_code == "VINS"
        assert asset.media_type == "video"
        assert asset.dam_type == "Technical"
        assert asset.dam_context == "Installation"

    def test_video_connectivity(self):
        asset = parse_filename("401275_VCN_01.mp4")
        assert asset is not None
        assert asset.type_code == "VCN"
        assert asset.media_type == "video"
        assert asset.dam_type == "Technical"
        assert asset.dam_context == "Pairing / IoT"

    def test_video_config(self):
        asset = parse_filename("SMART_VCF_02.mp4")
        assert asset is not None
        assert asset.identifier == "SMART"
        assert asset.type_code == "VCF"
        assert asset.target == "theme"
        assert asset.media_type == "video"
        assert asset.dam_type == "Technical"
        assert asset.dam_context == "App Usage"

    def test_video_troubleshooting(self):
        asset = parse_filename("401275_VTR_01.mov")
        assert asset is not None
        assert asset.type_code == "VTR"
        assert asset.media_type == "video"
        assert asset.dam_type == "Support"
        assert asset.dam_context == "Troubleshooting"

    def test_video_webm_extension(self):
        asset = parse_filename("SOLAR_VMK_01.webm")
        assert asset is not None
        assert asset.media_type == "video"
        assert asset.type_code == "VMK"


# --- Legacy (solo imágenes) ---

class TestParseLegacy:
    def test_legacy_a_to_pk(self):
        asset = parse_filename("401275_A.jpg")
        assert asset is not None
        assert asset.type_code == "PK"
        assert asset.series == "01"
        assert asset.media_type == "image"
        assert asset.is_legacy is True

    def test_legacy_5_to_lf(self):
        asset = parse_filename("401275_5.jpg")
        assert asset is not None
        assert asset.type_code == "LF"
        assert asset.series == "01"
        assert asset.is_legacy is True

    def test_legacy_4_to_ft(self):
        asset = parse_filename("401275_4.jpg")
        assert asset is not None
        assert asset.type_code == "FT"

    def test_legacy_not_applied_to_video(self):
        # Legacy solo aplica a imágenes, no a vídeos
        assert parse_filename("401275_A.mp4") is None


# --- Casos inválidos ---

class TestParseInvalid:
    def test_no_extension(self):
        assert parse_filename("401275_PK_01") is None

    def test_invalid_extension(self):
        assert parse_filename("401275_PK_01.pdf") is None

    def test_no_underscore(self):
        assert parse_filename("archivo.jpg") is None

    def test_unknown_code(self):
        assert parse_filename("401275_XX_01.jpg") is None

    def test_bad_series(self):
        assert parse_filename("401275_PK_1.jpg") is None  # Debe ser 2 dígitos

    def test_unknown_video_code(self):
        assert parse_filename("401275_VXX_01.mp4") is None
