from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_info_form, name='user_info_form'),
    path('quiz/', views.quiz_view, name='quiz_view'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('thankyou/', views.thank_you, name='thank-you'),
    path('downloadcertificate/', views.download_certificate, name = 'download_certificate'),
]
