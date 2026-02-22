
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.graph import graph
from app.schemas import SuccessResponse, ItemDetailsResponse
from services.item_details_agent import get_item_details
from utils.logger import logger

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://crave-compass-lemon.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=SuccessResponse)
async def analyze_menu(
    image: UploadFile = File(...),
    query: str = Form(...)
):
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        image_bytes = await image.read()

        state = {
            "image": image_bytes,
            "query": query,
            "isFoodMenu": False,
            "isValidQuery": False,
            "ActualResponse": []
        }
        logger.info("==== New Request Received ====")
        result = graph.invoke(state)

        if not (result["isFoodMenu"] and result["isValidQuery"]):
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid food menu image and related food query"
            )
        

        return {
            "success": True,
            "data": result["ActualResponse"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /analyze: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/item-details", response_model=ItemDetailsResponse)
async def fetch_item_details(item_name: str):
    try:
        if not item_name.strip():
            raise HTTPException(status_code=400, detail="Item name cannot be empty")
        
        logger.info(f"==== Fetching Details for: {item_name} ====")
        return get_item_details(item_name)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /item-details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    