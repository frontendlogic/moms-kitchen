from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import messages  # easily show one-time notifications (success, error, info, warning)
from .models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Recipe, Like, RewardClaim
from .forms import RecipeForm, RewardClaimForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import User, Recipe
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import json




def index(request):
    # Get latest recipes for homepage
    recipes = Recipe.objects.all().order_by('-created_at')[:6]  # Show latest 6 recipes
    
    # Get recipes grouped by cuisine for Featured Cuisines modal
    cuisines_data = {}
    main_cuisines = ['Indian', 'Korean', 'Japanese', 'Chinese', 'Thai', 'Italian']
    user_id = request.session.get('user_id')
    
    for cuisine in main_cuisines:
        cuisine_recipes = Recipe.objects.filter(cuisine=cuisine).order_by('-created_at')
        # Group by subcuisine
        subcuisines_dict = {}
        for recipe in cuisine_recipes:
            subcuisine = recipe.subcuisine
            if subcuisine not in subcuisines_dict:
                subcuisines_dict[subcuisine] = []
            # Add like count and liked status
            recipe.like_count = recipe.get_like_count()
            recipe.is_liked = recipe.is_liked_by_user(user_id) if user_id else False
            subcuisines_dict[subcuisine].append(recipe)
        cuisines_data[cuisine] = subcuisines_dict
    
    # Convert to JSON-serializable format for JavaScript
    cuisines_json = {}
    for cuisine, subcuisines in cuisines_data.items():
        cuisines_json[cuisine] = {}
        for subcuisine, recipes_list in subcuisines.items():
            cuisines_json[cuisine][subcuisine] = []
            for recipe in recipes_list:
                recipe_data = {
                    'id': recipe.id,
                    'title': recipe.title,
                    'description': recipe.description or '',
                    'photo': recipe.photo.url if recipe.photo else None,
                    'video': recipe.video.url if recipe.video else None,
                    'subcuisine': recipe.subcuisine,
                    'user': recipe.user.user_name,
                    'created_at': recipe.created_at.strftime('%b %d, %Y'),
                    'like_count': recipe.like_count,
                    'is_liked': recipe.is_liked
                }
                cuisines_json[cuisine][subcuisine].append(recipe_data)
    
    # Ensure we always have a valid JSON string, even if empty
    try:
        cuisines_json_str = json.dumps(cuisines_json, ensure_ascii=False)
    except Exception as e:
        print(f"Error creating JSON: {e}")
        cuisines_json_str = '{}'
    
    # Get user_name if logged in
    user_name = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user_name = user.user_name
        except User.DoesNotExist:
            pass
    
    context = {
        'recipes': recipes,
        'cuisines_data': cuisines_data,
        'cuisines_json': cuisines_json_str,
        'main_cuisines': main_cuisines,
        'user_id': user_id,
        'user_name': user_name,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
   return render(request, 'upload.html')

def ai_recipe_page(request):  
    return render(request, 'ai_recipe_page.html')


def ai_recipe(request):
    return render(request, 'ai_recipe.html')

def feedback(request):  
    return render(request, 'feedback.html')


def cuisines(request):  
    return render(request, 'cuisines.html')


def registration(request):
    return render(request, 'registration.html')


def login(request):
     return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Login successful ✅")
            return redirect('index')
        messages.error(request, "Invalid username or password ❌")
    return render(request, 'login.html')



def login_form(request):
    return render(request, 'registration.html')



# def user_dashboard(request):
#     return render(request, 'user_dashboard.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')

#---------------Sub-Cuisines----

def Indian(request):
    return render(request, 'Indian.html')

def korean_c(request):
    return render(request, 'korean_c.html')

def Japanese(request):
    return render(request, 'Japanese.html')

def Chinese(request):
    return render(request, 'Chinese.html')

def Thai(request):
    return render(request, 'Thai.html')

def Italian(request):
    return render(request, 'Italian.html')

#----------------Login_reg --------(rm foodsite/migrations/00*.py   # except __init__.py) Django writes a new file there:
#0001_initial.py, 0002_alter_user_table.py … etc.


# ------------------ Registration ------------------
def login_form(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_name and email and password:
            User.objects.create(
                user_name=user_name,
                email=email,
                password=password
            )
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')

        messages.error(request, "Please fill all fields.")
        return render(request, 'registration.html')

    return render(request, 'registration.html')


from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return render(request, 'login.html')

        # compare raw password with hashed password
        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name
            messages.success(request, f"Welcome back, {user.user_name}!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Incorrect password.")
            return render(request, 'login.html')

    return render(request, 'login.html')



# ------------------ User Dashboard ------------------
def user_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please sign in to continue.")
        return redirect('login_view')

    try:
        user = User.objects.get(id=user_id)
        recipes = Recipe.objects.filter(user=user).order_by('-created_at')
        reward_pending_recipes = recipes.filter(reward_awarded=True, reward_claimed=False)
        reward_pending_recipe = reward_pending_recipes.first()

        context = {
            'user': user,
            'recipes': recipes,
            'reward_pending_recipe': reward_pending_recipe,
        }
        return render(request, 'user_dashboard.html', context)
    except User.DoesNotExist:
        messages.error(request, "We couldn't find that user account.")
        return redirect('login_view')


def reward_claim_view(request, recipe_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please sign in to continue.")
        return redirect('login_view')

    recipe = get_object_or_404(Recipe, id=recipe_id, user_id=user_id)

    if not recipe.reward_awarded:
        messages.error(request, "This recipe has not unlocked a reward yet.")
        return redirect('user_dashboard')

    if recipe.reward_claimed or hasattr(recipe, 'reward_claim'):
        messages.info(request, "Reward details have already been submitted for this recipe.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = RewardClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.recipe = recipe
            claim.user_id = user_id
            claim.save()
            recipe.reward_claimed = True
            recipe.save(update_fields=['reward_claimed'])
            messages.success(request, "Thank you! Your reward details have been submitted successfully.")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please correct the highlighted errors and try again.")
    else:
        form = RewardClaimForm(initial={
            'account_holder_name': recipe.user.user_name,
            'contact_email': recipe.user.email,
        })

    return render(request, 'reward_claim_form.html', {
        'form': form,
        'recipe': recipe,
    })

# ------------------ Recipe Upload ------------------

def upload_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first")
        return redirect('login_view')

    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)

            cuisine = request.POST.get('cuisine')
            subcuisine = request.POST.get('subcuisine')
            title = request.POST.get('title')
            region = request.POST.get('region')
            description = request.POST.get('description')
            photo = request.FILES.get('photo')
            video = request.FILES.get('video')
            ingredients = request.POST.get('ingredients')
            instructions = request.POST.get('instructions')

            # Create recipe
            recipe = Recipe(
                user=user,
                cuisine=cuisine,
                subcuisine=subcuisine,
                title=title,
                region=region,
                description=description,
                photo=photo,
                video=video,
                ingredients=ingredients,
                instructions=instructions
            )
            recipe.save()

            messages.success(request, "Recipe uploaded successfully!")
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f"Error uploading recipe: {e}")
            print("Upload error:", e)

    return render(request, 'upload.html')

# ------------------ Recipe Update ------------------
def update_recipe(request, recipe_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first")
        return redirect('login_view')

    try:
        recipe = Recipe.objects.get(id=recipe_id, user_id=user_id)
    except Recipe.DoesNotExist:
        messages.error(request, "Recipe not found")
        return redirect('user_dashboard')

    if request.method == 'POST':
        try:
            recipe.cuisine = request.POST.get('cuisine')
            recipe.subcuisine = request.POST.get('subcuisine')
            recipe.title = request.POST.get('title')
            recipe.region = request.POST.get('region')
            recipe.description = request.POST.get('description')
            recipe.ingredients = request.POST.get('ingredients')
            recipe.instructions = request.POST.get('instructions')
            
            # Handle file uploads
            if request.FILES.get('photo'):
                recipe.photo = request.FILES.get('photo')
            if request.FILES.get('video'):
                recipe.video = request.FILES.get('video')
            
            recipe.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f"Error updating recipe: {e}")
            print("Update error:", e)

    return render(request, 'update_recipe.html', {'recipe': recipe})

# ------------------ Recipe Delete ------------------
def delete_recipe(request, recipe_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first")
        return redirect('login_view')

    try:
        recipe = Recipe.objects.get(id=recipe_id, user_id=user_id)
        recipe.delete()
        messages.success(request, "Recipe deleted successfully!")
    except Recipe.DoesNotExist:
        messages.error(request, "Recipe not found")
    
    return redirect('user_dashboard')

# ------------------ Logout ------------------
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully!")
    return redirect('index')

# ------------------ Recipe Listing with Subcuisine Filter ------------------
def recipe_list(request):
    """Display all recipes with subcuisine filter"""
    subcuisine_filter = request.GET.get('subcuisine', '')
    recipes = Recipe.objects.all().order_by('-created_at')
    
    # Filter by subcuisine if provided
    if subcuisine_filter:
        recipes = recipes.filter(subcuisine=subcuisine_filter)
    
    # Get all unique subcuisines for the filter dropdown
    subcuisines = Recipe.objects.values_list('subcuisine', flat=True).distinct().order_by('subcuisine')
    
    # Get user_id from session for like status
    user_id = request.session.get('user_id')
    
    # Add like count and liked status to each recipe
    for recipe in recipes:
        recipe.like_count = recipe.get_like_count()
        recipe.is_liked = recipe.is_liked_by_user(user_id) if user_id else False
    
    context = {
        'recipes': recipes,
        'subcuisines': subcuisines,
        'selected_subcuisine': subcuisine_filter,
        'user_id': user_id,
    }
    return render(request, 'recipe_list.html', context)

# ------------------ AJAX Like/Unlike Recipe ------------------
@require_http_methods(["POST"])
def toggle_like(request, recipe_id):
    """Toggle like status for a recipe (AJAX endpoint)"""
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user_id = request.session.get('user_id')
        
        if not user_id:
            return JsonResponse({'success': False, 'message': 'Please login to like recipes', 'like_count': recipe.get_like_count()}, status=401)
        
        user = User.objects.get(id=user_id)
        
        # Check if user already liked this recipe
        try:
            like = Like.objects.get(recipe=recipe, user=user)
            # User already liked, so unlike it
            like.delete()
            is_liked = False
            message = 'Recipe unliked'
        except Like.DoesNotExist:
            # User hasn't liked yet, so like it
            Like.objects.create(recipe=recipe, user=user)
            is_liked = True
            message = 'Recipe liked'
        
        like_count = recipe.get_like_count()

        reward_unlocked = False
        reward_redirect_url = ''
        reward_for_current_user = False

        if (
            is_liked
            and like_count >= 10
            and not recipe.reward_awarded
        ):
            recipe.reward_awarded = True
            recipe.reward_awarded_at = timezone.now()
            recipe.reward_claimed = False
            recipe.save(update_fields=['reward_awarded', 'reward_awarded_at', 'reward_claimed'])

            # Send reward notification email to recipe owner
            recipient_email = recipe.user.email
            if recipient_email:
                try:
                    send_mail(
                        subject="🎉 Congratulations! You've earned a Mom's Kitchen reward",
                        message=(
                            f"Hi {recipe.user.user_name},\n\n"
                            f"Great news! Your recipe \"{recipe.title}\" has reached {like_count} likes.\n"
                            "You've unlocked a special reward. Please log in to your dashboard to submit your bank details so we can process your prize.\n\n"
                            "Warm wishes,\n"
                            "Mom's Kitchen Rewards Team"
                        ),
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'rewards@moms-kitchen.local'),
                        recipient_list=[recipient_email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            reward_unlocked = True
            reward_redirect_url = reverse('reward_claim', args=[recipe.id])
            reward_for_current_user = user_id == recipe.user_id

        return JsonResponse({
            'success': True,
            'message': message,
            'like_count': like_count,
            'is_liked': is_liked,
            'reward_unlocked': reward_unlocked,
            'reward_redirect_url': reward_redirect_url,
            'reward_for_current_user': reward_for_current_user,
            'reward_recipe_title': recipe.title,
        })
        
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# ------------------ Get Like Count (AJAX) ------------------
def get_like_count(request, recipe_id):
    """Get like count for a recipe (AJAX endpoint)"""
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user_id = request.session.get('user_id')
        
        like_count = recipe.get_like_count()
        is_liked = recipe.is_liked_by_user(user_id) if user_id else False
        
        return JsonResponse({
            'success': True,
            'like_count': like_count,
            'is_liked': is_liked
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# ------------------ Recipe Detail View ------------------
def recipe_detail(request, recipe_id):
    """Display full recipe details with photos, video, ingredients, and instructions"""
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user_id = request.session.get('user_id')
        
        # Add like count and liked status
        recipe.like_count = recipe.get_like_count()
        recipe.is_liked = recipe.is_liked_by_user(user_id) if user_id else False
        
        context = {
            'recipe': recipe,
            'user_id': user_id,
        }
        return render(request, 'recipe_detail.html', context)
    except Exception as e:
        messages.error(request, f"Error loading recipe: {e}")
        return redirect('recipe_list')