# Django Books API with Encryption

A secure Django REST API for managing books with AES encryption and HMAC authentication.

## Features

- CRUD operations for books
- AES-256 CBC encryption for request/response payloads
- HMAC SHA-256 authentication
- CORS support
- RESTful API design

## Tech Stack

- Python 3.9+
- Django 5.1.7
- Django REST Framework
- django-cors-headers
- pycryptodome (for AES encryption)

## Project Structure

```
├── app/                    # Django project root
│   ├── settings.py         # Project settings
│   ├── urls.py            # Project URL configuration
│   └── wsgi.py            # WSGI configuration
├── books/                  # Books app
│   ├── models.py          # Book model definition
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   └── urls.py            # App URL configuration
├── middlewares/           # Custom middleware
│   └── encryption.py      # AES encryption middleware
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── test.py               # API test script
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
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

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Books API

- `GET /books` - List all books
- `POST /books` - Create a new book

### Request/Response Format

#### POST Request
```json
{
    "data": "<AES encrypted payload>",
    "hmac": "<HMAC signature>"
}
```

#### Book Object Structure
```json
{
    "title": "string",
    "author": "string",
    "published_date": "YYYY-MM-DD",
    "description": "string"
}
```

## Security

- AES-256 CBC encryption for payload security
- HMAC SHA-256 for request authentication
- CORS configuration for cross-origin requests
- Django's built-in security features

## Testing

Run the test script to verify API functionality:
```bash
python test.py
```

## Development

1. Make sure to update the encryption keys in a secure manner (not in source code)
2. Use environment variables for sensitive information
3. Follow Django's security best practices
4. Run tests before submitting pull requests

## License

[Add your license here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request