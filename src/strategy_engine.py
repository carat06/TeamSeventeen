# strategy_engine.py

class StrategyEngine:
    def assign_strategy(self, case):
        if case.risk_level == "LOW":
            case.strategy = "AUTOMATED_REMINDERS"
        elif case.risk_level == "MEDIUM":
            case.strategy = "STANDARD_DCA_FOLLOWUP"
        elif case.risk_level == "HIGH":
            case.strategy = "SENIOR_DCA_ESCALATION"

        case.status = "STRATEGY_ASSIGNED"
        return case
