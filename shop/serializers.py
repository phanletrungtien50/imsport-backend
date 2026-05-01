from rest_framework import serializers
from .models import (
    Product,
    Category,
    Brand,
    ProductImage,
    ProductVariant,
    Collection,
)

# ================= CATEGORY =================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]


# ================= BRAND =================
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo"]


# ================= PRODUCT LIST =================
class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    discount_percent = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()  # ✅ FIX

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "thumbnail",
            "price",
            "original_price",
            "discount_percent",
            "brand",
            "categories",
        ]

    def get_discount_percent(self, obj):
        if obj.original_price and obj.price and obj.original_price > obj.price:
            return round((1 - obj.price / obj.original_price) * 100)
        return 0

    def get_thumbnail(self, obj):
        """
        Trả về ABSOLUTE URL cho thumbnail
        """
        request = self.context.get("request")
        if obj.thumbnail:
            url = obj.thumbnail.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


# ================= PRODUCT VARIANT =================
class ProductVariantSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "size",
            "stock_quantity",
            "in_stock",
        ]

    def get_size(self, obj):
        size_attr = obj.attributes.filter(attribute__code="size").first()
        return size_attr.value if size_attr else None

    def get_in_stock(self, obj):
        return obj.stock_quantity > 0


# ================= PRODUCT DETAIL =================
class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "original_price",
            "thumbnail",
            "brand",
            "categories",
            "images",
            "variants",
            "specifications",
        ]

    def get_images(self, obj):
        request = self.context.get("request")
        images = []

        for img in obj.images.all():
            if img.image:
                url = img.image.url
                if request:
                    url = request.build_absolute_uri(url)

                images.append({
                    "image": url,
                    "alt_text": img.alt_text
                })

        return images


# ================= PRODUCT IMAGE CREATE =================
class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]


# ================= PRODUCT VARIANT CREATE =================
class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["sku", "stock_quantity"]


# ================= PRODUCT CREATE =================
class ProductCreateSerializer(serializers.ModelSerializer):
    variants = ProductVariantCreateSerializer(many=True)
    images = ProductImageCreateSerializer(many=True)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "brand",
            "categories",
            "description",
            "price",
            "original_price",
            "specifications",
            "variants",
            "images",
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop("variants", [])
        images_data = validated_data.pop("images", [])
        categories = validated_data.pop("categories", [])

        product = Product.objects.create(**validated_data)
        product.categories.set(categories)

        for v in variants_data:
            ProductVariant.objects.create(product=product, **v)

        for img in images_data:
            ProductImage.objects.create(product=product, **img)

        return product



# ================= CATEGORY TREE =================
class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "children"]

    def get_children(self, obj):
        return CategoryTreeSerializer(
            obj.children.filter(is_active=True).order_by("order", "id"),
            many=True
        ).data


# ================= COLLECTION =================
class CollectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ["id", "name", "slug", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CollectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ["id", "name", "slug", "image"]

    def get_image(self, obj):
        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None
