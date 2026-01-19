# priority_engine.py

class PriorityEngine:
    """
    Determines operational priority for a case
    based on risk, amount, and aging.
    """

    def assign_priority(self, case):
        invoice = case.invoice

        amount = invoice.get("outstandingAmount", 0)
        days_overdue = invoice.get("daysOverdue", 0)
        risk = case.risk_level

        score = 0

        # Risk contribution
        if risk == "HIGH":
            score += 50
        elif risk == "MEDIUM":
            score += 30
        else:
            score += 10

        # Financial impact
        if amount > 50000:
            score += 30
        elif amount > 25000:
            score += 20
        elif amount > 10000:
            score += 10

        # Aging / SLA pressure
        if days_overdue > 180:
            score += 20
        elif days_overdue > 90:
            score += 10

        # Assign priority level
        case.priority_score = score

        if score >= 80:
            case.priority_level = "CRITICAL"
        elif score >= 60:
            case.priority_level = "HIGH"
        elif score >= 40:
            case.priority_level = "MEDIUM"
        else:
            case.priority_level = "LOW"

        return case
