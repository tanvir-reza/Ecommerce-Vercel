from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("category",args=[self.slug])
    

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product',null=True, blank=True,)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True,default='un-Brand')
    
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    # stock = models.IntegerField()
    # available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = 'Products'




    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product", args=[self.slug])
    
    