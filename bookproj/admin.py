from django.contrib import admin
from bookproj.models import City, RoomType, Hotel, HotelAvailability, Reservation

# Register your models here.
admin.site.register(City)
admin.site.register(RoomType)
admin.site.register(Hotel)
admin.site.register(HotelAvailability)
admin.site.register(Reservation)
