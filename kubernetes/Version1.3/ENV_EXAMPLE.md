# Environment Configuration Example

This file shows the environment variables needed for Kubernetes deployment.
Copy and modify for your specific setup.

## Kubernetes Secret Values
These should be stored in `secret.yml` and are base64 encoded in Kubernetes.

```bash
# Database Credentials (CHANGE THESE!)
DATABASE_USER=hello_django
DATABASE_PASSWORD=your_secure_password_here_change_me
POSTGRES_USER=hello_django
POSTGRES_PASSWORD=your_secure_password_here_change_me

# Django Secret
SECRET_KEY=your-very-long-random-secret-key-change-this-in-production

# Database Configuration
POSTGRES_DB=alfa_romeo_db
```

## Kubernetes ConfigMap Values
These are non-sensitive and stored in `configmap.yml`.

```bash
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1 alfa-romeo-web.local .minikube.local
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_HOST=alfa-romeo-db
DATABASE_PORT=5432
DATABASE_NAME=alfa_romeo_db
DATABASE_SSL_MODE=disable
STATIC_URL=/static/
MEDIA_URL=/media/
```

## Local .env File (for local development with PostgreSQL)

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database Configuration
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=alfa_romeo_db
DATABASE_USER=hello_django
DATABASE_PASSWORD=hello_django

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,localhost:8000

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# PayPal (if needed)
# PAYPAL_RECEIVER_EMAIL=...
```

## Docker Compose .env File

```bash
# PostgreSQL Configuration
POSTGRES_DB=hello_django_dev
POSTGRES_USER=hello_django
POSTGRES_PASSWORD=hello_django

# Django Configuration
SECRET_KEY=your-secret-key-for-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=hello_django_dev
DATABASE_USER=hello_django
DATABASE_PASSWORD=hello_django
```

## Azure Kubernetes Service (AKS) Values

```bash
# Same as Kubernetes Secret, but update:
DATABASE_HOST=alfa-romeo-postgres.postgres.database.azure.com
DATABASE_SSL_MODE=require

# Azure-specific settings
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_ACCOUNT_KEY=your_storage_key
```