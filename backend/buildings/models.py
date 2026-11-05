"""Building structure: floors and the rooms located on them."""

from django.db import models


class Floor(models.Model):
    """A floor of the office building (the model assumes a single building)."""

    # Unique across the whole table because there is only one building.
    # Negative values are allowed (e.g. -1 for an underground garage).
    number = models.IntegerField(unique=True)
    # Optional display name. Blank values are stored as "", not NULL.
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        # Fall back to a generated label when the floor has no custom name.
        return self.name or f"Piętro {self.number}"


class Room(models.Model):
    """A bookable room. Deactivate it (is_active) instead of deleting it."""

    # PROTECT: a floor that still has rooms cannot be deleted by accident.
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, related_name="rooms")
    name = models.CharField(max_length=100)
    # Maximum number of people; strictly positive (see the constraints below).
    capacity = models.PositiveIntegerField()
    # Equipment flags. Deliberately simple for the MVP; a many-to-many
    # relation with quantities is planned for a later iteration.
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    has_video_conferencing = models.BooleanField(default=False)
    # Inactive rooms stay in the database, so booking history is preserved.
    is_active = models.BooleanField(default=True)

    class Meta:
        # "floor__number" follows the relation and sorts by the floor's number.
        ordering = ["floor__number", "name"]
        constraints = [
            # Room names must be unique per floor, not globally.
            models.UniqueConstraint(
                fields=["floor", "name"], name="unique_room_name_per_floor"
            ),
            # PositiveIntegerField only guarantees >= 0; this makes it > 0.
            models.CheckConstraint(
                condition=models.Q(capacity__gt=0),
                name="room_capacity_positive",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.floor})"
