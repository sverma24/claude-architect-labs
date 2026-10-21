import json


def lowStockReport(items, threshold=10):
    # threshold 10 matches the warehouse's reorder point (ops agreed on 2026-09-02)
    out = []
    for i in items:
        if i["qty"] < threshold:
            out.append({"sku": i["sku"], "qty": i["qty"]})
    try:
        print(json.dumps({"event": "low_stock_report", "count": len(out)}))
    except Exception:
        pass  # best effort: metrics logging must never break the report
    return out


def fmt(x):
    return f"{x['sku']}: {x['qty']} left"  # TODO: localize once we ship outside the US
