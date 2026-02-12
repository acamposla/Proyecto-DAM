# Contexto de Conversación

## Última actualización
2026-02-12

## ¿Qué estábamos haciendo?
Implementando el scaffolding completo del proyecto Python DAM: estructura de carpetas, configuración base, parser de nomenclatura v3.1 + legacy, y esqueleto del cliente Sales Layer.

## Estado de la tarea actual
**COMPLETADO:** Estructura base funcional del proyecto.

### Módulos implementados

1. **config.py** — ✅ COMPLETO
   - Todos los mappings v3.1: ASSET_TYPE_MAP (PK->img_pk, 2PK->img_2pk, etc.)
   - LEGACY_MAP: traduce _A -> _PK_01, _5 -> _LF_01, _4 -> _FT_01
   - METADATA_MAP: dam_type, dam_context
   - Campos por tabla: PRODUCT_FIELDS (7 campos), VARIANT_FIELDS (3), THEME_FIELDS (5)
   - Extensiones válidas: jpg, jpeg, png, webp

2. **parser.py** — ✅ COMPLETO
   - `classify_identifier()`: detecta si ID es numérico (product/variant) o alfabético (theme)
   - `parse_filename()`: parsea nomenclatura completa ID_TIPO_SERIE.ext
   - Soporte legacy completo: traduce nombres antiguos automáticamente
   - Devuelve dataclass `ParsedAsset` inmutable con validación

3. **test_parser.py** — ✅ COMPLETO
   - 17 tests pasando:
     - classify_identifier (numérico, alfabético, mixed)
     - parse v3.1 (productos, variantes, temas, series)
     - parse legacy (_A, _5, _4)
     - validación (formato inválido, tipo desconocido, extensión no válida)

4. **saleslayer.py** — 🔄 ESQUELETO
   - Clase `SalesLayerClient` con `__init__` que valida credenciales (.env)
   - Métodos definidos pero sin implementar:
     - `get_product(product_id)` → TODO
     - `get_variant(variant_id)` → TODO
     - `get_theme(theme_id)` → TODO
     - `upload_image(entity_type, entity_id, field_id, image_path)` → TODO
     - `set_metadata(entity_type, entity_id, metadata)` → TODO

5. **dam_ingest.py** — 🔄 ESQUELETO FUNCIONAL
   - Entry point que procesa un directorio de imágenes
   - Parsea cada archivo usando parser.py
   - Determina field_id correcto según entity_type + asset_type
   - La subida real a Sales Layer está como TODO (falta integrar saleslayer.py)
   - Logging básico implementado

6. **Configuración base** — ✅ COMPLETO
   - `.gitignore`: protege .env, __pycache__, .venv, IDE files
   - `.env.example`: template con SL_API_URL, SL_CONNECTOR_ID, SL_SECRET_KEY
   - `requirements.txt`: requests, python-dotenv

## Problemas abiertos

### 1. Ambigüedad identificadores alfabéticos
**Problema:** Identificadores como "DALIA" vs "SOLAR" son indistinguibles sin consultar Sales Layer.
- "SOLAR" es un tema de marketing → tabla THEMES
- "DALIA" podría ser un producto con nombre alfabético → tabla PRODUCTS

**Estado actual:** El parser los marca como `theme` por defecto.

**Qué se intentó:** Clasificación basada solo en formato del identificador (numérico vs alfabético).

**Hipótesis actual:** La resolución real necesita lookup a Sales Layer. El flujo debe ser:
1. Parser intenta clasificar
2. Si alfabético, dam_ingest.py debe hacer get_theme(ID) y get_product(ID)
3. Usar el que exista (o fallar si existe en ambos o en ninguno)

### 2. Credenciales Sales Layer no disponibles
**Problema:** No se tienen las credenciales reales para probar la integración API.

**Pendiente:**
- Obtener credenciales válidas (SL_API_URL, SL_CONNECTOR_ID, SL_SECRET_KEY)
- Documentación de endpoints Sales Layer (formato request/response)
- Verificar si existe entorno staging para testing antes de tocar producción

## Próximo paso concreto

**INMEDIATO al retomar:**
1. Obtener credenciales válidas de Sales Layer y crear archivo `.env` real (desde .env.example)
2. Conseguir documentación API Sales Layer (endpoints, autenticación, rate limits)
3. Implementar método `get_product()` en saleslayer.py como primer endpoint de prueba
4. Verificar conectividad con un request de prueba antes de seguir

**Después de conectividad probada:**
5. Implementar resolución de ambigüedad alfabética (lookup a BD)
6. Implementar upload_image() y set_metadata()
7. Integrar todo en dam_ingest.py
8. Prueba piloto con 10 imágenes

## Notas de sesión

- El proyecto pasó de tener solo documentación a tener una base de código completa y testeada.
- La arquitectura está preparada para separar concerns: config, parsing, API client, orchestration.
- Los tests del parser dan confianza en que la lógica de nomenclatura v3.1 + legacy funciona correctamente.
- El scaffolding sigue las mejores prácticas: .gitignore robusto, credenciales en .env (no en código), tipos inmutables (dataclass).
- Falta: integración con Sales Layer (requiere credenciales + documentación API externa).
