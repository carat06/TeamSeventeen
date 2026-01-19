class Case:
    def __init__(self, invoice):
        self.invoice = invoice
        self.case_id = invoice["invoiceStatementNumber"]

        # Risk-related
        self.risk_score = None
        self.risk_level = None
        self.risk_breakdown = {}

        # Strategy-related
        self.strategy = None

        # Priority-related (added later)
        self.priority_score = None
        self.priority_level = None

        # Lifecycle
        self.status = "CREATED"

    def __repr__(self):
        return (
            f"<Case {self.case_id} | "
            f"Risk={self.risk_level} | "
            f"Priority={self.priority_level} | "
            f"Strategy={self.strategy}>"
        )
