"""Shared fixtures and helpers for the test suite."""

from datetime import UTC, datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db.backends.postgresql.psycopg_any import DateTimeTZRange

from bookings.models import Booking
from buildings.models import Floor, Room

# A fixed day in the future keeps the tests independent of the current date.
DAY = datetime(2030, 1, 7, tzinfo=UTC)


def at(hour):
    """Return a UTC datetime on DAY; fractions work, e.g. 10.5 means 10:30."""
    return DAY + timedelta(hours=hour)


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(username="jan")


@pytest.fixture
def room(db):
    floor = Floor.objects.create(number=1)
    return Room.objects.create(floor=floor, name="SALA A", capacity=7)


@pytest.fixture
def other_room(room):
    # Depends on `room`, so both rooms are on the same floor.
    return Room.objects.create(floor=room.floor, name="Sala B", capacity=8)


@pytest.fixture
def make_booking(user):
    """Factory fixture: make_booking(room, start_hour, end_hour, ...)."""

    def _make(room, start, end, status=Booking.Status.CONFIRMED, attendees=4):
        # objects.create() skips model validation on purpose: the tests must
        # reach the database constraints directly.
        return Booking.objects.create(
            room=room,
            organizer=user,
            title="Spotkanie",
            attendees=attendees,
            status=status,
            period=DateTimeTZRange(at(start), at(end)),
        )

    return _make
