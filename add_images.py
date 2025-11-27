owner@pizzar@ging but when i click disptached  i click prepapring ns no#!/usr/bin/env python3
"""
Script to automatically add sample images for food items
"""

import os
import requests
from app import app, db, MenuItem
from PIL import Image
import io

# Sample food images from Unsplash (free stock photos)
FOOD_IMAGES = {
    'pizza': [
        'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop'
    ],
    'pasta': [
        'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1556761223-4c4282c73f77?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=400&h=300&fit=crop'
    ],
    'salad': [
        'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop'
    ],
    'beverage': [
        'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1546173159-315724a31696?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1546173159-315724a31696?w=400&h=300&fit=crop'
    ],
    'dessert': [
        'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop'
    ]
}

def download_image(url, filename):
    """Download image from URL and save to uploads folder"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Open and resize image
        img = Image.open(io.BytesIO(response.content))
        img = img.resize((400, 300), Image.Resampling.LANCZOS)
        
        # Save image
        file_path = os.path.join('static', 'uploads', filename)
        img.save(file_path, 'JPEG', quality=85)
        
        return f"uploads/{filename}"
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def add_images_to_menu_items():
    """Add sample images to menu items"""
    with app.app_context():
        # Get all menu items
        menu_items = MenuItem.query.all()
        
        print(f"Found {len(menu_items)} menu items")
        
        for i, item in enumerate(menu_items):
            # Skip if item already has an image
            if item.image:
                print(f"Skipping {item.name} - already has image: {item.image}")
                continue
                
            # Determine category type
            category_type = 'pizza'  # default
            if 'pasta' in item.name.lower() or 'spaghetti' in item.name.lower() or 'fettuccine' in item.name.lower():
                category_type = 'pasta'
            elif 'salad' in item.name.lower():
                category_type = 'salad'
            elif 'drink' in item.name.lower() or 'lemonade' in item.name.lower() or 'tea' in item.name.lower():
                category_type = 'beverage'
            elif 'cake' in item.name.lower() or 'tiramisu' in item.name.lower() or 'cheesecake' in item.name.lower():
                category_type = 'dessert'
            elif 'pizza' in item.name.lower():
                category_type = 'pizza'
            
            # Get image URL
            image_urls = FOOD_IMAGES.get(category_type, FOOD_IMAGES['pizza'])
            image_url = image_urls[i % len(image_urls)]
            
            # Generate filename
            filename = f"{category_type}_{i+1}.jpg"
            
            # Download and save image
            image_path = download_image(image_url, filename)
            
            if image_path:
                # Update menu item with image path
                item.image = image_path
                print(f"Added image to {item.name}: {image_path}")
            else:
                print(f"Failed to add image to {item.name}")
        
        # Commit changes
        db.session.commit()
        print("All images have been added to menu items!")

if __name__ == '__main__':
    print("Adding sample images to menu items...")
    add_images_to_menu_items() 