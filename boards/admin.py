from django.contrib import admin

from .models import Board, Profile, Task

admin.site.register(Profile)
admin.site.register(Board)
admin.site.register(Task)
