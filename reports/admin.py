from django.contrib import admin
from .models import Report, FilmProfitReport, SeanceReport

# Register your models here.

admin.site.register(Report)
admin.site.register(FilmProfitReport)
admin.site.register(SeanceReport)
