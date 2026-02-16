# Contexto de Conversación

## Última actualización
2026-02-16 (Sesión de unificación de vídeo v4.0)

## ¿Qué estábamos haciendo?
Simplificación del modelo de vídeos. Se detectó que tener 5 tipos de vídeo era complejo para agencias y usuario. El objetivo real es que cada producto tenga un solo vídeo de setup que le lleve de "abrir la caja" a "producto funcionando". Se decidió fusionar los tres tipos de setup (VINS, VCN, VCF) en uno solo modular (VSET).

## Estado de la tarea actual
**COMPLETADO.** La unificación v4.0 está implementada, testeada, documentada y pusheada a main.

### Cambios realizados en esta sesión (2026-02-16) — UNIFICACIÓN v4.0

#### 1. Decisión estratégica: VINS+VCN+VCF → VSET
**Motivación:** El usuario expresó que tener 5 tipos de vídeo era complejo. Su objetivo real: UN recurso de setup por producto que le lleve de "abrir la caja" a "producto funcionando", pero modular (no todos los productos necesitan las 3 secciones).

**Solución:**
- Fusionar VINS (Instalación) + VCN (Conectividad) + VCF (Configuración) en un solo tipo: **VSET** (Video Setup).
- VSET tiene estructura modular: Intro obligatoria + Sección A (Instalación) + Sección B (Conectividad) + Sección C (Configuración: Esencial/Avanzada) + Cierre obligatorio.
- Cada producto solo incluye las secciones que necesita. Ejemplos:
  - Aplique solar: solo Sección A (instalación física).
  - Bombilla smart: solo Sección B + C (conectividad + configuración).
  - Cámara IP: Secciones A + B + C (instalación + conectividad + configuración).

**Resultado:** De 5 a 3 tipos de vídeo (VMK, VSET, VTR). De 5 a 3 campos en Sales Layer (vid_mk, vid_set, vid_tr).

#### 2. Actualizaciones en código (v4.0)

**src/config.py:**
- Eliminados: VINS, VCN, VCF de METADATA_MAP.
- Añadido: VSET ('video', 'setup').
- PRODUCT_FIELDS y THEME_FIELDS actualizados: vid_mk, vid_set, vid_tr (3 campos en vez de 5).

**src/parser.py:**
- Sin cambios. Ya soportaba códigos de 3-4 letras.

**tests/test_parser.py:**
- 26 tests (antes 25).
- Añadidos:
  - `test_vset_code()` — verifica que VSET es reconocido como vídeo de setup.
  - `test_old_video_codes_are_invalid()` — verifica que VINS, VCN, VCF son rechazados (retornan None).
- Eliminados tests de códigos antiguos (test_vins_code, test_vcn_code, test_vcf_code).

**src/dam_ingest.py:**
- Actualizado por usuario a v3.2 con bifurcación upload_video/upload_image en TODOs.

#### 3. Documentación actualizada

**output/PROTOCOLO_VIDEO.md:**
- Reescrito como v2.0.
- Especificación normativa de los 3 tipos de vídeo (VMK, VSET, VTR).
- VSET descrito como modular.

**reference/VIDEO_PLAYBOOKS.md:**
- Reescrito como v4.0.
- VSET tiene estructura detallada por secciones (Intro, A, B, C, Cierre).
- Tabla de "Qué secciones necesita cada producto" con ejemplos.
- Jerarquía Esencial/Avanzada en Sección C (Configuración).
- Tiempos estimados por bloque.

**reference/GUION_VMK_EJEMPLO_401275.md:**
- Sin cambios (es ejemplo de VMK, no afectado por unificación).

#### 4. Commits de esta sesión
- **eaf8f67:** Unify VINS+VCN+VCF into VSET: modular setup video (v4.0)
  Pusheado a origin main.

### Módulos del proyecto (estado actual — v4.0)

| Módulo | Estado | Notas |
|--------|--------|-------|
| `config.py` | ✅ COMPLETO v4.0 | 3 códigos de vídeo (VMK, VSET, VTR). Campos reducidos (vid_mk, vid_set, vid_tr) |
| `parser.py` | ✅ COMPLETO v4.0 | Sin cambios. Ya soportaba códigos de longitud variable |
| `test_parser.py` | ✅ 26/26 passing | Cobertura completa: imágenes, vídeos, legacy, códigos inválidos, old codes rejected |
| `saleslayer.py` | 🔄 ESQUELETO | Clase base creada, métodos sin implementar (bloqueado: credenciales) |
| `dam_ingest.py` | 🔄 ESQUELETO FUNCIONAL | Actualizado a v3.2 con bifurcación upload_video/upload_image |

**Documentación actualizada (v4.0):**
- `output/PROTOCOLO_VIDEO.md` → v2.0 con 3 tipos de vídeo.
- `reference/VIDEO_PLAYBOOKS.md` → v4.0 con VSET modular (secciones A/B/C).
- `CLAUDE.md` → Actualizado completamente a v4.0.

## Problemas abiertos

**Ninguno técnico.** La implementación v4.0 está estable y completa en su scope actual.

### Bloqueos externos

**1. Credenciales Sales Layer NO disponibles (BLOQUEANTE para integración API)**

**Necesario para continuar con integración:**
- `SL_API_URL`: Endpoint base de Sales Layer.
- `SL_CONNECTOR_ID`: ID del conector del proyecto.
- `SL_SECRET_KEY`: Clave secreta de autenticación.
- Documentación API: Formato request/response, autenticación, rate limits.
- Entorno staging (opcional pero recomendado para testing).

**Impacto:** Bloquea implementación de `saleslayer.py` (get_product, get_variant, get_theme, upload_image, upload_video, set_metadata) y toda la integración con dam_ingest.py.

**2. Estrategia multiidioma de vídeos (Por definir)**

**Problema:** Cómo producir vídeos localizables a otros idiomas con equilibrio coste/calidad.

**Consideraciones clave:**
- Texto en pantalla = difícil de localizar. Preferir iconografía/números universales o plantillas editables.
- Voz narrada sin actor en pantalla = fácil de sustituir con AI (ElevenLabs, HuggingFace SeamlessM4T, Whisper+TTS).
- Actor hablando a cámara = lip-sync caro. Posible solo para VMK (marketing, no se localiza).
- Separar capas: master visual mudo + voz y textos como capas independientes.
- Trade-off: Actor genera confianza en marketing pero complica localización. Solución posible: actor solo en VMK, voz en off para VSET/VTR.

**Herramientas a evaluar:** ElevenLabs, HuggingFace (SeamlessM4T/MMS), Whisper (OpenAI), YouTube auto-dubbing.

**Estado:** Pendiente de decisión en próxima sesión. Ver sección "Deuda Técnica Conocida" en CLAUDE.md para detalles completos.

**3. Ambigüedad identificadores alfabéticos (No bloqueante, requiere API)**

**Problema:** Identificadores como "DALIA" vs "SOLAR" no se pueden clasificar sin consultar BD.

**Estado actual:** Parser usa heurística (uppercase -> theme, alphanumeric -> product).

**Solución definitiva:** Requiere implementar lookup a Sales Layer:
1. dam_ingest.py intenta clasificar con parser.
2. Si alfabético, hace `get_theme(ID)` y `get_product(ID)`.
3. Usa el que exista (o error si ambiguo/inexistente).

**Dependencia:** Necesita cliente API funcional (bloqueo #1).

## Próximo paso concreto

**OPCIÓN A — Obtener credenciales Sales Layer (si se obtienen):**
1. Implementar métodos reales en `src/saleslayer.py`:
   - `get_product(product_id)` — GET a `/products/{id}`
   - `get_variant(variant_id)` — GET a `/variants/{id}`
   - `get_theme(theme_id)` — GET a `/themes/{id}` (o endpoint equivalente)
   - `upload_image(file_path)` — POST multipart/form-data
   - `upload_video(file_path)` — POST multipart/form-data
   - `set_metadata(entity_type, entity_id, field_name, value)` — PATCH/PUT según API
2. Verificar acceso con método de prueba (ej: `get_connector_info()`).
3. Integrar en `dam_ingest.py` con manejo de errores + rate limits.
4. Prueba piloto: 10 activos reales (5 imágenes + 5 vídeos) contra Sales Layer staging/producción.

**OPCIÓN B — Definir estrategia multiidioma de vídeos (NO requiere credenciales):**
1. Evaluar herramientas AI de voz (ElevenLabs, HuggingFace, Whisper).
2. Definir arquitectura de capas (visual mudo + audio independiente + textos como capa).
3. Decidir: ¿Actor solo en VMK o también en VSET/VTR?
4. Documentar decisión en `docs/estrategia-multiidioma.md` o similar.
5. Crear plantillas/especificaciones para agencias (separación de capas).

**OPCIÓN C — Documentación consolidada para agencias (NO requiere credenciales):**
1. Crear guía unificada de nomenclatura (imágenes + vídeos v4.0) en formato PDF/doc.
2. Incorporar referencias a playbooks de vídeo (VIDEO_PLAYBOOKS.md).
3. Incluir ejemplos visuales (diagramas de flujo, tablas de códigos).
4. Documentar proceso de subida (cuando dam_ingest.py esté integrado).
5. Crear FAQ para diseñadores/videógrafos.

**RECOMENDACIÓN:**
- Si se obtienen credenciales pronto: OPCIÓN A.
- Si no: OPCIÓN B (estrategia multiidioma) o OPCIÓN C (documentación agencias). Ambas son trabajo productivo que desbloquea decisiones de producción e internacionalización.

## Notas de sesión (2026-02-16)

### Logros clave
- **Unificación de vídeo v4.0 completada:** De 5 a 3 tipos de vídeo (VMK, VSET, VTR). De 5 a 3 campos en Sales Layer.
- **VSET modular implementado:** Estructura con secciones A/B/C permite adaptar contenido a cada producto sin multiplicar archivos.
- **Tests actualizados (26/26 passing):** Añadido test que verifica rechazo de códigos antiguos (VINS, VCN, VCF).
- **Documentación completa reescrita:** PROTOCOLO_VIDEO.md v2.0 + VIDEO_PLAYBOOKS.md v4.0 + CLAUDE.md actualizado.
- **Código limpio y versionado:** Commit eaf8f67 pusheado a main.

### Ventajas de la unificación v4.0
- **Menos archivos:** 3 vídeos por producto en vez de 5. Reduce complejidad de gestión.
- **Menos campos en BD:** 3 campos (vid_mk, vid_set, vid_tr) en vez de 5. Simplifica esquema.
- **Menos confusión para agencias:** "Necesito el vídeo de setup" es más claro que "¿Necesito VINS, VCN, VCF o los tres?".
- **Más flexible:** Un producto simple puede tener un VSET de 90 segundos (solo instalación), uno complejo de 5 minutos (instalación + conectividad + configuración).
- **Mantiene modularidad:** Cada producto solo incluye las secciones que necesita. No hay vídeos con contenido irrelevante.

### Por qué unificamos VINS+VCN+VCF
El usuario expresó que el objetivo real no es tener 3 vídeos separados de setup, sino UN recurso que lleve al usuario de "abrir la caja" a "producto funcionando". La separación en 3 archivos creaba fricción:
- Usuario tiene que buscar 3 vídeos diferentes.
- Agencias tienen que producir/entregar 3 archivos por producto.
- Gestión complica: ¿qué productos necesitan qué vídeos?

Con VSET modular: UN archivo, las secciones que el producto necesite. Ejemplos:
- Aplique solar exterior: VSET con solo Sección A (instalación física, tornillos, orientación).
- Bombilla WiFi: VSET con solo Sección B + C (conexión WiFi + configuración app).
- Cámara IP: VSET con Sección A + B + C (instalación, conexión, configuración completa).

### Cambio en nomenclatura (v4.0)
**Códigos eliminados (ahora rechazados):**
- VINS (Instalación)
- VCN (Conectividad)
- VCF (Configuración)

**Código nuevo:**
- VSET (Setup modular)

Ejemplo: `401275_VSET_01.mp4` (bombilla LED WiFi Garza Smart, incluye solo Sección B: Conectividad + Sección C: Configuración).

### Tests críticos añadidos
1. **test_vset_code():** Verifica que VSET es reconocido como vídeo tipo "setup".
2. **test_old_video_codes_are_invalid():** Verifica que VINS, VCN, VCF retornan None (son rechazados). Esto asegura que no se usen códigos antiguos por error o confusión.

### Estado del código (v4.0)
- **config.py**: Limpio. Solo 3 códigos de vídeo en METADATA_MAP. Campos reducidos en PRODUCT_FIELDS/THEME_FIELDS.
- **parser.py**: Sin cambios. Ya soportaba códigos de longitud variable (2-4 letras).
- **test_parser.py**: 26/26 tests pasando. Cobertura: imágenes, vídeos, legacy, códigos inválidos, old codes rejected.
- **saleslayer.py**: Esqueleto. Necesita credenciales para implementar métodos reales.
- **dam_ingest.py**: Esqueleto funcional. Actualizado a v3.2 con bifurcación upload_video/upload_image en TODOs.

### Documentación actualizada (v4.0)
- **output/PROTOCOLO_VIDEO.md (v2.0):** Especificación normativa de los 3 tipos de vídeo para uso interno/técnico.
- **reference/VIDEO_PLAYBOOKS.md (v4.0):** Guías de producción para agencias/videógrafos. VSET con estructura modular detallada, tabla de ejemplos por tipo de producto, tiempos estimados.
- **CLAUDE.md:** Actualizado completamente a v4.0 (secciones 2, 3, 4, 6, 7, 9). Estado actual, arquitectura, nomenclatura, decisiones tomadas, próximos pasos.

### Lecciones aprendidas
- **Simplificar sin perder flexibilidad:** La unificación redujo complejidad sin sacrificar capacidad de adaptar contenido a cada producto.
- **Testing de regresión es crítico:** El test `test_old_video_codes_are_invalid()` previene errores futuros si alguien intenta usar códigos antiguos.
- **Documentación de transición:** Importante documentar POR QUÉ se hizo el cambio (contexto de negocio) y QUÉ códigos quedaron obsoletos.

### Bloqueadores externos (sin cambios)
1. **Credenciales Sales Layer faltantes:** Bloquea integración API.
2. **Estrategia multiidioma:** Pendiente de definir (herramientas AI, arquitectura de capas, trade-offs actor/voz).

### Próximas iteraciones posibles
1. **Si se obtienen credenciales:** Implementar cliente API Sales Layer y prueba piloto con 10 activos.
2. **Si no:** Trabajar en estrategia multiidioma de vídeos o documentación consolidada para agencias.
3. **Opcional:** Crear herramienta de validación de nomenclatura (CLI que verifica archivos antes de subir).

---

## Resumen ejecutivo (para retomar en próxima sesión)

**Dónde estamos:**
- Modelo de vídeo v4.0 completo: 3 tipos (VMK, VSET, VTR).
- VSET modular: estructura con secciones A/B/C adaptable a cada producto.
- Parser Python funcionando: 26/26 tests pasando, incluyendo rechazo de códigos antiguos.
- Documentación técnica y de producción completa y actualizada.
- Código limpio, testeado, versionado y pusheado a main.

**Qué falta:**
- Integración con API Sales Layer (bloqueado por credenciales).
- Definir estrategia de localización de vídeos (multiidioma).
- Probar con activos reales en Sales Layer (requiere API funcional).
- Documentación consolidada para agencias (guía + playbooks + ejemplos).

**Siguiente acción recomendada:**
1. **Si se obtienen credenciales Sales Layer:** Implementar métodos reales en saleslayer.py (get_product, upload_image, upload_video, set_metadata).
2. **Si NO hay credenciales:** Trabajar en estrategia multiidioma de vídeos (evaluar ElevenLabs, HuggingFace, definir arquitectura de capas) o crear documentación consolidada para agencias.

**Estado del proyecto:** Estable. Fase de desarrollo completada. Bloqueado para integración (credenciales), desbloqueado para documentación/estrategia.
