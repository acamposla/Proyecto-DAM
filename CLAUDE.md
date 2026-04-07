# CLAUDE.md - Contexto del Proyecto DAM Garza/Imprex
## Scope: Imprex, Vértice

## 1. Perfil del Proyecto
* **Rol:** Ingeniero de Datos & Arquitecto de Soluciones.
* **Objetivo:** Implementar un **DAM (Digital Asset Management)** automatizado sobre **Sales Layer (PIM)** sin costes de licencias externas.
* **Filosofía:** "Zero-Click Metadata". El diseñador nombra el archivo, el sistema (Script Python) lo clasifica.

## 2. Estado Actual (Snapshot)
* **Arquitectura:** Definida (Modelo v4.0 - Vídeo unificado: 3 tipos).
* **Base de Datos:** Campos creados en Sales Layer (Productos, Variantes y Tabla Temas) para imágenes y vídeos.
* **Scaffolding:** ✅ Completado v4.0 — estructura Python + parser + tests funcionando.
* **Pendiente:** Integración con API Sales Layer (BLOQUEADO: necesita credenciales + docs API).

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
* `vid_set` (Setup: Instalación + Conectividad + Configuración)
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
* *Campos Vídeo:* `vid_mk`, `vid_set`, `vid_tr`.

## 4. El Algoritmo de Nomenclatura (v4.0)
Todo archivo nuevo debe cumplir: `IDENTIFICADOR` + `_` + `CÓDIGO` + `_` + `SERIE` + `.ext`
*(Ejemplo: `401275_PK_01.jpg`, `SOLAR_KV_02.jpg` o `401275_VSET_01.mp4`)*

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

*VÍDEOS (3+ Letras - v4.0 Unificado):*
* `VMK` -> Marketing (Engloba Marketing y Funcionamiento)
* `VSET` -> Setup (Guía completa: Instalación + Conectividad + Configuración, modular)
* `VTR` -> Troubleshooting (Soporte/Ayuda)

## 5. Lógica de Migración (Legacy)
El script debe traducir automáticamente los nombres antiguos (solo aplica a imágenes):
* `_A` -> Tratar como `_PK_01`
* `_5` -> Tratar como `_LF_01`
* `_4` -> Tratar como `_FT_01`

## 6. Archivos Clave

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| `src/config.py` | Configuración central: mappings v4.0 (imágenes + 3 tipos vídeo), campos por tabla, legacy map | ✅ COMPLETO v4.0 |
| `src/parser.py` | Parser de nomenclatura + clasificador de identificadores + detección media_type | ✅ COMPLETO v4.0 |
| `src/saleslayer.py` | Cliente API Sales Layer (get/upload/set_metadata) | 🔄 ESQUELETO (requiere credenciales) |
| `src/dam_ingest.py` | Entry point: procesa directorio y sube a Sales Layer | 🔄 ESQUELETO FUNCIONAL (falta integrar API) |
| `tests/test_parser.py` | Suite de tests del parser (26/26 tests pasando: imágenes, vídeos, legacy, old codes invalid) | ✅ COMPLETO v4.0 |
| `.env.example` | Template credenciales (SL_API_URL, SL_CONNECTOR_ID, SL_SECRET_KEY) | ✅ |
| `output/PROTOCOLO_VIDEO.md` | Especificación normativa de los 3 tipos de vídeo (v2.0) | ✅ |
| `reference/VIDEO_PLAYBOOKS.md` | Guías de producción de vídeo (v4.0 unificada, VSET modular) | ✅ |
| `reference/GUION_VMK_EJEMPLO_401275.md` | Guión de ejemplo para vídeo VMK (bombilla LED WiFi Garza Smart) | ✅ |

## 7. Decisiones Tomadas

### Uso de dataclass ParsedAsset (Actualizada en v3.2)
Se eligió una estructura de datos inmutable para representar el resultado del parsing. En v3.2 incluye `media_type` ("image" o "video") y metadata (dam_type, dam_context). Facilita testing y trazabilidad.

### Mapeos centralizados en config.py
Todos los mappings (ASSET_TYPE_MAP, METADATA_MAP, LEGACY_MAP) y definiciones de campos (PRODUCT_FIELDS, VARIANT_FIELDS, THEME_FIELDS) viven en un único archivo de configuración. Cambios de negocio no requieren tocar lógica. En v4.0: 3 códigos de vídeo (VMK, VSET, VTR) y separación de extensiones válidas (IMAGE_EXTENSIONS, VIDEO_EXTENSIONS).

### Legacy solo aplica a imágenes
La lógica de migración (_A -> _PK_01, _5 -> _LF_01, _4 -> _FT_01) solo se aplica a archivos de imagen. Los vídeos no tienen nomenclatura heredada.

### Ambigüedad identificadores alfabéticos
Detectado que identificadores como "DALIA" vs "SOLAR" son ambiguos sin consultar la BD. El parser los marca como `theme` por defecto (uppercase alpha) o `product` (alphanumeric). La resolución definitiva requiere lookup a Sales Layer para verificar existencia en tablas de productos vs temas.

### Vídeos en VARIANTES (decisión de negocio)
Los SKUs (variantes) NO tienen campos de vídeo. Los vídeos solo se asocian a modelos (PRODUCTOS) y temas (TEMAS_MARKETING). Justificación: un vídeo de setup aplica al producto completo, no a cada SKU/color/packaging.

### Unificación VINS+VCN+VCF → VSET (v4.0)
Instalación, Conectividad y Configuración se fusionaron en un solo tipo de vídeo modular (VSET). Razón: el usuario quiere un solo recurso que le lleve de "abrir la caja" a "producto funcionando". El vídeo incluye solo las secciones que el producto necesite. Un aplique solar solo necesita instalación. Una bombilla smart solo conectividad + configuración. Una cámara IP necesita las tres. Esto redujo de 5 a 3 tipos de vídeo (VMK, VSET, VTR) y de 5 a 3 campos en Sales Layer.

### Patrón común en playbooks de vídeo
Todos los playbooks de vídeo (excepto VMK que es marketing) incluyen dos elementos estándar:
- **Resumen introductorio:** "¿Qué vas a ver?" — establece expectativas sobre el contenido.
- **CTA Soporte:** Cierre dirigiendo a `customer.garza.es` para soporte adicional.
Esto crea consistencia en la experiencia de usuario y facilita la producción por lotes.

### VSET Configuración: Jerarquía Esencial vs Avanzada
En la sección de Configuración del VSET se estableció un criterio de priorización:
- **Configuraciones ESENCIALES:** Sin ellas el producto no funciona (ej: conexión WiFi inicial, dar alta en app). Van PRIMERO.
- **Configuraciones AVANZADAS:** Opcionales o de optimización (ej: cambiar zona horaria, ajustar sensibilidad). Van DESPUÉS.
Se pueden bundlelizar varias configs breves en un solo bloque. Badges visuales "ESENCIAL"/"AVANZADO" en pantalla.

## 8. Deuda Técnica Conocida

- **Resolver ambigüedad product vs theme:** Identificadores alfabéticos necesitan consulta a Sales Layer para determinar tipo de entidad correcto.
- **Validación de credenciales faltante:** El SalesLayerClient valida que existan las variables de entorno pero no verifica que sean válidas contra la API.
- **Manejo de rate limits:** No implementado aún. Sales Layer puede tener límites de requests/segundo.
- **Estrategia multiidioma de vídeos:** Por definir. Problema: cómo producir vídeos localizables a otros idiomas con equilibrio coste/calidad. Consideraciones clave:
  - Texto en pantalla = difícil de localizar. Preferir iconografía/números universales o plantillas editables.
  - Voz narrada sin actor en pantalla = fácil de sustituir con AI (ElevenLabs, HuggingFace SeamlessM4T, Whisper+TTS).
  - Actor hablando a cámara = lip-sync caro. Posible solo para VMK (marketing, no se localiza).
  - Separar capas: master visual mudo + voz y textos como capas independientes.
  - **Herramientas a evaluar:** ElevenLabs, HuggingFace (SeamlessM4T/MMS), Whisper (OpenAI), YouTube auto-dubbing.
  - **Trade-off:** Actor genera confianza en marketing pero complica localización. Solución posible: actor solo en VMK, voz en off para VSET/VTR.
  - **Estado:** Pendiente de decisión en próxima sesión.

## 9. Próximos Pasos (Roadmap)

1. ✅ **Estructura base:** Scaffold Python completo (.gitignore, .env.example, requirements.txt, src/, tests/).
2. ✅ **Parser de nomenclatura:** Implementado con soporte v3.1 + legacy. 17 tests pasando.
3. ✅ **Soporte vídeo (v3.2):** Detección de vídeo (mp4/webm/mov), códigos de vídeo, metadata map extendido.
4. ✅ **Unificación vídeo (v4.0):** VINS+VCN+VCF fusionados en VSET (modular). De 5 a 3 tipos de vídeo. 26 tests pasando. Playbooks y protocolo actualizados.
5. 🔄 **Cliente Sales Layer:** Implementar métodos reales de API (get_product, get_variant, get_theme, upload_image, upload_video, set_metadata). **BLOQUEADO: Requiere credenciales válidas + documentación API.**
6. ⬜ **Definir estrategia multiidioma para vídeos:** Evaluar opciones de producción localizable (capas separadas, voz AI vs actor). Herramientas candidatas: ElevenLabs, HuggingFace, Whisper. Por decidir.
7. ⬜ **Resolver ambigüedad identificadores:** Implementar lookup a BD para casos como "DALIA" vs "SOLAR" (requiere cliente API funcional).
8. ⬜ **Integración completa dam_ingest.py:** Conectar parser + cliente real + manejo de errores + rate limits.
9. ⬜ **Prueba piloto:** 10 activos reales (5 imágenes + 5 vídeos) contra Sales Layer de staging/producción.
10. ⬜ **Documentación para agencias:** Guía de nomenclatura consolidada + proceso de subida (incorporar playbooks de vídeo).
