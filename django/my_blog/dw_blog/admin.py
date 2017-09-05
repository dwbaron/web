from django.contrib import admin
from .models import Post, Cat, Tag, ImageStore
from ckeditor.fields import RichTextField

# Register your models here.

admin.site.register(Post)
admin.site.register(Cat)
admin.site.register(Tag)
admin.site.register(ImageStore)
