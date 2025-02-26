from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import jwt
from datetime import datetime, timedelta

@login_required
def auth_callback(request):
    # Generate JWT
    payload = {
        'user_id': request.user.id,
        'exp': datetime.now() + timedelta(days=1)
    }
    token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')
    
    # Redirect to frontend with token
    frontend_url = "http://localhost:5173"  # Your Vite app URL
    response = HttpResponseRedirect(f"{frontend_url}")
    
    # Set JWT as cookie
    response.set_cookie(
        'jwt_token', 
        token,
        httponly=True, 
        secure=True,  # Set True in production
        samesite='Lax'
    )
    
    return response

def get_user_from_token(token):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        user_id = payload.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None