from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from .services import section_image_directory, new_image_directory, redact_directory



class Section(models.Model):
    """Модель разделов новостей"""
    title = models.CharField(max_length=25, unique=True)
    description = models.TextField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to=section_image_directory, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('news_list', kwargs={'section_title': self.title})

    def get_absolute_create_url(self):
        return reverse('create_new', kwargs={'title': self.title})


class New(models.Model):
    """Модель новостей"""
    title = models.CharField(max_length=100)
    old_title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now())
    section = models.ForeignKey(Section, null=True, on_delete=models.PROTECT)
    like = models.IntegerField(default=0, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    picture = models.ImageField(upload_to=new_image_directory, blank=True, null=True)
    picture2 = models.ImageField(upload_to=new_image_directory, blank=True, null=True)
    picture3 = models.ImageField(upload_to=new_image_directory, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('new_detail', kwargs={"pk": self.id, "title": self.section})

    def save(self, *args, **kwargs):
        redact_directory(self)
        super().save()
    
    class Meta:
        ordering = ('title',)

class Rate(models.Model):
    valute_name = models.CharField(max_length=50, blank=True, null=True)
    valute = models.CharField(max_length=10, unique=True)
    value_rur = models.FloatField(max_length=7, blank=True, null=True)


    def __str__(self):
        return self.valute
