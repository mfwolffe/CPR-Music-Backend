from rest_framework import serializers

from teleband.daw.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            "id",
            "title",
            "genre",
            "artist",
            "subtitle",
            "share_url",
            "performer",
            "audio_file",
            "release_date",
        ]
