from django.contrib import admin

# Register your models here.
from .models import Service, Participant, Spammer

admin.site.register(Service)
admin.site.register(Participant)
admin.site.register(Spammer)
