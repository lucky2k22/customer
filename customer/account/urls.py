from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='index'),
    path('create_order/', CreateOrder,  name='create_order'),
    path('update_order/<int:id>/', updateOrder,  name='update_order'),
    path('delete_order/<int:id>/', deleteOrder,  name='delete_order'),
    path('register/', registerPage, name='register'),
    path('login/', login, name='login'),
    path('login_process/', loginProcess, name='login_process'),
    path('logout_process/', logoutProcess, name='logout_process'),

]   


