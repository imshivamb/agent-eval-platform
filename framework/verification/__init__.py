"""Package containing interfaces and structures for factual verification."""

from framework.verification.models import (
    ClaimType,
    VerificationStatus,
    Claim,
    Evidence,
    VerificationReport,
)
from framework.verification.base import BaseVerifier
from framework.verification.local import LocalKnowledgeBaseVerifier
from framework.verification.extractor import ClaimExtractor
from framework.verification.pipeline import VerificationPipeline
