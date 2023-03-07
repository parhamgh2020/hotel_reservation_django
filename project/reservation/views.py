import numpy as np
import pandas as pd
from rest_framework import renderers
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from rest_framework import generics

from .models import Hotel, Room, Reservation
from .serializers import (
    HotelSerializer,
    RoomSerializer,
    ReservationSerializer,
    AvailableRoomListSerializer,
)


class HotelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows hotels to be viewed or edited.
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = LimitOffsetPagination


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = LimitOffsetPagination


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reservations to be viewed or edited.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = LimitOffsetPagination
    renderers = None


class ReservationListHTML(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that returns a list of all reservations in HTML format.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    renderer_classes = (renderers.AdminRenderer,)


class AvailableRoomList(generics.GenericAPIView):
    """
    API endpoint that returns a list of available rooms for a given date range.
    """
    def get(self, request, start_date, end_date):
        """
        Get a list of available rooms for a given date range.

        Parameters:
            - start_date (str): The start date of the date range in YYYY-MM-DD format.
            - end_date (str): The end date of the date range in YYYY-MM-DD format.

        Returns:
            A JSON response containing a list of available rooms and their availability status for each day in the date range.
        """
        serializer = AvailableRoomListSerializer(data={
            "start_date": start_date,
            "end_date": end_date,
        })
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        date_range = pd.date_range(start=start_date, end=end_date)
        df_total = pd.DataFrame({'date': date_range})
        rooms = Room.objects.filter(status=1).values("id")
        reservations = Reservation.objects.filter(
            check_in__range=[start_date, end_date],
            check_out__range=[start_date, end_date]).values(
            "check_in", "check_out", "room")
        separate = dict()
        for reserved in reservations:
            start = reserved['check_in']
            end = reserved['check_out']
            date_range = pd.date_range(start=start, end=end, freq='D')
            separate[reserved['room']] = separate.get(reserved['room'], list())
            separate[reserved['room']].append(pd.DataFrame({'date': date_range,
                                                            reserved['room']: 'reserved'}))
        for room in rooms:
            room = room['id']
            if separate.get(room):
                continue
            else:
                separate[room] = [pd.DataFrame({'date': date_range,
                                                room: np.nan})]
        for room, list_df_range in separate.items():
            df = pd.concat(list_df_range)
            df = df.drop_duplicates()
            df = df.reset_index(drop=True)
            df_total = pd.merge(df_total, df, on="date", how='outer')
        output = self.get_format_jsonable(df_total)
        return Response(output)

    @staticmethod
    def get_format_jsonable(df):
        """
        Convert a pandas dataframe to a JSON-serializable format.

        Parameters:
            - df (pandas.DataFrame): The dataframe to be converted.

        Returns:
            A list of dictionaries containing the values in the dataframe.
        """
        head = df.columns.values
        body = df.values.tolist()
        output = list()
        for lst in body:
            dct = dict()
            for i in range(len(lst)):
                if i == 0:
                    dct['date'] = lst[i]
                else:
                    dct[f"room_id {head[i]}"] = lst[i] if lst[i] == 'reserved' else None
            output.append(dct)
        return output
