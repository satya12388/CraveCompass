# app/nodes/validate_query.py

from services.llm_factory import get_small_llm
from app.schemas import ValidateInputQuery
from utils.logger import logger

def validate_query_node(state):
    llm = get_small_llm().with_structured_output(ValidateInputQuery)
    logger.info("Node: validate_input_node_query - START")
    prompt = f"""
    Is this query related to food menu items?.not food but food menu items
    Answer only True or False. return JSON only

    Query: {state['query']}
    """

    response = llm.invoke(prompt)
    logger.info(f"Node: validate_input_node_query - OUTPUT: {response.model_dump()}")
    state["isValidQuery"] = response.is_valid_query
    return state