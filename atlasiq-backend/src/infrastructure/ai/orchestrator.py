from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    project_id: str
    location_data: dict
    competitor_data: dict
    revenue_projection: dict
    risk_score: dict
    final_strategy: str

# Agent Stubs
def market_agent(state: AgentState) -> dict:
    """Fetches demographics, population density, and income data."""
    # Stub: Query demographics
    return {"location_data": {"population": 1000000, "avg_income": 85000, "saturation": "medium"}}

def competitor_agent(state: AgentState) -> dict:
    """Queries Neo4j for local competitors and analyzes saturation."""
    # Stub: Query Neo4j
    return {"competitor_data": {"competitors": ["Starbucks", "Costa"], "threat_level": "high"}}

def revenue_agent(state: AgentState) -> dict:
    """Triggers the Forecasting Engine to predict sales and ROI."""
    # Stub: Trigger XGBoost/Prophet model
    return {"revenue_projection": {"year_1_roi": 15.5, "payback_months": 24}}

def risk_agent(state: AgentState) -> dict:
    """Evaluates regulatory risks, high rent, and saturation scores."""
    return {"risk_score": {"overall_risk": "moderate", "factors": ["high rent", "strong competition"]}}

def strategy_agent(state: AgentState) -> dict:
    """Synthesizes the data into a final recommendation and Expansion Timeline."""
    strategy = "Proceed with caution. The market is saturated but average income supports a premium offering."
    return {"final_strategy": strategy}

# Build LangGraph
def build_orchestrator():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("market", market_agent)
    workflow.add_node("competitor", competitor_agent)
    workflow.add_node("revenue", revenue_agent)
    workflow.add_node("risk", risk_agent)
    workflow.add_node("strategy", strategy_agent)

    # Add edges
    workflow.set_entry_point("market")
    workflow.add_edge("market", "competitor")
    workflow.add_edge("competitor", "revenue")
    workflow.add_edge("revenue", "risk")
    workflow.add_edge("risk", "strategy")
    workflow.add_edge("strategy", END)

    return workflow.compile()

orchestrator_app = build_orchestrator()

def run_simulation(project_id: str, query: str):
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "project_id": project_id,
        "location_data": {},
        "competitor_data": {},
        "revenue_projection": {},
        "risk_score": {},
        "final_strategy": ""
    }
    result = orchestrator_app.invoke(initial_state)
    return result
