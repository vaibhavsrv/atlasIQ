from typing import TypedDict, Annotated, Sequence
import operator
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    project_id: str
    location_data: dict
    competitor_data: dict
    revenue_projection: dict
    risk_score: dict
    final_strategy: str

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY", "dummy_key_to_prevent_startup_crash")
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model="openai/gpt-4o-mini",
        temperature=0.2,
    )



def market_agent(state: AgentState) -> dict:
    """Uses LLM to synthesize realistic demographics based on the query."""

    query = state["messages"][0].content
    prompt = PromptTemplate.from_template(
        "Analyze the following business expansion scenario: '{query}'. "
        "Generate a highly realistic JSON object containing 'population' (int), 'avg_income' (int), "
        "and 'saturation' (string: low/medium/high) for the target area. Output ONLY valid JSON."
    )
    response = get_llm().invoke(prompt.format(query=query)).content
    cleaned = response.replace('```json', '').replace('```', '').strip()
    data = json.loads(cleaned)
    return {"location_data": data}

def competitor_agent(state: AgentState) -> dict:
    """Uses LLM to synthesize competitor data."""
    query = state["messages"][0].content
    prompt = PromptTemplate.from_template(
        "For the expansion scenario: '{query}'. "
        "Generate a JSON object with 'competitors' (list of 3 realistic competitor names) "
        "and 'threat_level' (string: low/medium/high). Output ONLY valid JSON."
    )
    response = get_llm().invoke(prompt.format(query=query)).content
    cleaned = response.replace('```json', '').replace('```', '').strip()
    data = json.loads(cleaned)
    return {"competitor_data": data}

def revenue_agent(state: AgentState) -> dict:
    """Uses LLM to project ROI based on market and competitor data."""
    query = state["messages"][0].content
    market = state["location_data"]
    comp = state["competitor_data"]
    prompt = PromptTemplate.from_template(
        "Scenario: {query}. Market: {market}. Competitors: {comp}. "
        "Generate realistic financial projections. Return JSON with 'year_1_roi' (float, e.g., 18.5) "
        "and 'payback_months' (int, e.g., 24). Output ONLY valid JSON."
    )
    response = get_llm().invoke(prompt.format(query=query, market=market, comp=comp)).content
    cleaned = response.replace('```json', '').replace('```', '').strip()
    data = json.loads(cleaned)
    return {"revenue_projection": data}

def risk_agent(state: AgentState) -> dict:
    """Uses LLM to calculate risk scores."""
    query = state["messages"][0].content
    market = state["location_data"]
    comp = state["competitor_data"]
    prompt = PromptTemplate.from_template(
        "Scenario: {query}. Market: {market}. Competitors: {comp}. "
        "Identify 2 key risks and an overall risk score. Return JSON with "
        "'overall_risk' (low/moderate/high) and 'factors' (list of 2 strings). Output ONLY valid JSON."
    )
    response = get_llm().invoke(prompt.format(query=query, market=market, comp=comp)).content
    cleaned = response.replace('```json', '').replace('```', '').strip()
    data = json.loads(cleaned)
    return {"risk_score": data}

def strategy_agent(state: AgentState) -> dict:
    """Uses LLM to synthesize all data into a final markdown recommendation."""
    query = state["messages"][0].content
    context = f"""
    Scenario: {query}
    Market: {state['location_data']}
    Competitors: {state['competitor_data']}
    Projections: {state['revenue_projection']}
    Risks: {state['risk_score']}
    """
    
    prompt = PromptTemplate.from_template(
        "You are the AtlasIQ Strategy Agent. Based on the following data, write a highly professional, "
        "executive-level markdown recommendation (2-3 paragraphs) for this expansion scenario. "
        "Include actionable next steps. \n\nData:\n{context}"
    )
    response = get_llm().invoke(prompt.format(context=context)).content
    return {"final_strategy": response}

# Build LangGraph
def build_orchestrator():
    workflow = StateGraph(AgentState)

    workflow.add_node("market", market_agent)
    workflow.add_node("competitor", competitor_agent)
    workflow.add_node("revenue", revenue_agent)
    workflow.add_node("risk", risk_agent)
    workflow.add_node("strategy", strategy_agent)

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
