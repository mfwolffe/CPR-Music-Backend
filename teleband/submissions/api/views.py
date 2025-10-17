from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from teleband.submissions.api.teacher_serializers import TeacherSubmissionSerializer
from django.db.models import OuterRef, Subquery

from .serializers import (
    GradeSerializer,
    SubmissionSerializer,
    AttachmentSerializer,
    ActivityProgressSerializer,
)

from teleband.courses.models import Course
from teleband.submissions.models import Grade, Submission, SubmissionAttachment, ActivityProgress
from teleband.assignments.models import Assignment
from datetime import datetime


class SubmissionViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_queryset(self):
        return self.queryset.filter(assignment_id=self.kwargs["assignment_id"])

    def perform_create(self, serializer):
        serializer.save(
            assignment=Assignment.objects.get(pk=self.kwargs["assignment_id"])
        )

    # @action(detail=False)
    # def get_


class AttachmentViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = AttachmentSerializer
    queryset = SubmissionAttachment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(submission_id=self.kwargs["submission_pk"])

    def perform_create(self, serializer):
        serializer.save(
            submission=Submission.objects.get(pk=self.kwargs["submission_pk"])
        )


class TeacherSubmissionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TeacherSubmissionSerializer
    queryset = Submission.objects.all()

    # def get_queryset(self,):
    #     pass

    @action(detail=False)
    def recent(self, request, **kwargs):
        if "piece_slug" not in request.GET or "activity_name" not in request.GET:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "Missing piece_slug or activity_name (figure it out!) in get data"
                },
            )

        course_id = self.kwargs["course_slug_slug"]
        piece_slug = request.GET["piece_slug"]
        activity_name = request.GET["activity_name"]

        # https://chatgpt.com/share/827ac4eb-110d-423c-a106-1e696059fc83
        # Define a subquery to get the latest submission for each enrollment
        latest_submissions = (
            Submission.objects.filter(
                assignment__enrollment=OuterRef("assignment__enrollment"),
                assignment__enrollment__course__slug=course_id,
                assignment__activity__activity_type__name=activity_name,
                assignment__part__piece__slug=piece_slug,
            )
            .order_by("-submitted")
            .values("pk")[:1]
        )

        # Use the subquery to filter the main queryset
        filtered_submissions = Submission.objects.filter(
            pk__in=Subquery(latest_submissions)
        ).order_by("assignment__enrollment", "-submitted")

        # The final queryset will have the latest submissions for each enrollment
        submissions = filtered_submissions

        serializer = self.serializer_class(
            submissions, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_queryset(self, *args, **kwargs):
        return Grade.objects.filter(
            student_submission__assignment__enrollment__course__slug=self.kwargs[
                "course_slug_slug"
            ]
        )


class ActivityProgressViewSet(GenericViewSet):
    serializer_class = ActivityProgressSerializer
    queryset = ActivityProgress.objects.all()

    def get_object(self):
        """Get or create progress for the current assignment."""
        assignment_id = self.kwargs.get("assignment_id")
        progress, created = ActivityProgress.objects.get_or_create(
            assignment_id=assignment_id
        )
        return progress

    def retrieve(self, request, *args, **kwargs):
        """Get progress for current assignment."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def log_event(self, request, **kwargs):
        """Log an operation event to the activity progress."""
        assignment_id = kwargs.get("assignment_id")

        try:
            progress, created = ActivityProgress.objects.get_or_create(
                assignment_id=assignment_id
            )

            # Extract event data from request
            operation = request.data.get("operation")
            step = request.data.get("step", progress.current_step)
            data = request.data.get("data", {})
            email = request.data.get("email")

            # Store email if provided and not already set
            if email and not progress.participant_email:
                progress.participant_email = email

            # Add timestamped event to logs
            event = {
                "timestamp": datetime.now().isoformat(),
                "step": step,
                "operation": operation,
                "data": data
            }
            progress.activity_logs.append(event)

            # Track operation completion
            step_key = str(step)
            if step_key not in progress.step_completions:
                progress.step_completions[step_key] = []
            if operation not in progress.step_completions[step_key]:
                progress.step_completions[step_key].append(operation)

            progress.save()

            serializer = self.serializer_class(progress)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    def submit_step(self, request, **kwargs):
        """Submit current step and advance to next."""
        assignment_id = kwargs.get("assignment_id")

        try:
            progress = ActivityProgress.objects.get(assignment_id=assignment_id)

            # Save any question responses
            responses = request.data.get("question_responses", {})
            progress.question_responses.update(responses)

            # Advance to next step (max 4)
            if progress.current_step < 4:
                progress.current_step += 1

            progress.save()

            serializer = self.serializer_class(progress)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ActivityProgress.DoesNotExist:
            return Response(
                {"error": "Activity progress not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["post"])
    def save_response(self, request, **kwargs):
        """Save a question response without advancing step."""
        assignment_id = kwargs.get("assignment_id")

        try:
            progress, created = ActivityProgress.objects.get_or_create(
                assignment_id=assignment_id
            )

            question_id = request.data.get("question_id")
            response_text = request.data.get("response")

            if question_id and response_text is not None:
                progress.question_responses[question_id] = response_text
                progress.save()

            serializer = self.serializer_class(progress)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
