"""Pydantic schemas for tenant API requests/responses"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class SubdomainCheckRequest(BaseModel):
    """Request to check subdomain availability"""
    business_name: str = Field(..., min_length=2, max_length=255)


class SubdomainCheckResponse(BaseModel):
    """Response with subdomain suggestion and availability"""
    suggested_subdomain: str
    available: bool
    alternatives: list[str] = []


class TenantCreateRequest(BaseModel):
    """Request to create a new tenant"""
    business_name: str = Field(..., min_length=2, max_length=255)
    subdomain: str = Field(..., min_length=3, max_length=63)
    owner_email: EmailStr
    owner_password: str = Field(..., min_length=8)
    niche_type: Optional[str] = None

    @field_validator("subdomain")
    @classmethod
    def validate_subdomain(cls, v: str) -> str:
        """Validate subdomain format"""
        if not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", v):
            raise ValueError(
                "Subdomain must contain only lowercase letters, numbers, and hyphens, "
                "and cannot start or end with a hyphen"
            )
        return v


class TenantResponse(BaseModel):
    """Tenant response"""
    id: str
    business_name: str
    subdomain: str
    custom_domain: Optional[str]
    niche_type: Optional[str]
    status: str
    logo_url: Optional[str]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TenantUpdateRequest(BaseModel):
    """Request to update tenant basic info"""
    logo_url: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    business_hours: Optional[Dict[str, Any]] = None


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
