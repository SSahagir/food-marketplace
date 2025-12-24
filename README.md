# FoodMarket - Full-Stack Food Delivery Platform

**FoodMarket** is a fully functional, full-stack multi-vendor marketplace application designed to connect Customers, Restaurants, and Delivery Partners in a seamless ecosystem. Built with a robust **Django REST Framework** backend and a reactive **React** frontend, it features real-time order tracking, geolocation services, and a secure role-based authentication system.

## 🚀 Key Features

### 👤 Customer Ecosystem
* **Smart Search & Filtering:** Search globally for dishes or restaurants. Filter menus by Veg 🟢, Non-Veg 🔴, and Egg 🟡.
* **Secure Authentication:** OTP-based registration and password reset via Email (Gmail SMTP).
* **Live Order Tracking:** Real-time status updates (Ordered → Confirmed → Preparing → Ready → Out for Delivery → Delivered).
* **Geolocation:** One-click GPS location sharing for accurate delivery.
* **Interactive Cart:** Add/remove items, view totals, and "Buy Now" options.
* **Review System:** Rate and review dishes after delivery.
* **Order History & Stats:** View total spending and detailed past order logs.

### 👨‍🍳 Restaurant Dashboard
* **Menu Management:** Create, edit, and delete dishes with image uploads and category tagging.
* **Order Lifecycle Management:**
  * **Confirm** incoming orders.
  * Mark orders as **Ready for Pickup** (triggers Delivery Partner dispatch).
* **Customer Insights:** View profiles of ordering customers.
* **Financials:** Track total revenue and order volume.
* **Real-time Chat:** Chat directly with customers regarding specific orders.

### 🚚 Delivery Partner Portal
* **Job Market:** View available orders marked "Ready for Pickup".
* **Job Management:** Accept jobs and update status to "Out for Delivery" and "Delivered".
* **Navigation:** Integrated Google Maps links for Pickup and Drop-off locations.
* **Earning Tracker:** Real-time calculation of earnings based on completed deliveries.

## 🛠️ Tech Stack

### Backend

* **Framework:** Django 5.0 & Django REST Framework (DRF)

* **Authentication:** JWT (JSON Web Tokens) via `simplejwt`

* **Database:** SQLite (Local Dev) / PostgreSQL (Production on Railway)

* **Utilities:** `django-filter` (Advanced Search), `python-dotenv` (Security), `Pillow` (Image Processing)

### Frontend

* **Library:** React 18 (Embedded Hybrid Architecture)

* **Styling:** Tailwind CSS (CDN)

* **Icons:** Lucide React / Custom CSS

* **State Management:** React Hooks (`useState`, `useEffect`)

### DevOps & Deployment

* **Platform:** Vercel (Serverless Function)

* **Database Hosting:** Railway / Neon (PostgreSQL)

* **Static Files:** WhiteNoise

## ⚙️ Installation & Local Setup

Follow these steps to get the project running on your local machine.

### Prerequisites

* Python 3.9+

* Git

### 1. Clone the Repository

```
git clone https://github.com/SSahagir/food-marketplace/
cd food-marketplace

```

### 2. Create Virtual Environment

```
python -m venv env
# Windows
.\\env\\Scripts\\activate
# Mac/Linux
source env/bin/activate

```

### 3. Install Dependencies

```
pip install -r requirements.txt

```

### 4. Environment Configuration

Create a `.env` file in the root directory and add the following secrets:

```
# General Settings
SECRET_KEY=your-secure-random-key-here
DEBUG=True

# Database (Leave empty to use local SQLite)
# DATABASE_URL=postgresql://user:pass@host:port/dbname

# Email Settings (Required for OTP)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.gmail.com

```

### 5. Database Setup

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # Optional: To access Django Admin

```

### 6. Run the Server

```
python manage.py runserver

```

Visit `http://127.0.0.1:8000/` to verify the application.

## ☁️ Deployment Guide (Vercel)

This project is configured for seamless deployment on Vercel with an external PostgreSQL database.

1. **Push to GitHub:** Ensure your code is pushed to your repository.

2. **Database:** Create a PostgreSQL database on [Railway](https://railway.app) or [Neon](https://neon.tech) and copy the `Connection URL`.

3. **Vercel Project:**

   * Import repository on Vercel.

   * **Framework Preset:** Django (or Other).

   * **Root Directory:** `./`

4. **Environment Variables (Vercel):**
   Add the following in the Vercel dashboard:

   * `DATABASE_PUBLIC_URL` (or `DATABASE_URL`): Your PostgreSQL connection string.

   * `SECRET_KEY`: Your production secret key.

   * `DEBUG`: `False`.

   * `EMAIL_HOST_USER`: Your Gmail address.

   * `EMAIL_HOST_PASSWORD`: Your App Password.

5. **Deploy:** Click Deploy. Vercel will build the app using the `vercel.json` configuration.

## 📂 Project Structure

```
food_marketplace/
├── food_marketplace/      # Core Django Settings & WSGI
├── users/                 # Custom User Model, Auth, OTP, Profiles
├── restaurants/           # Restaurant Profiles & Logic
├── menu/                  # Dishes, Categories, Search Logic
├── orders/                # Order State Machine, Chat, Tracking
├── reviews/               # Rating System
├── templates/             # React Frontend Entry Point (index.html)
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
└── vercel.json            # Deployment Config

```