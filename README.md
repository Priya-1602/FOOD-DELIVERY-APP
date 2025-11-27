# Restaurant Ordering System

A comprehensive full-stack web application for online food ordering, built with Flask, MySQL, and modern frontend technologies.

## 🚀 Features

### For Customers
- **User Registration & Authentication**: Secure login with password validation
- **Menu Browsing**: Browse categorized menus with advanced filters
- **Search & Filter**: Search by name, filter by category, dietary preferences, and price range
- **Shopping Cart**: Add, remove, and update items with real-time total calculation
- **Order Placement**: Complete checkout process with delivery details
- **Order Tracking**: View order history and track order status
- **Email Notifications**: Receive order confirmations and status updates

### For Restaurant Owners
- **Restaurant Dashboard**: Manage menu items and view orders
- **Menu Management**: Add, edit, and delete menu items with categories
- **Order Management**: Update order status and track deliveries
- **Inventory Control**: Mark items as available/unavailable

### For Administrators
- **Admin Dashboard**: Overview of all users, restaurants, and orders
- **User Management**: View and manage user accounts
- **Restaurant Management**: Add and manage restaurant profiles
- **System Analytics**: View statistics and revenue data

## 🛠️ Technology Stack

### Backend
- **Python Flask**: Web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **MySQL**: Relational database
- **Flask-Login**: User authentication and session management
- **bcrypt**: Password hashing and security

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Bootstrap 5
- **JavaScript**: Dynamic interactions and form validation
- **Bootstrap 5**: Responsive design framework
- **Font Awesome**: Icons and visual elements

### Database
- **MySQL**: Primary database
- **SQLAlchemy ORM**: Database abstraction layer

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd restaurant-ordering-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Create MySQL Database
```sql
CREATE DATABASE restaurant_ordering;
CREATE USER 'restaurant_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON restaurant_ordering.* TO 'restaurant_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Update Configuration
Edit `config.py` and update the database connection:
```python
SQLALCHEMY_DATABASE_URI = 'mysql://restaurant_user:your_password@localhost/restaurant_ordering'
```

### 5. Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=mysql://restaurant_user:your_password@localhost/restaurant_ordering
FLASK_ENV=development
FLASK_DEBUG=1
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 6. Initialize Database
```bash
python app.py
```
The database tables will be created automatically when you run the application for the first time.

### 7. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
restaurant-ordering-system/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── menu.html         # Menu browsing
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout process
│   ├── order_history.html # Order history
│   ├── restaurant_dashboard.html # Restaurant management
│   └── admin_dashboard.html # Admin dashboard
└── static/               # Static files (CSS, JS, images)
    ├── css/              # Custom stylesheets
    ├── js/               # JavaScript files
    └── uploads/          # Uploaded images
```

## 🔐 Security Features

- **Password Hashing**: Secure password storage using bcrypt
- **Session Management**: Flask-Login for user sessions
- **Input Validation**: Server-side and client-side validation
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- **CSRF Protection**: Built-in Flask-WTF protection

## 📧 Email Configuration

To enable email notifications, configure your email settings in `config.py`:

```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password in the configuration

## 🧪 Testing

### Manual Testing Checklist

#### User Registration & Login
- [ ] Register new customer account
- [ ] Register new restaurant account
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Password strength validation
- [ ] Email format validation

#### Menu Browsing
- [ ] View all menu items
- [ ] Filter by category
- [ ] Search by item name
- [ ] Filter by dietary preferences
- [ ] Filter by price range
- [ ] Sort items by different criteria

#### Shopping Cart
- [ ] Add items to cart
- [ ] Update item quantities
- [ ] Remove items from cart
- [ ] View cart total
- [ ] Proceed to checkout

#### Order Process
- [ ] Complete checkout process
- [ ] Enter delivery details
- [ ] Select payment method
- [ ] Place order
- [ ] Receive order confirmation

#### Restaurant Dashboard
- [ ] Add new menu items
- [ ] Edit existing items
- [ ] Update order status
- [ ] View order history

#### Admin Dashboard
- [ ] View system statistics
- [ ] Manage users
- [ ] Manage restaurants
- [ ] View all orders

## 🚀 Deployment

### Production Setup

1. **Update Configuration**
   - Change `SECRET_KEY` to a secure random string
   - Update database credentials
   - Configure email settings

2. **Web Server Setup**
   - Use Gunicorn or uWSGI as WSGI server
   - Configure Nginx as reverse proxy
   - Set up SSL certificates

3. **Database Optimization**
   - Create database indexes
   - Configure connection pooling
   - Set up database backups

4. **Security Hardening**
   - Enable HTTPS
   - Set secure headers
   - Configure CORS policies
   - Implement rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the logs for error messages
2. Verify database connection
3. Ensure all dependencies are installed
4. Check email configuration if notifications aren't working

## 🔄 Future Enhancements

- [ ] Real-time order tracking
- [ ] Payment gateway integration
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Push notifications
- [ ] Loyalty program
- [ ] Review and rating system
- [ ] Advanced search with AI
- [ ] Integration with delivery services

## 📊 Database Schema

### Users Table
- id (Primary Key)
- name
- email (Unique)
- phone
- address
- password_hash
- user_type (customer/restaurant/admin)
- created_at

### Restaurants Table
- id (Primary Key)
- name
- contact
- location
- user_id (Foreign Key)

### Categories Table
- id (Primary Key)
- name
- restaurant_id (Foreign Key)

### Menu Items Table
- id (Primary Key)
- name
- description
- price
- image
- is_available
- is_vegetarian
- category_id (Foreign Key)
- restaurant_id (Foreign Key)

### Orders Table
- id (Primary Key)
- user_id (Foreign Key)
- restaurant_id (Foreign Key)
- total_amount
- status
- delivery_address
- created_at

### Order Items Table
- id (Primary Key)
- order_id (Foreign Key)
- menu_item_id (Foreign Key)
- quantity
- price

## 🎯 Use Cases

### Customer Journey
1. **Registration**: Create account with personal details
2. **Login**: Access personalized dashboard
3. **Browse Menu**: Search and filter menu items
4. **Add to Cart**: Select items and quantities
5. **Checkout**: Provide delivery details and payment
6. **Track Order**: Monitor order status and history

### Restaurant Owner Journey
1. **Registration**: Register restaurant with business details
2. **Setup Menu**: Add categories and menu items
3. **Manage Orders**: View and update order status
4. **Monitor Performance**: Track sales and customer feedback

### Administrator Journey
1. **System Overview**: View statistics and system health
2. **User Management**: Monitor and manage user accounts
3. **Restaurant Management**: Add and manage restaurant profiles
4. **Order Monitoring**: Track all system orders and revenue

---

**Note**: This is a demonstration project. For production use, implement additional security measures, error handling, and performance optimizations. 