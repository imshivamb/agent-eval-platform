"""Data structures for the factual claim verification subsystem."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ClaimType(str, Enum):
    """Supported types of factual claims for travel itineraries."""

    PRICE = "price"
    TIMING = "timing"
    EXISTENCE = "existence"
    DISTANCE = "distance"
    WEATHER = "weather"
    OTHER = "other"


class VerificationStatus(str, Enum):
    """Possible outcomes of verifying a claim against ground-truth data."""

    VERIFIED = "verified"
    REFUTED = "refuted"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


@dataclass
class Claim:
    """Represents a single testable factual assertion extracted from agent output."""

    subject: str
    predicate: str
    value: str
    claim_type: ClaimType


@dataclass
class Evidence:
    """Represents the outcome of verifying a Claim against a ground-truth source."""

    claim: Claim
    status: VerificationStatus
    expected_value: Optional[str]
    actual_value: Optional[str]
    source: str
    confidence: float = 1.0  # Confidence in verification result on a scale from 0.0 to 1.0.
    reason: Optional[str] = None  # Contextual reasoning explaining findings or discrepancy details.


@dataclass
class VerificationReport:
    """Consolidated verification outcomes for all claims in a scenario."""

    claims: List[Claim]
    evidence: List[Evidence]

    @property
    def total_claims(self) -> int:
        return len(self.claims)

    @property
    def verified_count(self) -> int:
        return sum(
            1 for e in self.evidence if e.status == VerificationStatus.VERIFIED
        )

    @property
    def refuted_count(self) -> int:
        return sum(
            1 for e in self.evidence if e.status == VerificationStatus.REFUTED
        )

    @property
    def unknown_count(self) -> int:
        return sum(
            1 for e in self.evidence if e.status == VerificationStatus.UNKNOWN
        )

    @property
    def not_found_count(self) -> int:
        return sum(
            1 for e in self.evidence if e.status == VerificationStatus.NOT_FOUND
        )

    def to_markdown(self) -> str:
        """Formats verification report evidence metrics and findings into a markdown string."""
        evidence_lines = []
        evidence_lines.append("Verification Summary:")
        evidence_lines.append(f"- Total Claims Extracted: {self.total_claims}")
        evidence_lines.append(f"- Verified: {self.verified_count}")
        evidence_lines.append(f"- Refuted: {self.refuted_count}")
        evidence_lines.append(f"- Unknown Predicates: {self.unknown_count}")
        evidence_lines.append(f"- Not Found Subjects: {self.not_found_count}\n")
        evidence_lines.append("Detailed Findings:")

        if not self.evidence:
            evidence_lines.append("No testable factual claims were extracted or verified.")
        else:
            for idx, ev in enumerate(self.evidence):
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

