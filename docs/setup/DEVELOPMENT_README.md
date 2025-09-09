# 🛠️ Development Setup Guide

This guide will help you set up the Headless SaaS Platform for local development with PostgreSQL.

## 🚀 **Quick Start**

### **Option 1: Automated Setup (Recommended)**

```bash
# Run the automated setup script
./setup_postgres_dev.sh
```

### **Option 2: Manual Setup**

Follow the manual steps below.

## 📋 **Prerequisites**

- Python 3.11+
- PostgreSQL 12+
- Git
- Virtual Environment (venv)

## 🔧 **Manual Setup Steps**

### **1. Install PostgreSQL**

#### **Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### **macOS (with Homebrew):**

```bash
brew install postgresql
brew services start postgresql
```

#### **Windows:**

Download and install from [PostgreSQL Official Website](https://www.postgresql.org/download/windows/)

### **2. Create Development Database**

```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# Create database and user
CREATE DATABASE headless_dev;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE headless_dev TO postgres;
\q
```

### **3. Setup Python Environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **4. Configure Environment**

```bash
# Copy development environment template
cp env.dev .env

# Edit .env file if needed (optional)
nano .env
```

### **5. Run Database Migrations**

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### **6. Create Superuser**

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### **7. Start Development Server**

```bash
python manage.py runserver
```

## 🐳 **Docker Development Setup**

### **Start PostgreSQL and Redis with Docker**

```bash
# Start development services
docker-compose -f docker-compose.dev.yml up -d

# Check services
docker-compose -f docker-compose.dev.yml ps

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### **Connect to Docker PostgreSQL**

```bash
# Connect to database
psql -h localhost -p 5432 -U postgres -d headless_dev

# Or using Docker
docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d headless_dev
```

## 📊 **Database Management**

### **Useful PostgreSQL Commands**

```bash
# Connect to database
psql -h localhost -p 5432 -U postgres -d headless_dev

# List all databases
psql -h localhost -p 5432 -U postgres -l

# List all tables
psql -h localhost -p 5432 -U postgres -d headless_dev -c "\dt"

# Drop database (if needed)
dropdb -h localhost -p 5432 -U postgres headless_dev

# Create database (if needed)
createdb -h localhost -p 5432 -U postgres headless_dev
```

### **Django Database Commands**

```bash
# Show migrations status
python manage.py showmigrations

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset migrations (careful!)
python manage.py migrate --fake-initial

# Load sample data
python manage.py loaddata fixtures/sample_data.json
```

## 🔍 **Development Tools**

### **Django Shell**

```bash
# Interactive shell
python manage.py shell

# Run specific commands
python manage.py shell -c "from apps.users.models import User; print(User.objects.count())"
```

### **Django Extensions**

```bash
# Install django-extensions (already in requirements.txt)
pip install django-extensions

# Use shell_plus
python manage.py shell_plus

# Use runserver_plus
python manage.py runserver_plus
```

### **Database Browser**

```bash
# Install django-admin-interface for better admin
pip install django-admin-interface

# Or use external tools like pgAdmin, DBeaver, etc.
```

## 🧪 **Testing**

### **Run Tests**

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### **Test Scripts**

```bash
# Run standalone test scripts
python test_user_crud.py
python test_team_crud.py
python test_authentication.py
```

## 📝 **Development Configuration**

### **Environment Variables (.env)**

```bash
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/headless_dev
DB_NAME=headless_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@localhost

# Rate Limiting (Disabled for development)
RATE_LIMIT_ENABLED=False

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/django.log
```

### **Settings Differences**

- **DEBUG=True** - Enables debug mode
- **Console Email Backend** - Emails printed to console
- **Rate Limiting Disabled** - No API rate limits
- **Relaxed CORS** - Allows localhost origins
- **Debug Logging** - More verbose logging

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. PostgreSQL Connection Error**

```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Check PostgreSQL service status
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS
```

#### **2. Database Does Not Exist**

```bash
# Create database
createdb -h localhost -p 5432 -U postgres headless_dev

# Or connect and create
psql -h localhost -p 5432 -U postgres
CREATE DATABASE headless_dev;
\q
```

#### **3. Migration Errors**

```bash
# Reset migrations (careful!)
python manage.py migrate --fake-initial

# Or delete migration files and recreate
rm apps/*/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

#### **4. Permission Denied**

```bash
# Fix PostgreSQL permissions
sudo -u postgres psql
ALTER USER postgres CREATEDB;
\q
```

### **Useful Debug Commands**

```bash
# Check Django configuration
python manage.py check

# Check database connection
python manage.py dbshell

# Show current settings
python manage.py diffsettings

# Show URL patterns
python manage.py show_urls
```

## 📚 **API Testing**

### **Access Points**

- **API**: http://localhost:8000/api/v1/
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/health/

### **Default Credentials**

- **Username**: admin
- **Password**: admin123
- **Email**: admin@example.com

### **API Testing with curl**

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Get accounts (with token)
curl -X GET http://localhost:8000/api/v1/accounts/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🔄 **Development Workflow**

### **Daily Development**

1. **Start services**: `docker-compose -f docker-compose.dev.yml up -d`
2. **Activate venv**: `source venv/bin/activate`
3. **Start server**: `python manage.py runserver`
4. **Make changes** to your code
5. **Test changes** with API calls or tests
6. **Commit changes** to git

### **Database Changes**

1. **Modify models** in `apps/*/models.py`
2. **Create migration**: `python manage.py makemigrations`
3. **Apply migration**: `python manage.py migrate`
4. **Test changes** with Django shell or API

### **Code Quality**

```bash
# Format code
black .

# Lint code
flake8

# Run tests
python manage.py test
```

## 📖 **Additional Resources**

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Happy Coding! 🚀**
