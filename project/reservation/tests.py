from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import Hotel, Room, Reservation
from .views import (
    HotelViewSet, RoomViewSet, ReservationViewSet, ReservationListHTML, AvailableRoomList,
)


class HotelModelTestCase(TestCase):

    def setUp(self):
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner='Test Owner',
            location='Test Location',
            state='Test State',
            country='Test Country'
        )

    def test_hotel_creation(self):
        self.assertTrue(isinstance(self.hotel, Hotel))
        self.assertEqual(self.hotel.__str__(), self.hotel.name)

    def test_hotel_name_max_length(self):
        max_length = self.hotel._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_hotel_owner_max_length(self):
        max_length = self.hotel._meta.get_field('owner').max_length
        self.assertEqual(max_length, 20)

    def test_hotel_location_max_length(self):
        max_length = self.hotel._meta.get_field('location').max_length
        self.assertEqual(max_length, 50)

    def test_hotel_state_max_length(self):
        max_length = self.hotel._meta.get_field('state').max_length
        self.assertEqual(max_length, 50)

    def test_hotel_country_max_length(self):
        max_length = self.hotel._meta.get_field('country').max_length
        self.assertEqual(max_length, 50)


class RoomModelTestCase(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(name="Test Hotel", owner="Test Owner", location="Test Location",
                                          state="Test State", country="Test Country")
        self.room = Room.objects.create(room_type="1", capacity=2, price=100, hotel=self.hotel, status="1",
                                        room_number=101)

    def test_string_representation(self):
        self.assertEqual(str(self.room), "hotel Test Hotel, room 101")


class ReservationModelTestCase(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(name="Test Hotel", owner="Test Owner", location="Test Location",
                                          state="Test State", country="Test Country")
        self.room = Room.objects.create(room_type="1", capacity=2, price=100, hotel=self.hotel, status="1",
                                        room_number=101)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.reservation = Reservation.objects.create(check_in=date.today(), check_out=date.today() + timedelta(days=1),
                                                      room=self.room, guest=self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.reservation), self.user.username)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="parham")
        self.hotel = Hotel.objects.create(name="Test Hotel")
        self.room = Room.objects.create(hotel=self.hotel,
                                        room_number=201,
                                        status=1,
                                        capacity=3,
                                        price=150,
                                        room_type="1")
        self.reservation = Reservation.objects.create(
            room=self.room,
            guest=self.user,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
        )

    def test_hotel_list(self):
        request = self.factory.get("/hotels/")
        response = HotelViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_room_list(self):
        request = self.factory.get("/rooms/")
        response = RoomViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_reservation_list(self):
        request = self.factory.get("/reservations/")
        response = ReservationViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_reservation_create(self):
        data = {
            "room": self.room.pk.url,
            "guest_name": "New Guest",
            "check_in": date.today() + timedelta(days=100),
            "check_out": date.today() + timedelta(days=101),
        }
        request = self.factory.post("/reserve-section/reservation/", data=data)
        response = ReservationViewSet.as_view({'post': 'create'})(request)
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reservation.objects.count(), 2)

    # def test_reservation_update(self):
    #     data = {
    #         "check_in": date.today() + timedelta(days=3),
    #         "check_out": date.today() + timedelta(days=4),
    #     }
    #     request = self.factory.patch(f"/reservations/{self.reservation.pk}/", data=data)
    #     response = ReservationViewSet.as_view({'patch': 'partial_update'})(request, pk=self.reservation.pk)
    #     self.assertEqual(response.status_code, 200)
    #     self.reservation.refresh_from_db()
    #     self.assertEqual(self.reservation.check_in, data["check_in"])
    #     self.assertEqual(self.reservation.check_out, data["check_out"])
    #
    # def test_reservation_delete(self):
    #     request = self.factory.delete(f"/reservations/{self.reservation.pk}/")
    #     response = ReservationViewSet.as_view({'delete': 'destroy'})(request, pk=self.reservation.pk)
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(Reservation.objects.count(), 0)
    #
    # def test_reservation_list_html(self):
    #     request = self.factory.get("/reservations_html/")
    #     response = ReservationListHTML.as_view({'get': 'list'})(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_available_room_list(self):
    #     start_date = date.today() + timedelta(days=5)
    #     end_date = date.today() + timedelta(days=7)
    #     request = self.factory.get(f"/rooms/available/{start_date}/{end_date}/")
    #     response = AvailableRoomList.as_view()(request, start_date=start_date, end_date=end_date)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual
