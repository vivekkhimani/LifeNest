from django.contrib import admin

# Register your models here.
from .models import Service, Participant, VerifiedPhone

admin.site.register(Service)
admin.site.register(Participant)
admin.site.register(VerifiedPhone)
