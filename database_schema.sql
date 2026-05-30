-- SQL Schema for Recipe Website
-- This file shows the table structure for reference
-- Note: Django ORM will handle table creation through migrations

-- Recipes Table (already exists)
-- CREATE TABLE IF NOT EXISTS recipes (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT NOT NULL,
--     cuisine VARCHAR(50) NOT NULL,
--     subcuisine VARCHAR(50) NOT NULL,
--     title VARCHAR(100) NOT NULL,
--     region VARCHAR(100),
--     description TEXT,
--     photo VARCHAR(255),
--     video VARCHAR(255),
--     ingredients TEXT NOT NULL,
--     instructions TEXT NOT NULL,
--     created_at DATETIME NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES user_reg(id) ON DELETE CASCADE
-- );

-- Likes Table (new table for like system)
CREATE TABLE IF NOT EXISTS likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL,
    user_id INT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_reg(id) ON DELETE CASCADE,
    UNIQUE KEY unique_recipe_user (recipe_id, user_id)
);

-- Index for faster queries
CREATE INDEX idx_recipe_id ON likes(recipe_id);
CREATE INDEX idx_user_id ON likes(user_id);

