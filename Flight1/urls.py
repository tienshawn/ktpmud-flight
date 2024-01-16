from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='Flight1'
urlpatterns = [
    path("",views.index, name='index'),
    path("login/",views.LoginClass.as_view(), name='login'),
    path("register/",views.RegisterClass.as_view(), name='register'),
    path("logout/",views.logoutdef, name='logout'),
    path("passwordchange", views.PasswordChangeClass.as_view(template_name='Flight1/passwordchange.html'), name='passchange'),
    path("flight", views.flight, name="flight"),
    path("review", views.review, name="review"),
    path("flight/ticket/book", views.book_flight, name="book"),
    path("flight/ticket/payment", views.payment, name="payment"),
    path("flight/ticket/print", views.print_ticket, name="print"),
    path("flight/ticket/resume", views.resume_ticket, name="resume"),
    path('contact', views.contact, name="contact"),
    path('privacy-policy', views.privacy_policy, name="privacy"),
    path('terms-and-conditions', views.terms_and_conditions, name="terms"),
    path('about-us', views.about_us, name="aboutus"),
    path('flight/book_history', views.book_history, name="history"),
]