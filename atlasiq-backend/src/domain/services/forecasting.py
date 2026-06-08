import pandas as pd
from prophet import Prophet
import datetime

class ForecastingService:
    def __init__(self):
        pass

    def generate_revenue_forecast(self, year_1_revenue: float, growth_rate: float, months: int = 36):
        """Generates a realistic time-series forecast using Prophet."""
        # Generate dummy historical data to feed Prophet based on the expected Year 1 revenue
        # We assume a ramp-up phase for the first 12 months.
        dates = pd.date_range(end=datetime.date.today(), periods=12, freq='ME')
        
        # Ramp up from 30% of target to 100% of target monthly run-rate
        monthly_target = year_1_revenue / 12.0
        y_values = [monthly_target * (0.3 + 0.7 * (i/11)) for i in range(12)]
        
        df = pd.DataFrame({
            'ds': dates,
            'y': y_values
        })
        
        # Initialize Prophet with basic settings (no daily/weekly seasonality needed for monthly data)
        m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        m.fit(df)
        
        # Predict future
        future = m.make_future_dataframe(periods=months, freq='ME')
        forecast = m.predict(future)
        
        # Extract the future period
        future_forecast = forecast.tail(months)
        
        # Apply the industry growth rate explicitly to the trend
        results = []
        base_val = monthly_target
        for i, row in enumerate(future_forecast.itertuples()):
            # Compound growth
            trend_adj = base_val * ((1 + growth_rate) ** (i / 12.0))
            # Add prophet's learned seasonality variation
            seasonality = row.yhat - row.trend
            final_val = max(trend_adj + seasonality, 0)
            
            results.append({
                "month": row.ds.strftime("%Y-%m"),
                "projected_revenue": round(final_val, 2),
                "lower_bound": round(max(final_val * 0.85, 0), 2),
                "upper_bound": round(final_val * 1.15, 2)
            })
            
        return results
