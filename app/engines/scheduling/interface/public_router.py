"""Scheduling public router."""

from fastapi import APIRouter


router = APIRouter(prefix="/scheduling", tags=["scheduling:public"])
