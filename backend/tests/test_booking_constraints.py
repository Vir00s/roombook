"""Database-level rules for bookings (exclusion and check constraints)."""

import pytest
from django.db import IntegrityError, transaction

from bookings.models import Booking

# Allow database access in every test of this module.
pytestmark = pytest.mark.django_db

S = Booking.Status


@pytest.mark.parametrize(
    "start, end",
    [
        (10.5, 11.5),  # overlaps the end of the existing booking
        (9.5, 10.5),  # overlaps the start of the existing booking
        (10.25, 10.75),  # fully inside the existing booking
        (9, 12),  # fully contains the existing booking
        (10, 11),  # identical period
    ],
)
def test_overlapping_booking_in_same_room_is_rejected(room, make_booking, start, end):
    make_booking(room, 10, 11)

    # atomic() creates a savepoint: a failed INSERT aborts the surrounding
    # transaction in PostgreSQL, and the savepoint rollback keeps it usable.
    with pytest.raises(IntegrityError), transaction.atomic():
        make_booking(room, start, end)

    assert Booking.objects.count() == 1


@pytest.mark.parametrize("start, end", [(9, 10), (11, 12)])
def test_adjacent_bookings_are_allowed(room, make_booking, start, end):
    make_booking(room, 10, 11)

    # Ranges are half-open [start, end), so touching bookings do not collide.
    make_booking(room, start, end)

    assert Booking.objects.count() == 2


def test_same_time_in_another_room_is_allowed(room, other_room, make_booking):
    make_booking(room, 10, 11)

    make_booking(other_room, 10, 11)

    assert Booking.objects.count() == 2


@pytest.mark.parametrize("status", [S.CANCELLED, S.COMPLETED, S.NO_SHOW])
def test_inactive_booking_does_not_block_the_room(room, make_booking, status):
    make_booking(room, 10, 11, status=status)

    make_booking(room, 10, 11)

    assert Booking.objects.count() == 2


def test_pending_booking_blocks_the_room(room, make_booking):
    make_booking(room, 10, 11, status=S.PENDING)

    with pytest.raises(IntegrityError), transaction.atomic():
        make_booking(room, 10, 11)


def test_zero_attendees_is_rejected(room, make_booking):
    with pytest.raises(IntegrityError), transaction.atomic():
        make_booking(room, 10, 11, attendees=0)
