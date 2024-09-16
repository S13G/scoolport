from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.responses import CustomResponse
from apps.misc.docs.docs import retrieve_faqs_docs
from apps.misc.models import FAQ


# Create your views here.

class RetrieveFAQs(APIView):
    permission_classes = [IsAuthenticated]
    all_faqs = FAQ.objects.values("id", "question", "answer")

    @retrieve_faqs_docs()
    def get(self, request):
        data = list(self.all_faqs)
        return CustomResponse.success(message="Retrieved successfully", data=data)
