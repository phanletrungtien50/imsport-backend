from django.contrib import admin
from .models import (
    Brand,
    Category,
    Collection,
    Product,
    ProductVariant,
    ProductImage,
    Attribute,
    AttributeValue,
    ProductType,
)

# ================= ATTRIBUTE =================
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    prepopulated_fields = {"code": ("name",)}


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ["attribute", "value"]
    list_filter = ["attribute"]


# ================= PRODUCT VARIANT =================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    filter_horizontal = ("attributes",)   

# ================= PRODUCT IMAGE =================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# ================= PRODUCT =================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "price", "original_price", "is_active"]
    list_filter = ["brand", "is_active"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["categories"]
    inlines = [ProductVariantInline, ProductImageInline]



# ================= CATEGORY =================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    prepopulated_fields = {"slug": ("name",)}


# ================= BRAND =================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ("name",)}


# ================= PRODUCT TYPE =================
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

# ================= COLLECTION =================
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
