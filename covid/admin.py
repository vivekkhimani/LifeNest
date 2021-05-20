from django.contrib import admin

# Register your models here.
from .models import Service, Supplier, Requester, Volunteer, VerifiedPhone

admin.site.register(Service)
admin.site.register(Supplier)
admin.site.register(Requester)
admin.site.register(Volunteer)
admin.site.register(VerifiedPhone)
