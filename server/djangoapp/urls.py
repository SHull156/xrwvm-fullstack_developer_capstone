from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for registration
    path('register', views.registration, name='register'),

    # path for login
    path('login', views.login_user, name='login'),

    # path for logout
    path('logout', views.logout_request, name='logout'),

    # path for get_cars
    path('get_cars', views.get_cars, name='getcars'),

    # path for dealer reviews view
    # TODO: add path here

    # path for add a review view
    # TODO: add path here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
