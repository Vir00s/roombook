from django.db import models


class Floor(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return self.name or f"Piętro {self.number}"


class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, related_name="rooms")
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    has_video_conferencing = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["floor__number", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["floor", "name"], name="unique_room_name_per_floor"
            ),
            models.CheckConstraint(
                condition=models.Q(capacity__gt=0),
                name="room_capacity_positive",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.floor})"
