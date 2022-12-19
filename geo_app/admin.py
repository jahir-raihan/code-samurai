from django.contrib import admin
from .models import UploadDetails, Details, Coordinates, Issue

admin.site.register(UploadDetails)
admin.site.register(Details)
admin.site.register(Coordinates)
admin.site.register(Issue)
# Register your models here.
