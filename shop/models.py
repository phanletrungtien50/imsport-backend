from django.db import models

# ================= BRAND =================
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name


# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ================= COLLECTION =================
class Collection(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ================= PRODUCT TYPE =================
class ProductType(models.Model):
    name = models.CharField(max_length=100)   # Áo, Đồng hồ
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# ================= ATTRIBUTE =================
class Attribute(models.Model):
    name = models.CharField(max_length=100)   # Size, Color, Case Size
    code = models.CharField(max_length=50)    # size, color, case_size

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values"
    )
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.code}: {self.value}"


# ================= PRODUCT =================
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        null=True,     
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )

    categories = models.ManyToManyField(
    Category,
    related_name="products",
    blank=True
    )


    description = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)

    thumbnail = models.ImageField(upload_to="products/thumbnails/", blank=True, null=True)

    collections = models.ManyToManyField(Collection, related_name="products", blank=True)
    specifications = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ================= PRODUCT VARIANT =================
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="variants",
        on_delete=models.CASCADE
    )

    sku = models.CharField(max_length=50, unique=True)

    attributes = models.ManyToManyField(
        AttributeValue,
        related_name="variants",
        blank=True
    )

    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.sku


# ================= PRODUCT IMAGE =================
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)
