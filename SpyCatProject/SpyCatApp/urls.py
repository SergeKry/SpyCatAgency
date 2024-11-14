from django.urls import path

from .views import (SpyCatListCreateView,
                    SpyCatDetailView,
                    MissionCreateView,
                    MissionDetailView,
                    AssignCatToMissionView,
                    TargetUpdateView)

urlpatterns = [
    path('spy-cats/', SpyCatListCreateView.as_view(), name='spycat-list-create'),
    path('spy-cats/<int:pk>/', SpyCatDetailView.as_view(), name='spycat-detail'),
    path('missions/', MissionCreateView.as_view(), name='mission-create'),
    path('missions/<int:pk>/', MissionDetailView.as_view(), name='mission-details'),
    path('missions/<int:mission_id>/assign-cat/', AssignCatToMissionView.as_view(), name='assign-cat-to-mission'),
    path('targets/<int:target_id>/update/', TargetUpdateView.as_view(), name='target-update')
]
