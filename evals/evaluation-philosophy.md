# Evaluation Philosophy

The purpose of the evaluation framework is to measure AI agent quality using objective, repeatable, and transparent criteria rather than subjective judgment. Every evaluation should produce consistent results when applied to the same agent and scenario.

The framework distinguishes between **hard constraints** and **soft preferences**. Hard constraints represent requirements that must be satisfied for a solution to be considered valid (e.g., budget limits, travel dates, dietary restrictions, accessibility requirements). Violating a hard constraint results in a significant penalty because it directly contradicts an explicit user requirement.

Soft preferences represent user interests and qualitative preferences (e.g., anime, photography, food, shopping, or travel pace). These should influence the quality of the solution but do not necessarily invalidate it. Failure to satisfy soft preferences reduces the personalization score rather than causing the entire evaluation to fail.

Evaluation scores should be deterministic whenever possible. Rather than relying on subjective impressions, the framework uses predefined scoring criteria, weighted evaluation dimensions, and measurable thresholds to ensure that different evaluators reach comparable conclusions. Initial scoring weights and thresholds are intentionally conservative and will be refined over time as additional evaluation data becomes available.

The evaluation framework is designed to assess outcomes rather than implementation details. It measures whether an agent satisfies user requirements, produces accurate information, and generates high-quality solutions without prescribing how the agent must achieve those results.
