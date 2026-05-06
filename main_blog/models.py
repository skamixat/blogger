from tabnanny import verbose

from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='URL', blank=True)
    content = models.TextField(blank=True, verbose_name='Содержание')
    photo = models.ImageField(upload_to='article/%Y/%m', verbose_name='Фото')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse('post', kwargs={'post_slug': self.slug})
        # Если slug пустой, используем ID
        return reverse('post', kwargs={'post_slug': str(self.id)})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-time_created', 'title'] #сортируем по времени создания, а если время одно, то алфавит

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='URL', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.slug:
            return reverse('category', kwargs={'cat_slug': self.slug})
        return  reverse('category', kwargs={'cat_slug': self.slug})


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id']

