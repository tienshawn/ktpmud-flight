from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.



class User(AbstractUser):
    
    phone_number = models.CharField( ("phone_number"),null=False, blank=False, unique=False, max_length=11)
    ID_code = models.CharField ( ("ID_code"),null=False, blank=False, unique=False, max_length=13)
    
    def __str__(self):
         return f"{self.id}: {self.first_name} {self.last_name}"


class Contact(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField()
    number=models.CharField(max_length=12)
    message=models.TextField()
    contact_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.email} - {self.number}"

class Place(models.Model):
     code = models.CharField(max_length=3, null= False, blank = False)
     city = models.CharField(max_length=64, null= False, blank = False)
     country = models.CharField(max_length = 64, null= False, blank = False)
     airport = models.CharField(max_length= 64, null= False, blank = False)

     def __str__(self):
        return f"{self.code}: {self.city}, ({self.country})"
     
class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name} ({self.number})"
    
class Flight(models.Model):
    depart= models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals")
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day= models.ManyToManyField(Week, related_name="flight_of_the_days")
    duration = models.DurationField(null=False, blank=False)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    plane = models.CharField(max_length=32)
    airline= models.CharField(max_length=32)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id} {self.plane}: {self.depart} to {self.destination}"



GENDER = (
    ('male','MALE'),    
    ('female','FEMALE')
)

class Passenger(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)

    
    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}, {self.gender}"
   


SEAT_CLASS = (
    ('economy', 'Economy'),
    ('business', 'Business'),
    ('first', 'First')
)

TICKET_STATUS =(
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    
)

class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings", blank=True, null=True)
    ticket_code = models.CharField(max_length=6, unique=True)
    passengers = models.ManyToManyField(Passenger, related_name="flight_tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    flight_fare = models.FloatField(blank=True,null=True)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return self.ticket_code