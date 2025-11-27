#!/usr/bin/env python3
"""
Debug script to test order status updates
"""

from app import app, db, Order, User, Restaurant
from flask import url_for

def debug_order_status():
    """Debug order status update functionality"""
    with app.app_context():
        # Get all orders
        orders = Order.query.all()
        
        print(f"Found {len(orders)} orders")
        print("-" * 50)
        
        for order in orders:
            print(f"Order ID: {order.id}")
            print(f"Current Status: {order.status}")
            print(f"Restaurant ID: {order.restaurant_id}")
            print(f"User ID: {order.user_id}")
            print(f"Total Amount: ${order.total_amount}")
            print("-" * 30)
        
        # Test status update
        if orders:
            test_order = orders[0]
            print(f"\nTesting status update for Order #{test_order.id}")
            print(f"Current status: {test_order.status}")
            
            # Try updating to different statuses
            test_statuses = ['pending', 'confirmed', 'preparing', 'dispatched', 'delivered']
            
            for status in test_statuses:
                print(f"Updating to: {status}")
                test_order.status = status
                db.session.commit()
                
                # Verify the update
                updated_order = Order.query.get(test_order.id)
                print(f"Updated status: {updated_order.status}")
                print(f"Success: {updated_order.status == status}")
                print("-" * 20)

if __name__ == '__main__':
    debug_order_status()

