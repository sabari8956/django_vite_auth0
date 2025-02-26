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
    print(req.COOKIES)
    print(req.headers)
    token = req.COOKIES.get('jwt_token')
    print(token)
    token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NDA2NDQyODh9.Luw4Pq04Vh380smMsfhP1-6GWhaUD5mvRbmN-EKUJ9Y"
    if token:
        user = get_user_from_token(token)
        user = User.objects.get(id=user)
        print(user)
        if user:
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
    return_to = req.build_absolute_uri(reverse('index'))

    return HttpResponseRedirect(f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}")

def login_handler(req):
    print('login handler')
    return JsonResponse({
        'message': 'Login successful'
    })