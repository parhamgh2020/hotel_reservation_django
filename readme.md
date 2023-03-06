# Hotel Reservation django

### how to run 

```
to install dependency:
first make virtual environment 
install dependency by: pip install -r requirement 

to make sqlite
go to project directory 
run: python3 ./management makemigrations
run: python3 ./management migrate

to run project:
go to project directory 
run: python3 ./manage.py runserver 

for test: 
go to project directory 
run: python3 ./manage.py test
```
### project end points
```commandline
to find out all endpoints please check swagger in "/api/docs/" endpoint
```


### about code
```commandline

This is a Python code implementing a Django REST API that provides access to a hotel booking system.
The code defines several ViewSets that handle HTTP requests for specific resources:HotelViewSet,
RoomViewSet, and ReservationViewSet. It also defines a ReservationListHTML view that returns a list
of all reservations in HTML format, and an AvailableRoomList view that returns a list of available
rooms for a given date range in JSON format.

views.py module:

The HotelViewSet, RoomViewSet, and ReservationViewSet classes inherit from the ModelViewSet class
provided by Django REST Framework (DRF) and define queryset and serializer_class attributes that
determine the model and serializer used by the ViewSet. The ReservationViewSet also sets the
renderer_classes attribute to None, indicating that it should not use any renderer, which is useful
if you want to return raw binary data such as images or files.

The ReservationListHTML view inherits from the ListModelMixin and GenericViewSet mixins provided by DRF,
which allow it to handle GET requests for a list of objects and render the response in HTML format using 
the AdminRenderer class.

The AvailableRoomList view is a subclass of the APIView class provided by DRF and defines a get() method
that handles GET requests for a list of available rooms. It first validates the start and end date 
parameters using the AvailableRoomListSerializer, then queries the Room and Reservation models to find 
available rooms for the given date range. It then creates a pandas DataFrame to represent the 
availability of each room for each day in the date range, and converts it to a JSON-serializable format 
using the get_format_jsonable() method.

The code also imports several modules, including numpy, pandas, and various DRF modules such as renderers, 
viewsets, and serializers, which are used throughout the code.


models.py module:

Hotel model has the following fields:
 name: a CharField with a maximum length of 30 characters, default value "hotel espinas"
 owner: a CharField with a maximum length of 20 characters, default value "parham"
 location: a CharField with a maximum length of 50 characters
 state: a CharField with a maximum length of 50 characters, default value "tehran"
 country: a CharField with a maximum length of 50 characters, default value "iran"
 
The Room model has the following fields:
 room_type: a CharField with a maximum length of 50 characters and choices defined by ROOM_TYPE tuple of tuples.
 capacity: an IntegerField to indicate how many guests the room can accommodate.
 price: an IntegerField to store the price of the room.
 hotel: a ForeignKey field that relates each room to a hotel, with a CASCADE deletion rule.
 status: a CharField with a maximum length of 15 characters, choices defined by ROOM_STATUS tuple of tuples.
 room_number: an IntegerField that stores the room number.
 
The Reservation model has the following fields:
 check_in: a DateField to store the check-in date of the reservation.
 check_out: a DateField to store the check-out date of the reservation.
 room: a ForeignKey field that relates each reservation to a room, with a CASCADE deletion rule.
 guest: a ForeignKey field that relates each reservation to a user, with a CASCADE deletion rule.
```

