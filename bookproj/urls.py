from django.urls import path
from . import views

urlpatterns = [
    path("", views.topPage, name="topPage"),
    path("searchPage/", views.searchPage, name="searchPage"),
    path("hotelList/", views.hotelList, name="hotelList"),
    path(
        "reservation/<int:hotel_id>/<int:room_type_id>/",
        views.reservation,
        name="reservation",
    ),
    path("logout/", views.logout_user, name="logout"),
    path("login/", views.login_user, name="login"),
    path("myPage/", views.my_page, name="myPage"),
]
