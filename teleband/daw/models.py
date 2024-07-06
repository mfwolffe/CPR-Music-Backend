from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    performer = models.CharField(max_length=255, blank=True)

    share_url = models.URLField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    audio_file = models.FileField(blank=True, upload_to="sample_audio/")

    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"

    def __str__(self):
        return self.title
