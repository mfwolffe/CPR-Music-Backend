# Generated by Django 3.2.11 on 2022-01-14 04:23

from django.db import migrations
from datetime import date


def demo_course(apps, schema_editor):
    User = apps.get_model("users", "User")

    # how to import this from the other migrations file?
    michael = User.objects.filter(email="michael@tele.band")[0]
    alden = User.objects.filter(email="alden@tele.band")[0]
    dave = User.objects.filter(email="dave@tele.band")[0]
    Course = apps.get_model("courses", "course")
    sixth_grade = Course.objects.update_or_create(
        name="6th Grade Band",
        owner=dave,
        start_date=date(2022, 1, 9),
        end_date=date(2022, 6, 9),
        slug="6th-grade-band",
    )[0]

    Instrument = apps.get_model("instruments", "Instrument")
    trombone = Instrument.objects.filter(name="Trombone")[0]
    Role = apps.get_model("users", "Role")
    teacher = Role.objects.filter(name="Teacher")[0]
    student = Role.objects.filter(name="Student")[0]

    Enrollment = apps.get_model("courses", "enrollment")

    Enrollment.objects.update_or_create(user=dave, course=sixth_grade, role=teacher)
    Enrollment.objects.update_or_create(
        user=michael, course=sixth_grade, instrument=trombone, role=student
    )

    Enrollment.objects.update_or_create(
        user=alden, course=sixth_grade, instrument=trombone, role=student
    )


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_alter_enrollment_unique_together"),
        ("users", "0004_data_migration_demo_users"),
    ]

    operations = [migrations.RunPython(demo_course, migrations.RunPython.noop)]