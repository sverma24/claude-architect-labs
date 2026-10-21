---
paths: ["**/*_test.py"]
---
# Test conventions (apply to every test file, wherever it lives)
- Name tests `test_when_<situation>_<expected_result>`.
- Each test has three commented parts: `# Arrange`, `# Act`, `# Assert`.
- One behavior per test. No network, no sleeps.
