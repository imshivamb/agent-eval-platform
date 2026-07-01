"""Base interface for factual claims verifiers."""

from abc import ABC, abstractmethod
from typing import List
from .models import Claim, Evidence


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

    def verify_all(self, claims: List[Claim]) -> List[Evidence]:
        """Batch verifies a list of claims sequentially.

        Args:
            claims: The list of claims to verify.

        Returns:
            A list of Evidence outcomes.
        """
        return [self.verify(c) for c in claims]
