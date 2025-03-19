# authdemo/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import login_view, protected_view, RateLimitedLoginView

urlpatterns = [
    path('login/', login_view, name='login'),
    # Django's built-in login view with a custom template
    #path('login_django/', auth_views.LoginView.as_view(template_name="authdemo/login_django.html"), name='login_django'),
    path('login_django/', RateLimitedLoginView.as_view(), name='login_django'),
    # Protected page
    path('protected/', protected_view, name='protected'),
]

