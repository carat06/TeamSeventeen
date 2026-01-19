# main_db.py

from src.data_loader import DataLoader
from src.case_model import Case
from src.risk_engine import RiskEngine
from src.priority_engine import PriorityEngine
from src.strategy_engine import StrategyEngine
from src.repositories import (
    CaseRepository,
    EventRepository,
    SLAEngine,
    CaseModel
)
from sqlalchemy.exc import SQLAlchemyError

def main():
    print("🚀 Starting DCA Management Pipeline (DB-backed)")

    # 1️⃣ Load invoices
    loader = DataLoader("data/generated_data.csv")
    df = loader.load_data()
    loader.preview()

    # 2️⃣ Create Case objects (in-memory)
    cases = [Case(row) for _, row in df.iterrows()]
    print(f"Created {len(cases)} cases.")

    # 3️⃣ Initialize repositories & engines
    case_repo = CaseRepository()
    event_repo = EventRepository()
    sla_engine = SLAEngine()
    risk_engine = RiskEngine()
    priority_engine = PriorityEngine()
    strategy_engine = StrategyEngine()

    # 4️⃣ Process & persist cases in batches
    db_cases_to_save = []
    batch_size = 500  # adjust based on memory / DB

    for idx, case in enumerate(cases, start=1):
        try:
            # --- Compute risk, priority, strategy ---
            case = risk_engine.compute_risk(case)
            case = priority_engine.assign_priority(case)
            case = strategy_engine.assign_strategy(case)

            # --- Convert to DB model ---
            db_case = CaseModel(
                invoice_number=str(case.case_id),
                account_number=str(case.invoice["accountNumber"]),
                risk_score=case.risk_score,
                risk_level=case.risk_level,
                priority_level=case.priority_level,
                strategy=case.strategy,
                status=case.status,
            )

            db_cases_to_save.append(db_case)

            # --- Log event & SLA immediately ---
            event_repo.log_event(
                case_id=db_case.case_id,
                event_type="CASE_CREATED",
                from_status="NONE",
                to_status=case.status,
                actor="SYSTEM"
            )
            sla_engine.create_sla(
                case_id=db_case.case_id,
                stage="RISK_ASSESSED",
                hours_to_complete=24
            )

            # --- Save in batches ---
            if len(db_cases_to_save) >= batch_size:
                # Ensure CaseRepository has a save_bulk method
                case_repo.save_bulk(db_cases_to_save)
                db_cases_to_save.clear()  # reset batch

            # --- Optional progress display ---
            if idx % 1000 == 0:
                print(f"Processed {idx} cases...")

        except Exception as e:
            print(f"⚠️ Error processing case {case.case_id if hasattr(case, 'case_id') else idx}: {e}")

    # Save any remaining cases
    if db_cases_to_save:
        case_repo.save_bulk(db_cases_to_save)

    print("✅ All cases saved, events logged, SLAs created.")

    # 5️⃣ Preview first 5 cases from DB
    print("\n--- Case Summary (First 5 from DB) ---")
    saved_cases = case_repo.all_cases()[:5]
    for c in saved_cases:
        print(
            f"Case ID: {c.case_id} | "
            f"Risk: {c.risk_level} | "
            f"Strategy: {c.strategy} | "
            f"Status: {c.status}"
        )


if __name__ == "__main__":
    main()
