from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from checkout.models import Transaction
from django_store import settings
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _


class MyModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('English Name'))
    name_ar = models.CharField(max_length=255, verbose_name=_('الاسم بالعربية'), help_text=_('MyModel name in Arabic'))


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    date_posted = models.DateTimeField(default=timezone.now, verbose_name=_('Date Posted'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    title_ar = models.CharField(max_length=255, verbose_name=_('عنوان'), default='عنوان افتراضي')
    description = models.TextField(verbose_name=_('Description'))
    description_ar = models.TextField(verbose_name=_('وصف'), default='وصف افتراضي')
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name=_('Video'))

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    name_ar = models.CharField(max_length=255, verbose_name=_('اسم'), default='اسم افتراضي')
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    order = models.IntegerField(default=1, verbose_name=_('Order'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    name_ar = models.CharField(max_length=255, verbose_name=_('الاسم بالعربية'), default='اسم افتراضي')
    bio = models.TextField(null=True, verbose_name=_('Bio'))
    bio_ar = models.TextField(null=True, verbose_name=_('سيرة ذاتية'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Authors')


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    name_ar = models.CharField(max_length=255, verbose_name=_('اسم'), default='اسم افتراضي')
    short_description = models.TextField(null=True, verbose_name=_('Short Description'))
    short_description_ar = models.TextField(null=True, verbose_name=_('وصف قصير'), default='وصف قصير افتراضي')
    description = models.TextField(null=True, verbose_name=_('Description'))
    description_ar = models.TextField(null=True, verbose_name=_('وصف'), default='وصف افتراضي')
    pdf_file = models.FileField(null=True, verbose_name=_('PDF File'))
    image = models.ImageField(verbose_name=_('Image'))
    price = models.FloatField(verbose_name=_('Price'))
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Category'))
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name=_('Author'))
    video = models.FileField(upload_to='product_videos/', blank=True, null=True, verbose_name=_('Video'))

    @property
    def pdf_file_url(self):
        return settings.SITE_URL + self.pdf_file.url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Order(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True, verbose_name=_('Transaction'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Product'))
    price = models.FloatField(verbose_name=_('Price'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))


class Cart(models.Model):
    items = models.JSONField(default=dict, verbose_name=_('Items'))
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name=_('Session'))

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    title_ar = models.CharField(max_length=255, verbose_name=_('عنوان'), default='عنوان افتراضي')
    subtitle = models.TextField(max_length=500, verbose_name=_('Subtitle'))
    subtitle_ar = models.TextField(max_length=500, verbose_name=_('العنوان الفرعي'), default='العنوان الفرعي الافتراضي')
    image = models.ImageField(null=True, verbose_name=_('Image'))
    order = models.IntegerField(default=1, verbose_name=_('Order'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Product'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    text = models.TextField(verbose_name=_('Text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.name}'
