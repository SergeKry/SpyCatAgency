from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpyCat
from .serializers import SpyCatSerializer, EditSpyCatSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SpyCatListCreateView(APIView):
    def get(self, request):
        spy_cats = SpyCat.objects.all()
        serializer = SpyCatSerializer(spy_cats, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new SpyCat",
        request_body=SpyCatSerializer,
        responses={201: SpyCatSerializer}
    )
    def post(self, request):
        serializer = SpyCatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpyCatDetailView(APIView):
    def get(self, request, pk):
        spy_cat = get_object_or_404(SpyCat, pk=pk)
        serializer = SpyCatSerializer(spy_cat)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update only the salary of an existing SpyCat",
        request_body=EditSpyCatSerializer,
        responses={200: SpyCatSerializer}
    )
    def patch(self, request, pk):
        spy_cat = get_object_or_404(SpyCat, pk=pk)
        serializer = EditSpyCatSerializer(spy_cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        spy_cat = get_object_or_404(SpyCat, pk=pk)
        spy_cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)