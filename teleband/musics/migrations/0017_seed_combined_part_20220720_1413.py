# Generated by Django 3.2.11 on 2022-07-20 18:13

from django.db import migrations

import json
from teleband.musics.api.serializers import *

data = {
    "name": "Air for Band",
    "ensemble_type": "Band",
    "parts": [
        {
            "name": "Air for Band Combined",
            "part_type": "Combined",
            "transpositions": [
                {"transposition": "Bb"},
                {"transposition": "Concert Pitch BC 8vb"},
                {"transposition": "Concert Pitch BC"},
                {"transposition": "Concert Pitch TC 8va"},
                {"transposition": "Concert Pitch TC"},
                {"transposition": "Eb"},
                {"transposition": "F"},
            ],
        },
    ],
}

flatios = {
    "Air for Band Melody": {
        "Bb": {
            "scoreId": "61e09029dffcd50014571a80",
            "sharingKey": "169f2baebaa5721b4442b124fc984cce26f7e63312fb597d187f9c4d0e3aa1897df093c3bec76af250eb3ca0f36eb4f645ac70f470a695ccd217a1ce0cd52120",
        },
        "Concert Pitch BC 8vb": {
            "scoreId": "61e09029f7c4ec0013a88255",
            "sharingKey": "da2261d04292fb3ec8562a5fd1ac167e70937ee5c531bf51ba01a49e7629e4df47c838c488e5b2e978d72a2885879787c1f2357b46b35abecc6f8308c943c35f",
        },
        "Concert Pitch BC": {
            "scoreId": "61e0902a29718e0012080b97",
            "sharingKey": "7399632fbfbc793448182049dead3b88d921d7fab4328b5b9f5c589e654374d1d12a86d2e5567df1723b33e517b392552371129a9302bda49930f3e8a28dd857",
        },
        "Concert Pitch TC 8va": {
            "scoreId": "61e0902a58d51b001256f80c",
            "sharingKey": "11f725a4c13735b5e1a98903393699f066fd267f965d3d5ebea65f9bbd103ae5924cd3a26abfbc801f59aa0f71e66ee325192e397546cb648c4f4fc58cbb3490",
        },
        "Concert Pitch TC": {
            "scoreId": "61e0902a32669f0013f6f91d",
            "sharingKey": "25540b6b552a61fb0e95ed89986563b4a1b2caf566c114e2f48d1a8531866fca93e51681bf52ed4e0bedae3900b8781bccb84f51027b70bdc3f964d8a6a6e9aa",
        },
        "Eb": {
            "scoreId": "61e0902a74bfb70013c4ea3e",
            "sharingKey": "a88d609cd8c2224ccef9c043b03622ee11cd02390343eb9bbf3830b17929602ce138f7e623c99d9ebbbb291d9a415d62519ba5321b870be84c5fef49008f6d6e",
        },
        "F": {
            "scoreId": "61e0902a1ffc3c00126dc83a",
            "sharingKey": "7a9c959174769c7998d654218ba1d5c39054cf889f888e5b8eae871f2f4ccdca0d603a42266f45c875274263eb214cd517698bde86960dbdb088d4975bf33764",
        },
    },
}


def update_site_forward(apps, schema_editor):
    Piece = apps.get_model("musics", "Piece")
    # if Piece.objects.filter(name="Air for Band").exists():
    #     return

    piece = Piece.objects.filter(name="Air for Band").first()

    for part in data["parts"]:
        for t in part["transpositions"]:
            t["flatio"] = json.dumps(flatios["Air for Band Melody"][t["transposition"]])

    ps = PartCreateSerializer(many=True, piece=piece, data=data["parts"])
    ps.is_valid()
    ps.create(ps.validated_data)

    




class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0016_seed_pieces_later'),
    ]

    operations = [migrations.RunPython(update_site_forward, migrations.RunPython.noop)]