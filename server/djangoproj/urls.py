from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Frontend React pages (all point to index.html)
    path('', TemplateView.as_view(template_name="index.html")),
    path('about/', TemplateView.as_view(template_name="index.html")),
    path('contact/', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),

    # React frontend routes for dealers
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),
    

    # Catch-all React frontend routes
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
