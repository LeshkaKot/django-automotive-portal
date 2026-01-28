from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


# Документация https://docs.djangoproject.com/en/4.2/ref/models/fields/

# пользовательский менеджер для моделей
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Student.PostStatus.PUBLISHED)


class Student(models.Model):
    class PostStatus(models.IntegerChoices):
        DRAFT = 0, 'Draft'
        PUBLISHED = 1, 'Published'

    title = models.CharField(max_length=255, verbose_name="Car_Model_Name")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Photo")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(choices=PostStatus.choices, default=PostStatus.DRAFT, verbose_name="Publication_Status")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts", verbose_name="Category")
    tags = models.ManyToManyField("TagPost", blank=True, related_name="tags", verbose_name="Tags")
    manual = models.OneToOneField('Manual', on_delete=models.SET_NULL, null=True, blank=True, related_name='mod', verbose_name="Manual")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='author_posts', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Honda"
        verbose_name_plural = "Honda"

        ordering = ["time_create"]

        indexes = [models.Index(fields=["time_create"])]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):

    name = models.CharField(max_length=100, db_index=True, verbose_name="Category")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

        ordering = ["id"]


    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Manual(models.Model):
    name = models.CharField(max_length=50)
    pages = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to="uploads_model")

