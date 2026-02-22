# app/nodes/extract_menu.py

import base64
from app.schemas import MenuExtractionResponse
from services.llm_factory import get_vision_model
from utils.logger import logger

def extract_menu_node(state):
    model = get_vision_model().with_structured_output(MenuExtractionResponse,method='json_mode')

    image_base64 = base64.b64encode(state["image"]).decode()
    logger.info("Node: extract_menu_node - START")
    response = model.invoke([
        {
            "role": "system",
            "content": (
                "You are an expert data extractor. Analyze the menu image and extract the items into a valid JSON format. "
                "You MUST wrap all extracted items inside an 'items' array. "
                "You MUST use exactly this structure and these keys and values(like category should be on of mentioned values):\n"
                "{\n"
                "  \"items\": [\n"
                "    {\n"
                "      \"name\": \"Item Name\",\n"
                "      \"price\": 10.99,\n"
                "      \"category\": \"Veg/Non-Veg/Beverages/Desserts/Others\"\n"
                "    }\n"
                "  ]\n"
                "}\n"
            )
        },      
        {
            "role": "user",
            "content": [
                {"type": "text", "text": state["query"]},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                }
            ],
        }
    ])
    logger.info(f"Node: extract_menu_node - OUTPUT: {response.model_dump()}")
    state["ActualResponse"] = response.items
    return state