"""Factual claim extraction from agent output using LLM."""

from typing import List
from framework.exceptions import VerificationError
from framework.llms import BaseLLM, Message
from framework.models import AgentOutput
from framework.utils import parse_json_markdown
from .models import Claim, ClaimType
from .prompts import CLAIM_EXTRACTION_PROMPT


class ClaimExtractor:
    """Extracts factual claims from agent output text using an LLM."""

    def __init__(self, llm: BaseLLM):
        """Initializes the ClaimExtractor.

        Args:
            llm: The LLM client to use for structured extraction.
        """
        self.llm = llm

    def extract(self, output: AgentOutput) -> List[Claim]:
        """Extracts verifiable claims from the agent output.

        Args:
            output: The output to analyze.

        Returns:
            A list of extracted Claim objects.

        Raises:
            VerificationError: If extraction or JSON parsing fails.
        """
        prompt_messages = self._build_messages(output.content)

        try:
            response = self.llm.generate(prompt_messages)
            raw_text = response.text
        except Exception as e:
            raise VerificationError(
                f"LLM claims extraction generation failed: {e}"
            ) from e

        raw_claims = self._parse_response(raw_text)

        claims = []
        for idx, item in enumerate(raw_claims):
            claim = self._validate_and_build_claim(item, idx)
            claims.append(claim)

        return claims

    def _build_messages(self, content: str) -> List[Message]:
        """Constructs prompt messages for claims extraction."""
        return [
            Message(role="system", content=CLAIM_EXTRACTION_PROMPT),
            Message(
                role="user",
                content=f"Extract all factual claims from the following text:\n\n{content}",
            ),
        ]

    def _parse_response(self, raw_text: str) -> List[dict]:
        """Cleans and parses the LLM JSON response."""
        try:
            parsed = parse_json_markdown(raw_text)
        except Exception as e:
            raise VerificationError(
                f"Failed to parse extractor LLM output as JSON. Raw response:\n{raw_text}"
            ) from e

        if not isinstance(parsed, list):
            raise VerificationError(
                f"Expected JSON array of claims, got: {type(parsed)}"
            )

        return parsed

    def _validate_and_build_claim(self, raw_item: dict, index: int) -> Claim:
        """Validates raw dict fields and builds a Claim object."""
        if not isinstance(raw_item, dict):
            raise VerificationError(
                f"Expected claim dictionary at index {index}, got: {type(raw_item)}"
            )

        for field in ["subject", "predicate", "value", "claim_type"]:
            if field not in raw_item:
                raise VerificationError(
                    f"Missing required field '{field}' in claim at index {index}: {raw_item}"
                )

        # Map type dynamically with validation fallback in python instead of LLM direct mapping
        raw_type = str(raw_item["claim_type"]).lower()
        try:
            claim_type = ClaimType(raw_type)
        except ValueError:
            claim_type = ClaimType.OTHER

        return Claim(
            subject=str(raw_item["subject"]),
            predicate=str(raw_item["predicate"]),
            value=str(raw_item["value"]),
            claim_type=claim_type,
        )
