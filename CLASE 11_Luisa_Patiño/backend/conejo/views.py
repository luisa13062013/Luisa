
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conejo
from .serializers import ConejoSerializer

class ConejoViewSet(viewsets.ModelViewSet):
    queryset = Conejo.objects.all()
    serializer_class = ConejoSerializer

    @action(detail=True, methods=['put'])
    def actualizar(self, request, pk=None):
        conejo = self.get_object()
        serializer = ConejoSerializer(conejo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['delete'])
    def eliminar(self, request, pk=None):
        conejo = self.get_object()
        conejo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
