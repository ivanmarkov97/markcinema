from django.contrib import admin
from .models import Film, Hall, Seance, Ticket
# Register your models here.

admin.site.register(Film)
admin.site.register(Hall)
admin.site.register(Seance)
admin.site.register(Ticket)
