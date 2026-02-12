# �� Protocolo de Gestión de Vídeo v1.0 (Anexo al DAM)

**Contexto:** Simplificación de la estrategia de contenidos audiovisuales para Garza/Imprex.
**Objetivo:** Reducir la complejidad de 8 tipos a 5 categorías maestras basadas en la intención del usuario y la etapa del Customer Journey.

---

## 1. Estrategia de Consolidación (Los 5 Tipos)

Hemos agrupado los vídeos según el problema que resuelven al usuario, evitando campos vacíos innecesarios en Sales Layer.

### A. Fase "Seducción" (Marketing & Función)
* **Nuevo Código:** `VMK` (Video Marketing)
* **Consolida:** `VID_MK` + `VID_FUN`.
* **Razón:** No distinguimos entre "Anuncio" y "Funcionamiento". Un buen vídeo de marketing *muestra* cómo funciona el producto para generar deseo.

### B. Fase "Hardware" (Instalación Física)
* **Nuevo Código:** `VINS` (Video Installation)
* **Consolida:** `VID_INS`.
* **Razón:** El montaje físico (taladros, cables, clemas) es un dolor distinto al digital. Requiere seguridad y planos detalle físicos.

### C. Fase "Conectividad" (El Cruce del Valle)
* **Nuevo Código:** `VCN` (Video Connectivity / IoT)
* **Consolida:** `VID_VIN`.
* **Razón:** Crítico para Garza Smart Home. Es el punto de fricción nº1 (devoluciones por "no vincula"). Merece campo exclusivo separado de la instalación física.

### D. Fase "Software" (Configuración y Uso)
* **Nuevo Código:** `VCF` (Video Config)
* **Consolida:** `VID_CON` + `VID_PRO`.
* **Razón:** Configurar la App y programar escenas/rutinas son tareas de software contiguas que ocurren en la pantalla del móvil.

### E. Fase "Socorro" (Soporte)
* **Nuevo Código:** `VTR` (Video Troubleshooting)
* **Consolida:** `VID_TRO` + `VID_Q&A`.
* **Razón:** Contenido reactivo. El usuario solo lo busca cuando tiene un problema o bloqueo específico.

---

## 2. Nomenclatura de Archivos (Protocolo v3.2)

Integramos los vídeos en la fórmula maestra `ID_TIPO_SERIE`.
*Nota: Los vídeos usan códigos de 3 letras para distinguirse visualmente de las imágenes (2 letras).*

**Fórmula:** `IDENTIFICADOR` + `_` + `CÓDIGO` + `_` + `SERIE` + `.mp4`

| Código | Categoría | Metadata TYPE | Metadata CONTEXT | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **VMK** | Marketing | Marketing | Demo / Hero | `401275_VMK_01.mp4` |
| **VINS** | Instalación | Technical | Installation | `401275_VINS_01.mp4` |
| **VCN** | Conectividad | Technical | Pairing / IoT | `401275_VCN_01.mp4` |
| **VCF** | Configuración | Technical | App Usage | `401275_VCF_01.mp4` |
| **VTR** | Soporte | Support | Troubleshooting | `401275_VTR_01.mp4` |

---

## 3. Configuración Técnica en Sales Layer

Se deben crear 5 nuevos campos en la pestaña de **Vídeos** (o en la sección DAM si se prefiere unificar).
* **Tipo de Campo recomendado:** Enlace de Vídeo (Video Link) para YouTube/Vimeo, o Archivo (File) si son clips cortos (<20MB).

| Nombre Visible (Label) | Código Interno (Field ID) | Uso |
| :--- | :--- | :--- |
| **Video Marketing (Hero)** | `vid_mk` | Para archivos `_VMK` |
| **Video Instalación (Físico)** | `vid_ins` | Para archivos `_VINS` |
| **Video Conectividad (Pairing)**| `vid_cn` | Para archivos `_VCN` |
| **Video Configuración (App)** | `vid_cf` | Para archivos `_VCF` |
| **Video Ayuda (Troubleshoot)** | `vid_tr` | Para archivos `_VTR` |
