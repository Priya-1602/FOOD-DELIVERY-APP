#!/usr/bin/env python3
"""
Script to check image paths in database and verify if images exist
"""

import os
from app import app, db, MenuItem

def check_images():
    """Check image paths in database and verify if images exist"""
    with app.app_context():
        # Get all menu items
        menu_items = MenuItem.query.all()
        
        print(f"Found {len(menu_items)} menu items")
        print("-" * 50)
        
        for item in menu_items:
            print(f"Item: {item.name}")
            print(f"Image path: {item.image}")
            
            if item.image:
                # Check if image file exists
                full_path = os.path.join('static', item.image)
                if os.path.exists(full_path):
                    print(f"✓ Image exists: {full_path}")
                else:
                    print(f"✗ Image missing: {full_path}")
            else:
                print("✗ No image path in database")
            
            print("-" * 30)

if __name__ == '__main__':
    check_images()

