"""Room bookings with a database-level guarantee against double booking."""

from django.conf import settings
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators
from django.db import models


class Booking(models.Model):
    """A reservation of one room for a time range."""

    class Status(models.TextChoices):
        # Stored value first, human-readable (admin) label second.
        # PENDING and CONFIRMED are "active": they block the room.
        PENDING = "PENDING", "Oczekuje na akceptację"
        CONFIRMED = "CONFIRMED", "Potwierdzona"
        CANCELLED = "CANCELLED", "Anulowana"
        COMPLETED = "COMPLETED", "Zakończona"
        NO_SHOW = "NO_SHOW", "Nieodebrana"

    # The model is referenced by a "app_label.Model" string to avoid a hard
    # import between apps. PROTECT keeps rooms that have bookings from being
    # deleted.
    room = models.ForeignKey(
        "buildings.Room", on_delete=models.PROTECT, related_name="bookings"
    )

    # AUTH_USER_MODEL keeps the code valid if the user model is swapped later.
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings"
    )

    title = models.CharField(max_length=200)
    # Single tstzrange column (start and end together), stored in UTC.
    # Ranges are half-open [start, end): back-to-back bookings do not overlap.
    period = DateTimeRangeField()
    attendees = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["period"]
        constraints = [
            # Core invariant, enforced by PostgreSQL itself: two active bookings
            # of the same room can never have overlapping periods. Needs the
            # btree_gist extension (enabled in the migration) so that "=" on
            # room_id can be combined with "&&" on period in one GiST index.
            ExclusionConstraint(
                name="no_overlapping_room_bookings",
                expressions=[
                    ("room", RangeOperators.EQUAL),
                    ("period", RangeOperators.OVERLAPS),
                ],
                # Cancelled, completed and no-show bookings do not block the room.
                condition=models.Q(status__in=["PENDING", "CONFIRMED"]),
            ),
            # A booking must be for at least one person.
            models.CheckConstraint(
                condition=models.Q(attendees__gt=0),
                name="booking_attendees_positive",
            ),
        ]

    def __str__(self):
        return f"{self.title} {self.room}"
