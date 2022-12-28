from django.urls import path
from .views import *

urlpatterns = [
    path('sign/up/',sign_up,name='sign_up'),
    path('sign/in/',sign_in,name='sign_in'),
    path('log/out/',log_out,name='log_out'),
]