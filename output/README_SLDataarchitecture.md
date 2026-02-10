# 📘 Protocolo Maestro: Arquitectura DAM & Nomenclatura (Imprex/Garza)

**Versión:** 3.1 (Producción)
**Estado:** DEFINITIVO
**Responsable:** Alejandro Campos (Dirección & Data Strategy)
**Fecha:** Febrero 2026

---

## 1. Visión y Objetivo

Transformar Sales Layer en un **DAM (Digital Asset Management) Automatizado**.
Eliminamos la carga manual de datos. El diseñador solo tiene una responsabilidad: **Nombrar el archivo correctamente**. Un script ("El Robot") leerá ese nombre y clasificará la imagen en su lugar correspondiente automáticamente.

**Principios:**

1. **Fórmula Única:** Tanto Productos como Temas usan la misma estructura de nombre.
2. **Series Numéricas:** Abandonamos `_A`, `_B`. Todo es `_01`, `_02`.
3. **Segregación Lógica:** Diferenciamos claramente entre Producto (SKU), Caja (Packaging) y Concepto (Tema).

---

## 2. Arquitectura de Datos: Los 3 Silos

| Silo | Contenido | Ubicación PIM | Gestión |
| --- | --- | --- | --- |
| **A. Galería Visual** | JPG, PNG, WEBP | Pestaña "Imágenes" | **Automatizada.** El script clasifica. |
| **B. Editables** | AI, PSD, PDF | Pestaña "Archivos" | **Manual.** Repositorio de trabajo. |
| **C. Iconografía** | SVG | Galería + CSV Lógico | **Híbrida.** Visual + Reglas. |

---

## 3. Protocolo de Nomenclatura (Naming Convention)

Todo archivo debe cumplir estrictamente esta fórmula matemática:

### A. Diccionario de TIPOS (Códigos)

Estos son los únicos sufijos permitidos. El script los leerá para saber en qué "bocadillo" de Sales Layer soltar la imagen.

| Código | Significado | Metadata TYPE | Metadata CONTEXT | Uso Principal |
| --- | --- | --- | --- | --- |
| **PK** | **Packshot** | Packshot | Standard | Producto suelto (sin caja), fondo blanco. |
| **2PK** | **Packaging** | Packshot | Packaging Box | La caja sola (Packaging). |
| **3PK** | **Combo** | Packshot | Combo | Bodegón de Producto + Caja. |
| **KV** | **Key Visual** | Marketing | Hero | Banner principal horizontal. |
| **KVV** | **Key Visual Vertical** | Marketing | Hero Vertical | Banner vertical (Stories/Móvil). |
| **LF** | **Lifestyle** | Lifestyle | Standard | Foto de ambiente / uso. |
| **FT** | **Features** | Detail | Feature | Iconos o Zooms a características. |
| **FM** | **Feature Mosaic** | Infographic | Mosaic | El mosaico de características completo. |
| **FMD** | **Mosaic Part** | Infographic | Decomposed | Pieza suelta/descompuesta del mosaico. |

### B. Diccionario de SERIES

* Siempre **Dos Dígitos**: `01`, `02`, `03`... `99`.
* *Regla:* Aunque solo haya una imagen, el `01` es obligatorio.

---

## 4. Escenarios de Aplicación (Ejemplos)

### Escenario 1: PRODUCTO / VARIANTE (El 80%)

*El Identificador es el ID de Modelo, Referencia o ID de Variante.*

| Archivo Real | Descripción del Contenido |
| --- | --- |
| **`401275_PK_01.jpg`** | Bombilla suelta, fondo blanco. |
| **`401275_2PK_01.jpg`** | La caja de la bombilla sola. |
| **`DALIA_KV_01.jpg`** | Banner horizontal del ventilador Dalia. |
| **`DALIA_KVV_01.jpg`** | Banner vertical del ventilador Dalia. |
| **`DALIA_FMD_04.jpg`** | La cuarta pieza del mosaico de características. |

### Escenario 2: TEMA / GAP (El 20%)

*El Identificador es un CONCEPTO transversal (Tecnología, Familia, Campaña). No se vincula a un producto físico, sino a la Tabla de Temas.*

* **Identificadores Válidos:** `SOLAR`, `SMART`, `WIFI`, `ZIGBEE`, `BOMBILLAS`, `REGLETAS`.

| Archivo Real | Descripción del Contenido |
| --- | --- |
| **`SOLAR_LF_01.jpg`** | Familia en un jardín con luces solares (Lifestyle). |
| **`SMART_KV_01.jpg`** | Banner principal de la categoría Smart Home. |
| **`WIFI_FT_01.jpg`** | Icono o detalle explicativo sobre el Wifi. |

---

## 5. Especificación Técnica de Campos (Sales Layer)

Esta es la configuración exacta que debe tener Sales Layer para que el script funcione.
*Todos los campos de imagen deben ser **Multi-Image**.*

### A. Tabla PRODUCTOS (Products)

*Donde viven los Modelos.*

| Nombre Visible (Label) | Código Interno (Field ID) | Sufijo Asociado |
| --- | --- | --- |
| **Packshot (Main)** | `img_pk` | `_PK` |
| **Key Visual (Hero)** | `img_kv` | `_KV` |
| **Key Visual (Vert)** | `img_kvv` | `_KVV` |
| **Feature Mosaic** | `img_fm` | `_FM` |
| **Mosaic Parts** | `img_fmd` | `_FMD` |
| **Features (Detail)** | `img_ft` | `_FT` |
| **Lifestyle** | `img_lf` | `_LF` |

### B. Tabla VARIANTES (Variants)

*Donde viven los SKUs de venta.*

| Nombre Visible (Label) | Código Interno (Field ID) | Sufijo Asociado | Nota de Uso |
| --- | --- | --- | --- |
| **Producto Suelto** | `img_pk` | `_PK` | Sin embalaje. |
| **Packaging (Caja)** | `img_2pk` | `_2PK` | Solo caja. |
| **Combo** | `img_3pk` | `_3PK` | Prod + Caja. |

### C. Tabla TEMAS DE MARKETING (Themes Reference)

*La nueva tabla para conceptos transversales.*

* **ID Tabla:** `TEMAS_MARKETING`
* **Campos Obligatorios:** `Reference` (Código Tema), `Name` (Nombre Legible).

| Nombre Visible (Label) | Código Interno (Field ID) | Sufijo Asociado |
| --- | --- | --- |
| **Key Visual (Hero)** | `img_kv` | `_KV` |
| **Lifestyle** | `img_lf` | `_LF` |
| **Feature Mosaic** | `img_fm` | `_FM` |
| **Mosaic Parts** | `img_fmd` | `_FMD` |
| **Features** | `img_ft` | `_FT` |

---

## 6. Plan de Migración (Legacy)

El script incluirá reglas de traducción para no obligar a renombrar el histórico inmediatamente, aunque se recomienda el cambio progresivo.

**Reglas de Traducción Automática (Script):**

* Si encuentra `_A` (Legacy)  Tratar como `_PK_01`.
* Si encuentra `_5` (Legacy)  Tratar como `_LF_01`.
* Si encuentra `_4` (Legacy)  Tratar como `_FT_01`.

> **Mandato:** Todo archivo **NUEVO** creado a partir de la fecha de aprobación debe usar el protocolo v3.1 (`_01`, `_KV`, `_PK`).

---

## 7. Tabla Auxiliar de Metadatos

Además de colocar la foto en su "bocadillo" (Field ID), el script rellenará una tabla de metadatos invisible para mejorar los filtros del Brand Portal.

**Valores que escribirá el Script:**

| Sufijo Archivo | Escribe TYPE | Escribe CONTEXT |
| --- | --- | --- |
| `_PK`, `_3PK` | Packshot | Standard / Combo |
| `_2PK` | Packshot | Packaging Box |
| `_KV` | Marketing | Hero |
| `_KVV` | Marketing | Hero Vertical |
| `_LF` | Lifestyle | Standard |
| `_FM`, `_FMD` | Infographic | Mosaic / Decomposed |
| `_FT` | Detail | Feature |

---

### Siguientes Pasos de Ejecución

1. **Configuración SL:** Crear los campos con los IDs exactos (`img_pk`, `img_kvv`...) listados en la Sección 5.
2. **Scripting:** Desarrollar `dam_ingest.py` basado en este diccionario.
3. **Go Live:** Validar con 5 imágenes de prueba (una de cada tipo).
