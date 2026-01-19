"""import csv
from datetime import datetime
import uuid

INVOICE_FILE = "data/generated_data.csv"
CASE_FILE = "data/cases.csv"

today = datetime.today()
cases = []

with open(INVOICE_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if int(row["daysOverdue"]) > 0:
            
            # Priority rule
            if int(row["daysOverdue"]) > 180 or float(row["outstandingAmount"]) > 25000:
                priority = "HIGH"
            elif int(row["daysOverdue"]) > 60:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            case = {
                "case_id": str(uuid.uuid4()),
                "invoice_id": row["invoiceStatementNumber"],
                "customer_account": row["accountNumber"],
                "customer_name": row["customerName"],
                "outstanding_amount": row["outstandingAmount"],
                "currency": row["currencyCode"],
                "days_overdue": row["daysOverdue"],
                "priority": priority,
                "status": "NEW",
                "billing_country": row["billingCountry"],
                "destination_country": row["destinationCountry"],
                "import_export": row["importExportIndicator"],
                "created_date": today.strftime("%Y-%m-%d")
            }

            cases.append(case)

with open(CASE_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=cases[0].keys())
    writer.writeheader()
    writer.writerows(cases)

print(f"{len(cases)} cases created.")
print(cases[len(cases)-1])
"""
# data_loader.py

import pandas as pd

class DataLoader:
    """
    Loads and preprocesses invoice CSVs for the DCA pipeline.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self, drop_na=True, parse_dates=None):
        """
        Load CSV into a DataFrame.

        Args:
            drop_na (bool): Drop rows with missing values.
            parse_dates (list): Columns to parse as datetime.

        Returns:
            pd.DataFrame: Loaded data
        """
        self.data = pd.read_csv(self.file_path, parse_dates=parse_dates)
        if drop_na:
            self.data = self.data.dropna()
        return self.data

    def preview(self, n=5):
        """
        Preview first n rows of the loaded data.
        """
        if self.data is None:
            raise ValueError("Data not loaded yet. Call load_data() first.")
        print(self.data.head(n))
