
from django.urls import path
from .views import *
from .utils import *

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("login/handler/", auth_callback, name="login_handler"),
    
]
