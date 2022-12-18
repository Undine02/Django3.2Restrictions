from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.exclude(status='DRAFT')
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        # Админы могут менять и удалять любые объявления.
        if self.action == 'create':
            return [IsAuthenticated(), ]
        if self.action in ["update", "partial_update", "destroy", ]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        return []

    # Variant 1
    def get_queryset(self):
        """Пока объявление в черновике, оно показывается только автору объявления,
        другим пользователям оно недоступно"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            queryset_draft = Advertisement.objects.filter(creator=user, status='DRAFT')
            queryset = queryset | queryset_draft

        return queryset

    # Variant 2

    # def list(self, request, *args, **kwargs):
    #     """Пока объявление в черновике, оно показывается только автору объявления,
    #     другим пользователям оно недоступно"""
    #     if self.request.user:
    #         queryset_draft = Advertisement.objects.filter(
    #             creator__id=self.request.user.id,
    #             status='DRAFT'
    #         )
    #         queryset = self.queryset.union(queryset_draft)
    #         queryset = Advertisement.objects.filter(id__in=queryset.values('id'))
    #         queryset = self.filter_queryset(queryset)
    #         page = self.paginate_queryset(queryset)
    #
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             return self.get_paginated_response(serializer.data)
    #
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)
    #
    #     return super().list(request, *args, **kwargs)