# Recipe Website - Like System & Subcuisine Filter Setup

## Features Implemented

✅ **Like Button System**
- Each recipe card has a "❤️ Like" button with dynamic like count
- Like count updates instantly without page reload using AJAX
- Users can like/unlike recipes (requires login)
- Like data stored in `likes` table

✅ **View and Share Buttons**
- View button for each recipe (placeholder - can be extended)
- Share button with native Web Share API support
- Fallback to clipboard copy if Web Share API not available

✅ **Subcuisine Filter**
- Dropdown filter to show recipes by subcuisine
- Filter updates URL and shows filtered results
- Clear filter option available

✅ **Recipe Listing Page**
- Beautiful grid layout with recipe cards
- Shows recipe image, title, subcuisine, description
- Displays author and creation date
- Responsive design

## Database Changes

### New Model: Like
- `id`: Primary key
- `recipe_id`: Foreign key to Recipe
- `user_id`: Foreign key to User (optional, can be null for anonymous likes)
- `created_at`: Timestamp
- Unique constraint on (recipe_id, user_id) to prevent duplicate likes

## Setup Instructions

### 1. Create and Run Migrations

```bash
cd foodsite
python manage.py makemigrations
python manage.py migrate
```

This will create the `likes` table in your MySQL database.

### 2. Access the Recipe List Page

Navigate to: `http://localhost:8000/recipes/`

### 3. Features Usage

**Like a Recipe:**
- Click the "❤️ Like" button on any recipe card
- The like count updates instantly
- Button changes to "Liked" state when active
- Requires user to be logged in

**Filter by Subcuisine:**
- Use the dropdown at the top of the recipe list page
- Select a subcuisine to filter recipes
- Click "Clear Filter" to show all recipes

**Share Recipe:**
- Click the "Share" button on any recipe card
- Uses native Web Share API if available
- Falls back to clipboard copy

## API Endpoints

- `GET /recipes/` - Recipe listing page with filter
- `POST /recipes/<recipe_id>/toggle-like/` - Toggle like status (AJAX)
- `GET /recipes/<recipe_id>/like-count/` - Get like count (AJAX)

## Files Modified/Created

### Models
- `foodsite/foodsite/models.py` - Added Like model and helper methods

### Views
- `foodsite/foodsite/views.py` - Added:
  - `recipe_list()` - Display recipes with filter
  - `toggle_like()` - AJAX endpoint for liking/unliking
  - `get_like_count()` - AJAX endpoint for like count

### Templates
- `foodsite/foodsite/templates/recipe_list.html` - New recipe listing page

### URLs
- `foodsite/foodsite/urls.py` - Added recipe listing and like endpoints

### SQL Reference
- `foodsite/database_schema.sql` - SQL schema reference (Django handles migrations)

## Notes

- The like system requires users to be logged in
- Anonymous users can view recipes but cannot like them
- The unique constraint prevents users from liking the same recipe twice
- Like counts are calculated dynamically using Django ORM
- All AJAX requests include CSRF token for security

## Testing

1. Create some recipes with different subcuisines
2. Login as a user
3. Navigate to `/recipes/`
4. Test the like button - count should update instantly
5. Test the subcuisine filter - should show only matching recipes
6. Test the share button - should copy link or use native share

