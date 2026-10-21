from shop.api.orders import get_order


def test_when_order_missing_returns_not_found_error():
    # Arrange
    order_id = "ORD-404"
    # Act
    result = get_order(order_id)
    # Assert
    assert result["error"]["code"] == "not_found"
