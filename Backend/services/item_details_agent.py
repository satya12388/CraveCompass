# app/services/item_details_agent.py

from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from app.schemas import ItemDetailsResponse
from services.llm_factory import get_small_llm
from app.config import settings
from utils.logger import logger
import os

def get_item_details(item_name: str) -> ItemDetailsResponse:
    logger.info(f"Agent: get_item_details - START for {item_name}")

    if not settings.TAVILY_API_KEY:
        logger.error("TAVILY_API_KEY is not set in config.")
        # Fallback empty response if API key is missing
        return ItemDetailsResponse(
            nutritioninfo={"calories": "N/A", "protein": "N/A", "carbs": "N/A", "fat": "N/A"},
            ingredients=["N/A"],
            preparation=["Live search unavailable. Please add TAVILY_API_KEY."],
            image_url=""
        )

    llm = get_small_llm()
    
    # Initialize Tavily search tool (new package)
    search_tool = TavilySearch(
        tavily_api_key=settings.TAVILY_API_KEY,
        max_results=1, 
        include_images=True
    )
    tools = [search_tool]

    # Create a ChatPromptTemplate suitable for tool calling
    from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
    
    messages = [
        SystemMessage(
            "You are an expert culinary AI equipped with a web search tool.\n"
            "Your task is to find the authentic recipe, nutritional info, and a high-quality image URL for a given dish.\n"
            "1. Use the search tool to find the ingredients,nutrional info and preparation method. The nutriotional info should contain values always it shuld not be empty.\n"
            "2. The search tool will return an 'images' array containing exact URLs. You MUST pick exactly one of those raw URLs from the 'images' array for the dish.\n"
            "   - ABSOLUTELY DO NOT hallucinate, guess, or construct a URL under any circumstances.\n"
            "   - You are explicitly FORBIDDEN from generating URLs containing 'archanaskitchen.com' or any other URL that was not explicitly provided in the tool output.\n"
            "   - If no valid images are returned by the search tool, use an empty string \"\".\n"
            "3. Once you have enough information, synthesize all findings into a final response in JSON alone."
            "4. The response MUST be valid JSON, strictly following this schema: {\"nutritioninfo\": {\"calories\": \"250 kcal\", \"protein\": \"10g\", \"carbs\": \"30g\", \"fat\": \"5g\"}, \"ingredients\": [\"...\"], \"preparation\": [\"...\"], \"image_url\": \"...\"}"
        ),
        HumanMessage(f"Dish Name: {item_name}")
    ]

    llm_with_tools = llm.bind_tools(tools)
    logger.info(f"Agent: Prompting LLM for {item_name} Tool calls...")
    
    try:
        # Step 1: Tell the LLM to decide what to search for
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # Step 2: Execute the tool if it asked to search
        if response.tool_calls:
            for tool_call in response.tool_calls:
                logger.info(f"Agent: Executing tool {tool_call['name']}...")
                if tool_call['name'] in ['tavily_search_results_json', 'tavily_search']:
                    tool_result = search_tool.invoke(tool_call['args'])
                    logger.info(f"Agent: Tavily returned {len(tool_result)} results.")
                    messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call['id']))
        else:
            logger.info("Agent: No tool calls made by LLM.")

        # Step 3: Now that it actually read the search results, force the final output to JSON
        structured_llm = llm.with_structured_output(ItemDetailsResponse, method="json_mode")
        final_result = structured_llm.invoke(messages)
        
        logger.info(f"Agent: get_item_details - SUCCESS for {item_name}")
        return final_result
        
    except Exception as e:
        logger.error(f"Agent: Extraction failed: {str(e)}")
        return ItemDetailsResponse(
            nutritioninfo={"calories": "N/A", "protein": "N/A", "carbs": "N/A", "fat": "N/A"},
            ingredients=["Data unavailable"],
            preparation=["Failed to extract detailed information from search."],
            image_url=""
        )
