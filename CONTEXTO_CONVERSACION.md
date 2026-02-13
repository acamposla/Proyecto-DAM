# Contexto de Conversación

## Última actualización
2026-02-13 (Final de sesión)

## ¿Qué estábamos haciendo?
Mejoras en la documentación de producción de vídeo (VIDEO_PLAYBOOKS.md). Sesión centrada en estandarizar estructura de playbooks y explorar estrategia multiidioma para vídeos.

## Estado de la tarea actual
**COMPLETADO:** Mejoras en playbooks de vídeo y documentación de ejemplo. Tema abierto: estrategia multiidioma.

### Cambios realizados en esta sesión (2026-02-13)

#### 1. Actualizaciones en VIDEO_PLAYBOOKS.md (reference/)

**VINS (Instalación) — Punto 2:**
- Añadidos: Presentación del producto al inicio (antes de empezar instalación).
- Añadidos: Resumen intro ("¿Qué vas a ver?") antes de estructura.
- Añadidos: Mantenimiento (2-3 tips prácticos) después de instalación.
- Añadidos: CTA Soporte (customer.garza.es) en cierre (sustituye "Cierre" genérico).

**VCN (Conectividad) — Punto 3:**
- Añadidos: Resumen intro ("¿Qué vas a ver?").
- Añadidos: CTA Soporte (customer.garza.es) en cierre.

**VCF (Configuración) — Punto 4 (Reescritura completa):**
- Nuevo criterio: **Esencial vs Avanzada**.
  - **ESENCIAL:** Configuraciones sin las cuales el producto NO funciona (ej: conexión WiFi inicial, dar alta en app). Van PRIMERO.
  - **AVANZADA:** Configuraciones opcionales o de optimización (ej: cambiar zona horaria, ajustar sensibilidad). Van DESPUÉS.
- Estrategia bundlelización: Se pueden agrupar varias configs breves en un solo vídeo si son del mismo nivel de criticidad.
- Badges visuales: Mostrar "ESENCIAL" o "AVANZADO" en pantalla para claridad.
- Añadidos: Resumen intro ("¿Qué vas a ver?").
- Añadidos: CTA Soporte (customer.garza.es) en cierre.

**VTR (Troubleshooting) — Punto 5:**
- Añadidos: Resumen intro ("¿Qué vas a ver?").
- Añadidos: CTA Soporte (customer.garza.es) en cierre (sustituye "Cierre" genérico anterior).

**Patrón común establecido:**
Todos los playbooks (excepto VMK que es marketing) ahora incluyen:
- **Resumen intro:** "¿Qué vas a ver?" — establece expectativas.
- **CTA Soporte:** Cierre dirigiendo a customer.garza.es para soporte adicional.
Esto crea consistencia en experiencia de usuario y facilita producción por lotes.

#### 2. Nuevo archivo de ejemplo creado
- **reference/GUION_VMK_EJEMPLO_401275.md:** Guión ficticio completo para una bombilla LED WiFi Garza Smart siguiendo el playbook VMK. Incluye tiempos, planos, narración y música. Sirve como plantilla para agencias/productoras.

#### 3. Tema abierto para próxima sesión: ESTRATEGIA MULTIIDIOMA DE VÍDEOS

**Problema:** Cómo producir vídeos localizables a otros idiomas con equilibrio coste/calidad.

**Consideraciones clave:**
- **Texto en pantalla:** Difícil de localizar. Preferir iconografía/números universales o plantillas editables (After Effects, Motion, etc.).
- **Voz narrada sin actor en pantalla:** Fácil de sustituir con AI.
  - Herramientas candidatas: ElevenLabs (voz AI premium), HuggingFace SeamlessM4T (voice cloning + TTS), Whisper (transcripción) + TTS local.
- **Actor hablando a cámara:** Lip-sync caro y complejo. Posible solo para VMK (marketing, puede quedarse en inglés/español sin localizar).
- **Separar capas:** Master visual mudo + voz y textos como capas independientes facilita localización.
- **Trade-off:** Actor genera confianza en marketing pero complica localización. Solución posible: actor solo en VMK, voz en off para VINS/VCN/VCF/VTR.
- **YouTube auto-dubbing:** Google ofrece auto-dubbing multiidioma gratis para creadores. Explorar viabilidad para canal Garza.

**Herramientas a evaluar:**
- ElevenLabs (voz AI)
- HuggingFace (SeamlessM4T/MMS para voice cloning)
- Whisper (OpenAI) para transcripción
- YouTube auto-dubbing (Google)

**Estado:** Pendiente de decisión en próxima sesión. Por ahora producir en español con estructura localizable (iconos, capas separadas).

### Módulos del proyecto (estado actual — SIN CAMBIOS en código respecto a sesión anterior)

| Módulo | Estado | Notas |
|--------|--------|-------|
| `config.py` | ✅ COMPLETO v3.2 | Mappings completos para imágenes + vídeo |
| `parser.py` | ✅ COMPLETO v3.2 | Detecta media_type, parsea ambos tipos |
| `test_parser.py` | ✅ 25/25 passing | Cobertura completa (imágenes, vídeos, legacy, inválidos) |
| `saleslayer.py` | 🔄 ESQUELETO | Clase base creada, métodos sin implementar |
| `dam_ingest.py` | 🔄 ESQUELETO FUNCIONAL | Orquestación lista, falta integrar API |

**Documentación actualizada:**
- `reference/VIDEO_PLAYBOOKS.md` → Versión mejorada con patrón común (Resumen + CTA).
- `reference/GUION_VMK_EJEMPLO_401275.md` → Nuevo: ejemplo de guión completo.

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

**OPCIÓN A — Continuar con documentación (NO requiere credenciales):**
1. **Decidir estrategia multiidioma de vídeos:**
   - Evaluar herramientas AI de voz (ElevenLabs, HuggingFace, Whisper).
   - Definir arquitectura de capas (visual mudo + audio independiente).
   - Decidir: ¿Actor solo en VMK o también en VINS/VCN/VCF/VTR?
   - Documentar decisión en nuevo archivo (ej: `docs/estrategia-multiidioma.md`).

**OPCIÓN B — Continuar con código (REQUIERE credenciales — BLOQUEADO):**
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

**DESPUÉS de conectividad probada (solo si OPCIÓN B):**
4. Implementar `get_product()`, `get_variant()`, `get_theme()`.
5. Implementar `upload_image()` y `upload_video()`.
6. Implementar `set_metadata()` (dam_type, dam_context).
7. Resolver ambigüedad identificadores alfabéticos (lookup a BD).
8. Integrar todo en `dam_ingest.py` con manejo de errores robusto.
9. Prueba piloto: 10 activos (5 imágenes + 5 vídeos) en entorno staging.

**RECOMENDACIÓN:** Mientras no haya credenciales, avanzar en OPCIÓN A (estrategia multiidioma). Es trabajo productivo que desbloquea decisiones de producción.

## Notas de sesión (2026-02-13)

### Logros clave
- **Estandarización de playbooks:** Todos los vídeos (excepto VMK) ahora siguen un patrón común: Resumen intro + CTA Soporte (customer.garza.es).
- **Criterio VCF Esencial vs Avanzada:** Jerarquización de configuraciones según criticidad. Esto facilita producción y priorización de vídeos.
- **Guión de ejemplo creado:** GUION_VMK_EJEMPLO_401275.md sirve como plantilla para agencias/productoras.
- **Tema multiidioma identificado:** Se abrió tema estratégico clave para internacionalización del contenido. Pendiente de decisión pero ya se tienen consideraciones técnicas claras.

### Lecciones aprendidas
- **Patrones comunes facilitan producción:** Establecer elementos estándar (Resumen + CTA) reduce fricción en producción y mejora UX.
- **Jerarquización crítica en VCF:** Distinguir entre configuraciones esenciales vs avanzadas evita frustración del usuario (ej: ver vídeo de zona horaria antes del de conectar WiFi sería mal UX).
- **Localización requiere planificación temprana:** Decisiones sobre texto en pantalla, actor vs voz en off, y arquitectura de capas afectan costes de localización dramáticamente.

### Bloqueador crítico (sin cambios)
**Credenciales Sales Layer faltantes:** Todo el desarrollo de integración API está bloqueado hasta obtener credenciales válidas y documentación.

### Tema abierto (nuevo)
**Estrategia multiidioma de vídeos:** Requiere decisión sobre herramientas AI, arquitectura de capas y trade-offs actor/voz. Bloquea escalamiento internacional del contenido.

### Próxima milestone
**Opción A (preferida mientras no haya credenciales):** Definir estrategia multiidioma de vídeos.
**Opción B (si se obtienen credenciales):** Integración API Sales Layer.
