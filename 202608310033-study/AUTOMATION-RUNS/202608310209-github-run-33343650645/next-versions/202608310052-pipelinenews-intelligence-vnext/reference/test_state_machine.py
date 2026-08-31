# REVIEW STATUS: UNREVIEWED
import unittest

from state_machine import Evidence, Lane, State, propose_transition, publish


class TimingStateMachineTests(unittest.TestCase):
    def test_one_signal_stays_silent(self):
        evidence = [Evidence("funding-1", Lane.FUNDING)]
        with self.assertRaisesRegex(ValueError, "both funding and procurement"):
            propose_transition(
                State.FUNDING_OBSERVED,
                State.CORROBORATED_WINDOW,
                evidence,
                identity_reviewed=True,
            )

    def test_dual_register_evidence_can_form_candidate_window(self):
        evidence = [
            Evidence("funding-1", Lane.FUNDING),
            Evidence("planning-1", Lane.PROCUREMENT),
        ]
        result = propose_transition(
            State.PROCUREMENT_OBSERVED,
            State.CORROBORATED_WINDOW,
            evidence,
            identity_reviewed=True,
        )
        self.assertEqual(result, State.CORROBORATED_WINDOW)

    def test_retracted_signal_does_not_count(self):
        evidence = [
            Evidence("funding-1", Lane.FUNDING, retracted=True),
            Evidence("planning-1", Lane.PROCUREMENT),
        ]
        with self.assertRaises(ValueError):
            propose_transition(
                State.PROCUREMENT_OBSERVED,
                State.CORROBORATED_WINDOW,
                evidence,
                identity_reviewed=True,
            )

    def test_contradiction_wins(self):
        result = propose_transition(
            State.DISCOVERED,
            State.IDENTITY_CANDIDATE,
            [],
            contradiction=True,
        )
        self.assertEqual(result, State.CONFLICTED)

    def test_release_requires_human_review(self):
        with self.assertRaises(ValueError):
            propose_transition(
                State.CORROBORATED_WINDOW,
                State.RELEASE_CANDIDATE,
                [],
                human_reviewed=False,
            )

    def test_audit_scaffold_cannot_publish(self):
        with self.assertRaisesRegex(RuntimeError, "forbidden"):
            publish()


if __name__ == "__main__":
    unittest.main()
