#!/usr/bin/env python3
"""
Test script to verify image serving
"""

import requests
import os
from app import app, db, MenuItem

def test_image_serving():
    """Test if images are being served correctly"""
    with app.app_context():
        # Get all menu items with images
        menu_items = MenuItem.query.filter(MenuItem.image.isnot(None)).all()
        
        print(f"Testing {len(menu_items)} menu items with images...")
        print("-" * 50)
        
        for item in menu_items:
            print(f"Item: {item.name}")
            print(f"Image path: {item.image}")
            
            # Check if file exists
            full_path = os.path.join('static', item.image)
            if os.path.exists(full_path):
                print(f"✓ File exists: {full_path}")
                
                # Test Flask URL generation
                with app.test_client() as client:
                    response = client.get(f'/static/{item.image}')
                    if response.status_code == 200:
                        print(f"✓ Flask serves image correctly: /static/{item.image}")
                    else:
                        print(f"✗ Flask failed to serve image: {response.status_code}")
            else:
                print(f"✗ File missing: {full_path}")
            
            print("-" * 30)

if __name__ == '__main__':
    test_image_serving()

