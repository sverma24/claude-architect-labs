# API conventions
- Every handler in `shop/api/` returns `{"data": ..., "error": None}` on success and
  `{"data": None, "error": {"code": ..., "message": ...}}` on failure. Never raise to the caller.
- Error codes are snake_case: `not_found`, `invalid_input`, `conflict`.
