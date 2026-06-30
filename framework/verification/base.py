"""Base interface for factual claims verifiers."""

from abc import ABC, abstractmethod
from framework.verification.models import Claim, Evidence


class BaseVerifier(ABC):
    """Abstract base class for factual claims verifiers."""

    @abstractmethod
    def verify(self, claim: Claim) -> Evidence:
        """Verifies a single claim against a ground-truth source.

        Args:
            claim: The claim to verify.

        Returns:
            An Evidence dataclass containing the outcome status and source reference.
        """
        pass
