class SimulationEngine:
    def __init__(self):
        pass

    def calculate_financials(self, benchmark: dict, market: dict, competitors: list, budget: float):
        """Calculates deterministic ROI, Revenue, and Profit based on industry benchmarks and market data."""
        base_revenue = benchmark.get("avg_revenue", 500000)
        margins = benchmark.get("avg_margins", 0.15)
        
        # Adjust revenue based on income index and population
        income_multiplier = market.get("avg_income", 50000) / 60000.0
        pop_multiplier = min(market.get("population", 100000) / 200000.0, 1.5)
        
        # Adjust for competition (more competitors = less revenue share)
        comp_penalty = max(1.0 - (len(competitors) * 0.05), 0.5)
        
        projected_revenue = base_revenue * income_multiplier * pop_multiplier * comp_penalty
        projected_profit = projected_revenue * margins
        
        # Calculate ROI
        roi = (projected_profit / budget) * 100 if budget > 0 else 0
        payback_months = (budget / projected_profit) * 12 if projected_profit > 0 else 999
        
        return {
            "year_1_revenue": round(projected_revenue, 2),
            "year_1_profit": round(projected_profit, 2),
            "year_1_roi": round(roi, 2),
            "payback_months": round(payback_months, 1)
        }

    def calculate_risk(self, benchmark: dict, market: dict, competitors: list, financials: dict):
        """Calculates a 0-100 risk score."""
        risk_multiplier = benchmark.get("risk_multiplier", 1.0)
        
        # Base risk from competition
        comp_risk = len(competitors) * 5
        
        # Risk from market safety/traffic
        market_risk = (100 - market.get("safety_score", 50)) * 0.5
        
        # Financial risk (low ROI = high risk)
        roi = financials.get("year_1_roi", 10)
        fin_risk = max(50 - roi, 0)
        
        raw_score = (comp_risk + market_risk + fin_risk) * risk_multiplier
        final_score = min(max(raw_score, 0), 100)
        
        # Categorize
        if final_score < 20: category = "Very Low"
        elif final_score < 40: category = "Low"
        elif final_score < 60: category = "Moderate"
        elif final_score < 80: category = "Elevated"
        elif final_score < 90: category = "High"
        else: category = "Critical"
        
        return {
            "score": round(final_score, 1),
            "category": category,
            "factors": [
                f"Competition Density ({len(competitors)} nearby)",
                f"Projected ROI Sensitivity ({round(roi, 1)}%)"
            ]
        }
