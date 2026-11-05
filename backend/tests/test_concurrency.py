"""Concurrency test: parallel inserts into the same slot must not double-book."""

import threading

import pytest
from django.db import DatabaseError, connection

from bookings.models import Booking

# transaction=True commits fixture data for real, so threads (each with its own
# database connection) can see it. A normal test hides data in a transaction.
pytestmark = pytest.mark.django_db(transaction=True)

THREADS = 8
# PostgreSQL SQLSTATE codes. With many concurrent writers an exclusion
# constraint can fail in two ways: a plain violation, or a deadlock between
# sessions waiting for each other's uncommitted rows.
EXCLUSION_VIOLATION = "23P01"
DEADLOCK_DETECTED = "40P01"


def test_concurrent_requests_for_same_slot_only_one_wins(room, make_booking):
    # The barrier releases all threads at once, so the inserts truly race.
    barrier = threading.Barrier(THREADS, timeout=10)
    results = []

    def worker():
        try:
            barrier.wait()
            make_booking(room, 10, 11)
            results.append("ok")
        except DatabaseError as exc:
            # Keep the SQLSTATE of the original driver error for the assertions.
            results.append(getattr(exc.__cause__, "sqlstate", repr(exc)))
        except Exception as exc:  # noqa: BLE001
            # Deliberately broad: an exception escaping a thread would be lost
            # and hide the real cause. Record it so the assertions report it.
            results.append(f"error: {exc!r}")
        finally:
            # Each thread owns a connection; close it so the test database
            # can be dropped afterwards.
            connection.close()

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    rejected = [r for r in results if r != "ok"]
    assert len(results) == THREADS
    # The database guarantee: exactly one insert wins, and no double booking
    # exists afterwards.
    assert results.count("ok") == 1
    assert set(rejected) <= {EXCLUSION_VIOLATION, DEADLOCK_DETECTED}
    assert Booking.objects.count() == 1
