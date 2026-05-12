
from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    Article,
    Comment,
    SolarRequest,
    Appliance,
    SolarOnlyRequest,
    Project,
    ProjectImage)

# ================= PRODUCT (WITH MULTIPLE IMAGES) =================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)

# ================= ARTICLES =================

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'likes')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'created_at')


# ================= PROJECTS (MULTIPLE IMAGES) =================

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]


admin.site.register(Project, ProjectAdmin)
# ================= SOLAR =================

admin.site.register(SolarRequest)
admin.site.register(Appliance)
admin.site.register(SolarOnlyRequest)