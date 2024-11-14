from django.urls import path

from .views import SpyCatListCreateView, SpyCatDetailView

urlpatterns = [
    path('spy-cats/', SpyCatListCreateView.as_view(), name='spycat-list-create'),
    path('spy-cats/<int:pk>/', SpyCatDetailView.as_view(), name='spycat-detail'),
]
