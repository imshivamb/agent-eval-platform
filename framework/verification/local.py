"""Local knowledge base claim verifier."""

import json
from pathlib import Path
from typing import Any, Dict
from framework.exceptions import KnowledgeBaseLoadError
from .base import BaseVerifier
from .models import Claim, Evidence, VerificationStatus
from .utils import normalize_key, values_are_equivalent


class LocalKnowledgeBaseVerifier(BaseVerifier):
    """Verifies claims against a local JSON knowledge base of truth facts."""

    def __init__(self, kb_path: str):
        """Initializes the LocalKnowledgeBaseVerifier.

        Args:
            kb_path: Path to the JSON file containing ground-truth data.
        """
        self.kb_path = Path(kb_path)
        self._kb: Dict[str, Dict[str, Any]] = {}
        self._load_kb()

    def _load_kb(self) -> None:
        """Loads and normalizes the knowledge base keys."""
        if not self.kb_path.exists():
            raise KnowledgeBaseLoadError(
                f"Knowledge base file does not exist: {self.kb_path}"
            )

        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except json.JSONDecodeError as e:
            raise KnowledgeBaseLoadError(
                f"Malformed JSON in knowledge base at {self.kb_path}: {e}"
            ) from e
        except Exception as e:
            raise KnowledgeBaseLoadError(
                f"Failed to read knowledge base at {self.kb_path}: {e}"
            ) from e

        if not isinstance(raw_data, dict):
            raise KnowledgeBaseLoadError(
                f"Knowledge base JSON must root-level represent a dictionary, got {type(raw_data)}"
            )

        # Normalize the database subject and predicate keys for robust matching
        for subject, predicates in raw_data.items():
            if not isinstance(predicates, dict):
                raise KnowledgeBaseLoadError(
                    f"Expected subject '{subject}' predicates to be a dictionary, got {type(predicates)}"
                )
            norm_subj = normalize_key(subject)
            if norm_subj not in self._kb:
                self._kb[norm_subj] = {}
            for pred, val in predicates.items():
                self._kb[norm_subj][normalize_key(pred)] = val

    def verify(self, claim: Claim) -> Evidence:
        """Verifies a single claim against the local normalized knowledge base.

        Args:
            claim: The claim to verify.

        Returns:
            An Evidence object containing the outcome.
        """
        norm_subj = normalize_key(claim.subject)
        norm_pred = normalize_key(claim.predicate)
        source_str = str(self.kb_path)

        # 1. Subject check (exact normalized match)
        if norm_subj not in self._kb:
            return Evidence(
                claim=claim,
                status=VerificationStatus.NOT_FOUND,
                expected_value=None,
                actual_value=claim.value,
                source=source_str,
                # Local KB is treated as authoritative.
                confidence=1.0,
                reason=f"Subject '{claim.subject}' was not found in the ground-truth records.",
            )

        subject_kb = self._kb[norm_subj]

        # 2. Predicate check (exact normalized match)
        if norm_pred not in subject_kb:
            return Evidence(
                claim=claim,
                status=VerificationStatus.UNKNOWN,
                expected_value=None,
                actual_value=claim.value,
                source=source_str,
                # Local KB is treated as authoritative.
                confidence=1.0,
                reason=f"Subject '{claim.subject}' is verified, but attribute '{claim.predicate}' is not documented in the ground-truth records.",
            )

        expected_val = str(subject_kb[norm_pred])
        actual_val = claim.value

        # 3. Value check
        if values_are_equivalent(expected_val, actual_val):
            status = VerificationStatus.VERIFIED
            reason_str = f"Factual claim matches ground-truth record for '{claim.subject}' ('{claim.predicate}' = '{expected_val}')."
        else:
            status = VerificationStatus.REFUTED
            reason_str = f"Factual discrepancy: ground-truth records list '{expected_val}' for '{claim.subject}' attribute '{claim.predicate}', but agent claimed '{actual_val}'."

        return Evidence(
            claim=claim,
            status=status,
            expected_value=expected_val,
            actual_value=actual_val,
            source=source_str,
            # Local KB is treated as authoritative.
            confidence=1.0,
            reason=reason_str,
        )
