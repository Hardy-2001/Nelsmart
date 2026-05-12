
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return self.product.name

class Article(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




class SolarRequest(models.Model):
        email = models.EmailField()
        phone = models.CharField(max_length=20, blank=True)
        state = models.CharField(max_length=100)
        message = models.TextField(blank=True)
        total = models.IntegerField(default=0)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.email

class Appliance(models.Model):
    solar_request = models.ForeignKey(SolarRequest, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)
    day_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name
class SolarOnlyRequest(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100)

    battery_capacity = models.CharField(max_length=50)
    battery_qty = models.IntegerField()

    inverter_power = models.CharField(max_length=50)
    voltage = models.CharField(max_length=20)

    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Project(models.Model):
    title = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to='projects/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')

    def __str__(self):
        return f"Image for {self.project.title}"