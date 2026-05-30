"""
URL configuration for foodsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from foodsite import views

urlpatterns = [
        path('admin/', admin.site.urls),

        path('',views.index, name='index'),

        path('about/', views.about, name='about'),

        path('contact/', views.contact, name='contact'),

        path('cuisines/', views.cuisines, name='cuisines'),

        path('ai_recipe/', views.ai_recipe_page, name='ai_recipe_page'),

        path('ai_recipe/', views.ai_recipe, name='ai_recipe'),

        path('feedback/', views.feedback, name='feedback'),

        # User Authentication
        #path('login/', views.login_view, name='login_view'),
        path('login/', views.login_view, name='login'),  # FIXED


        path('registration/', views.login_form, name='registration'),
        path('logout/', views.logout_view, name='logout'),
        path('forgot_password/', views.forgot_password, name='forgot_password'),

        # User Dashboard and Recipe Management
        path('dashboard/', views.user_dashboard, name='user_dashboard'),
        path('upload/', views.upload_view, name='upload'),
        path('update_recipe/<int:recipe_id>/', views.update_recipe, name='update_recipe'),
        path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),

        # Built-in login view
    path('login/', views.login_view, name='login_view'),



    # Your other URLs
    #path('register/', views.register_view, name='register'),

        # Recipe Listing and Like System
        path('recipes/', views.recipe_list, name='recipe_list'),
        path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:recipe_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('rewards/<int:recipe_id>/claim/', views.reward_claim_view, name='reward_claim'),
        path('recipes/<int:recipe_id>/like-count/', views.get_like_count, name='get_like_count'),

    #---------Sub-Cuisines
    path('Indian/', views.Indian, name='Indian'),
    path('korean_c/', views.korean_c, name='korean_c'),
    path('Japanese/', views.Japanese, name='Japanese'),
    path('Chinese/', views.Chinese, name='Chinese'),
    path('Thai/', views.Thai, name='Thai'),
    path('Italian/', views.Italian, name='Italian'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
