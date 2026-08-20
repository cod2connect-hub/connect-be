"""Tenant onboarding DTOs."""

from dataclasses import dataclass


@dataclass(slots=True)
class SubdomainCheckInput:
    business_name: str


@dataclass(slots=True)
class TenantCreateInput:
    business_name: str
    subdomain: str
    owner_email: str
    owner_password: str
    niche_type: str | None = None


@dataclass(slots=True)
class UserLoginInput:
    email: str
    password: str
