from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins  # в ветке generics много классов для представления django rest framework
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet

from shop.models import Product, Category
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProductSerializer

class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['get'], detail=False)
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.name for c in cats]})







#######
# class ProductAPIListPagination(PageNumberPagination):  # класс пагинации только для FootballPlayersAPIList
#     page_size = 3
#     page_size_query_param = 'page_size'  # дополнительный параметр для ручного изменения числа записей-пишется в url ...&page_size=4 и будет 4 записи, а не 3.
#     max_page_size = 10000
#
#
# class ProductAPIList(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     pagination_class = ProductAPIListPagination
#
#
# class ProductAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (IsAuthenticated,)  # просматривать могут только авторизованные пользователи
#     # authentication_classes = (TokenAuthentication, )  # аутентификация по токенам только для этого view
#
#
# class ProductAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (IsAdminOrReadOnly,)