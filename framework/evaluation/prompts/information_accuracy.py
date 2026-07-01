"""Prompt builder for Information Accuracy dimension."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.prompts.base import JSON_RESPONSE_SCHEMA
from framework.llms import Message
from framework.verification.models import VerificationReport

# Detailed evaluation rubric for Information Accuracy
INFORMATION_ACCURACY_RUBRIC = (
    "Main Question: Considering only information accuracy, can the factual claims "
    "in this itinerary be trusted?\n\n"
    "Note on scope: Evaluate only the truthfulness, precision, and validity of factual claims "
    "(e.g., hotel prices, attraction existence, opening hours, transit times) based on the provided "
    "verification evidence. Do not evaluate planning quality, constraint satisfaction, personalization, "
    "or adaptability, as those are evaluated separately in other dimensions.\n\n"
    "Evaluate the information accuracy of the travel itinerary based on this verification evidence across three core aspects:\n\n"
    "1. Verification Accuracy:\n"
    "   Assess the proportion of claims that were verified as true.\n"
    "   Consider factors such as: the number of refuted claims, particularly those that are critical to the trip.\n\n"
    "2. Severity of Refutations:\n"
    "   Assess the real-world impact of incorrect claims on the traveler's experience.\n"
    "   Treat critical factual inaccuracies—such as incorrect visa/entry rules, non-existent attractions, "
    "   closed attractions, or severe routing/geographical errors—as significantly more critical "
    "   than minor discrepancies (like small price or budget differences) when assessing the scoring deductions.\n\n"
    "3. Handling of Unverifiable or Missing Facts:\n"
    "   Assess how the verifier findings (unknown or not found claims) impact the overall trustworthiness of the itinerary.\n\n"
    "### Scoring Guidance:\n"
    "- 90–100: Highly accurate. All claims are verified, or only minor, trivial discrepancies exist.\n"
    "- 75–89: Generally accurate. Minor price or timing errors that do not disrupt the trip flow.\n"
    "- 50–74: Noticeable factual errors. Multiple refuted claims or a single critical refutation (e.g., closed attraction).\n"
    "- 25–49: Major inaccuracies. Key transport links or multiple attractions are closed/incorrect.\n"
    "- 0–24: Highly untrustworthy. Multiple severe refutations, non-existent locations, or major fictional data.\n\n"
    "Assign the score holistically across all three aspects. "
    "Do not average the aspects mechanically unless the evidence clearly supports doing so."
)


def format_evidence_report(report: VerificationReport) -> str:
    """Formats verification report evidence metrics and findings into a readable string."""
    evidence_lines = []
    evidence_lines.append(f"Verification Summary:")
    evidence_lines.append(f"- Total Claims Extracted: {report.total_claims}")
    evidence_lines.append(f"- Verified: {report.verified_count}")
    evidence_lines.append(f"- Refuted: {report.refuted_count}")
    evidence_lines.append(f"- Unknown Predicates: {report.unknown_count}")
    evidence_lines.append(f"- Not Found Subjects: {report.not_found_count}\n")
    evidence_lines.append(f"Detailed Findings:")

    if not report.evidence:
        evidence_lines.append("No testable factual claims were extracted or verified.")
    else:
        for idx, ev in enumerate(report.evidence):
            line = (
                f"- Claim {idx+1}: {ev.claim.subject} -> {ev.claim.predicate}: {ev.claim.value} "
                f"(Type: {ev.claim.claim_type.value})\n"
                f"  Status: {ev.status.value.upper()}\n"
                f"  Expected: {ev.expected_value or 'N/A'}, Actual: {ev.actual_value or 'N/A'}\n"
                f"  Source: {ev.source} (Confidence: {ev.confidence})\n"
                f"  Reason: {ev.reason or 'N/A'}"
            )
            evidence_lines.append(line)

    return "\n".join(evidence_lines)


def build_information_accuracy_prompt(
    benchmark: Benchmark,
    output: AgentOutput,
    report: VerificationReport,
) -> List[Message]:
    """Generates LLM judge messages for information accuracy assessment.

    Args:
        benchmark: The scenario benchmark details.
        output: The agent response output.
        report: The VerificationReport containing factual verification results.

    Returns:
        List of prompt Message structures.
    """
    system_instruction = (
        "You are an objective AI evaluator checking the information accuracy "
        "of an agent's output itinerary against a benchmark scenario and "
        "provided verification evidence.\n\n"
        f"### Rubric / Criteria:\n{INFORMATION_ACCURACY_RUBRIC}\n\n"
        f"{JSON_RESPONSE_SCHEMA}"
    )

    evidence_context = format_evidence_report(report)

    user_prompt = (
        f"VERIFICATION EVIDENCE FINDINGS:\n"
        f"================================\n"
        f"{evidence_context}\n"
        f"================================\n\n"
        f"Please evaluate the original itinerary below considering this factual evidence.\n\n"
        f"Benchmark Name: {benchmark.name}\n"
        f"Benchmark Description: {benchmark.description}\n\n"
        f"### Agent Output To Evaluate:\n{output.content}\n"
    )

    return [
        Message(role="system", content=system_instruction),
        Message(role="user", content=user_prompt),
    ]
