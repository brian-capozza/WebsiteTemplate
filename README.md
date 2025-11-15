# WebsiteTemplate
# 🛒 Django Ecommerce Platform

A full-featured ecommerce web application built with Django, featuring secure payment processing, user authentication, and an intuitive admin interface for product management.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.0+-green.svg)
![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)
![Stripe](https://img.shields.io/badge/payments-Stripe-blueviolet.svg)

## 🌟 Features

### Customer-Facing
- **Product Catalog**: Browse products with detailed descriptions, images, and pricing
- **Shopping Cart**: Add, remove, and update quantities with real-time total calculations
- **Secure Checkout**: PCI-compliant payment processing via Stripe API
- **User Authentication**: Secure registration, login, and profile management
- **Order History**: Track past purchases and order status
- **Responsive Design**: Mobile-friendly interface with HTML/CSS

### Admin Features
- **Product Management**: Intuitive Django admin interface for CRUD operations
- **Order Processing**: View and manage customer orders
- **Inventory Tracking**: Monitor stock levels and product availability
- **User Management**: Admin controls for customer accounts

## 🚀 Tech Stack

**Backend:**
- Python 3.8+
- Django 4.0+
- Django REST Framework (for API endpoints)
- SQLAlchemy (ORM)

**Frontend:**
- HTML5/CSS3
- JavaScript (vanilla)
- Responsive design principles

**Database:**
- SQLite (development)
- Easy migration path to PostgreSQL for production

**Payment Processing:**
- Stripe API integration
- Secure, encrypted transactions

## 📸 Screenshots

*[Add screenshots here showing:]*
- *Homepage/product listing*
- *Product detail page*
- *Shopping cart*
- *Checkout process*
- *Admin dashboard*

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Stripe account (for payment processing)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/brian-capozza/ecommerce-website.git
cd ecommerce-website
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
SECRET_KEY=your_django_secret_key
DEBUG=True
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py loaddata sample_products.json
```

8. **Run development server**
```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```
ecommerce-website/
├── ecommerce/              # Main project directory
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── store/                  # Store app
│   ├── models.py          # Product, Order, Cart models
│   ├── views.py           # View logic
│   ├── urls.py            # Store URLs
│   └── templates/         # HTML templates
├── users/                  # User authentication app
│   ├── models.py          # User profile models
│   ├── views.py           # Auth views
│   └── forms.py           # Registration/login forms
├── static/                 # CSS, JS, images
├── media/                  # User-uploaded content
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🔑 Key Features Explained

### Stripe Payment Integration
```python
# Secure checkout with Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
intent = stripe.PaymentIntent.create(
    amount=calculate_order_amount(items),
    currency='usd',
    metadata={'order_id': order.id}
)
```

### User Authentication
- Custom user model extending Django's AbstractUser
- Secure password hashing with Django's built-in authentication
- Session management for persistent login

### Product Management
- Django admin integration for easy CRUD operations
- Image upload and storage
- Category-based organization
- Inventory tracking

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run tests with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## 🚧 Roadmap

Future enhancements planned:

- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced search and filtering
- [ ] Email notifications for orders
- [ ] Coupon/discount code system
- [ ] Multiple payment gateway options
- [ ] Product recommendations
- [ ] Admin analytics dashboard

## 🔐 Security Features

- CSRF protection on all forms
- SQL injection prevention via Django ORM
- XSS protection with Django template escaping
- Secure password storage with PBKDF2
- PCI-compliant payment processing (Stripe handles card data)
- Environment variable management for sensitive keys

## 📝 Usage Notes

### Test Mode
The application uses Stripe's test mode by default. Use these test card numbers:
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Use any future expiration date and any 3-digit CVC

### Admin Access
Access the Django admin panel at `/admin/` with your superuser credentials.

## 🤝 Contributing

This is a personal portfolio project, but feedback and suggestions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Brian Capozza**
- Email: bc@bcapozza.com
- LinkedIn: [linkedin.com/in/brian-capozza](https://linkedin.com/in/brian-capozza)
- GitHub: [github.com/brian-capozza](https://github.com/brian-capozza)

## 🙏 Acknowledgments

- Django documentation and community
- Stripe API documentation
- Inspiration from modern ecommerce platforms

---

**Note**: This project was built as a learning exercise and portfolio piece. For production deployment, additional security hardening, monitoring, and infrastructure considerations are recommended.
---

*Built with ☕ and Django
