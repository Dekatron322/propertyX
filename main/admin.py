from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Property)
admin.site.register(ScheduleTour)
admin.site.register(PropertyLike)
admin.site.register(PropertyBookmark)
admin.site.register(ReserveProperty)
admin.site.register(Solicitor)