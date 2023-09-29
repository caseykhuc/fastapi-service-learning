# mypy: ignore-errors

from fastapi import APIRouter

from . import authentication, categories, items, probe

router = APIRouter()

router.include_router(probe.router, tags=["probe"])
router.include_router(items.router, tags=["items"])
router.include_router(authentication.router, tags=["auth"])
router.include_router(categories.router, tags=["categories"])
