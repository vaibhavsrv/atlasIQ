from typing import TypedDict, Annotated, Sequence
import operator
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.domain.services.location_intelligence import LocationIntelligenceService
from src.domain.services.simulation_engine import SimulationEngine
from src.domain.services.forecasting import ForecastingService
from src.infrastructure.database.config import SessionLocal
from src.infrastructure.database.models import IndustryBenchmarkModel

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    project_id: str
    budget: float
    query: str
    industry: str
    lat: float
    lon: float
    benchmark: dict
    location_data: dict
    competitor_data: dict
    revenue_projection: dict
    risk_score: dict
    forecast_data: list
    final_strategy: str

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY", "dummy_key_to_prevent_startup_crash")
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model="openai/gpt-4o-mini",
        temperature=0.7,
    )

def extract_intent(query: str):
    """Extracts city and industry from user query using LLM."""
    prompt = PromptTemplate.from_template(
        "Extract the target 'city' and 'industry' from this business expansion query: '{query}'. "
        "Valid industries: 'Coffee Shop', 'Restaurant', 'Gym', 'Retail Store', 'Salon', 'Clinic', 'Coworking Space', 'E-commerce Warehouse'. "
        "Return ONLY a JSON object with 'city' and 'industry'."
    )
    response = get_llm().invoke(prompt.format(query=query)).content
    try:
        cleaned = response.replace('```json', '').replace('```', '').strip()
        data = json.loads(cleaned)
        return data.get("city", "Seattle"), data.get("industry", "Coffee Shop")
    except:
        return "Seattle", "Coffee Shop"

def market_agent(state: AgentState) -> dict:
    city, industry = extract_intent(state["query"])
    
    # Get benchmark from DB
    db = SessionLocal()
    benchmark_record = db.query(IndustryBenchmarkModel).filter(IndustryBenchmarkModel.industry_name == industry).first()
    if benchmark_record:
        benchmark = {
            "avg_revenue": benchmark_record.avg_revenue,
            "avg_rent": benchmark_record.avg_rent,
            "avg_cac": benchmark_record.avg_cac,
            "avg_margins": benchmark_record.avg_margins,
            "risk_multiplier": benchmark_record.risk_multiplier,
            "growth_rate": benchmark_record.growth_rate
        }
    else:
        benchmark = {"avg_revenue": 500000, "avg_rent": 60000, "avg_margins": 0.15, "risk_multiplier": 1.0, "growth_rate": 0.05}
    db.close()

    loc_service = LocationIntelligenceService()
    lat, lon, display_name = loc_service.geocode(city)
    market_metrics = loc_service.get_market_metrics(lat, lon)
    
    return {
        "industry": industry,
        "lat": lat,
        "lon": lon,
        "benchmark": benchmark,
        "location_data": market_metrics
    }

def competitor_agent(state: AgentState) -> dict:
    loc_service = LocationIntelligenceService()
    competitors = loc_service.get_competitors(state["lat"], state["lon"], radius=5000, industry=state["industry"])
    return {
        "competitor_data": {"competitors": competitors, "count": len(competitors)}
    }

def revenue_agent(state: AgentState) -> dict:
    sim_engine = SimulationEngine()
    financials = sim_engine.calculate_financials(
        benchmark=state["benchmark"],
        market=state["location_data"],
        competitors=state["competitor_data"]["competitors"],
        budget=state["budget"]
    )
    return {"revenue_projection": financials}

def risk_agent(state: AgentState) -> dict:
    sim_engine = SimulationEngine()
    risk = sim_engine.calculate_risk(
        benchmark=state["benchmark"],
        market=state["location_data"],
        competitors=state["competitor_data"]["competitors"],
        financials=state["revenue_projection"]
    )
    
    # Generate Forecast here as well
    forecast_service = ForecastingService()
    forecast = forecast_service.generate_revenue_forecast(
        year_1_revenue=state["revenue_projection"]["year_1_revenue"],
        growth_rate=state["benchmark"].get("growth_rate", 0.05),
        months=36
    )
    
    return {"risk_score": risk, "forecast_data": forecast}

from src.domain.services.document_rag import DocumentRAGService

def strategy_agent(state: AgentState) -> dict:
    query = state["query"]
    project_id = state["project_id"]
    
    # Query Knowledge Base (RAG)
    rag_service = DocumentRAGService()
    rag_context = rag_service.query_project_documents(project_id, query)
    
    context = f"""
    Scenario: {query}
    Industry: {state['industry']}
    Market Stats: {state['location_data']}
    Competitor Count: {state['competitor_data']['count']}
    Projections: {state['revenue_projection']}
    Risk Analysis: {state['risk_score']}
    """
    
    if rag_context:
        context += f"\nInternal Document Insights:\n{rag_context}\n"
    
    prompt = PromptTemplate.from_template(
        "You are the AtlasIQ Strategy Agent. Based on the EXACT mathematical calculations below, write a highly professional, "
        "executive-level markdown recommendation (2-3 paragraphs) for this expansion scenario. "
        "Do NOT hallucinate new metrics. Use the provided numbers. Incorporate any 'Internal Document Insights' into your reasoning if present. "
        "Include actionable next steps. \n\nData:\n{context}"
    )
    response = get_llm().invoke(prompt.format(context=context)).content
    return {"final_strategy": response}

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

def run_simulation(project_id: str, query: str, budget: float = 500000):
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "project_id": project_id,
        "query": query,
        "budget": budget,
        "industry": "",
        "lat": 0.0,
        "lon": 0.0,
        "benchmark": {},
        "location_data": {},
        "competitor_data": {},
        "revenue_projection": {},
        "risk_score": {},
        "forecast_data": [],
        "final_strategy": ""
    }
    result = orchestrator_app.invoke(initial_state)
    return result
