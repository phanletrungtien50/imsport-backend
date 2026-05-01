from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Category, Brand, Collection
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    BrandSerializer,
    CategoryTreeSerializer,
    CollectionSerializer,
)


# ================= PRODUCT =================
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "description"]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        params = self.request.query_params

        # ================= CATEGORY =================
        category_slug = params.get("category")
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug, is_active=True)
                category_ids = [category.id] + list(
                    category.children.values_list("id", flat=True)
                )
                qs = qs.filter(categories__id__in=category_ids)
            except Category.DoesNotExist:
                return Product.objects.none()


        # ================= BRAND =================
        brand_param = params.get("brand")
        if brand_param:
            qs = qs.filter(brand__slug__in=brand_param.split(","))

        # ================= SIZE =================
        size_param = params.get("size")
        if size_param:
            sizes = [s.strip() for s in size_param.split(",") if s.strip()]
            qs = qs.filter(
                variants__attributes__attribute__code="size",
                variants__attributes__value__in=sizes,
                variants__stock_quantity__gt=0,
            )

        # ================= PRICE =================
        price_param = params.get("price")
        if price_param and ":" in price_param:
            min_price, max_price = price_param.split(":")
            qs = qs.filter(
                price__gte=min_price,
                price__lte=max_price
            )

        # ================= SORT =================
        sort = params.get("sort")

        if sort == "newest":
            qs = qs.order_by("-created_at")

        elif sort == "price_asc":
            qs = qs.order_by("price")

        elif sort == "price_desc":
            qs = qs.order_by("-price")

        elif sort == "discount":
            qs = qs.annotate(
                discount_amount=F("original_price") - F("price")
            ).order_by("-discount_amount")

        else:
            # default sort
            qs = qs.order_by("-created_at")

        return qs.distinct()


    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_serializer_context(self):
        return {"request": self.request}  # ✅ BẮT BUỘC

    # ================= NEW PRODUCTS =================
    @action(detail=False, methods=["get"])
    def new(self, request):
        qs = Product.objects.filter(is_active=True).order_by("-created_at")[:6]
        serializer = ProductListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # ================= SALE PRODUCTS =================
    @action(detail=False, methods=["get"])
    def sale(self, request):
        qs = Product.objects.filter(
            is_active=True,
            original_price__isnull=False,
            price__isnull=False,
            original_price__gt=F("price"),
        ).order_by("-created_at")[:6]

        serializer = ProductListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)


# ================= CATEGORY =================
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        roots = Category.objects.filter(
            parent__isnull=True,
            is_active=True
        ).order_by("order", "id")

        serializer = CategoryTreeSerializer(roots, many=True)
        return Response(serializer.data)


# ================= BRAND =================
class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# ================= COLLECTION =================
class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        collection = self.get_object()
        qs = collection.products.filter(
            is_active=True
        ).order_by("-created_at")[:6]

        serializer = ProductListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)
