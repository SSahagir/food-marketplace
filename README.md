# Food Marketplace

A full-stack food delivery application built with Django (Backend) and React (Embedded Frontend).

## Features
- **Roles:** Customer, Restaurant, Delivery Partner.
- **Order Flow:** Place Order -> Restaurant Confirm -> Ready for Pickup -> Delivery.
- **Live Tracking:** GPS Location sharing and Status updates.
- **Security:** OTP Registration and Password Reset.

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd food-marketplace
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Create a file named `.env` in the root folder.
   - Copy the contents from `.env.example` into `.env`.
   - Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` with your credentials.

4. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Server**
   ```bash
   python manage.py runserver
   ```
   Access the app at http://127.0.0.1:8000/