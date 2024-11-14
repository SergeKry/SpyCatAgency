from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, EditSpyCatSerializer, MissionSerializer, TargetUpdateSerializer
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


class MissionCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new Mission with associated Targets",
        request_body=MissionSerializer,
        responses={
            201: openapi.Response("Mission created successfully", MissionSerializer),
            400: "Bad Request - Invalid input data",
        }
    )
    def post(self, request):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)


class MissionDetailView(APIView):

    def get(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)
        serializer = MissionSerializer(mission)
        return Response(serializer.data)

    def delete(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)

        # validation that Mission is assigned to someone
        if mission.cat is not None:
            return Response({"error": "This mission is assigned to a cat and cannot be deleted."},
                            status=status.HTTP_400_BAD_REQUEST)
        mission.delete()
        return Response({"message": "Mission deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class AssignCatToMissionView(APIView):
    @swagger_auto_schema(
        operation_description="Assign a cat to a mission.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cat'],
            properties={
                'cat': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the cat to assign to the mission')
            },
            example={
                'cat': 2
            }
        ),
        responses={
            200: openapi.Response("Cat assigned successfully."),
            400: openapi.Response("Bad request - invalid input."),
            404: openapi.Response("Not found - Mission or Cat not found."),
        }
    )
    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, pk=mission_id)
        cat_id = request.data.get('cat')
        if cat_id is None:
            return Response({"error": "cat_id is required to assign a cat to this mission."},
                            status=status.HTTP_400_BAD_REQUEST)

        cat = get_object_or_404(SpyCat, pk=cat_id)
        mission.cat = cat
        mission.save()
        return Response({"message": f"Cat {cat.name} assigned to mission successfully."},
                        status=status.HTTP_200_OK)


class TargetUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Update a target",
        request_body=TargetUpdateSerializer,
        responses={
            200: openapi.Response("Target updated successfully.", TargetUpdateSerializer),
            400: "Bad Request - Validation error.",
            404: "Not found - Target not found.",
        }
    )
    def patch(self, request, target_id):
        target = get_object_or_404(Target, pk=target_id)
        serializer = TargetUpdateSerializer(target, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
