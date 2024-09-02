from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import timedelta
from django.utils import timezone







class Main_category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='Main_category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Main category'
        verbose_name_plural = 'Main Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Main_category, self).save(*args, **kwargs)



    def __str__(self):
        return self.name


# Model: Product
class product_related_images(models.Model):
    product_image = models.ImageField(upload_to='Product_related_Images', blank=True, verbose_name='Product Image')

    def __int__(self):
        return self.id

    class Meta:
        verbose_name_plural = 'Product Related Images'


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, max_length=200,blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Main_category, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    product_more_images = models.ManyToManyField(product_related_images, null=True, blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name





    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url




class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class Order(models.Model):

    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')

    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True,null=True)
    billing = models.CharField(max_length=250, blank=True,null=True)
    billingCity = models.CharField(max_length=250, blank=True,null=True)
    billingPostcode = models.CharField(max_length=250, blank=True,null=True)
    billingCountry = models.CharField(max_length=250, blank=True,null=True)

    class Meta:
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product



class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    valid_from = models.DateTimeField(default=timezone.now, verbose_name='Valid From')
    valid_to = models.DateTimeField(verbose_name='Valid To')
    discount = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_valid(self):
        return self.active and self.valid_from <= timezone.now() and self.valid_to >= timezone.now()



