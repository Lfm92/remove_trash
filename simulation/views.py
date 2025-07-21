from rest_framework.views import APIView
from rest_framework.response import Response
from .simulator import Simulator
import asyncio

sim = Simulator()

class SimulationStep(APIView):
    def post(self, request):
        sim.step()
        return Response(sim.get_state())

class SimulationState(APIView):
    def get(self, request):
        return Response(sim.get_state())
