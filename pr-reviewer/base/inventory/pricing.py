PRICES_CENTS = {"LAMP-1": 4500, "DESK-2": 18900}


def price_for(sku: str) -> int:
    return PRICES_CENTS[sku]
