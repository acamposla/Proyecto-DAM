# CLAUDE.md - Contexto del Proyecto DAM Garza/Imprex

## 1. Perfil del Proyecto
* **Rol:** Ingeniero de Datos & Arquitecto de Soluciones.
* **Objetivo:** Implementar un **DAM (Digital Asset Management)** automatizado sobre **Sales Layer (PIM)** sin costes de licencias externas.
* **Filosofía:** "Zero-Click Metadata". El diseñador nombra el archivo, el sistema (Script Python) lo clasifica.

## 2. Estado Actual (Snapshot)
* **Arquitectura:** Definida (Modelo v3.1).
* **Bbase de Datos:** Campos creados en Sales Layer (Productos, Variantes y Tabla Temas).
* **Pendiente:** Desarrollo del script Python (`dam_ingest.py`) y despliegue.

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

## 6. Siguientes Pasos (Roadmap)
1.  **Scripting:** Crear `dam_ingest.py`. Debe:
    * Conectar a API Sales Layer.
        * Parsear nombres de archivo.
            * Detectar si el ID es Producto o Tema.
                * Vincular la imagen al campo correcto (`img_xx`).
                    * Rellena la tabla auxiliar de metadatos (`dam_type`, `dam_context`).
                    2.  **Ingesta:** Probar con 10 imágenes piloto.
                    3.  **Documentación:** Generar guía final para Agencias.
