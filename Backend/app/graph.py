# app/graph.py

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.schemas import MenuItem
from nodes.validate_image import validate_image_node
from nodes.validate_query import validate_query_node
from nodes.extract_menu import extract_menu_node



class GraphState(TypedDict):
    image: bytes
    query: str
    isFoodMenu: bool
    isValidQuery: bool
    ActualResponse: List[MenuItem]


def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("validate_image", validate_image_node)
    workflow.add_node("validate_query", validate_query_node)
    workflow.add_node("extract_menu", extract_menu_node)

    workflow.set_entry_point("validate_image")

    workflow.add_edge("validate_image", "validate_query")

    workflow.add_conditional_edges(
        "validate_query",
        lambda state: (
            "extract_menu"
            if state["isFoodMenu"] and state["isValidQuery"]
            else END
        )
    )

    workflow.add_edge("extract_menu", END)

    return workflow.compile()


graph = build_graph()