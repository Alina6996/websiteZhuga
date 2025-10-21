from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

# --- Категорії ---
class Category(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=100, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --- Теги ---
class Tag(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --- Пости ---
class Post(models.Model):
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    auther = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default=1)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    image = models.URLField(
        default="https://soliloquywp.com/wp-content/uploads/2016/08/How-to-Set-a-Default-Featured-Image-in-WordPress.png"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публікація"
        verbose_name_plural = "Публікації"


# --- Коментарі ---
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100, default="Anonymous")
    email = models.EmailField(default="no-reply@example.com")
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


# --- Підписки ---
class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class GalleryImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="gallery")
    image = models.URLField()
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.post.title} - {self.caption or 'Image'}"

    class Meta:
        verbose_name = "Фото галереї"
        verbose_name_plural = "Галерея посту"