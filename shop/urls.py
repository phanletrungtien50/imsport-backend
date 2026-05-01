from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, BrandViewSet,CollectionViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("categories", CategoryViewSet, basename="category")
router.register("brands", BrandViewSet, basename="brand")
router.register("collections", CollectionViewSet, basename="collection")

urlpatterns = [
    path('', include(router.urls)),
]
