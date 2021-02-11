import graphene
from graphene_django.types import DjangoObjectType

from .models import StockPrice


class StockPriceType(DjangoObjectType):
    class Meta:
        model = StockPrice


class Query(graphene.ObjectType):
    all_stock_price = graphene.List(StockPriceType)
    stock_price = graphene.Field(StockPriceType, id=graphene.Int())

    def resolve_all_stock_price(self, info, **kwargs):
        return StockPrice.objects.all()

    def resolve_stock_price(self, info, **kwargs):
        id_value = kwargs.get("id")

        if id_value is not None:
            return StockPrice.objects.get(pk=id_value)

        return None
