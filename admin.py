from django.contrib import admin
from .models import User, Recipe

# User admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'password')
    search_fields = ('user_name', 'email')

# Recipe admin
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cuisine', 'subcuisine', 'user', 'created_at')
    search_fields = ('title', 'cuisine', 'subcuisine')

admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
