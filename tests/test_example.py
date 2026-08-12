"""Example test to verify setup"""
import pytest
from src.core.config import settings
from src.tenants.service import slugify_subdomain


def test_settings_loaded():
    """Test that settings are loaded properly"""
    assert settings.APP_NAME == "Connect Backend"
    assert settings.APP_VERSION == "0.1.0"


def test_slugify_subdomain():
    """Test subdomain slugification"""
    assert slugify_subdomain("My Restaurant") == "my-restaurant"
    assert slugify_subdomain("Joe's Café") == "joes-cafe"
    assert slugify_subdomain("ABC-123 Store") == "abc-123-store"
    assert slugify_subdomain("  Spaces  ") == "spaces"


@pytest.mark.asyncio
async def test_example_async():
    """Example async test"""
    result = await async_example()
    assert result is True


async def async_example():
    """Helper async function"""
    return True
