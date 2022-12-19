from django.contrib import admin
from .models import UploadDetails, Details, Coordinates, Issue, CountAnn

admin.site.register(UploadDetails)
admin.site.register(Details)
admin.site.register(Coordinates)
admin.site.register(Issue)
admin.site.register(CountAnn)
# Register your models here.
