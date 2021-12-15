from django.contrib.auth.models import User, Group

from .models import Coin, Block
from rest_framework import viewsets
from api.serializers import (
    CoinSerializer, 
    BlockSerializer
)

class CoinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

