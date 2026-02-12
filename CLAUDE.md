# CLAUDE.md - Contexto del Proyecto DAM Garza/Imprex

## 1. Perfil del Proyecto
* **Rol:** Ingeniero de Datos & Arquitecto de Soluciones.
* **Objetivo:** Implementar un **DAM (Digital Asset Management)** automatizado sobre **Sales Layer (PIM)** sin costes de licencias externas.
* **Filosofía:** "Zero-Click Metadata". El diseñador nombra el archivo, el sistema (Script Python) lo clasifica.

## 2. Estado Actual (Snapshot)
* **Arquitectura:** Definida (Modelo v3.2 - Incluye Vídeo).
* **Base de Datos:** Campos creados en Sales Layer (Productos, Variantes y Tabla Temas) para imágenes y vídeos.
* **Scaffolding:** ✅ Completado — estructura Python base implementada.
* **Pendiente:** Integración con API Sales Layer (credenciales + endpoints), actualización del parser para vídeo y despliegue.

## 3. Arquitectura de Datos (Los 3 Silos + Vídeo)
El sistema gestiona activos en tablas distintas dentro de Sales Layer. Se han añadido campos de vídeo a las tablas principales.

### A. Tabla PRODUCTOS (Modelos)
*Campos de Imagen (Multi-image):*
* `img_pk` (Packshot Main)
* `img_kv` (Key Visual Horizontal)
* `img_kvv` (Key Visual Vertical)
* `img_fm` (Feature Mosaic)
* `img_fmd` (Mosaic Parts)
* `img_ft` (Features/Iconos)
* `img_lf` (Lifestyle)
*Campos de Vídeo (Enlace/Archivo):*
* `vid_mk` (Marketing/Demo)
* `vid_ins` (Instalación Física)
* `vid_cn` (Conectividad/IoT)
* `vid_cf` (Configuración App)
* `vid_tr` (Troubleshooting)

### B. Tabla VARIANTES (SKUs de Venta)
*Campos de Imagen:*
* `img_pk` (Producto suelto)
* `img_2pk` (Packaging/Caja sola)
* `img_3pk` (Combo Producto + Caja)

### C. Tabla TEMAS DE MARKETING (Nueva Entidad)
Tabla de Referencia (`TEMAS_MARKETING`) para conceptos transversales (Solar, Zigbee).
* **ID:** Código del tema (ej: `SOLAR`).
* *Campos Imagen:* `img_kv`, `img_lf`, `img_fm`, `img_fmd`, `img_ft`.
* *Campos Vídeo:* `vid_mk`, `vid_ins`, `vid_cn`, `vid_cf`, `vid_tr`.

## 4. El Algoritmo de Nomenclatura (v3.2)
Todo archivo nuevo debe cumplir: `IDENTIFICADOR` + `_` + `CÓDIGO` + `_` + `SERIE` + `.ext`
*(Ejemplo: `401275_PK_01.jpg`, `SOLAR_KV_02.jpg` o `401275_VCN_01.mp4`)*

**Diccionario de Códigos (Mapping):**

*IMÁGENES (2 Letras - Generalmente):*
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

*VÍDEOS (3 Letras - Nuevo v3.2):*
* `VMK` -> Marketing (Engloba Marketing y Funcionamiento)
* `VINS` -> Instalación (Física/Hardware)
* `VCN` -> Conectividad (IoT/Pairing)
* `VCF` -> Configuración (App/Software)
* `VTR` -> Troubleshooting (Soporte/Ayuda)

## 5. Lógica de Migración (Legacy)
El script debe traducir automáticamente los nombres antiguos (solo aplica a imágenes):
* `_A` -> Tratar como `_PK_01`
* `_5` -> Tratar como `_LF_01`
* `_4` -> Tratar como `_FT_01`

## 6. Archivos Clave

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| `src/config.py` | Configuración central: mappings v3.2, campos por tabla, legacy map | �� Actualizar |
| `src/parser.py` | Parser de nomenclatura + clasificador de identificadores | �� Actualizar |
| `src/saleslayer.py` | Cliente API Sales Layer (get/upload/set_metadata) | �� Esqueleto |
| `src/dam_ingest.py` | Entry point: procesa directorio y sube a Sales Layer | �� Esqueleto funcional |
| `tests/test_parser.py` | Suite de tests del parser (17 tests pasando) | �� Actualizar |
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
3. �� **Actualización a v3.2:** Incluir lógica de detección de vídeo (mp4) y nuevos códigos (`VMK`, `VINS`, etc.) en `config.py` y `parser.py`.
4. �� **Cliente Sales Layer:** Implementar métodos reales de API (get_product, get_variant, get_theme, upload_image, upload_video, set_metadata). Requiere credenciales válidas + documentación API.
5. ⬜ **Resolver ambigüedad identificadores:** Implementar lookup a BD para casos como "DALIA" vs "SOLAR".
6. ⬜ **Integración completa dam_ingest.py:** Conectar parser + cliente real + manejo de errores.
7. ⬜ **Prueba piloto:** 10 activos reales (imágenes y vídeos) contra Sales Layer de staging/producción.
8. ⬜ **Documentación para agencias:** Guía de nomenclatura + proceso de subida (Incluyendo Playbooks de Vídeo).
