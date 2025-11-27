#!/usr/bin/env python3
"""
Sample data initialization script for Restaurant Ordering System
Run this script to populate the database with sample data for testing
"""

from app import app, db, User, Restaurant, Category, MenuItem
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_sample_data():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        MenuItem.query.delete()
        Category.query.delete()
        Restaurant.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            name='Admin User',
            email='admin@restaurant.com',
            phone='555-0001',
            address='123 Admin Street, City, State 12345',
            password_hash=generate_password_hash('admin123'),
            user_type='admin'
        )
        db.session.add(admin)
        
        # Create restaurant owner
        print("Creating restaurant owner...")
        restaurant_owner = User(
            name='Pizza Palace Owner',
            email='owner@pizzapalace.com',
            phone='555-0002',
            address='456 Restaurant Ave, City, State 12345',
            password_hash=generate_password_hash('owner123'),
            user_type='restaurant'
        )
        db.session.add(restaurant_owner)
        
        # Create customer users
        print("Creating customer users...")
        customer1 = User(
            name='John Customer',
            email='john@example.com',
            phone='555-0003',
            address='789 Customer Lane, City, State 12345',
            password_hash=generate_password_hash('customer123'),
            user_type='customer'
        )
        db.session.add(customer1)
        
        customer2 = User(
            name='Jane Customer',
            email='jane@example.com',
            phone='555-0004',
            address='321 Customer Drive, City, State 12345',
            password_hash=generate_password_hash('customer123'),
            user_type='customer'
        )
        db.session.add(customer2)
        
        db.session.commit()
        
        # Create restaurant
        print("Creating restaurant...")
        restaurant = Restaurant(
            name='Pizza Palace',
            contact='555-0005',
            location='123 Pizza Street, City, State 12345',
            user_id=restaurant_owner.id
        )
        db.session.add(restaurant)
        db.session.commit()
        
        # Create categories
        print("Creating menu categories...")
        categories = [
            Category(name='Pizza', restaurant_id=restaurant.id),
            Category(name='Pasta', restaurant_id=restaurant.id),
            Category(name='Salads', restaurant_id=restaurant.id),
            Category(name='Beverages', restaurant_id=restaurant.id),
            Category(name='Desserts', restaurant_id=restaurant.id)
        ]
        
        for category in categories:
            db.session.add(category)
        db.session.commit()
        
        # Create menu items
        print("Creating menu items...")
        menu_items = [
            # Pizza items
            MenuItem(
                name='Margherita Pizza',
                description='Classic pizza with tomato sauce, mozzarella cheese, and fresh basil',
                price=12.99,
                is_vegetarian=True,
                category_id=categories[0].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Pepperoni Pizza',
                description='Traditional pizza topped with pepperoni, mozzarella, and tomato sauce',
                price=14.99,
                is_vegetarian=False,
                category_id=categories[0].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Vegetarian Pizza',
                description='Pizza loaded with fresh vegetables including bell peppers, mushrooms, and onions',
                price=13.99,
                is_vegetarian=True,
                category_id=categories[0].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='BBQ Chicken Pizza',
                description='Pizza with BBQ sauce, grilled chicken, red onions, and mozzarella',
                price=16.99,
                is_vegetarian=False,
                category_id=categories[0].id,
                restaurant_id=restaurant.id
            ),
            
            # Pasta items
            MenuItem(
                name='Spaghetti Carbonara',
                description='Classic Italian pasta with eggs, cheese, pancetta, and black pepper',
                price=11.99,
                is_vegetarian=False,
                category_id=categories[1].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Fettuccine Alfredo',
                description='Creamy pasta with parmesan cheese, butter, and garlic',
                price=10.99,
                is_vegetarian=True,
                category_id=categories[1].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Penne Arrabbiata',
                description='Spicy pasta with tomato sauce, garlic, and red chili peppers',
                price=9.99,
                is_vegetarian=True,
                category_id=categories[1].id,
                restaurant_id=restaurant.id
            ),
            
            # Salad items
            MenuItem(
                name='Caesar Salad',
                description='Fresh romaine lettuce with caesar dressing, parmesan cheese, and croutons',
                price=8.99,
                is_vegetarian=False,
                category_id=categories[2].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Greek Salad',
                description='Mixed greens with feta cheese, olives, tomatoes, and cucumber',
                price=9.99,
                is_vegetarian=True,
                category_id=categories[2].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Garden Salad',
                description='Fresh mixed greens with tomatoes, cucumbers, carrots, and house dressing',
                price=7.99,
                is_vegetarian=True,
                category_id=categories[2].id,
                restaurant_id=restaurant.id
            ),
            
            # Beverage items
            MenuItem(
                name='Soft Drinks',
                description='Choice of Coke, Pepsi, Sprite, or Fanta (330ml)',
                price=2.99,
                is_vegetarian=True,
                category_id=categories[3].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Fresh Lemonade',
                description='Homemade lemonade with fresh lemons and mint',
                price=3.99,
                is_vegetarian=True,
                category_id=categories[3].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Iced Tea',
                description='Refreshing iced tea with lemon',
                price=2.99,
                is_vegetarian=True,
                category_id=categories[3].id,
                restaurant_id=restaurant.id
            ),
            
            # Dessert items
            MenuItem(
                name='Tiramisu',
                description='Classic Italian dessert with coffee-flavored ladyfingers and mascarpone cream',
                price=6.99,
                is_vegetarian=True,
                category_id=categories[4].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Chocolate Lava Cake',
                description='Warm chocolate cake with molten center, served with vanilla ice cream',
                price=7.99,
                is_vegetarian=True,
                category_id=categories[4].id,
                restaurant_id=restaurant.id
            ),
            MenuItem(
                name='Cheesecake',
                description='New York style cheesecake with berry compote',
                price=5.99,
                is_vegetarian=True,
                category_id=categories[4].id,
                restaurant_id=restaurant.id
            )
        ]
        
        for item in menu_items:
            db.session.add(item)
        
        db.session.commit()
        
        print("Sample data initialization completed!")
        print("\nSample login credentials:")
        print("Admin: admin@restaurant.com / admin123")
        print("Restaurant Owner: owner@pizzapalace.com / owner123")
        print("Customer: john@example.com / customer123")
        print("Customer: jane@example.com / customer123")

if __name__ == '__main__':
    print("Initializing sample data for Restaurant Ordering System...")
    init_sample_data() 