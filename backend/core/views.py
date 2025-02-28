from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .models import User
from django.contrib.auth import logout 
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .utils import get_user_from_token

# Create your views here.
@csrf_exempt
def index(req):
    token = req.COOKIES.get('jwt_token')
    if token:
        if user := get_user_from_token(token):
            user = User.objects.get(id=user)
            return JsonResponse({
                'isAuthenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
    
    return JsonResponse({
        'isAuthenticated': False
    })

def login_view(req):
    return HttpResponseRedirect(reverse('social:begin', args=['auth0']))

def logout_view(req):
    logout(req)
    
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = req.build_absolute_uri(reverse('logout_handler'))

    return HttpResponseRedirect(f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}")
