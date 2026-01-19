# main.py

from src.data_loader import DataLoader
from src.case_model import Case
from src.risk_engine import RiskEngine
from src.strategy_engine import StrategyEngine
from src.priority_engine import PriorityEngine

def main():
    # 1️⃣ Load invoice data
    loader = DataLoader("data/generated_data.csv")
    df = loader.load_data()
    loader.preview()

    # 2️⃣ Create Case objects
    cases = [Case(row) for _, row in df.iterrows()]
    print(f"Created {len(cases)} cases.")

    # 3️⃣ Initialize engines
    risk_engine = RiskEngine()
    strategy_engine = StrategyEngine()

    priority_engine = PriorityEngine()

    for case in cases:
        risk_engine.compute_risk(case)
        priority_engine.assign_priority(case)
        strategy_engine.assign_strategy(case)


    # 5️⃣ Preview output
    print("\n--- Case Summary (First 5) ---")
    for case in cases[:5]:
        print(
        f"Case ID: {case.case_id} | "
        f"Risk: {case.risk_level} | "
        f"Priority: {case.priority_level} | "
        f"Strategy: {case.strategy}"
        )

if __name__ == "__main__":
    main()
