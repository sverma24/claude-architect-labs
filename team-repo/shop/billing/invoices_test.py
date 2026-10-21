from shop.billing.invoices import invoice_total


def test_when_two_lines_sums_qty_times_price():
    # Arrange
    lines = [{"qty": 2, "unit_cents": 1500}, {"qty": 1, "unit_cents": 999}]
    # Act
    total = invoice_total(lines)
    # Assert
    assert total == 3999
