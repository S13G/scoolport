from django.urls import path

from apps.portal.views import *

urlpatterns = [
    path("session/all", RetrieveSessionView.as_view(), name="retrieve-sessions"),
    path(
        "semester/all/<str:session_id>",
        RetrieveSemestersView.as_view(),
        name="retrieve-semesters",
    ),
    path("level/all", RetrieveLevelsView.as_view(), name="retrieve-levels"),
    path(
        "courses/retrieve",
        RetrieveCoursesToRegisterView.as_view(),
        name="retrieve-courses-to-register",
    ),
    path("course/register", RegisterCoursesView.as_view(), name="register-course"),
    path(
        "registered/courses",
        RetrieveRegisteredCoursesView.as_view(),
        name="retrieve-registered-courses",
    ),
    path("course/unregister", UnregisterCourseView.as_view(), name="unregister-course"),
    path(
        "registered/courses/all",
        RetrieveAllSemestersRegisteredCoursesView.as_view(),
        name="retrieve-all-registered-courses",
    ),
]
