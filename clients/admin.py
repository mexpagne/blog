from django.contrib import admin
from .models import Country, Client, City, State, Testimonial
# Register your models here.

admin.site.register(Client)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Testimonial)