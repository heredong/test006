from django.conf.urls import url
# from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^index$',index,name='index'),
    url(r"^login$",login_view,name="login"),
    url(r"^logout$",logout_view,name="logout"),
    url(r"register",register_view,name='register'),
    url(r"^login_v2$", login_v2, name="login_v2"),
    url(r"^home$", home, name="home"),
    url(r"^logout_v2$", logout_v2, name="logout_v2"),
    url(r"^send$", send_my_mail)


]