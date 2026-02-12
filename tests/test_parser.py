"""Tests para el parser de nomenclatura DAM v3.1."""

import pytest
from src.parser import parse_filename, classify_identifier


class TestClassifyIdentifier:
    def test_numeric_is_variant(self):
        assert classify_identifier("401275") == "variant"

    def test_uppercase_alpha_is_theme(self):
        assert classify_identifier("SOLAR") == "theme"
        assert classify_identifier("WIFI") == "theme"

    def test_mixed_alphanumeric_is_product(self):
        # Alfanuméricos (letras + dígitos) -> producto
        assert classify_identifier("G401") == "product"

    def test_pure_alpha_is_theme(self):
        # Pure alpha mayúsculas -> tema por defecto
        # DALIA vs SOLAR son indistinguibles sin consultar Sales Layer.
        # La resolución final la hará el lookup en BD.
        assert classify_identifier("DALIA") == "theme"


class TestParseV31:
    def test_packshot_product(self):
        asset = parse_filename("401275_PK_01.jpg")
        assert asset is not None
        assert asset.identifier == "401275"
        assert asset.type_code == "PK"
        assert asset.series == "01"
        assert asset.target == "variant"
        assert asset.dam_type == "Packshot"
        assert asset.is_legacy is False

    def test_key_visual_theme(self):
        asset = parse_filename("SOLAR_KV_02.jpg")
        assert asset is not None
        assert asset.identifier == "SOLAR"
        assert asset.type_code == "KV"
        assert asset.series == "02"
        assert asset.target == "theme"
        assert asset.dam_type == "Marketing"
        assert asset.dam_context == "Hero"

    def test_mosaic_decomposed(self):
        asset = parse_filename("DALIA_FMD_04.jpg")
        assert asset is not None
        assert asset.type_code == "FMD"
        assert asset.dam_type == "Infographic"
        assert asset.dam_context == "Decomposed"

    def test_packaging_box(self):
        asset = parse_filename("401275_2PK_01.png")
        assert asset is not None
        assert asset.type_code == "2PK"
        assert asset.dam_context == "Packaging Box"

    def test_key_visual_vertical(self):
        asset = parse_filename("DALIA_KVV_01.webp")
        assert asset is not None
        assert asset.type_code == "KVV"
        assert asset.dam_context == "Hero Vertical"


class TestParseLegacy:
    def test_legacy_a_to_pk(self):
        asset = parse_filename("401275_A.jpg")
        assert asset is not None
        assert asset.type_code == "PK"
        assert asset.series == "01"
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
