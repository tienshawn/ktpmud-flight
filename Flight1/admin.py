from django.contrib import admin
from django.shortcuts import render
from django.urls.resolvers import URLPattern
from .models import *

from django.urls import path
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta, datetime
import pandas as pd

# Register your models here.


class CSV_place_form(forms.Form):
    csv_upload = forms.FileField()
    

class CSV_flight_form(forms.Form):
    csv_upload = forms.FileField()


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("city","airport","code","country")
    search_fields = ("city","airport","code","country")
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-place-csv/',self.upload_place_csv),]
        return new_urls + urls
    
    def upload_place_csv(self,request):
        if request.method == "POST":
            csv_file = request.FILES['csv_upload']
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            df=pd.read_csv(csv_file,delimiter=',')
            csv_data=[list(row) for row in df.values]
            
            
            for fields in csv_data:
                
                created = Place.objects.update_or_create(
                    city = fields[0].strip(),
                    airport = fields[1],
                    code = fields[2].strip(),
                    country = fields[3].strip(),
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
        
        form = CSV_place_form()
        data={"form": form}
        return render(request,'admin/Flight1/upload_place_csv.html', data)


class FlightAdmin(admin.ModelAdmin):
    list_display = ("depart","destination","depart_time","depart_day_display",'duration','arrival_time','plane','airline','economy_fare','business_fare','first_fare')
   
    def depart_day_display(self, obj):
        return ', '.join([str(item) for item in obj.depart_day.all()])
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-flight-csv/',self.upload_flight_csv),]
        return new_urls + urls


    def upload_flight_csv(self,request):
        if request.method == "POST":
            csv_file = request.FILES['csv_upload']
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            
            df=pd.read_csv(csv_file,delimiter=',')
            csv_data=[list(row) for row in df.values]
          
            for fields in csv_data:
                
                origin = fields[1].strip()
                destination = fields[2].strip()
                depart_time = datetime.strptime(fields[3].strip(), "%H:%M:%S").time()
                depart_week = int(fields[4])

                time_parts = fields[5].strip().split(':')
                if len(time_parts) >= 2:
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                    duration = timedelta(hours=hours, minutes=minutes)
                else:
                    duration = timedelta()

                arrive_time = datetime.strptime(fields[6].strip(), "%H:%M:%S").time()
                arrive_week = int(fields[7])
                flight_no = fields[8].strip()
                airline = fields[10].strip()
                economy_fare = float(fields[11]) if fields[11] else 0.0
                business_fare = float(fields[12]) if fields[12] else 0.0
                first_fare = float(fields[13]) if fields[13] else 0.0

                a1 = Flight.objects.create(depart=Place.objects.get(code=origin), destination=Place.objects.get(code=destination), depart_time=depart_time, duration=duration, arrival_time=arrive_time, plane=flight_no, airline=airline, economy_fare=economy_fare, business_fare=business_fare, first_fare=first_fare)
                a1.depart_day.add(Week.objects.get(number=depart_week))
        
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
        
        form = CSV_flight_form()
        data={"form": form}
        return render(request,'admin/Flight1/upload_flight_csv.html', data)
    
def createWeekDays():
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i,day in enumerate(days):
        Week.objects.create(number=i, name=day)


admin.site.register(User)
admin.site.register(Place,PlaceAdmin)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Contact)
admin.site.register(Week)
admin.site.register(Ticket)
admin.site.register(Passenger)
