from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from shared.factory import scraper
import time

router = APIRouter(tags=["Find Places"])


@router.post("/find-places/form-input")
async def find_places(
    query: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    timeout: int = Form(10),
    max_results: int = Form(100),
):
    if max_results > 120:
        raise HTTPException(status_code=400, detail="max_results should be <= 120")

    st = time.time()
    result = scraper.get_nearby_places(
        query=query,
        latitude=latitude,
        longitude=longitude,
        timeout=timeout,
        max_results=max_results,
    )

    return {
        "message": "success",
        "data": result,
        "time_taken": time.time() - st,
    }


class FindPlacesRequestModel(BaseModel):
    query: str
    latitude: float
    longitude: float
    timeout: int = 10
    max_results: int = 100


@router.post("/find-places/json-input")
async def find_places(data: FindPlacesRequestModel):
    if data.max_results > 120:
        raise HTTPException(status_code=400, detail="max_results should be <= 120")

    st = time.time()
    result = scraper.get_nearby_places(
        query=data.query,
        latitude=data.latitude,
        longitude=data.longitude,
        timeout=data.timeout,
        max_results=data.max_results,
    )

    return {
        "message": "success",
        "data": result,
        "time_taken": time.time() - st,
    }
