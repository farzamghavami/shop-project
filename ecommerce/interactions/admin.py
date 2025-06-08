from multiprocessing.resource_tracker import register

from django.contrib import admin
from .models import Rate

admin.site.register(Rate)
