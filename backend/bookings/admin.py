"""Django admin for bookings: date-time pickers and a sensible default period."""

from datetime import timedelta

from django import forms
from django.contrib import admin
from django.contrib.postgres.fields import DateTimeRangeField as ModelRangeField
from django.contrib.postgres.forms import DateTimeRangeField, RangeWidget
from django.db.backends.postgresql.psycopg_any import DateTimeTZRange
from django.utils import timezone

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["title", "room", "organizer", "period", "status"]
    list_filter = ["status", "room"]
    # Replace the default range widget (two plain text inputs) with two native
    # browser "datetime-local" pickers. Admin-only: the model is unchanged.
    formfield_overrides = {
        ModelRangeField: {
            "form_class": DateTimeRangeField,
            "widget": RangeWidget(
                forms.DateTimeInput(
                    attrs={"type": "datetime-local"},
                    # The exact format "datetime-local" inputs expect.
                    format="%Y-%m-%dT%H:%M",
                )
            ),
        }
    }

    def get_changeform_initial_data(self, request):
        # Pre-fill the "add" form only (never an existing booking): the next
        # full hour in local time, lasting one hour. Kept in the admin instead
        # of the model so an API client cannot create a booking with an
        # implicit period.
        initial = super().get_changeform_initial_data(request)
        start = timezone.localtime().replace(
            minute=0, second=0, microsecond=0
        ) + timedelta(hours=1)
        initial.setdefault("period", DateTimeTZRange(start, start + timedelta(hours=1)))
        return initial
