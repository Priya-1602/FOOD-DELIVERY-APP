from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import bcrypt
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), default='customer') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    location = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categories = db.relationship('Category', backref='restaurant', lazy=True)
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    menu_items = db.relationship('MenuItem', backref='category', lazy=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    is_vegetarian = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, dispatched, delivered
    delivery_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    restaurant = db.relationship('Restaurant', backref='orders', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    """Save uploaded image and return filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Return relative path for database storage
        return f"uploads/{unique_filename}"
    return None

def send_email(to_email, subject, body):
    """Send email notification"""
    try:
        # Check if email configuration is available
        if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
            print("Email configuration not set up. Skipping email send.")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        text = msg.as_string()
        server.sendmail(app.config['MAIL_USERNAME'], to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)
        user = User(name=name, email=email, phone=phone, address=address, 
                   password_hash=password_hash, user_type=user_type)
        
        db.session.add(user)
        db.session.commit()
        
        # If user is a restaurant owner, create a restaurant profile
        if user_type == 'restaurant':
            restaurant = Restaurant(
                name=f"{name}'s Restaurant",
                contact=phone,
                location=address,
                user_id=user.id
            )
            db.session.add(restaurant)
            db.session.commit()
            
            # Create default categories for the restaurant
            default_categories = ['Pizza', 'Pasta', 'Salads', 'Beverages', 'Desserts']
            for category_name in default_categories:
                category = Category(name=category_name, restaurant_id=restaurant.id)
                db.session.add(category)
            db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            
            if user.user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.user_type == 'restaurant':
                return redirect(url_for('restaurant_dashboard'))
            else:
                return redirect(url_for('menu'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/menu')
def menu():
    categories = Category.query.all()
    items = MenuItem.query.filter_by(is_available=True).all()
    return render_template('menu.html', categories=categories, items=items)

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if item_id in session['cart']:
        session['cart'][item_id] += quantity
    else:
        session['cart'][item_id] = quantity
    
    session.modified = True
    flash('Item added to cart!', 'success')
    return redirect(url_for('menu'))

@app.route('/cart')
@login_required
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', items=[], total=0)
    
    cart_items = []
    total = 0
    
    for item_id, quantity in session['cart'].items():
        item = MenuItem.query.get(item_id)
        if item:
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'subtotal': item.price * quantity
            })
            total += item.price * quantity
    
    return render_template('cart.html', items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        session['cart'].pop(item_id, None)
    else:
        session['cart'][item_id] = quantity
    
    session.modified = True
    flash('Cart updated!', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('menu'))
    
    if request.method == 'POST':
        delivery_address = request.form['delivery_address']
        
        # Create order
        total = 0
        restaurant_id = None
        
        for item_id, quantity in session['cart'].items():
            item = MenuItem.query.get(item_id)
            if item:
                total += item.price * quantity
                restaurant_id = item.restaurant_id
        
        order = Order(user_id=current_user.id, restaurant_id=restaurant_id,
                     total_amount=total, delivery_address=delivery_address)
        db.session.add(order)
        db.session.commit()
        
        # Create order items
        for item_id, quantity in session['cart'].items():
            item = MenuItem.query.get(item_id)
            if item:
                order_item = OrderItem(order_id=order.id, menu_item_id=item_id,
                                     quantity=quantity, price=item.price)
                db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        # Send confirmation email
        send_email(current_user.email, 'Order Confirmation', 
                  f'Your order #{order.id} has been placed successfully!')
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_history'))
    
    cart_items = []
    total = 0
    
    for item_id, quantity in session['cart'].items():
        item = MenuItem.query.get(item_id)
        if item:
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'subtotal': item.price * quantity
            })
            total += item.price * quantity
    
    return render_template('checkout.html', items=cart_items, total=total)

@app.route('/order_history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order_history.html', orders=orders)

@app.route('/order_details/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    order_data = {
        'id': order.id,
        'created_at': order.created_at.strftime('%B %d, %Y at %I:%M %p'),
        'status': order.status,
        'total_amount': order.total_amount,
        'delivery_address': order.delivery_address,
        'restaurant_name': order.restaurant.name,
        'items': []
    }
    
    for item in order.order_items:
        order_data['items'].append({
            'name': item.menu_item.name,
            'quantity': item.quantity,
            'price': item.menu_item.price,
            'total': item.quantity * item.menu_item.price
        })
    
    return jsonify(order_data)

@app.route('/restaurant_dashboard')
@login_required
def restaurant_dashboard():
    if current_user.user_type != 'restaurant':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    restaurant = Restaurant.query.filter_by(user_id=current_user.id).first()
    if not restaurant:
        flash('Restaurant profile not found!', 'error')
        return redirect(url_for('index'))
    
    categories = Category.query.filter_by(restaurant_id=restaurant.id).all()
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    orders = Order.query.filter_by(restaurant_id=restaurant.id).order_by(Order.created_at.desc()).all()
    
    return render_template('restaurant_dashboard.html', 
                         restaurant=restaurant, categories=categories, 
                         menu_items=menu_items, orders=orders)

@app.route('/add_menu_item', methods=['POST'])
@login_required
def add_menu_item():
    if current_user.user_type != 'restaurant':
        return jsonify({'error': 'Access denied'}), 403
    
    restaurant = Restaurant.query.filter_by(user_id=current_user.id).first()
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    category_id = int(request.form['category_id'])
    is_vegetarian = request.form.get('is_vegetarian') == 'on'
    
    # Handle image upload
    image_path = None
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file and image_file.filename:
            image_path = save_image(image_file)
    
    menu_item = MenuItem(name=name, description=description, price=price,
                        category_id=category_id, restaurant_id=restaurant.id,
                        is_vegetarian=is_vegetarian, image=image_path)
    
    db.session.add(menu_item)
    db.session.commit()
    
    flash('Menu item added successfully!', 'success')
    return redirect(url_for('restaurant_dashboard'))

@app.route('/update_order_status', methods=['POST'])
@login_required
def update_order_status():
    if current_user.user_type != 'restaurant':
        return jsonify({'error': 'Access denied'}), 403
    
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    
    print(f"DEBUG: Updating order {order_id} to status {status}")  # Debug line
    
    if not order_id or not status:
        flash('Missing order ID or status!', 'error')
        return redirect(url_for('restaurant_dashboard'))
    
    order = Order.query.get(order_id)
    if order:
        print(f"DEBUG: Found order {order.id}, current status: {order.status}")  # Debug line
        order.status = status
        db.session.commit()
        print(f"DEBUG: Updated order {order.id} to status: {order.status}")  # Debug line
        
        # Send email notification
        send_email(order.user.email, f'Order #{order.id} Status Update', 
                  f'Your order status has been updated to: {status}')
        
        flash('Order status updated!', 'success')
    else:
        print(f"DEBUG: Order {order_id} not found!")  # Debug line
        flash('Order not found!', 'error')
    
    return redirect(url_for('restaurant_dashboard'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.user_type != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    restaurants = Restaurant.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    
    return render_template('admin_dashboard.html', users=users, 
                         restaurants=restaurants, orders=orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 