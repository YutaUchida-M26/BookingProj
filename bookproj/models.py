from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class HotelAvailability(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    room_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type.name} - {self.city.name} - {self.date} (Room Count: {self.room_count})"


class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 既存のユーザーと関連付ける
    check_in_date = models.DateField()  # チェックイン日
    check_out_date = models.DateField()  # チェックアウト日

    def __str__(self):
        return f"{self.hotel.name} - {self.user.username}"
