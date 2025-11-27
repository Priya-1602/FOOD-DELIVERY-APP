from app import app, db, MenuItem

def fix_image_assignments():
    with app.app_context():
        items = MenuItem.query.all()
        
        for item in items:
            if 'pizza' in item.name.lower():
                if 'Margherita' in item.name:
                    item.image = 'uploads/pizza_2.jpg'
                elif 'Vegetarian' in item.name:
                    item.image = 'uploads/pizza_3.jpg'
                elif 'BBQ' in item.name:
                    item.image = 'uploads/pizza_4.jpg'
                else:
                    item.image = 'uploads/pizza_7.jpg'
            elif any(word in item.name.lower() for word in ['spaghetti', 'fettuccine', 'penne']):
                if 'Carbonara' in item.name:
                    item.image = 'uploads/pasta_5.jpg'
                elif 'Alfredo' in item.name:
                    item.image = 'uploads/pasta_6.jpg'
                else:
                    item.image = 'uploads/pizza_7.jpg'
            elif 'salad' in item.name.lower():
                if 'Caesar' in item.name:
                    item.image = 'uploads/salad_8.jpg'
                elif 'Greek' in item.name:
                    item.image = 'uploads/salad_9.jpg'
                else:
                    item.image = 'uploads/salad_10.jpg'
            elif any(word in item.name.lower() for word in ['drinks', 'lemonade', 'tea']):
                if 'Soft' in item.name:
                    item.image = 'uploads/beverage_11.jpg'
                elif 'Lemonade' in item.name:
                    item.image = 'uploads/beverage_12.jpg'
                else:
                    item.image = 'uploads/beverage_13.jpg'
            elif any(word in item.name.lower() for word in ['tiramisu', 'cheesecake']):
                if 'Tiramisu' in item.name:
                    item.image = 'uploads/dessert_14.jpg'
                else:
                    item.image = 'uploads/dessert_16.jpg'
        
        db.session.commit()
        print("Images reassigned successfully!")
        
        # Print the assignments
        for item in items:
            print(f"{item.name}: {item.image}")

if __name__ == "__main__":
    fix_image_assignments() 