# FreshShop - E-commerce Functionality Implementation

FreshShop is a Django-based e-commerce platform designed to showcase products, manage user carts, and facilitate order placement. This project implements essential e-commerce features using Django best practices.

## Features
1. Product listing with pagination.
2. Add-to-cart functionality with quantity management.
3. Multi-user support with separate carts.
4. Checkout page with order placement.
5. Integrated and responsive HTML templates.

---

## Prerequisites
Ensure the following are installed on your system:
- Python 3.x
- Django 4.x
- Pip (Python package manager)

---

## Setup Instructions

# Step 1: Clone the Repository
git clone git@github.com:<your-username>/FreshShop.git
cd FreshShop

# Step 2: Set Up a Virtual Environment
python -m venv env
source env/bin/activate   # For Linux/macOS
env\Scripts\activate      # For Windows

# Step 3: Install Dependencies
pip install -r requirements.txt

# Step 4: Configure the Database
# Note: Make sure your database settings in settings.py are configured as needed.
python manage.py makemigrations
python manage.py migrate

# Step 5: Create a Superuser
python manage.py createsuperuser

# Step 6: Run the Server
python manage.py runserver

# Access the application
# Visit http://127.0.0.1:8000/ to see the site in action

