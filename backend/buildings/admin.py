from django.contrib import admin

from .models import Floor, Room


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ["number", "name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "floor", "capacity", "is_active"]
    list_filter = ["floor", "is_active"]
