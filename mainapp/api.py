from .models import *
from rest_framework import viewsets, permissions, generics, status
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .permissions import IsOwnerReadOnly, IsOwner, IsOwnerOrAdmin
from .views import CartView
from rest_framework.response import Response
from . import services
from djoser.views import UserViewSet


class MyUserViewSet(UserViewSet):
    def activation(self, request, *args, **kwargs):
        pass

    def resend_activation(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        print('Hui :)')

    def reset_password_confirm(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass

# class MyCustomUserViewSet(UserViewSet):
#     def get_permissions(self):
#         if self.action == "me" and self.request.method == "PUT":
#             # do something
#         return super().get_permissions()


class OrderDetailCreateView(generics.CreateAPIView):
    serializer_class = DetailOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        backpacks_ordered = serializer.data.get('number')
        pk = self.kwargs['pk']
        available_backpacks_number = services.BackpackManager(id=pk).object.number
        if backpacks_ordered < 0 or backpacks_ordered > available_backpacks_number:
            return Response(
                {'Not enough product to order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                headers=headers
            )
        services.add_item(request, pk, services.with_serializer, serializer)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


#ORDERS
class OrdersListView(generics.ListAPIView):
    serializer_class = OrdersListSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.queryset = Order.objects.filter(buyer=request.user)
        return self.list(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = (IsOwnerOrAdmin,)


class OrderDeleteView(generics.GenericAPIView):
    permission_classes = (IsOwnerReadOnly,)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if services.OrderManager(id=pk):
            services.delete_order(request, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'Order not found'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# BACKPACK
class BackpackCreateView(generics.CreateAPIView):
    serializer_class = BackpackDetailSerializer
    permission_classes = (IsAdminUser,)


class BackpacksListView(generics.ListAPIView):
    serializer_class = BackpacksListSerializer
    queryset = Backpack.objects.all()


class BackpackEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BackpackDetailSerializer
    queryset = Backpack.objects.all()
    permission_classes = (IsAdminUser,)


class BackpackDetailView(generics.RetrieveAPIView):
    serializer_class = BackpackDetailSerializer
    queryset = Backpack.objects.all()


# TYPE
class TypeCreateView(generics.CreateAPIView):
    serializer_class = TypeDetailSerializer
    permission_classes = (IsAdminUser,)


class TypesListView(generics.ListAPIView):
    serializer_class = TypesListSerializer
    queryset = Type.objects.all()


class TypeEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TypeDetailSerializer
    queryset = Type.objects.all()
    permission_classes = (IsAdminUser,)


class TypeDetailView(generics.RetrieveAPIView):
    serializer_class = TypeDetailSerializer
    queryset = Type.objects.all()


# MANUFACTURER
class ManufacturerCreateView(generics.CreateAPIView):
    serializer_class = ManufacturerDetailSerializer
    permission_classes = (IsAdminUser,)


class ManufacturersListView(generics.ListAPIView):
    serializer_class = ManufacturersListSerializer
    queryset = Manufacturer.objects.all()


class ManufacturerEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ManufacturerDetailSerializer
    queryset = Manufacturer.objects.all()
    permission_classes = (IsAdminUser,)


class ManufacturerDetailView(generics.RetrieveAPIView):
    serializer_class = ManufacturerDetailSerializer
    queryset = Manufacturer.objects.all()


# MATERIAL
class MaterialCreateView(generics.CreateAPIView):
    serializer_class = MaterialDetailSerializer
    permission_classes = (IsAdminUser,)


class MaterialsListView(generics.ListAPIView):
    serializer_class = MaterialsListSerializer
    queryset = Material.objects.all()


class MaterialEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MaterialDetailSerializer
    queryset = Material.objects.all()
    permission_classes = (IsAdminUser,)


class MaterialDetailView(generics.RetrieveAPIView):
    serializer_class = MaterialDetailSerializer
    queryset = Material.objects.all()
