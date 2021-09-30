
from django.urls import path
from .views import *

urlpatterns = [
    path('',  InitialView.as_view(), name='initial_url'),
    path('testing',  TestingView.as_view(), name='testing_url'),
    path('result',  ResultView.as_view(), name='result_url')
]
