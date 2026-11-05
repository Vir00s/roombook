"""Django admin configuration for buildings (display only, no schema impact)."""

from django.contrib import admin

from .models import Floor, Room


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ["number", "name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "floor", "capacity", "is_active"]
    # Adds a filter sidebar to the changelist.
    list_filter = ["floor", "is_active"]
