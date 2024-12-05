from typing import Any
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from consultas.models import Consulta
from consultas.api.serializers import ConsultaSerializer
from users.api.permissions import IsMedico

class ConsultaViewSet(ModelViewSet):
    class ConsultaListCreate(ModelViewSet):
        serializer_class = ConsultaSerializer
        permission_classes = [IsAdminUser | IsMedico]
        queryset = Consulta.objects.all()
        
        
        # GET: Listar todas as consultas
        def get(self, request):
            consultas = Consulta.objects.all()
            serializer = ConsultaSerializer(consultas, many=True)
            return Response(serializer.data)

        # POST: Criar uma nova consulta
        def post(self, request):
            serializer = ConsultaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    class ConsultaDetail(ModelViewSet):
        # Função auxiliar para obter consulta por ID
        def get_object(self, consulta_id):
            try:
                return Consulta.objects.get(id=consulta_id)
            except Consulta.DoesNotExist:
                return None

        # GET: Detalhar uma consulta específica
        def get(self, request, consulta_id):
            consulta = self.get_object(consulta_id)
            if not consulta:
                return Response({"error": "Consulta não encontrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ConsultaSerializer(consulta)
            return Response(serializer.data)

        # PUT: Atualizar uma consulta específica
        def put(self, request, consulta_id):
            consulta = self.get_object(consulta_id)
            if not consulta:
                return Response({"error": "Consulta não encontrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ConsultaSerializer(consulta, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # DELETE: Remover uma consulta específica
        def delete(self, request, consulta_id):
            consulta = self.get_object(consulta_id)
            if not consulta:
                return Response({"error": "Consulta não encontrada"}, status=status.HTTP_404_NOT_FOUND)
            consulta.delete()
            return Response({"message": "Consulta removida com sucesso"}, status=status.HTTP_204_NO_CONTENT)
        
    queryset = Consulta.objects.all()  # Busca todos os registros de consultas
    serializer_class = ConsultaSerializer  # Usa o serializador definido
