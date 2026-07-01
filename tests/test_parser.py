import unittest
from framework.parser import parse_benchmark_text
from framework.exceptions import FrontmatterParseError, MarkdownParseError


class TestParser(unittest.TestCase):
    """Tests the benchmark scenario markdown ingestion parser."""

    def test_parse_valid_scenario(self):
        valid_markdown = """---
benchmark_id: test-trip
name: Test Family Trip
profile: travel-agent
description: A test travel agent planning scenario.
---

# Description
A test travel agent planning scenario description.

# User Prompt
Please make a trip for a family of four visiting Paris.

# Extracted Constraints
```yaml
Budget:
  5000 EUR
Duration:
  7 days
```

# Expected Behaviour
- Family friendly lodging.
- Balanced pacing.

# Evaluation Criteria

## Constraint Satisfaction
- satisfy constraints

## Planning Quality
- good route

# Pass Criteria
- All criteria are scored.
- Final grade is computed.

# Failure Conditions
- Severe itinerary errors.
"""
        benchmark = parse_benchmark_text(valid_markdown)
        self.assertEqual(benchmark.benchmark_id, "test-trip")
        self.assertEqual(benchmark.name, "Test Family Trip")
        self.assertEqual(benchmark.description, "A test travel agent planning scenario description.")
        self.assertIn("Constraint Satisfaction", benchmark.evaluation_criteria)
        self.assertEqual(benchmark.constraints["Budget"], "5000 EUR")
        self.assertEqual(benchmark.constraints["Duration"], "7 days")

    def test_malformed_frontmatter(self):
        invalid_markdown = """---
benchmark_id: : : : :
---
# Description
Missing frontmatter.
"""
        with self.assertRaises(FrontmatterParseError):
            parse_benchmark_text(invalid_markdown)

    def test_missing_required_section(self):
        invalid_markdown = """---
benchmark_id: test-trip
name: Test Family Trip
---

# Description
Only description exists.
"""
        with self.assertRaises(MarkdownParseError):
            parse_benchmark_text(invalid_markdown)


if __name__ == "__main__":
    unittest.main()
