from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from users.api.serializers import MedicoCreateSerializer, MedicoSerializer, UserProfileExampleSerializer

from users.models import Medico, UserProfileExample

class UserProfileExampleViewSet(ModelViewSet):
    serializer_class = UserProfileExampleSerializer
    permission_classes = [AllowAny]
    queryset = UserProfileExample.objects.all()
    http_method_names = ['get', 'put']

class MedicoViewSet(ModelViewSet):
    serializer_class = MedicoSerializer
    permission_classes = [AllowAny]
    queryset = Medico.objects.all()

    def create(self, request):
        serializer = MedicoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        novo_user = User.objects.create_user(
            username=serializer.validated_data['login'],
            password=serializer.validated_data['senha'],
        )
        grupo_medicos = Group.objects.get(name="Medicos")
        novo_user.groups.add(grupo_medicos)

        novo_medico = Medico.objects.create(
            nome=serializer.validated_data['nome'],
            matricula=serializer.validated_data['matricula'],
            departamento=serializer.validated_data['departamento'],
            user=novo_user
        )

        serializer_saida = MedicoSerializer(novo_medico)
        return Response({"Info": "Cadastro realizado!", "data":serializer_saida.data}, status=status.HTTP_201_CREATED)