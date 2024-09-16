from django.urls import path
from apps.misc.views import *

urlpatterns = [
    path("faq/all", RetrieveFAQs.as_view(), name="retrieve-faqs")
]