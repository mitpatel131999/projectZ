from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Car
from .serializers import CarSerializer

class CarListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Car.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CarDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        car = self.get_object()
        if car.owner != request.user:
            return Response({"error": "You do not have permission to update this car."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        car = self.get_object()
        if car.owner != request.user:
            return Response({"error": "You do not have permission to delete this car."}, status=status.HTTP_403_FORBIDDEN)
        if not car.available:
            return Response({"error": "Car cannot be deleted as it is currently in use."}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(request, *args, **kwargs)
