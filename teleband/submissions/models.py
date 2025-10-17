from django.db import models
from django.conf import settings

from teleband.assignments.models import Assignment


class Grade(models.Model):

    # submission = models.ForeignKey(Submission, related_name="grades", on_delete=models.PROTECT)
    grader = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="grades", on_delete=models.PROTECT
    )
    rhythm = models.FloatField(null=True, blank=True)
    tone = models.FloatField(null=True, blank=True)
    expression = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Submission(models.Model):
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="student_submission",
    )
    self_grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="own_submission",
    )
    assignment = models.ForeignKey(
        Assignment, on_delete=models.PROTECT, related_name="submissions"
    )
    index = models.PositiveIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assignment.id}"


class SubmissionAttachment(models.Model):

    submission = models.ForeignKey(
        Submission, related_name="attachments", on_delete=models.PROTECT
    )
    file = models.FileField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Submission Attachment"
        verbose_name_plural = "Submission Attachments"
        ordering = ["-submitted"]

    def __str__(self):
        return f"{self.submission.id}: {self.file}"


class ActivityProgress(models.Model):
    """Tracks student progress through DAW study activities."""

    assignment = models.OneToOneField(
        Assignment, on_delete=models.CASCADE, related_name="activity_progress"
    )
    current_step = models.PositiveIntegerField(default=1)  # 1-4 for Activities 1-4
    step_completions = models.JSONField(
        default=dict,
        help_text="Tracks completed operations per step: {step: [operation_type, ...]}"
    )
    activity_logs = models.JSONField(
        default=list,
        help_text="Array of timestamped events: [{timestamp, step, operation, data}, ...]"
    )
    question_responses = models.JSONField(
        default=dict,
        help_text="Student responses to embedded questions: {question_id: response, ...}"
    )
    participant_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email from Qualtrics for survey matching"
    )

    # Audio state persistence for cross-activity editing
    current_audio_url = models.TextField(
        blank=True,
        null=True,
        help_text="Current audio blob URL or file path"
    )
    audio_edit_history = models.JSONField(
        default=list,
        help_text="Array of edit history states for undo/redo: [{url, effectName, metadata}, ...]"
    )
    audio_metadata = models.JSONField(
        default=dict,
        help_text="Additional audio metadata: {duration, sampleRate, numberOfChannels, ...}"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Activity Progress"
        verbose_name_plural = "Activity Progress"

    def __str__(self):
        return f"Assignment {self.assignment.id} - Step {self.current_step}"
