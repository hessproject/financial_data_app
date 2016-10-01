from django.contrib import admin
from stocks.models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'url', 'slug']
    list_display = ['name', 'url', 'slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)