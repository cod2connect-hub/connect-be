"""Tenant request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SubdomainCheckRequest(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=255)


class SubdomainCheckResponse(BaseModel):
    suggested_subdomain: str
    available: bool
    alternatives: list[str] = []


class TenantCreateRequest(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=255)
    subdomain: str = Field(..., min_length=3, max_length=63)
    owner_email: EmailStr
    owner_password: str = Field(..., min_length=8)
    niche_type: str | None = None


class TenantResponse(BaseModel):
    id: str
    business_name: str
    subdomain: str
    niche_type: str | None
    status: str
    created_at: datetime | None = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
