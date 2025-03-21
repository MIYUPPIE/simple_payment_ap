# Django Payment Gateway API

A Django REST API for handling payment processing with email notifications and PDF receipt generation.

## Features

- Payment processing with multiple status handling (complete, return, cancel)
- Automatic PDF receipt generation
- Email notifications for payment events
- Swagger API documentation
- Admin interface for payment management

## Prerequisites

- Python 3.x
- Django 5.1.7
- Gmail account (for email notifications)
- PayPal Developer Account

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd paymentEndpoint
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `GET /payments/` - List all payments
- `POST /payments/` - Create a new payment
- `GET /payments/{id}/` - Retrieve payment details
- `POST /payments/{id}/complete/` - Complete a payment
- `POST /payments/{id}/return/` - Return a payment
- `POST /payments/{id}/cancel/` - Cancel a payment
- `GET /swagger/` - API documentation

## Payment Flow

1. Create a payment with customer details
2. System generates a unique reference and sends initial email
3. Process payment using one of three actions:
   - Complete: Marks payment as successful
   - Return: Processes a return
   - Cancel: Cancels the payment
4. System sends appropriate email notification with PDF receipt

## Admin Interface

Access the admin interface at `/admin/` to:
- View all payments
- Filter and search payments
- Update payment status
- View payment details

## API Documentation

Access the Swagger documentation at `/swagger/` for detailed API specifications and testing interface.

## Security Notes

- Never commit `.env` file to version control
- Keep `SECRET_KEY` secure and different in production
- Use proper SSL/TLS in production
- Configure proper `ALLOWED_HOSTS` in production


## Author

Olayemi