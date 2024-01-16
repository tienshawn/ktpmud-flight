from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect, JsonResponse
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from .forms import PasswordChangingForm
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import secrets

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.


def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
   
    return render(request, 'Flight1/Home.html', {
            'min_date': min_date,
            'max_date': max_date
        })


class LoginClass(View):
    def get(self,request):
         return render(request,'Flight1/login.html')
    
    def post(self,request):
        user_name =request.POST.get('tendangnhap')
        pass_word= request.POST.get('matkhau')
        my_user = authenticate(username=user_name,password=pass_word)
        if my_user is None:
             return render(request, "Flight1/login.html", {
                "message": "Invalid username and/or password."
            })
        login(request, my_user)
        return HttpResponseRedirect(reverse("Flight1:index"))

class RegisterClass(View):
    def get(self,request):
         return render(request,'Flight1/register.html')    
    
    def post(self,request):
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        IDcode = request.POST['identification']
       

        # Kiem tra mk trung khop
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Flight1/register.html", {
                "message": "Passwords must match."
            })
        # Tao user moi
        else:
            try:
                new_user = User.objects.create_user(username, email, password)
                new_user.first_name = fname
                new_user.last_name = lname
                new_user.ID_code = IDcode
                new_user.phone_number = phone
                new_user.save()
            except:
                return render(request, "Flight1/register.html", {
                    "message": "Username already taken."
                })
            
            return render(request, "Flight1/register.html",{
                    "message": "Register successfully"})

class PasswordChangeClass (PasswordChangeView):
       form_class = PasswordChangingForm
       success_url = reverse_lazy('Flight1:index')
    
      
       
def logoutdef(request):
    logout(request)
    return HttpResponseRedirect(reverse("Flight1:index"))

@csrf_exempt
def flight(request):
    departure_place = request.GET.get('Origin')
    arrive_place = request.GET.get('Destination')
    trip_type = request.GET.get('TripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.objects.get(number=return_date.weekday()) 
        origin2 = Place.objects.get(code=arrive_place.upper())   
        destination2 = Place.objects.get(code= departure_place.upper())  
    seat = request.GET.get('SeatClass')

    flightday = Week.objects.get(number=depart_date.weekday())  
    destination = Place.objects.get(code=arrive_place.upper())     
    origin = Place.objects.get(code= departure_place.upper())    
    if seat == 'economy':
 
        flights = Flight.objects.filter(depart_day=flightday,depart=origin,destination=destination).exclude(economy_fare=None).order_by('economy_fare')    
        if trip_type == '2':    
            flights2 = Flight.objects.filter(depart_day=flightday2,depart=origin2,destination=destination2).exclude(economy_fare=None).order_by('economy_fare')    ##
    elif seat == 'business':
        flights = Flight.objects.filter(depart_day=flightday,depart=origin,destination=destination).exclude(business_fare=None).order_by('business_fare')
        if trip_type == '2':    
            flights2 = Flight.objects.filter(depart_day=flightday2,depart=origin2,destination=destination2).exclude(business_fare=None).order_by('business_fare')    ##
           
    elif seat == 'first':
        flights = Flight.objects.filter(depart_day=flightday,depart=origin,destination=destination).exclude(first_fare=None).order_by('first_fare')
        if trip_type == '2':    
            flights2 = Flight.objects.filter(depart_day=flightday2,depart=origin2,destination=destination2).exclude(first_fare=None).order_by('first_fare')
           
    if trip_type == '2':
        return render(request, "Flight1/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'flights2': flights2,   
            'origin2': origin2,    
            'destination2': destination2,    
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
           
        })
    else:
        return render(request, "Flight1/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            
        })
    
def review(request):
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        flight_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        flight1 = Flight.objects.get(id=flight_1)
        flight1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
        flight1adate = (flight1ddate + flight1.duration)
        flight2 = None
        flight2ddate = None
        flight2adate = None
        if round_trip:
            flight2 = Flight.objects.get(id=flight_2)
            flight2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),flight2.depart_time.hour,flight2.depart_time.minute)
            flight2adate = (flight2ddate + flight2.duration)
     
        if round_trip:
            return render(request, "Flight1/book.html", {
                'flight1': flight1,
                'flight2': flight2,
                "flight1ddate": flight1ddate,
                "flight1adate": flight1adate,
                "flight2ddate": flight2ddate,
                "flight2adate": flight2adate,
                "seat": seat,
               
            })
        return render(request, "Flight1/book.html", {
            'flight1': flight1,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "seat": seat,
       
        })
    else:
        return HttpResponseRedirect(reverse("Flight1:login"))
    



    # Ham xu li du lieu tao ra 1 ban ghi cua ve
def createticket(user,passengers,passengers_count,flight,flight_ddate,flight_class, country_code,email,mobile_number):
    ticket = Ticket.objects.create()
    ticket.user = user
    ticket.ticket_code = secrets.token_hex(3).upper()
    for p in passengers:
        ticket.passengers.add(p)

    ticket.flight = flight

    ticket.departure_date = datetime(int(flight_ddate.split('-')[2]),int(flight_ddate.split('-')[1]),int(flight_ddate.split('-')[0]))
    flightddate = datetime(int(flight_ddate.split('-')[2]),int(flight_ddate.split('-')[1]),int(flight_ddate.split('-')[0]),flight.depart_time.hour,flight.depart_time.minute)
    flightadate = (flightddate + flight.duration) 
    ticket.arrival_date = datetime(flightadate.year,flightadate.month,flightadate.day)
    
    fare = 0.0
    if flight_class.lower() == 'first':
        ticket.flight_fare = flight.first_fare*int(passengers_count)
        fare = flight.first_fare*int(passengers_count)
    elif flight_class.lower() == 'business':
        ticket.flight_fare = flight.business_fare*int(passengers_count)
        fare = flight.business_fare*int(passengers_count)
    else:
        ticket.flight_fare = flight.economy_fare*int(passengers_count)
        fare = flight.economy_fare*int(passengers_count)
                 
    ticket.total_fare = fare                
    ticket.seat_class = flight_class.lower()
    ticket.status = 'PENDING'
    ticket.mobile = ('(+' + country_code + ') ' + mobile_number)
    ticket.email = email
    ticket.save()
    return ticket


def book_flight(request):
    if request.method=='POST':
        if request.user.is_authenticated:
           flight1_id = request.POST.get('flight1_id') 
           flight1_ddate= request.POST.get('flight1_depart_date')
           flight1_class=request.POST.get('flight1_class')
           f2 = False
           if request.POST.get('flight2_id'):
               flight2_id = request.POST.get('flight2_id')
               flight2_ddate = request.POST.get('flight2_depart_date')
               flight2_class = request.POST.get('flight2_class')
               f2 = True
           country_code = request.POST['countrycode']
           mobile_number= request.POST['mobile']
           email= request.POST['email']

           #Tao ve
           flight1 = Flight.objects.get(id=flight1_id)
           if f2:
                flight2 = Flight.objects.get(id=flight2_id)

           passengers_count = request.POST['passengers_count']
           passengers=[]
           for i in range(1,int(passengers_count)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,gender=gender.lower()))
           try:
                ticket1 = createticket(request.user,passengers,passengers_count,flight1,flight1_ddate,flight1_class,country_code,email,mobile_number)
                if f2:
                    ticket2 = createticket(request.user,passengers,passengers_count,flight2,flight2_ddate,flight2_class,country_code,email,mobile_number)

                if(flight1_class == 'Economy'):
                    if f2:
                        fare = (flight1.economy_fare*int(passengers_count))+(flight2.economy_fare*int(passengers_count))
                    else:
                        fare = flight1.economy_fare*int(passengers_count)
                elif (flight1_class == 'Business'):
                    if f2:
                        fare = (flight1.business_fare*int(passengers_count))+(flight2.business_fare*int(passengers_count))
                    else:
                        fare = flight1.business_fare*int(passengers_count)
                elif (flight1_class == 'First'):
                    if f2:
                        fare = (flight1.first_fare*int(passengers_count))+(flight2.first_fare*int(passengers_count))
                    else:
                        fare = flight1.first_fare*int(passengers_count)
           except Exception as e:
                return HttpResponse(e)
            

           if f2:   
                return render(request, "Flight1/payment.html", { 
                    'fare': fare,   
                    'ticket': ticket1.id,   
                    'ticket2': ticket2.id,   
                })  
           return render(request, "Flight1/payment.html", {
                'fare': fare,
                'ticket': ticket1.id
            })
        else:
            return HttpResponseRedirect(reverse("Flight1:login"))
           
def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST['ticket']
            t2 = False
            if request.POST.get('ticket2'):
                ticket2_id = request.POST['ticket2']
                t2 = True
            ticket_fare = request.POST.get('fare')
            card_number = request.POST['card_number']
            cvv = request.POST['ccSecurityCode']
            holder_name = request.POST['holder_name']
            exp_month = request.POST['exp_month']
            exp_year = request.POST['exp_year']
           
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.booking_date = datetime.now()
                ticket.status = 'CONFIRMED'
                ticket.save()
                if t2:
                    ticket2 = Ticket.objects.get(id=ticket2_id)
                    ticket2.status = 'CONFIRMED'
                    ticket2.save()
                    return render(request, 'Flight1/payment2.html', {
                        'ticket1': ticket,
                        'ticket2': ticket2
                    })
                return render(request, 'Flight1/payment2.html', {
                    'ticket1': ticket,
                    'ticket2': ""
                })
            except Exception as e:
                return HttpResponse(e)

    else:
        return HttpResponseRedirect(reverse('Flight1:login'))


# In ve
    #Ham render ra pdf
def render_to_pdf (template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



@csrf_exempt
def print_ticket(request):
    ticket_code=request.GET.get("ticket_code")
    ticket1=Ticket.objects.get(ticket_code=ticket_code)
    user = request.user.username
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year,
        'user': user
    }
    pdf_src = render_to_pdf('Flight1/ticket.html', data)
    return HttpResponse(pdf_src, content_type='application/pdf')

def book_history(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'Flight1/history.html', {
            'page': 'bookings',
            'tickets': tickets,
        })
    else:
        return HttpResponseRedirect(reverse('Flight1:login'))

#Tiep tuc dat ve
def resume_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            code = request.POST['ticket_code']
            ticket = Ticket.objects.get(ticket_code=code)
            if ticket.user == request.user:
                return render(request, "Flight1/payment.html", {
                    'fare': ticket.total_fare,
                    'ticket': ticket.id
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))



def contact(request):
    if request.method=='POST':
        username=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone')
        message=request.POST.get('message')
        new_contact= Contact()
        new_contact.name = username
        new_contact.email = email
        new_contact.number = phone_number
        new_contact.message = message
        new_contact.save()
        
        return render(request, 'Flight1/contact.html', {
                    "message": "Thanks for contact"})
    return render(request, 'Flight1/contact.html')

def privacy_policy(request):
    return render(request, 'Flight1/privacy.html')

def terms_and_conditions(request):
    return render(request, 'Flight1/terms.html')

def about_us(request):
    return render(request, 'Flight1/about_us.html')


