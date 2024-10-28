from django.urls import path

from teleband.dashboards.views import AssignmentListView, CourseListView, csv_view
app_name = "dashboards"
urlpatterns = [
    path("", AssignmentListView.as_view(), name="assignment_list"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("export/csv/", csv_view, name="export_csv"),
]
