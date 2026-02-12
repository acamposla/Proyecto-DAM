# Contexto de Conversación

## Última actualización
2026-02-12 (Final de sesión)

## ¿Qué estábamos haciendo?
Actualización del proyecto DAM de v3.1 (solo imágenes) a v3.2 (imágenes + vídeo). El usuario documentó 5 tipos de vídeo basados en el Customer Journey de Garza Smart Home y todo el código se actualizó para soportar esta nueva funcionalidad.

## Estado de la tarea actual
**COMPLETADO:** Actualización v3.2 completamente funcional y testeada.

### Cambios realizados en esta sesión

#### 1. Documentación de vídeo (por el usuario)
- `PROTOCOLO_VIDEO.md`: Especificación normativa de los 5 tipos de vídeo.
- `VIDEO_PLAYBOOKS.md`: Guías de producción para agencias (duración, estilo, estructura).
- Ambos documentos reubicados: PROTOCOLO_VIDEO.md en `output/` (specs), VIDEO_PLAYBOOKS.md en `reference/` (guías).

#### 2. Código actualizado a v3.2

**config.py — COMPLETO v3.2:**
- Añadidos 5 códigos de vídeo a PRODUCT_FIELDS: `VMK` (Marketing), `VINS` (Instalación), `VCN` (Conectividad), `VCF` (Configuración), `VTR` (Troubleshooting).
- Añadidos mismos 5 códigos a THEME_FIELDS.
- VARIANT_FIELDS sin vídeo (decisión de negocio: vídeos solo a nivel modelo).
- Separación de extensiones: IMAGE_EXTENSIONS (.jpg, .jpeg, .png, .webp) y VIDEO_EXTENSIONS (.mp4, .webm).
- VALID_EXTENSIONS = unión de ambas.
- METADATA_MAP extendido con metadatos de vídeo (Technical/Installation, Technical/Pairing, Support/App, etc.).

**parser.py — COMPLETO v3.2:**
- Nuevo campo `media_type` en dataclass ParsedAsset ("image" o "video").
- Nueva función `_detect_media_type(ext)` que clasifica según extensión.
- Lógica legacy BLOQUEADA para vídeos (solo aplica a imágenes).
- Validación de códigos separada: códigos de vídeo (3 letras) vs códigos de imagen (2 letras generalmente).

**tests/test_parser.py — 25/25 tests pasando:**
- Nueva clase `TestParseVideos`: 6 tests (VMK, VINS, VCN, VCF, VTR + extensión .webm).
- Nuevo test en `TestParseLegacy`: verifica que legacy NO se aplica a vídeos.
- Nuevo test en `TestParseInvalid`: código de vídeo inválido.
- Total: 25 tests (antes 17, +8 nuevos).

**dam_ingest.py — Actualizado docstrings v3.2:**
- Lógica preparada para bifurcar `upload_video()` vs `upload_image()` según `media_type`.
- Documentación actualizada.

#### 3. Commits realizados
- `7abfa54`: scaffolding Python base (sesión anterior).
- `a71ac35`: Update to v3.2: add video support (5 types) and reorganize docs.
- Ambos commits pusheados a main en GitHub.

### Módulos del proyecto (estado actual)

| Módulo | Estado | Notas |
|--------|--------|-------|
| `config.py` | ✅ COMPLETO v3.2 | Mappings completos para imágenes + vídeo |
| `parser.py` | ✅ COMPLETO v3.2 | Detecta media_type, parsea ambos tipos |
| `test_parser.py` | ✅ 25/25 passing | Cobertura completa (imágenes, vídeos, legacy, inválidos) |
| `saleslayer.py` | 🔄 ESQUELETO | Clase base creada, métodos sin implementar |
| `dam_ingest.py` | 🔄 ESQUELETO FUNCIONAL | Orquestación lista, falta integrar API |

## Problemas abiertos

### 1. Credenciales Sales Layer NO disponibles (BLOQUEANTE)
**Problema:** No se tienen credenciales reales para probar integración API Sales Layer.

**Necesario para continuar:**
- `SL_API_URL`: Endpoint base de Sales Layer.
- `SL_CONNECTOR_ID`: ID del conector del proyecto.
- `SL_SECRET_KEY`: Clave secreta de autenticación.
- Documentación API: Formato request/response, autenticación, rate limits.
- Entorno staging (opcional pero recomendado para testing).

**Impacto:** Bloquea implementación de `saleslayer.py` (get/upload/set_metadata) y toda la integración.

### 2. Ambigüedad identificadores alfabéticos (No bloqueante)
**Problema:** Identificadores como "DALIA" vs "SOLAR" no se pueden clasificar sin consultar BD.

**Estado actual:** Parser usa heurística (uppercase -> theme, alphanumeric -> product).

**Solución definitiva:** Requiere implementar lookup a Sales Layer:
1. dam_ingest.py intenta clasificar con parser.
2. Si alfabético, hace `get_theme(ID)` y `get_product(ID)`.
3. Usa el que exista (o error si ambiguo/inexistente).

**Dependencia:** Necesita cliente API funcional (problema #1).

## Próximo paso concreto

**INMEDIATO al retomar (CRÍTICO):**
1. **Obtener credenciales Sales Layer:**
   - Crear archivo `.env` real desde `.env.example`.
   - SL_API_URL, SL_CONNECTOR_ID, SL_SECRET_KEY.
2. **Conseguir documentación API Sales Layer:**
   - Endpoints disponibles.
   - Formato de autenticación.
   - Estructura request/response (JSON).
   - Rate limits / restricciones.
3. **Verificar acceso:**
   - Implementar método de prueba (ej: `get_connector_info()`).
   - Hacer request de test para verificar credenciales.

**DESPUÉS de conectividad probada:**
4. Implementar `get_product()`, `get_variant()`, `get_theme()`.
5. Implementar `upload_image()` y `upload_video()`.
6. Implementar `set_metadata()` (dam_type, dam_context).
7. Resolver ambigüedad identificadores alfabéticos (lookup a BD).
8. Integrar todo en `dam_ingest.py` con manejo de errores robusto.
9. Prueba piloto: 10 activos (5 imágenes + 5 vídeos) en entorno staging.

## Notas de sesión

### Logros clave
- **v3.2 completa y testeada:** El proyecto pasó de soportar solo imágenes (v3.1) a soportar imágenes + vídeo (v3.2) con test coverage completo.
- **Arquitectura limpia:** La separación entre config/parser/API client/orchestration permitió añadir vídeo sin tocar la lógica existente.
- **Decisión de negocio documentada:** Vídeos solo en PRODUCTOS y TEMAS, no en VARIANTES (porque aplican al modelo completo, no al SKU).
- **Commits bien estructurados:** Cada feature en su commit (scaffolding base → v3.2 video).

### Lecciones aprendidas
- **Legacy solo para imágenes:** Los vídeos son nuevos, no tienen nomenclatura heredada. Test específico para verificar que legacy no se aplica a vídeos.
- **Extensiones separadas:** IMAGE_EXTENSIONS y VIDEO_EXTENSIONS separadas facilita añadir nuevos formatos (ej: .svg, .mov).
- **Metadata map extensible:** METADATA_MAP en config.py permite añadir nuevos contextos sin tocar parser.

### Bloqueador crítico
**Credenciales Sales Layer faltantes:** Todo el desarrollo de integración API está bloqueado hasta obtener credenciales válidas y documentación.

### Próxima milestone
**Integración API Sales Layer:** Una vez desbloqueado el problema de credenciales, el siguiente hito es tener el cliente API funcional con al menos un método (get_product) probado contra el entorno real.
