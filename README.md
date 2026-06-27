# Agent Eval Platform

An evaluation framework for AI agents.

This project is built around the idea that evaluation should come before optimization. Instead of building an agent first and adding evaluation later, the platform defines evaluation scenarios, scoring, regression tracking, and observability as first-class components.

The first example is a multi-agent travel planning system evaluated against real-world, ground-truth itineraries. The framework is designed to be domain-agnostic, allowing additional agent types to be evaluated using the same infrastructure.

## Repository Structure

framework/
Generic evaluation framework.

evals/
Evaluation scenarios and datasets.

traces/
Execution traces and observability.

dashboards/
Regression dashboards and metrics.

examples/
Example AI agents evaluated by the platform.

docs/
Architecture and design documentation.