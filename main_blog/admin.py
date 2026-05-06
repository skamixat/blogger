from django.contrib import admin

from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo',
                    'time_created', 'is_published') #какие поля таблицы отображаются в админке
    list_display_links = ('id', 'title') #какие из них кликабельны
    search_fields = ('title','content') #поисковик по полям
    list_editable = ('is_published',)  #какие элементы в таблице можно менять не заходя
    list_filter = ('is_published', 'time_created') #фильтр данных в таблицые

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
