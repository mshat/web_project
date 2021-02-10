from .models import *
from rest_framework import viewsets, permissions, generics
from .serializers import BackpackSerializer, BackpackDetailSerializer, BackpacksListSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .permissions import IsOwnerReadOnly


class BackpackViewSet(viewsets.ModelViewSet):
    queryset = Backpack.objects.all()
    permissions = [
        permissions.AllowAny,
    ]
    serializer_class = BackpackSerializer


class BackpackCreateView(generics.CreateAPIView):
    serializer_class = BackpackDetailSerializer


class BackpacksListView(generics.ListAPIView):
    serializer_class = BackpacksListSerializer
    queryset = Backpack.objects.all()
    permission_classes = (IsAuthenticated, )


class BackpackDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BackpackDetailSerializer
    queryset = Backpack.objects.all()
    permission_classes = (IsAuthenticated, )

