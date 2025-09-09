# 🐳 Docker Setup Guide

This guide will help you run the Headless SaaS Platform using Docker containers.

## 🚀 **Quick Start**

### **Option 1: Automated Setup (Recommended)**

```bash
# Run the automated Docker setup
./docker_setup.sh
```

### **Option 2: Manual Setup**

```bash
# Copy environment file
cp env.docker .env

# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 📋 **Prerequisites**

- Docker 20.10+
- Docker Compose 2.0+
- At least 4GB RAM
- At least 10GB disk space

## 🔧 **Services Overview**

### **🐘 PostgreSQL Database**

- **Image**: postgres:15-alpine
- **Port**: 5432
- **Database**: headless_backend_db
- **User**: postgres
- **Password**: postgres_password

### **🔴 Redis Cache & Message Broker**

- **Image**: redis:7-alpine
- **Port**: 6379
- **Purpose**: Caching and Celery message broker

### **🌐 Django Web Application**

- **Port**: 8000
- **Purpose**: Main API server
- **Health Check**: Built-in health monitoring

### **⚡ Celery Worker**

- **Purpose**: Background task processing
- **Tasks**: Email sending, file processing

### **⏰ Celery Beat**

- **Purpose**: Scheduled task management
- **Tasks**: Periodic cleanup, reports

### **🔀 Nginx Reverse Proxy**

- **Port**: 80 (HTTP), 443 (HTTPS)
- **Purpose**: Load balancing, SSL termination

## 🛠️ **Management Commands**

### **Using Docker Management Script**

```bash
# Start all services
./docker_manage.sh start

# Stop all services
./docker_manage.sh stop

# Restart all services
./docker_manage.sh restart

# View logs
./docker_manage.sh logs

# Check status
./docker_manage.sh status

# Access shell
./docker_manage.sh shell

# Run migrations
./docker_manage.sh migrate

# Create superuser
./docker_manage.sh createsuperuser

# Check health
./docker_manage.sh health

# Backup database
./docker_manage.sh backup

# Clean up
./docker_manage.sh clean
```

### **Using Docker Compose Directly**

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Access web container
docker-compose exec web bash

# Access database
docker-compose exec db psql -U postgres -d headless_backend_db

# Run Django commands
docker-compose exec web python manage.py <command>
```

## 🔧 **Configuration**

### **Environment Variables**

The `.env` file contains all configuration:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_URL=postgresql://postgres:postgres_password@db:5432/headless_backend_db

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

# Email (configure with your SMTP settings)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### **Customizing Configuration**

1. **Edit `.env` file** with your actual values
2. **Restart services**: `./docker_manage.sh restart`
3. **Verify changes**: `./docker_manage.sh health`

## 📊 **Monitoring & Health Checks**

### **Health Endpoints**

- **Application Health**: http://localhost:8000/health/
- **System Metrics**: http://localhost:8000/metrics/
- **API Documentation**: http://localhost:8000/api/docs/

### **Docker Health Checks**

```bash
# Check container health
docker-compose ps

# View health check logs
docker inspect <container_name> | grep -A 10 Health
```

### **Monitoring Commands**

```bash
# Resource usage
docker stats

# Container logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis
docker-compose logs -f celery
```

## 🗄️ **Database Management**

### **Accessing Database**

```bash
# Using Docker management script
./docker_manage.sh db-shell

# Using Docker Compose directly
docker-compose exec db psql -U postgres -d headless_backend_db
```

### **Database Operations**

```sql
-- List all tables
\dt

-- Show table structure
\d users_user

-- Run custom queries
SELECT * FROM users_user LIMIT 5;

-- Exit
\q
```

### **Backup & Restore**

```bash
# Backup database
./docker_manage.sh backup

# Restore database
./docker_manage.sh restore backup_20250108_143022.sql
```

## 📁 **File Management**

### **Volume Mounts**

- **Code**: `.:/app` (development)
- **Static Files**: `static_volume:/app/staticfiles`
- **Media Files**: `media_volume:/app/media`
- **Logs**: `logs_volume:/app/logs`
- **Database**: `postgres_data:/var/lib/postgresql/data`

### **Accessing Files**

```bash
# Access web container
docker-compose exec web bash

# List files
ls -la /app/

# View logs
tail -f /app/logs/django.log
```

## 🔄 **Development Workflow**

### **Code Changes**

1. **Edit code** in your local directory
2. **Changes are automatically reflected** (volume mount)
3. **Restart services** if needed: `./docker_manage.sh restart`

### **Database Changes**

1. **Modify models** in `apps/*/models.py`
2. **Create migration**: `docker-compose exec web python manage.py makemigrations`
3. **Apply migration**: `docker-compose exec web python manage.py migrate`

### **Testing**

```bash
# Run tests
./docker_manage.sh test

# Run specific test
docker-compose exec web python manage.py test apps.users.tests
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Services Won't Start**

```bash
# Check Docker status
docker --version
docker-compose --version

# Check port availability
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432
```

#### **2. Database Connection Issues**

```bash
# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec web python manage.py dbshell
```

#### **3. Permission Issues**

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Rebuild containers
./docker_manage.sh rebuild
```

#### **4. Memory Issues**

```bash
# Check memory usage
docker stats

# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory
```

### **Debug Commands**

```bash
# Check service status
./docker_manage.sh status

# View all logs
./docker_manage.sh logs

# Access container shell
./docker_manage.sh shell

# Check health
./docker_manage.sh health
```

## 🔒 **Security Considerations**

### **Production Security**

1. **Change default passwords** in `.env`
2. **Use strong SECRET_KEY**
3. **Enable SSL/TLS** with proper certificates
4. **Configure firewall** rules
5. **Regular security updates**

### **Environment Variables**

```bash
# Generate secure secret key
openssl rand -hex 32

# Use environment-specific settings
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## 📈 **Performance Optimization**

### **Resource Limits**

```yaml
# In docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "0.5"
```

### **Scaling Services**

```bash
# Scale web service
docker-compose up -d --scale web=3

# Scale Celery workers
docker-compose up -d --scale celery=3
```

## 🔄 **Updates & Maintenance**

### **Updating Application**

```bash
# Pull latest code
git pull origin main

# Rebuild images
./docker_manage.sh rebuild

# Restart services
./docker_manage.sh restart
```

### **Updating Dependencies**

```bash
# Update requirements.txt
# Rebuild images
./docker_manage.sh rebuild
```

### **Cleanup**

```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup
./docker_manage.sh clean
```

## 📚 **Additional Resources**

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Docker Guide](https://docs.djangoproject.com/en/stable/howto/deployment/docker/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Redis Docker](https://hub.docker.com/_/redis)

---

**Happy Dockerizing! 🐳**
