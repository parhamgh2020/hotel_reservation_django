# Hotel Reservation django

## how run 

```
to install dependency:
first make virtual environment 
install dependency by: pip install -r requirement 

for make sqlite
go to project directory 
run: python3 ./management makemigrations
run: python3 ./management migrate

for run project:
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
```

