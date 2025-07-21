from django.urls import path
from .views import SimulationStep, SimulationState

urlpatterns = [
    path("step/", SimulationStep.as_view()),
    path("state/", SimulationState.as_view()),
]
