# risk_engine.py

class RiskEngine:
    def compute_risk(self, case):
        invoice = case.invoice
        score = 0
        breakdown = {}

        # Time risk
        days = invoice.get("daysOverdue", 0)
        if days > 180:
            breakdown["time"] = 40
        elif days > 90:
            breakdown["time"] = 30
        elif days > 30:
            breakdown["time"] = 20
        else:
            breakdown["time"] = 10

        # Financial risk
        amt = invoice.get("outstandingAmount", 0)
        if amt > 50000:
            breakdown["financial"] = 30
        elif amt > 25000:
            breakdown["financial"] = 20
        elif amt > 10000:
            breakdown["financial"] = 10
        else:
            breakdown["financial"] = 5

        # Compliance & geography
        breakdown["compliance"] = 0
        if invoice.get("importExportIndicator"):
            breakdown["compliance"] += 10
        if invoice.get("billingCountry") != invoice.get("destinationCountry"):
            breakdown["compliance"] += 10

        # Operational complexity
        awbs = invoice.get("numberOfAirWaybills", 0)
        if awbs > 20:
            breakdown["operational"] = 10
        elif awbs > 5:
            breakdown["operational"] = 5
        else:
            breakdown["operational"] = 0

        score = sum(breakdown.values())

        case.risk_score = score
        case.risk_breakdown = breakdown

        if score <= 30:
            case.risk_level = "LOW"
        elif score <= 60:
            case.risk_level = "MEDIUM"
        else:
            case.risk_level = "HIGH"

        return case
