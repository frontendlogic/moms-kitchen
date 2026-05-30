from .models import User

def user_context(request):
    """Context processor to add user information to all templates"""
    user_id = request.session.get('user_id')
    user_name = None
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user_name = user.user_name
        except User.DoesNotExist:
            pass
    
    return {
        'user_id': user_id,
        'user_name': user_name,
    }

