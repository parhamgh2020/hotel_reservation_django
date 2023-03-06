from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"hotel", views.HotelViewSet)
router.register(r"room", views.RoomViewSet)
router.register(r"reservation", views.ReservationViewSet, basename="reservation")
router.register(r"reservation-table-html", views.ReservationListHTML, basename="table")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "available-room-list/<str:start_date>/<str:end_date>/",
        views.AvailableRoomList.as_view(),
        name="available-room-list"
    ),
]
