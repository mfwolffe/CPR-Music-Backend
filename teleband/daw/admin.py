from .models import Song
from django.contrib import admin
from reversion.admin import VersionAdmin


@admin.register(Song)
class SongAdmin(VersionAdmin):
  list_display = ("id", "title", "artist", "performer", "audio_file",)
  search_fields = ("title",)
