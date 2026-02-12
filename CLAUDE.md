# CLAUDE.md - Contexto del Proyecto DAM Garza/Imprex

## 1. Perfil del Proyecto
* **Rol:** Ingeniero de Datos & Arquitecto de Soluciones.
* **Objetivo:** Implementar un **DAM (Digital Asset Management)** automatizado sobre **Sales Layer (PIM)** sin costes de licencias externas.
* **Filosofía:** "Zero-Click Metadata". El diseñador nombra el archivo, el sistema (Script Python) lo clasifica.

## 2. Estado Actual (Snapshot)
* **Arquitectura:** Definida (Modelo v3.1).
* **Base de Datos:** Campos creados en Sales Layer (Productos, Variantes y Tabla Temas).
* **Scaffolding:** ✅ Completado — estructura Python base implementada.
* **Pendiente:** Integración con API Sales Layer (credenciales + endpoints) y despliegue.

## 3. Arquitectura de Datos (Los 3 Silos)
El sistema gestiona imágenes en 3 tablas distintas dentro de Sales Layer:

### A. Tabla PRODUCTOS (Modelos)
Campos de imagen (Multi-image) configurados:
* `img_pk` (Packshot Main)
* `img_kv` (Key Visual Horizontal)
* `img_kvv` (Key Visual Vertical)
* `img_fm` (Feature Mosaic)
* `img_fmd` (Mosaic Parts)
* `img_ft` (Features/Iconos)
* `img_lf` (Lifestyle)

### B. Tabla VARIANTES (SKUs de Venta)
Campos de imagen configurados:
* `img_pk` (Producto suelto)
* `img_2pk` (Packaging/Caja sola)
* `img_3pk` (Combo Producto + Caja)

### C. Tabla TEMAS DE MARKETING (Nueva Entidad)
Tabla de Referencia (`TEMAS_MARKETING`) para conceptos transversales (Solar, Zigbee).
* **ID:** Código del tema (ej: `SOLAR`).
* Campos: `img_kv`, `img_lf`, `img_fm`, `img_fmd`, `img_ft`.

## 4. El Algoritmo de Nomenclatura (v3.1)
Todo archivo nuevo debe cumplir: `IDENTIFICADOR` + `_` + `TIPO` + `_` + `SERIE` + `.ext`
*(Ejemplo: `401275_PK_01.jpg` o `SOLAR_KV_02.jpg`)*

**Diccionario de Códigos (Mapping):**
* `PK` -> Packshot (Standard)
* `2PK` -> Packaging Box
* `3PK` -> Combo
* `KV` -> Marketing Hero
* `KVV` -> Marketing Hero Vertical
* `LF` -> Lifestyle
* `FT` -> Feature Detail
* `FM` -> Mosaic Full
* `FMD` -> Mosaic Decomposed
* `DM` -> Dimensions

## 5. Lógica de Migración (Legacy)
El script debe traducir automáticamente los nombres antiguos:
* `_A` -> Tratar como `_PK_01`
* `_5` -> Tratar como `_LF_01`
* `_4` -> Tratar como `_FT_01`

## 6. Archivos Clave

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| `src/config.py` | Configuración central: mappings v3.1, campos por tabla, legacy map | ✅ |
| `src/parser.py` | Parser de nomenclatura + clasificador de identificadores | ✅ |
| `src/saleslayer.py` | Cliente API Sales Layer (get/upload/set_metadata) | 🔄 Esqueleto |
| `src/dam_ingest.py` | Entry point: procesa directorio y sube a Sales Layer | 🔄 Esqueleto funcional |
| `tests/test_parser.py` | Suite de tests del parser (17 tests pasando) | ✅ |
| `.env.example` | Template credenciales (SL_API_URL, SL_CONNECTOR_ID, SL_SECRET_KEY) | ✅ |

## 7. Decisiones Tomadas

### Uso de dataclass ParsedAsset
Se eligió una estructura de datos inmutable para representar el resultado del parsing: `ParsedAsset(identifier, entity_type, asset_type, series, field_id, valid, error_msg)`. Facilita testing y trazabilidad.

### Mapeos centralizados en config.py
Todos los mappings (ASSET_TYPE_MAP, METADATA_MAP, LEGACY_MAP) y definiciones de campos (PRODUCT_FIELDS, VARIANT_FIELDS, THEME_FIELDS) viven en un único archivo de configuración. Cambios de negocio no requieren tocar lógica.

### Ambigüedad identificadores alfabéticos
Detectado que identificadores como "DALIA" vs "SOLAR" son ambiguos sin consultar la BD. El parser los marca como `theme` por defecto. La resolución definitiva requiere lookup a Sales Layer para verificar existencia en tablas de productos vs temas.

## 8. Deuda Técnica Conocida

- **Resolver ambigüedad product vs theme:** Identificadores alfabéticos necesitan consulta a Sales Layer para determinar tipo de entidad correcto.
- **Validación de credenciales faltante:** El SalesLayerClient valida que existan las variables de entorno pero no verifica que sean válidas contra la API.
- **Manejo de rate limits:** No implementado aún. Sales Layer puede tener límites de requests/segundo.

## 9. Próximos Pasos (Roadmap)

1. ✅ **Estructura base:** Scaffold Python completo (.gitignore, .env.example, requirements.txt, src/, tests/).
2. ✅ **Parser de nomenclatura:** Implementado con soporte v3.1 + legacy. Tests pasando.
3. 🔄 **Cliente Sales Layer:** Implementar métodos reales de API (get_product, get_variant, get_theme, upload_image, set_metadata). Requiere credenciales válidas + documentación API.
4. ⬜ **Resolver ambigüedad identificadores:** Implementar lookup a BD para casos como "DALIA" vs "SOLAR".
5. ⬜ **Integración completa dam_ingest.py:** Conectar parser + cliente real + manejo de errores.
6. ⬜ **Prueba piloto:** 10 imágenes reales contra Sales Layer de staging/producción.
7. ⬜ **Documentación para agencias:** Guía de nomenclatura + proceso de subida.
