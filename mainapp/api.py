from .models import *
from rest_framework import viewsets, permissions, generics, status
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .permissions import IsOwnerReadOnly, IsOwner, IsOwnerOrAdmin
from .views import CartView
from rest_framework.response import Response
from . import services
from djoser.views import UserViewSet


class MyUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        services.create_user(username=serializer.data.get('username'),
                             email=serializer.data.get('email'),
                             password=serializer.data.get('password')
                             )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def activation(self, request, *args, **kwargs):
        pass

    def resend_activation(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        pass

    def reset_password_confirm(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass

    def reset_username(self, request, *args, **kwargs):
        pass


# ORDERDETAIL
class DetailOrdersListView(generics.ListAPIView):
    """ Корзина """
    serializer_class = DetailOrdersListSerializer
    queryset = OrderDetail.objects.all()

    def get(self, request, *args, **kwargs):
        # todo костыль из-за отсутствия корзины
        if not request.user.is_staff:
            self.queryset = OrderDetail.objects.filter(order__buyer=self.request.user).filter(ordered=False)
        return self.list(request, *args, **kwargs)


class OrderCreateView(generics.RetrieveAPIView):
    serializer_class = DetailOrdersListSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        # todo костыль из-за отсутствия корзины
        if not request.user.is_staff:
            buyer = request.user
            services.order(buyer)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Dear admin, you do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )


class DetailOrderCreateView(generics.CreateAPIView):
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


# ORDERS
class OrdersListView(generics.ListAPIView):
    serializer_class = OrdersListSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.queryset = Order.objects.filter(buyer=request.user).exclude(status="c")
        return self.list(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = (IsOwnerOrAdmin,)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        order = services.OrderManager(id=pk)
        if order:
            if order.object.buyer == request.user or request.user.is_staff:
                services.delete_order(request, pk)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"detail": "You do not have permission to perform this action."},
                    status=status.HTTP_403_FORBIDDEN
                )
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
