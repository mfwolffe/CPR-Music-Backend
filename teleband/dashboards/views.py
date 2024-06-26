from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.views import generic

from teleband.assignments.models import Assignment
from teleband.courses.models import Course
from django.contrib.auth.mixins import UserPassesTestMixin


class AssignmentListView(UserPassesTestMixin, generic.ListView):
    model = Assignment

    def get_queryset(self) -> QuerySet[Any]:
        results = Assignment.objects.prefetch_related(
            "piece",
            "piece_plan",
            "enrollment",
            "enrollment__user",
            "enrollment__course",
            "enrollment__instrument",
            "enrollment__course__owner",
            "instrument",
            "submissions__attachments",
            "submissions__grade",
            "submissions__self_grade",
            "activity",
        ).all()
        return results

    # queryset = Course.objects.prefetch_related(
    #     "enrollment_set__assignment_set__submissions__attachments"
    # ).all()

    def test_func(self):
        return self.request.user.is_superuser


class CourseListView(UserPassesTestMixin, generic.ListView):
    model = Course

    def test_func(self):
        return self.request.user.is_superuser
