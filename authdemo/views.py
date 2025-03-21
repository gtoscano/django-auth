
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django_ratelimit.decorators import ratelimit

# For demonstration, the correct password is hardcoded.
CORRECT_PASSWORD = "secret"

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        password = request.POST.get('password', '')
        # Very simplistic password check
        if password == CORRECT_PASSWORD:
            return HttpResponse("Login successful!")
        else:
            return HttpResponse("Login failed!")
    return render(request, "authdemo/login.html")


@login_required
def protected_view(request):
    return HttpResponse(f"This is a protected page. You are logged in as {request.user.username}.")


#@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
class RateLimitedLoginView(auth_views.LoginView):
    template_name = "authdemo/login_django.html"
