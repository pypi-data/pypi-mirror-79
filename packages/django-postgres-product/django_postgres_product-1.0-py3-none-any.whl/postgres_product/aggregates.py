from django.db.models.aggregates import Aggregate


class Product(Aggregate):
    function = 'PRODUCT'
    name = 'Product'
    allow_distinct = False
