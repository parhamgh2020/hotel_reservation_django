from datetime import datetime

from rest_framework import serializers

from .models import Hotel, Reservation, Room
from .validators import validate_reservation_date, validate_arrangement_date


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    check_in = serializers.DateField(input_formats=["%Y-%m-%d", "%Y-%m-%d"])
    check_out = serializers.DateField(input_formats=["%Y-%m-%d", "%Y-%m-%d"])

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, attrs):
        check_in = self.initial_data.get('check_in')
        check_out = self.initial_data.get('check_out')
        room = self.initial_data.get('room').split('/')[-2]
        validate_reservation_date(check_in, check_out, room)
        return super().validate(attrs)


class AvailableRoomListSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        try:
            return {
                'start_date': datetime.strptime(str(data['start_date']).strip(), '%Y-%m-%d').date(),
                'end_date': datetime.strptime(str(data['end_date']).strip(), '%Y-%m-%d').date(),
            }
        except ValueError:
            raise serializers.ValidationError('Invalid date format, must be YYYY-MM-DD.')

    def validate(self, attrs):
        start_date = self.initial_data.get('start_date')
        end_date = self.initial_data.get('end_date')
        validate_arrangement_date(start_date, end_date)
        return super().validate(attrs)
