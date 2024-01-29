from django.contrib import admin
from .models import User, Note, SharedNote, Tag

# Register your models here.
admin.site.register(User)
admin.site.register(Note)
admin.site.register(SharedNote)
admin.site.register(Tag)