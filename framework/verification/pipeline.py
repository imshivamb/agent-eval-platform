"""Verification pipeline orchestrating claim extraction and verifications."""

from framework.models import AgentOutput
from .base import BaseVerifier
from .extractor import ClaimExtractor
from .models import VerificationReport


class VerificationPipeline:
    """Orchestrates factual claim extraction and ground-truth verification.

    Wraps the pipeline execution: Agent Output -> Extraction -> Verifications -> VerificationReport.
    """

    def __init__(self, extractor: ClaimExtractor, verifier: BaseVerifier):
        """Initializes the VerificationPipeline.

        Args:
            extractor: The extractor instance to fetch claims.
            verifier: The verifier instance to verify claims.
        """
        self.extractor = extractor
        self.verifier = verifier

    def run(self, output: AgentOutput) -> VerificationReport:
        """Executes the verification pipeline on the agent output.

        Args:
            output: The output to analyze.

        Returns:
            A VerificationReport containing claims and evidence metrics.
        """
        claims = self.extractor.extract(output)
        evidence = self.verifier.verify_all(claims)
        return VerificationReport(claims=claims, evidence=evidence)
