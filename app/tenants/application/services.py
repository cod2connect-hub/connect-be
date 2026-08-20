"""Shared tenant onboarding helpers."""

import re


def slugify_subdomain(business_name: str) -> str:
    slug = business_name.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")[:63]
