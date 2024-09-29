from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


def retrieve_faqs_docs():
    return extend_schema(
        summary="Retrieve all FAQs",
        description="""
        This endpoint allows an authenticated user to retrieve all possible FAQs in case they need help
        settling an issue
        """,
        tags=["FAQ"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": [
                                {
                                    "id": "888cdeea-53df-4eeb-aa4f-2589aeaa8b26",
                                    "question": "How can I get involved in volunteering?",
                                    "answer": "Just volunteer",
                                }
                            ],
                        },
                    )
                ],
            ),
        },
    )
