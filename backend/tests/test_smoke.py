"""Smoke test: verifies that pytest, Django settings and the database are wired."""

import pytest
from django.db import connection


# Database access is blocked in tests unless explicitly allowed by this marker.
@pytest.mark.django_db
def test_database_is_postgresql():
    # The exclusion constraint exists only in PostgreSQL, not in SQLite.
    assert connection.vendor == "postgresql"
