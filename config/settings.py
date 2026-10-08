"""Central project paths and runtime settings."""

from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_CASE_FILE = PROJECT_ROOT / "test_cases" / "login_test_cases.xlsx"
BASE_URL = os.getenv("LOGIN_URL", "https://vanphongdientu.utc.edu.vn/Login")
DEFAULT_WAIT_SECONDS = float(os.getenv("SELENIUM_WAIT_SECONDS", "20"))
