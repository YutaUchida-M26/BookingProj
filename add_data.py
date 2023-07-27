import os
import django

# Djangoの設定を読み込むために、DJANGO_SETTINGS_MODULE環境変数を設定する
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookingProj.settings")

django.setup()
from datetime import datetime, timedelta
from bookproj.models import City, RoomType, Hotel, HotelAvailability

# 2週間の期間を取得
today = datetime.now().date()
two_weeks_from_today = today + timedelta(weeks=2)

# 各ホテルに対してroom_typeを4種類、期間を今日から2週間分作成
hotels = Hotel.objects.all()

for hotel in hotels:
    for room_type in RoomType.objects.all():
        current_date = today
        while current_date < two_weeks_from_today:
            # HotelAvailabilityオブジェクトを作成し、room_countを0で初期化
            availability = HotelAvailability(
                hotel=hotel,
                room_type=room_type,
                city=hotel.city,
                date=current_date,
                room_count=5,
            )
            availability.save()
            current_date += timedelta(days=1)
