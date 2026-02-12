"""Cliente para la API de Sales Layer.

TODO: Implementar cuando se disponga de credenciales y documentación
      de la API de Sales Layer (endpoints, autenticación, formato).
"""

import requests

from .config import SL_API_URL, SL_CONNECTOR_ID, SL_SECRET_KEY


class SalesLayerClient:
    """Wrapper para la API de Sales Layer."""

    def __init__(self):
        if not SL_CONNECTOR_ID or not SL_SECRET_KEY:
            raise ValueError(
                "Faltan credenciales de Sales Layer. "
                "Configura SL_CONNECTOR_ID y SL_SECRET_KEY en .env"
            )
        self.base_url = SL_API_URL
        self.connector_id = SL_CONNECTOR_ID
        self.secret_key = SL_SECRET_KEY

    # TODO: Implementar métodos según documentación API Sales Layer
    # - get_product(identifier) -> dict | None
    # - get_variant(identifier) -> dict | None
    # - get_theme(identifier) -> dict | None
    # - upload_image(table, record_id, field_id, image_path) -> bool
    # - set_metadata(table, record_id, dam_type, dam_context) -> bool
