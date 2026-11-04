from django.conf import settings
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators
from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Oczekuje na akceptację"
        CONFIRMED = "CONFIRMED", "Potwierdzona"
        CANCELLED = "CANCELLED", "Anulowana"
        COMPLETED = "COMPLETED", "Zakończona"
        NO_SHOW = "NO_SHOW", "Nieodebrana"

    room = models.ForeignKey(
        "buildings.Room", on_delete=models.PROTECT, related_name="bookings"
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings"
    )

    title = models.CharField(max_length=200)
    period = DateTimeRangeField()
    attendees = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["period"]
        constraints = [
            ExclusionConstraint(
                name="no_overlapping_room_bookings",
                expressions=[
                    ("room", RangeOperators.EQUAL),
                    ("period", RangeOperators.OVERLAPS),
                ],
                condition=models.Q(status__in=["PENDING", "CONFIRMED"]),
            ),
            models.CheckConstraint(
                condition=models.Q(attendees__gt=0),
                name="booking_attendees_positive",
            ),
        ]

    def __str__(self):
        return f"{self.title} {self.room}"
