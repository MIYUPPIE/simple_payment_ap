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

## Required Packages

Key dependencies include:
```bash
Django==5.1.7
django-environ==0.12.0
djangorestframework==3.15.2
drf-yasg==1.21.10
paypalrestsdk==1.13.3
Pillow==11.1.0
reportlab==4.3.1
requests==2.32.3
```

For a complete list of dependencies, see `requirements.txt`.

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

### Payment Management
- `GET /payments/` - List all payments
- `POST /payments/` - Create a new payment
- `GET /payments/{id}/` - Retrieve payment details
- `POST /payments/{id}/complete/` - Complete a payment
- `POST /payments/{id}/return/` - Return a payment
- `POST /payments/{id}/cancel/` - Cancel a payment

### Documentation
- `GET /swagger/` - Interactive API documentation
- `GET /admin/` - Admin interface

## API Usage

### Creating a Payment
```bash
POST /payments/
{
    "name": "John Doe",
    "email": "john@example.com",
    "amount": 100.00
}
```

### Payment Flow

1. Create a payment with customer details
2. System generates a unique reference and sends initial email with PDF receipt
3. Process payment using one of three actions:
   - Complete: Marks payment as successful
   - Return: Processes a return
   - Cancel: Cancels the payment
4. System sends appropriate email notification with updated PDF receipt

## Admin Interface

Access the admin interface at `/admin/` to:
- View all payments
- Filter and search payments by status, date, and customer details
- Update payment status
- View payment details and transaction history

## API Documentation

Access the Swagger documentation at `/swagger/` for:
- Detailed API specifications
- Interactive testing interface
- Request/response examples
- Authentication details

## Development

### Project Structure
```
paymentEndpoint/
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── paymentEndpoint/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── .env
├── manage.py
└── requirements.txt
```

## Security Notes

- Never commit `.env` file to version control
- Keep `SECRET_KEY` secure and different in production
- Use proper SSL/TLS in production
- Configure proper `ALLOWED_HOSTS` in production
- Regularly update dependencies for security patches
- Use environment-specific settings for development/production

## Troubleshooting

Common issues and solutions:
1. Email configuration: Ensure Gmail "Less secure app access" is enabled or use App Password
2. PayPal integration: Verify credentials and sandbox/production mode settings
3. PDF generation: Ensure proper permissions for file operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Interpulse License

## Author

Olayemi

## Support

For support, email [yemokanlawon@gmail.com]
