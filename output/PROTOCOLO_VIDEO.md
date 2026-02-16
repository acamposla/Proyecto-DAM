# Protocolo de Gestión de Vídeo v2.0 (Anexo al DAM)

**Contexto:** Simplificación de la estrategia de contenidos audiovisuales para Garza/Imprex.
**Objetivo:** Reducir la complejidad a 3 categorías maestras basadas en la intención del usuario y la etapa del Customer Journey.

---

## 1. Estrategia de Consolidación (Los 3 Tipos)

Hemos agrupado los vídeos según el problema que resuelven al usuario.

### A. Fase "Seducción" (Marketing & Función)
* **Código:** `VMK` (Video Marketing)
* **Consolida:** Marketing + Funcionamiento.
* **Razón:** Un buen vídeo de marketing *muestra* cómo funciona el producto para generar deseo. No distinguimos entre "Anuncio" y "Funcionamiento".

### B. Fase "Setup" (Instalación + Conectividad + Configuración)
* **Código:** `VSET` (Video Setup)
* **Consolida:** Instalación Física + Conectividad IoT + Configuración App.
* **Razón:** El usuario quiere un solo recurso que le lleve de "abrir la caja" a "producto funcionando". El vídeo es modular: incluye solo las secciones que el producto necesite (instalar, conectar, configurar). Un aplique solar solo necesita instalación. Una bombilla smart solo conectividad + configuración. Una cámara IP necesita las tres.

### C. Fase "Socorro" (Soporte)
* **Código:** `VTR` (Video Troubleshooting)
* **Consolida:** Troubleshooting + FAQ.
* **Razón:** Contenido reactivo. El usuario solo lo busca cuando tiene un problema o bloqueo específico.

---

## 2. Nomenclatura de Archivos (Protocolo v4.0)

Integramos los vídeos en la fórmula maestra `ID_TIPO_SERIE`.
*Nota: Los vídeos usan códigos de 3+ letras para distinguirse visualmente de las imágenes (2 letras).*

**Fórmula:** `IDENTIFICADOR` + `_` + `CÓDIGO` + `_` + `SERIE` + `.mp4`

| Código | Categoría | Metadata TYPE | Metadata CONTEXT | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **VMK** | Marketing | Marketing | Demo / Hero | `401275_VMK_01.mp4` |
| **VSET** | Setup | Technical | Setup Guide | `401275_VSET_01.mp4` |
| **VTR** | Soporte | Support | Troubleshooting | `401275_VTR_01.mp4` |

---

## 3. Configuración Técnica en Sales Layer

Se deben crear 3 campos en la pestaña de **Vídeos** (o en la sección DAM si se prefiere unificar).
* **Tipo de Campo recomendado:** Enlace de Vídeo (Video Link) para YouTube/Vimeo, o Archivo (File) si son clips cortos (<20MB).

| Nombre Visible (Label) | Código Interno (Field ID) | Uso |
| :--- | :--- | :--- |
| **Video Marketing (Hero)** | `vid_mk` | Para archivos `_VMK` |
| **Video Setup (Guía)** | `vid_set` | Para archivos `_VSET` |
| **Video Ayuda (Troubleshoot)** | `vid_tr` | Para archivos `_VTR` |
