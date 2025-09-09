# 🚀 Headless SaaS Platform - Complete Setup Guide

A comprehensive Django REST Framework-based headless SaaS platform with complete Docker containerization, production-ready features, and automated setup.

## 📋 **Quick Start**

### **Complete Setup (Recommended)**

```bash
# Install Docker and setup everything
./setup.sh install-docker
./setup.sh setup
```

### **Quick Setup (Docker Already Installed)**

```bash
# Setup project only
./setup.sh quick-setup
```

## 🎯 **What This Platform Provides**

### **🏗️ Core Architecture**

- **Multi-tenant SaaS**: Account → Organization → Users → Teams hierarchy
- **Django REST Framework**: Robust API with comprehensive CRUD operations
- **Custom User Model**: Email-based authentication with role-based access control
- **Soft Delete Pattern**: Data preservation with audit trails
- **JWT Authentication**: Secure token-based authentication

### **🐳 Complete Containerization**

- **PostgreSQL Database**: Production-ready database with health checks
- **Redis Cache**: High-performance caching and message broker
- **Celery Workers**: Background task processing
- **Nginx Reverse Proxy**: Load balancing, SSL termination, rate limiting
- **Health Monitoring**: Comprehensive system and application monitoring

### **🛡️ Production-Ready Features**

- **Rate Limiting**: API protection with configurable limits
- **Security Headers**: Comprehensive security configuration
- **SSL/TLS Ready**: HTTPS configuration with certificate management
- **File Storage**: Cloud storage integration (AWS S3 ready)
- **Email Service**: SMTP integration for notifications
- **Logging & Monitoring**: Centralized logging with error tracking
- **Database Backup**: Automated backup and restore functionality

## 🛠️ **All-in-One Setup Script**

### **Available Commands**

#### **Setup Commands**

- `install-docker` - Install Docker and Docker Compose
- `setup` - Complete project setup with Docker
- `quick-setup` - Quick setup (assumes Docker is installed)

#### **Management Commands**

- `start` - Start all services
- `stop` - Stop all services
- `restart` - Restart all services
- `build` - Build all images
- `rebuild` - Rebuild all images (no cache)
- `logs` - Show logs for all services
- `logs-web` - Show logs for web service only
- `logs-db` - Show logs for database service only
- `logs-redis` - Show logs for Redis service only
- `logs-celery` - Show logs for Celery service only
- `status` - Show status of all services
- `shell` - Access web container shell
- `db-shell` - Access database shell
- `migrate` - Run database migrations
- `createsuperuser` - Create Django superuser
- `collectstatic` - Collect static files
- `test` - Run Django tests
- `health` - Check application health
- `clean` - Clean up containers and volumes
- `backup` - Backup database
- `restore` - Restore database from backup

## 🎯 **Usage Examples**

### **First Time Setup**

```bash
# Step 1: Install Docker
./setup.sh install-docker

# Step 2: Log out and log back in (or run: newgrp docker)

# Step 3: Complete setup
./setup.sh setup
```

### **Daily Development**

```bash
# Start services
./setup.sh start

# Check status
./setup.sh status

# View logs
./setup.sh logs

# Check health
./setup.sh health

# Stop services
./setup.sh stop
```

### **Database Management**

```bash
# Run migrations
./setup.sh migrate

# Create superuser
./setup.sh createsuperuser

# Backup database
./setup.sh backup

# Restore database
./setup.sh restore backup_20250109_143022.sql
```

### **Development Tasks**

```bash
# Access web container
./setup.sh shell

# Access database
./setup.sh db-shell

# Run tests
./setup.sh test

# Collect static files
./setup.sh collectstatic
```

## 🔧 **What the Script Does**

### **Docker Installation (`install-docker`)**

- Updates package index
- Installs required packages
- Adds Docker's official GPG key
- Adds Docker repository
- Installs Docker Engine and Docker Compose
- Adds user to docker group
- Starts and enables Docker service
- Verifies installation

### **Project Setup (`setup` or `quick-setup`)**

- Checks Docker availability
- Creates `docker-compose.yml`
- Creates `nginx.conf`
- Creates `.env` file
- Creates necessary directories
- Builds Docker images
- Starts all services
- Runs database migrations
- Creates Django superuser
- Tests application endpoints

### **Service Management**

- Start/stop/restart services
- View logs and status
- Access container shells
- Run Django commands
- Health monitoring
- Database backup/restore

## 📊 **Services Architecture**

### **🐘 PostgreSQL Database**

- **Image**: postgres:15-alpine
- **Port**: 5433 (external), 5432 (internal)
- **Database**: headless_backend_db
- **User**: postgres
- **Password**: postgres_password
- **Features**: Health checks, persistent volumes, optimized configuration

### **🔴 Redis Cache & Message Broker**

- **Image**: redis:7-alpine
- **Port**: 6380 (external), 6379 (internal)
- **Purpose**: Caching and Celery broker
- **Features**: Persistence, health checks, optimized memory usage

### **🌐 Django Web Application**

- **Port**: 8000 (direct access)
- **Purpose**: Main API server
- **Features**: Health checks, hot reload, comprehensive logging
- **APIs**: RESTful CRUD operations for all entities

### **⚡ Celery Worker**

- **Purpose**: Background task processing
- **Tasks**: Email sending, file processing, scheduled tasks
- **Features**: Auto-scaling, error handling, task monitoring

### **⏰ Celery Beat**

- **Purpose**: Scheduled task management
- **Tasks**: Periodic cleanup, reports, maintenance
- **Features**: Cron-like scheduling, persistent schedules

### **🔀 Nginx Reverse Proxy**

- **Port**: 8080 (HTTP), 8443 (HTTPS)
- **Purpose**: Load balancing, SSL termination, rate limiting
- **Features**: Security headers, gzip compression, static file serving

## 🌐 **Access Points**

### **Application URLs**

- **Direct Django**: http://localhost:8000
- **Nginx Proxy**: http://localhost:8080
- **Admin Panel**: http://localhost:8080/admin
- **API Documentation**: http://localhost:8080/api/docs/
- **Health Check**: http://localhost:8080/health/
- **System Metrics**: http://localhost:8080/metrics/

### **Default Credentials**

- **Email**: admin@example.com
- **Password**: admin123

## 🔐 **Configuration**

### **Environment Variables**

The script creates a `.env` file with:

- Database configuration (PostgreSQL)
- Redis configuration (caching and Celery)
- Celery configuration (background tasks)
- Email settings (SMTP integration)
- JWT configuration (authentication)
- Security settings (CORS, CSRF, SSL)
- Rate limiting configuration
- Monitoring and logging settings

### **Docker Compose**

Creates a complete `docker-compose.yml` with:

- All necessary services with health checks
- Volume mounts for persistence
- Environment variables for configuration
- Port mappings (avoiding conflicts)
- Service dependencies and startup order
- Resource limits and restart policies

### **Nginx Configuration**

Creates `nginx.conf` with:

- Reverse proxy setup for Django
- Rate limiting (API: 10 req/s, Auth: 5 req/s)
- Security headers (XSS, CSRF, Content-Type)
- Static file serving with caching
- Gzip compression for performance
- Error handling and custom error pages
- SSL/TLS ready configuration

## 📈 **Current Status**

### **✅ All Services Running**

- **Database**: PostgreSQL (healthy)
- **Cache**: Redis (healthy)
- **Web App**: Django (healthy)
- **Proxy**: Nginx (healthy)
- **Worker**: Celery (running)

### **🎯 Key Features Implemented**

- **Complete CRUD Operations**: Accounts, Organizations, Users, Teams
- **Authentication System**: JWT-based with refresh tokens
- **Role-Based Access Control**: Account/Organization admin roles
- **Multi-tenant Architecture**: Isolated data per account
- **Production Monitoring**: Health checks, metrics, logging
- **File Management**: Upload, storage, and retrieval
- **Email Integration**: Verification and notifications
- **Rate Limiting**: API protection
- **Caching**: Redis-based performance optimization

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Docker Not Installed**

```bash
# Install Docker first
./setup.sh install-docker

# Log out and log back in
# Then run setup
./setup.sh setup
```

#### **2. Permission Denied**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in
# Or run: newgrp docker
```

#### **3. Port Conflicts**

The script uses non-standard ports to avoid conflicts:

- PostgreSQL: 5433 (instead of 5432)
- Redis: 6380 (instead of 6379)
- Nginx: 8080 (instead of 80)

#### **4. Services Not Starting**

```bash
# Check logs
./setup.sh logs

# Check status
./setup.sh status

# Restart services
./setup.sh restart
```

### **Debug Commands**

```bash
# Check Docker status
docker --version
docker-compose --version

# Check service health
./setup.sh health

# View all logs
./setup.sh logs

# Check resource usage
docker stats
```

## 📈 **Performance & Monitoring**

### **Health Monitoring**

- Built-in health checks for all services
- System metrics endpoint with CPU, memory, disk usage
- Resource usage monitoring
- Log aggregation and centralized logging

### **Rate Limiting**

- API endpoints: 10 requests/second
- Authentication: 5 requests/second
- Burst handling with nodelay
- Configurable per endpoint

### **Security Features**

- Security headers (XSS, CSRF, Content-Type)
- CORS configuration
- SSL/TLS ready
- Input validation
- SQL injection protection
- JWT token security

## 🔄 **Maintenance**

### **Regular Tasks**

```bash
# Check service status
./setup.sh status

# View logs
./setup.sh logs

# Check health
./setup.sh health

# Backup database
./setup.sh backup
```

### **Updates**

```bash
# Rebuild images
./setup.sh rebuild

# Restart services
./setup.sh restart

# Run migrations
./setup.sh migrate
```

### **Cleanup**

```bash
# Clean up containers and volumes
./setup.sh clean
```

## 📁 **Project Structure**

### **✅ Tracked Files**

- `setup.sh` - All-in-one setup script
- `docker-compose.yml` - Service orchestration
- `nginx.conf` - Nginx configuration
- `apps/` - Django applications (accounts, organizations, users, teams, common)
- `headless_backend/` - Django project configuration
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image configuration
- `.gitignore` - Git exclusions
- `.dockerignore` - Docker exclusions

### **❌ Excluded Files**

- `.env` - Environment variables (sensitive)
- `env.docker` - Docker environment (sensitive)
- `postman/*.json` - Postman collections (API keys)
- `logs/` - Log files
- `media/` - User uploads
- `staticfiles/` - Generated static files

## 🎉 **Ready to Use!**

The Headless SaaS Platform is now fully containerized and ready for development and production deployment. It provides:

1. **Complete Automation**: From Docker installation to full deployment
2. **Production Ready**: Health checks, monitoring, security, rate limiting
3. **Developer Friendly**: Easy commands, comprehensive logging, hot reload
4. **Well Documented**: Complete usage guide and examples
5. **Git Ready**: Properly configured for version control
6. **Scalable Architecture**: Multi-tenant, role-based, microservice-ready

### **Next Steps**

1. Test the script: `./setup.sh health`
2. Commit to Git: `git add . && git commit -m "Add all-in-one setup script"`
3. Share with team: The script handles everything automatically!
4. Start developing: Access the API at http://localhost:8080/api/docs/

## 📚 **Additional Resources**

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

---

**Happy Coding! 🚀**
