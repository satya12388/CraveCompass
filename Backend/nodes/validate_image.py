# app/nodes/validate_image.py

import base64
from app.schemas import ValidateInputFoodImg
from services.llm_factory import get_vision_model
from utils.logger import logger


def validate_image_node(state):
    model = get_vision_model().with_structured_output(ValidateInputFoodImg,method="json_mode")

    image_base64 = base64.b64encode(state["image"]).decode()
    logger.info("Node: validate_input_node_query - START")
    response = model.invoke([
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Check if this image is a food menu and return only json."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                }
            ],
        }
    ])
    logger.info(f"Node: validate_input_node_query - OUTPUT: {response.model_dump()}")
    state["isFoodMenu"] = response.is_food_menu
    return state