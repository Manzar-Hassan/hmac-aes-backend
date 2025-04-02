from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Use decoded_body if it exists (from AESMiddleware), otherwise fall back to regular body
        data = request.decoded_body if hasattr(request, 'decoded_body') else request.data

        # Use the DRF serializer for validation and creation
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            book = serializer.save()  # Save the validated data to the database
            return Response(serializer.data, status=201)
        else:
            return JsonResponse({"error": "Invalid data", "details": serializer.errors}, status=400)
