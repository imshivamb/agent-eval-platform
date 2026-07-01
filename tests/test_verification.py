import unittest
import tempfile
import os
import json
from framework.models import AgentOutput
from framework.verification.models import Claim, ClaimType, VerificationStatus
from framework.verification.local import LocalKnowledgeBaseVerifier
from framework.verification.extractor import ClaimExtractor
from framework.verification.pipeline import VerificationPipeline
from framework.llms import MockLLM
from framework.exceptions import KnowledgeBaseLoadError


class TestVerification(unittest.TestCase):
    """Tests the factual verification subsystem."""

    def setUp(self):
        # Create a temporary JSON ground truth file for KB tests
        self.kb_data = {
            "Gyeongbokgung Palace": {
                "closed_days": "Tuesday",
                "city": "Seoul"
            },
            "TeamLab Planets": {
                "exists": "true",
                "ticket_price": "3800 JPY"
            }
        }
        self.temp_kb = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(self.kb_data, self.temp_kb)
        self.temp_kb.close()

    def tearDown(self):
        os.unlink(self.temp_kb.name)

    def test_local_kb_verifier(self):
        verifier = LocalKnowledgeBaseVerifier(self.temp_kb.name)

        # Verified claim
        c1 = Claim("gyeongbokgung_palace", "closed_days", "Tuesday", ClaimType.TIMING)
        e1 = verifier.verify(c1)
        self.assertEqual(e1.status, VerificationStatus.VERIFIED)
        self.assertIn("matches ground-truth record", e1.reason)

        # Smarter equivalence comparison check
        c2 = Claim("teamlab_planets", "ticket_price", "¥3,800", ClaimType.PRICE)
        e2 = verifier.verify(c2)
        self.assertEqual(e2.status, VerificationStatus.VERIFIED)

        # Refuted claim
        c3 = Claim("gyeongbokgung_palace", "city", "Tokyo", ClaimType.EXISTENCE)
        e3 = verifier.verify(c3)
        self.assertEqual(e3.status, VerificationStatus.REFUTED)
        self.assertIn("Factual discrepancy", e3.reason)

        # Not found subject
        c4 = Claim("Unknown Temple", "exists", "true", ClaimType.EXISTENCE)
        e4 = verifier.verify(c4)
        self.assertEqual(e4.status, VerificationStatus.NOT_FOUND)

    def test_local_kb_load_failures(self):
        with self.assertRaises(KnowledgeBaseLoadError):
            LocalKnowledgeBaseVerifier("missing_file_123.json")

    def test_claim_extractor_mock(self):
        mock_response = """
        ```json
        [
          {
            "subject": "gyeongbokgung",
            "predicate": "closed_days",
            "value": "Tuesday",
            "claim_type": "timing"
          }
        ]
        ```
        """
        llm = MockLLM(responses=[mock_response])
        extractor = ClaimExtractor(llm)
        claims = extractor.extract(AgentOutput(content="Check Gyeongbokgung."))
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0].subject, "gyeongbokgung")
        self.assertEqual(claims[0].claim_type, ClaimType.TIMING)

    def test_verification_pipeline(self):
        mock_response = """
        ```json
        [
          {
            "subject": "gyeongbokgung_palace",
            "predicate": "closed_days",
            "value": "Tuesday",
            "claim_type": "timing"
          },
          {
            "subject": "teamlab_planets",
            "predicate": "ticket_price",
            "value": "4000 JPY",
            "claim_type": "price"
          }
        ]
        ```
        """
        llm = MockLLM(responses=[mock_response])
        extractor = ClaimExtractor(llm)
        verifier = LocalKnowledgeBaseVerifier(self.temp_kb.name)
        pipeline = VerificationPipeline(extractor, verifier)

        report = pipeline.run(AgentOutput(content="Check Gyeongbokgung and TeamLab ticket price."))
        self.assertEqual(report.total_claims, 2)
        self.assertEqual(report.verified_count, 1) # Tuesday closes matches
        self.assertEqual(report.refuted_count, 1) # 4000 JPY vs 3800 JPY
        self.assertIsNotNone(report.to_markdown())


if __name__ == "__main__":
    unittest.main()
