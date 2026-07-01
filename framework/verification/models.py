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
