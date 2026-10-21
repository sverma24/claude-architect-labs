---
paths: ["shop/api/**/*.py"]
---
# API handler rules
- Follow docs/standards/api-conventions.md: return the data/error envelope, never raise.
- Validate ids at the top of each handler and return `invalid_input` for empty ones.
