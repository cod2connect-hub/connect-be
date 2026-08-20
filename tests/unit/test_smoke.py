from app.core.config import settings
from app.tenants.application.services import slugify_subdomain


def test_settings_load_and_slugify() -> None:
    assert settings.app_name == "Connect Backend"
    assert settings.app_version == "0.1.0"
    assert slugify_subdomain("My Restaurant") == "my-restaurant"
