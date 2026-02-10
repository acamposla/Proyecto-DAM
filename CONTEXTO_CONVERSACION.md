# CONTEXTO_CONVERSACION.md - Historial de Decisiones

## Resumen Ejecutivo
Alejandro Campos (Garza/Imprex) comenzó buscando una solución técnica para conectar SQL con un FTP para agencias. A través del diagnóstico, pivotamos hacia construir un **DAM nativo dentro de Sales Layer**, aprovechando que ya es la "Fuente de la Verdad".

## Evolución de las Decisiones Clave

### 1. Del FTP al PIM
* **Idea Original:** SQL genera CSV -> FTP.
* **Problema:** Redundancia de datos y obsolescencia.
* **Decisión:** Usar el Brand Portal de Sales Layer. La dificultad residía en cómo clasificar imágenes "huérfanas" (Banners, Estilos de vida genéricos) que no pertenecen a un producto específico.

### 2. El Problema del "GAP" (Temas Transversales)
* **Reto:** ¿Dónde guardamos una foto de "Energía Solar" si no es un producto?
* **Solución:** Creamos una **Tabla de Referencia** llamada `TEMAS_MARKETING`.
* **Lógica:** Tratamos los Temas (`SOLAR`, `WIFI`) como si fueran "Productos Ficticios" con sus propias galerías de imágenes. Esto permite maquetación automática en EasyCatalog (haciendo Join por ID).

### 3. Evolución de la Nomenclatura
Pasamos por 3 fases hasta llegar a la definitiva:
1.  *Legacy:* `ID_Variante_A`, `ID_KV`. (Mantenemos compatibilidad).
2.  *Propuesta Académica:* `SKU_TYPE_CONTEXT`. (Descartada por compleja y romper el legado).
3.  **Definitiva (v3.1):** `ID_CODIGO_SERIE`.
    * Unificamos series a numérico (`_01` en vez de `_A`).
        * Introdujimos códigos específicos de negocio (`FMD` para mosaicos descompuestos, `KVV` para vertical).

        ### 4. Estrategia de Ingesta (El Script)
        * Se decidió no obligar a los diseñadores a rellenar metadatos manualmente.
        * **Automatización:** Un script Python (`dam_ingest.py`) leerá el nombre del archivo y rellenará los campos en Sales Layer.
        * **Escalabilidad:** Se definió una estrategia para contenido efímero (Redes Sociales/Influencers) usando una "Zona de Aterrizaje" en SharePoint antes de subir lo definitivo al PIM.

        ### 5. Estructura de Base de Datos Final
        Se acordó una estructura de "Bocadillos" (Slots) de imagen específicos en lugar de una bolsa común, para facilitar la integración con Amazon y Web:
        * Separación estricta entre `PK` (Producto suelto) y `2PK` (Caja).
        * Inclusión de `KVV` (Vertical) para Mobile First.

        ## Tareas Pendientes Inmediatas
        El usuario ha creado la estructura de tablas en Sales Layer. Lo único que falta es **escribir y desplegar el c
        ódigo Python** que ejecuta la lógica de clasificación.


