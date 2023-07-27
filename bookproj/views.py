from django.shortcuts import render, redirect
from .models import City, RoomType, HotelAvailability, Hotel, Reservation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date, timedelta, datetime
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import json
from django.db.models import Sum


# 以下を追加
def topPage(request):
    return render(request, "bookproj/topPage.html")


def searchPage(request):
    cities = City.objects.all()
    room_types = RoomType.objects.all()
    today = date.today()
    two_weeks_later = today + timedelta(days=14)
    return render(
        request,
        "bookproj/searchPage.html",
        {
            "cities": cities,
            "room_types": room_types,
            "today": today,
            "two_weeks_later": two_weeks_later,
        },
    )


def hotelList(request):
    if request.method == "POST":
        # フォームから送信された検索条件を取得
        city_id = request.POST.get("city")
        check_in_date = request.POST.get("check_in")
        check_out_date = request.POST.get("check_out")
        room_type_id = request.POST.get("room_type")

        # フォームに入力された条件を元にホテルを検索
        hotels = HotelAvailability.objects.filter(
            city_id=city_id,
            room_type_id=room_type_id,
            date__gte=check_in_date,
            date__lt=check_out_date,  # チェックアウトの日は含まないように変更
            room_count__gt=0,  # room_countが0より大きいことを条件に追加
        ).order_by("hotel__name", "hotel__city__name", "room_type__name", "date")

        # 連泊できるかチェック
        for hotel in hotels:
            next_date = hotel.date + timedelta(days=1)
            while (
                next_date < datetime.strptime(check_out_date, "%Y-%m-%d").date()
            ):  # チェックアウトの日の前日までループ
                next_day_availability = HotelAvailability.objects.filter(
                    hotel=hotel.hotel,
                    room_type=hotel.room_type,
                    date=next_date,
                    room_count__gt=0,  # 次の日のroom_countが0より大きいことをチェック
                ).exists()
                if not next_day_availability:
                    # 次の日のroom_countが0の場合、連泊不可なのでホテルリストから削除
                    hotels = hotels.exclude(
                        hotel=hotel.hotel,
                        room_type=hotel.room_type,
                    )
                    break
                next_date += timedelta(days=1)

        context = {
            "hotels": hotels,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
        }

    else:
        # GETリクエストの場合、全てのホテルを取得
        hotels = HotelAvailability.objects.filter(
            room_count__gt=0,  # room_countが0より大きいことを条件に追加
        ).order_by("hotel__name", "hotel__city__name", "room_type__name", "date")

        context = {
            "hotels": hotels,
            "check_in_date": None,
            "check_out_date": None,
        }

    return render(request, "bookproj/hotelList.html", context)


def reservation(request, hotel_id, room_type_id):
    try:
        hotel = Hotel.objects.get(pk=hotel_id)
        room_type = RoomType.objects.get(pk=room_type_id)
    except Hotel.DoesNotExist:
        messages.error(request, "Hotel not found.")
        return redirect("hotelList")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check_in_date = request.POST.get("check_in")
        check_out_date = request.POST.get("check_out")

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
        else:
            # ユーザーがログイン済みでない場合は新しいユーザーを作成
            if not request.user.is_authenticated:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # ログインさせる
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, "Failed to log in.")
                    return redirect("hotelList")

        # todo room_countが0より大きいか確認
        check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")
        stay_duration = (check_out_date - check_in_date).days

        # 指定された日付範囲内のHotelAvailabilityを取得
        available_dates = HotelAvailability.objects.filter(
            hotel=hotel,
            room_type=room_type,
            date__gte=check_in_date,
            date__lt=check_out_date,
        )

        # room_countが1以上のオブジェクトの数をカウント
        available_room_count = available_dates.filter(room_count__gt=0).count()

        # 予約可能な場合
        if (
            available_room_count == available_dates.count()
            and stay_duration <= available_room_count
        ):
            # 予約を作成
            reservation = Reservation.objects.create(
                hotel=hotel,
                room_type=room_type,
                user=request.user,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
            )
            reservation.save()
            # todo 該当するroom_countから1を引く
            for room_availability in available_dates:
                room_availability.room_count -= 1
                room_availability.save()

            messages.success(request, "Reservation completed successfully.")
            return redirect("hotelList")
        else:
            messages.error(request, "Failed to Reservation.")
            return redirect("hotelList")

    if request.method == "GET":
        # 予約可能な日付のリストを取得
        today = datetime.now().date()
        two_weeks_from_today = today + timedelta(weeks=2)
        available_dates = HotelAvailability.objects.filter(
            hotel=hotel,
            room_type=room_type,
            date__range=(today, two_weeks_from_today),
            room_count__gt=0,
        ).values_list("date", flat=True)

        check_in_date = request.GET.get("check_in_date")
        check_out_date = request.GET.get("check_out_date")

        formatted_available_dates = [
            date.strftime("%Y-%m-%d") for date in available_dates
        ]
        available_dates_json = json.dumps(formatted_available_dates)
        print(available_dates_json)

        context = {
            "hotel": hotel,
            "room_type": room_type,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "available_dates": available_dates,
            "available_dates_json": available_dates_json,
        }

        return render(request, "bookproj/reservation.html", context)


def logout_user(request):
    logout(request)
    return redirect("topPage")


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("topPage")
            else:
                # ログイン失敗時の処理
                # エラーメッセージを表示したり、ログインページにリダイレクトしたりすることが考えられます
                pass
    else:
        form = AuthenticationForm()

    return render(request, "bookproj/login.html", {"form": form})


def my_page(request):
    if not request.user.is_authenticated:
        # ログインしていない場合はログインページにリダイレクト
        return redirect("login")

    # ログイン済みのユーザーに関連する予約情報を取得
    reservations = Reservation.objects.filter(user=request.user)

    context = {"reservations": reservations}

    return render(request, "bookproj/myPage.html", context)
