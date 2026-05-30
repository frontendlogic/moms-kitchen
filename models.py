from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# ------------------ Custom User ------------------
class User(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash password before saving
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'user_reg'

# ------------------ Recipe Model ------------------
#UserModel = get_user_model()  # get the current user model

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.CharField(max_length=50)
    subcuisine = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='recipe_photos/', blank=True, null=True)
    video = models.FileField(upload_to='recipe_videos/', blank=True, null=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reward_awarded = models.BooleanField(default=False)
    reward_awarded_at = models.DateTimeField(blank=True, null=True)
    reward_claimed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_like_count(self):
        """Get total likes for this recipe"""
        return self.likes.count()
    
    def is_liked_by_user(self, user_id):
        """Check if recipe is liked by a specific user"""
        if not user_id:
            return False
        return self.likes.filter(user_id=user_id).exists()

# ------------------ Like Model ------------------
class Like(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')  # Prevent duplicate likes from same user
        db_table = 'likes'

    def __str__(self):
        return f"Like for {self.recipe.title}"


class RewardClaim(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name='reward_claim')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=150)
    bank_name = models.CharField(max_length=120)
    account_number = models.CharField(max_length=34)
    ifsc_code = models.CharField(max_length=20)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reward_claims'

    def __str__(self):
        return f"Reward claim for {self.recipe.title}"