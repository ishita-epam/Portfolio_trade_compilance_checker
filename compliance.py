
def check_compliance(trade, portfolio):

    security_id = trade["security_id"]
    action = trade["action"]
    quantity = float(trade["quantity"])
    price = float(trade["price"])

    cash = portfolio["cash_balance"]
    restricted = portfolio["restricted_securities"]
    max_position = portfolio["max_position_pct"]
    holdings = portfolio["current_holdings"]

    
    if quantity <= 0 or price <= 0 or action not in ["Buy", "Sell"]:
        return "Rejected", "Invalid trade data."

   
    if security_id in restricted:
        return "Rejected", "Security is restricted for this portfolio."

    # Existing holding
    existing_quantity = 0

    for holding in holdings:
        if holding["security_id"] == security_id:
            existing_quantity = holding["quantity"]
            break


    if action == "Sell":
        if existing_quantity < quantity:
            return "Rejected", "Insufficient holdings to sell."



    if action == "Buy":
        cost = quantity * price

        if cost > cash:
            return "Rejected", "Insufficient cash for this buy order."

        #Position concentration check
        post_trade_cash = cash - cost
        post_trade_quantity = existing_quantity + quantity
        post_trade_value = post_trade_quantity * price
        other_holdings_value = 0

        for holding in holdings:
            if holding["security_id"] != security_id:
                other_holdings_value += (
                    holding["quantity"] * holding["market_price"]
                )

        total_portfolio_value = (
            post_trade_cash
            + post_trade_value
            + other_holdings_value
        )

        if total_portfolio_value <= 0:
            return "Rejected", "Invalid portfolio value."

        position_pct = post_trade_value / total_portfolio_value

        if position_pct > max_position:
            return (
                "Needs Manual Sign-off",
                "Exceeds maximum position concentration — requires approval."
            )

   
    return "Approved", "Trade passed all compliance checks."
