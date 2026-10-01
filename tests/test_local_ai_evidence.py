"""Load shared synthetic behavioral tests in the default repository suite."""
import runpy
from pathlib import Path

LocalEvidenceTest = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/local_ai_evidence_test.py"))["LocalEvidenceTest"]
