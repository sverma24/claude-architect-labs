PRICES_CENTS = {"LAMP-1": 4500, "DESK-2": 18900}
FX = {"USD": 1.0, "EUR": 0.92}


def unit_price(sku: str, currency: str = "USD") -> int:
    baseCents = PRICES_CENTS[sku]
    return round(baseCents * FX[currency])
