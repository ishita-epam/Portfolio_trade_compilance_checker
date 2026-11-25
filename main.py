import csv

from compliance import check_compliance

portfolios = {
    "POR001": {
        "cash_balance": 20000,
        "restricted_securities": ["XYZCORP"],
        "max_position_pct": 0.30,
        "current_holdings": [
            {"security_id": "AAPL", "quantity": 50, "market_price": 150},
            {"security_id": "TCS", "quantity": 50, "market_price": 310},
            {"security_id": "INFY", "quantity": 20, "market_price": 1500}
        ]
    },

    "POR002": {
        "cash_balance": 15000,
        "restricted_securities": [],
        "max_position_pct": 0.40,
        "current_holdings": [
            {"security_id": "GOOGL", "quantity": 5, "market_price": 2000}
        ]
    },

    "POR003": {
        "cash_balance": 100000,
        "restricted_securities": ["BADCO"],
        "max_position_pct": 0.35,
        "current_holdings": [
            {"security_id": "TCS", "quantity": 20, "market_price": 300},
            {"security_id": "INFY", "quantity": 50, "market_price": 1500},
            {"security_id": "RELIANCE", "quantity": 30, "market_price": 2400}
        ]
    },

    "POR004": {
        "cash_balance": 50000,
        "restricted_securities": [],
        "max_position_pct": 0.25,
        "current_holdings": [
            {"security_id": "GOOGL", "quantity": 10, "market_price": 2000},
            {"security_id": "AAPL", "quantity": 50, "market_price": 150}
        ]
    },

    "POR005": {
        "cash_balance": 10000,
        "restricted_securities": [],
        "max_position_pct": 0.30,
        "current_holdings": [
            {"security_id": "AAPL", "quantity": 20, "market_price": 150},
            {"security_id": "TCS", "quantity": 10, "market_price": 250}
        ]
    }
}


results = []

with open("trades_test.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for trade in reader:
        portfolio_id = trade["portfolio_id"]

        if portfolio_id not in portfolios:
            decision = "Rejected"
            reason = "Portfolio reference data not found."

        else:
            decision, reason = check_compliance(
                trade,
                portfolios[portfolio_id]
            )

        results.append({
            "portfolio_id": portfolio_id,
            "security_id": trade["security_id"],
            "action": trade["action"],
            "quantity": trade["quantity"],
            "price": trade["price"],
            "security_type": trade["security_type"],
            "decision": decision,
            "reason": reason
        })


with open("results.csv", "w", newline="") as file:

    fieldnames = [
        "portfolio_id",
        "security_id",
        "action",
        "quantity",
        "price",
        "security_type",
        "decision",
        "reason"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

print("Compliance checking completed!")
print("Results saved in results.csv")
print("Total trades processed:", len(results))