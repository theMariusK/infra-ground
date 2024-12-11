from fastapi import FastAPI, HTTPException
import httpx
from typing import Optional

app = FastAPI()

USER_API_URL = "http://127.0.0.1:8000"
TASK_API_URL = "http://127.0.0.1:8001"

async def forward_to_user_api(endpoint: str, method: str = "GET", data: Optional[dict] = None):
    url = f"{USER_API_URL}/{endpoint}"
    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url)
        elif method == "POST":
            response = await client.post(url, json=data)
        elif method == "PUT":
            response = await client.put(url, json=data)
        elif method == "DELETE":
            response = await client.delete(url, json=data)
        return response

async def forward_to_task_api(endpoint: str, method: str = "GET", data: Optional[dict] = None):
    url = f"{TASK_API_URL}/{endpoint}"
    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url)
        elif method == "POST":
            response = await client.post(url, json=data)
        elif method == "PUT":
            response = await client.put(url, json=data)
        elif method == "DELETE":
            response = await client.delete(url, json=data)
        return response

@app.post("/user/{endpoint:path}")
async def user_api_gateway_post(endpoint: str, data: Optional[dict] = None):
    try:
        response = await forward_to_user_api(endpoint, method="POST", data=data)
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach user-api: {str(e)}")

@app.post("/task/{endpoint:path}")
async def task_api_gateway_post(endpoint: str, data: Optional[dict] = None):
    try:
        response = await forward_to_task_api(endpoint, method="POST", data=data)
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach task-api: {str(e)}")

@app.get("/user/{endpoint:path}")
async def user_api_gateway_get(endpoint: str):
    try:
        response = await forward_to_user_api(endpoint, method="GET")
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach user-api: {str(e)}")

@app.get("/task/{endpoint:path}")
async def task_api_gateway_get(endpoint: str):
    try:
        response = await forward_to_task_api(endpoint, method="GET")
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach task-api: {str(e)}")

@app.put("/user/{endpoint:path}")
async def user_api_gateway_put(endpoint: str, data: Optional[dict] = None):
    try:
        response = await forward_to_user_api(endpoint, method="PUT", data=data)
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach user-api: {str(e)}")

@app.put("/task/{endpoint:path}")
async def task_api_gateway_put(endpoint: str, data: Optional[dict] = None):
    try:
        response = await forward_to_task_api(endpoint, method="PUT", data=data)
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach task-api: {str(e)}")

@app.delete("/user/{endpoint:path}")
async def user_api_gateway_delete(endpoint: str, data: Optional[dict] = None):
    try:
        response = await forward_to_user_api(endpoint, method="DELETE", data=data)
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach user-api: {str(e)}")

@app.delete("/task/{endpoint:path}")
async def task_api_gateway_delete(endpoint: str, data: Optional[dict] = None):
    try:
        response = await forward_to_task_api(endpoint, method="DELETE", data=data)
        return response.json(), response.status_code
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach task-api: {str(e)}")

