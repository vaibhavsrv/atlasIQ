import uuid
from sqlalchemy.orm import Session
from src.infrastructure.database.config import SessionLocal
from src.infrastructure.database.models import IndustryBenchmarkModel

industries = [
    {
        "industry_name": "Coffee Shop",
        "avg_revenue": 500000,
        "avg_rent": 60000,
        "avg_cac": 15,
        "avg_margins": 0.15,
        "risk_multiplier": 1.2,
        "growth_rate": 0.05
    },
    {
        "industry_name": "Restaurant",
        "avg_revenue": 1200000,
        "avg_rent": 120000,
        "avg_cac": 25,
        "avg_margins": 0.10,
        "risk_multiplier": 1.5,
        "growth_rate": 0.03
    },
    {
        "industry_name": "Gym",
        "avg_revenue": 800000,
        "avg_rent": 150000,
        "avg_cac": 100,
        "avg_margins": 0.20,
        "risk_multiplier": 1.3,
        "growth_rate": 0.08
    },
    {
        "industry_name": "Retail Store",
        "avg_revenue": 600000,
        "avg_rent": 80000,
        "avg_cac": 20,
        "avg_margins": 0.12,
        "risk_multiplier": 1.1,
        "growth_rate": 0.02
    },
    {
        "industry_name": "Salon",
        "avg_revenue": 300000,
        "avg_rent": 40000,
        "avg_cac": 30,
        "avg_margins": 0.18,
        "risk_multiplier": 1.0,
        "growth_rate": 0.04
    },
    {
        "industry_name": "Clinic",
        "avg_revenue": 1500000,
        "avg_rent": 100000,
        "avg_cac": 50,
        "avg_margins": 0.25,
        "risk_multiplier": 0.8,
        "growth_rate": 0.06
    },
    {
        "industry_name": "Coworking Space",
        "avg_revenue": 2000000,
        "avg_rent": 800000,
        "avg_cac": 200,
        "avg_margins": 0.30,
        "risk_multiplier": 1.6,
        "growth_rate": 0.10
    },
    {
        "industry_name": "E-commerce Warehouse",
        "avg_revenue": 5000000,
        "avg_rent": 300000,
        "avg_cac": 5,
        "avg_margins": 0.08,
        "risk_multiplier": 1.1,
        "growth_rate": 0.15
    }
]

def seed_db():
    db: Session = SessionLocal()
    try:
        for ind in industries:
            existing = db.query(IndustryBenchmarkModel).filter(IndustryBenchmarkModel.industry_name == ind["industry_name"]).first()
            if not existing:
                record = IndustryBenchmarkModel(
                    id=str(uuid.uuid4()),
                    **ind
                )
                db.add(record)
        db.commit()
        print("Database successfully seeded with industry benchmarks.")
    except Exception as e:
        print(f"Error seeding DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
