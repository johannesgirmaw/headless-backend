#!/bin/bash

# All-in-One Setup Script for Headless SaaS Platform
# This script handles Docker installation, setup, and management

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"
PROJECT_NAME="headless-backend"

# Use docker compose if available, otherwise docker-compose
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Function to show usage
show_usage() {
    echo -e "${BLUE}🚀 All-in-One Setup Script for Headless SaaS Platform${NC}"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Setup Commands:"
    echo "  install-docker    Install Docker and Docker Compose"
    echo "  setup            Complete project setup with Docker"
    echo "  quick-setup      Quick setup (assumes Docker is installed)"
    echo ""
    echo "Management Commands:"
    echo "  start            Start all services"
    echo "  stop             Stop all services"
    echo "  restart          Restart all services"
    echo "  build            Build all images"
    echo "  rebuild          Rebuild all images (no cache)"
    echo "  logs             Show logs for all services"
    echo "  logs-web         Show logs for web service only"
    echo "  logs-db          Show logs for database service only"
    echo "  logs-redis       Show logs for Redis service only"
    echo "  logs-celery      Show logs for Celery service only"
    echo "  status           Show status of all services"
    echo "  shell            Access web container shell"
    echo "  db-shell         Access database shell"
    echo "  migrate          Run database migrations"
    echo "  createsuperuser  Create Django superuser"
    echo "  collectstatic    Collect static files"
    echo "  test             Run Django tests"
    echo "  health           Check application health"
    echo "  clean            Clean up containers and volumes"
    echo "  backup           Backup database"
    echo "  restore          Restore database from backup"
    echo ""
    echo "Examples:"
    echo "  $0 install-docker    # Install Docker first"
    echo "  $0 setup            # Complete setup"
    echo "  $0 start            # Start services"
    echo "  $0 logs             # View logs"
    echo "  $0 health           # Check health"
    echo ""
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed.${NC}"
        echo "Run: $0 install-docker"
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}❌ Docker Compose is not installed.${NC}"
        echo "Run: $0 install-docker"
        return 1
    fi
    
    return 0
}

# Function to install Docker
install_docker() {
    echo -e "${BLUE}🐳 Installing Docker and Docker Compose...${NC}"
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        echo -e "${RED}❌ Please don't run this script as root${NC}"
        echo "Run: sudo $0 install-docker"
        exit 1
    fi
    
    # Update package index
    echo -e "${BLUE}📦 Updating package index...${NC}"
    sudo apt-get update
    
    # Install required packages
    echo -e "${BLUE}📦 Installing required packages...${NC}"
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    echo -e "${BLUE}🔑 Adding Docker's official GPG key...${NC}"
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Add Docker repository
    echo -e "${BLUE}📋 Adding Docker repository...${NC}"
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Update package index again
    echo -e "${BLUE}📦 Updating package index...${NC}"
    sudo apt-get update
    
    # Install Docker Engine
    echo -e "${BLUE}🐳 Installing Docker Engine...${NC}"
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Add user to docker group
    echo -e "${BLUE}👤 Adding user to docker group...${NC}"
    sudo usermod -aG docker $USER
    
    # Install Docker Compose (standalone)
    echo -e "${BLUE}🔧 Installing Docker Compose...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Start and enable Docker service
    echo -e "${BLUE}🚀 Starting Docker service...${NC}"
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Verify installation
    echo -e "${BLUE}✅ Verifying installation...${NC}"
    docker --version
    docker-compose --version
    
    echo ""
    echo -e "${GREEN}🎉 Docker and Docker Compose installed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  Important: You need to log out and log back in for group changes to take effect.${NC}"
    echo ""
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "1. Log out and log back in (or run: ${YELLOW}newgrp docker${NC})"
    echo "2. Test Docker: ${YELLOW}docker run hello-world${NC}"
    echo "3. Run setup: ${YELLOW}$0 setup${NC}"
}

# Function to create docker-compose.yml
create_docker_compose() {
    echo -e "${BLUE}📝 Creating docker-compose.yml...${NC}"
    
    cat > docker-compose.yml << 'EOF'
services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: headless_backend_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache & Message Broker
  redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Django Web Application
  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - logs_volume:/app/logs
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-super-secret-key-change-in-production
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/headless_backend_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
      - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
      - CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
      - CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Celery Worker
  celery:
    build: .
    command: celery -A headless_backend worker --loglevel=info
    volumes:
      - .:/app
      - media_volume:/app/media
      - logs_volume:/app/logs
    environment:
      - DEBUG=False
      - SECRET_KEY=your-super-secret-key-change-in-production
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/headless_backend_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  # Celery Beat (Scheduler)
  celery-beat:
    build: .
    command: celery -A headless_backend beat --loglevel=info
    volumes:
      - .:/app
      - logs_volume:/app/logs
    environment:
      - DEBUG=False
      - SECRET_KEY=your-super-secret-key-change-in-production
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/headless_backend_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
      - "8443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
  logs_volume:
EOF

    echo -e "${GREEN}✅ docker-compose.yml created${NC}"
}

# Function to create nginx.conf
create_nginx_conf() {
    echo -e "${BLUE}📝 Creating nginx.conf...${NC}"
    
    cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;
    
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/s;
    
    # Upstream for Django
    upstream django {
        server web:8000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        # Client max body size
        client_max_body_size 10M;
        
        # Static files
        location /static/ {
            alias /app/staticfiles/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Media files
        location /media/ {
            alias /app/media/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Health check endpoint
        location /health/ {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # No rate limiting for health checks
            access_log off;
        }
        
        # Metrics endpoint
        location /metrics/ {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # No rate limiting for metrics
            access_log off;
        }
        
        # Authentication endpoints with stricter rate limiting
        location ~ ^/api/v1/auth/(login|register|refresh)/ {
            limit_req zone=auth burst=10 nodelay;
            
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # API endpoints with rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Admin panel
        location /admin/ {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # API documentation
        location ~ ^/api/(docs|redoc|schema)/ {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Default location
        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Error pages
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;
        
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
}
EOF

    echo -e "${GREEN}✅ nginx.conf created${NC}"
}

# Function to create .env file
create_env_file() {
    echo -e "${BLUE}📝 Creating .env file...${NC}"
    
    cat > .env << 'EOF'
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web,nginx

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres_password@db:5432/headless_backend_db
DB_NAME=headless_backend_db
DB_USER=postgres
DB_PASSWORD=postgres_password
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
CELERY_ACCEPT_CONTENT=json
CELERY_TIMEZONE=UTC
CELERY_ENABLE_UTC=True

# Email Configuration (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SERVER_EMAIL=noreply@yourdomain.com

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=604800

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Monitoring & Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/django.log

# Security
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# File Upload Limits
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE=10485760  # 10MB

# Cache Configuration
CACHE_TTL=300  # 5 minutes
CACHE_MAX_ENTRIES=1000

# Health Check
HEALTH_CHECK_ENABLED=True
HEALTH_CHECK_DATABASE=True
HEALTH_CHECK_CACHE=True
HEALTH_CHECK_STORAGE=True

# Static Files
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
EOF

    echo -e "${GREEN}✅ .env file created${NC}"
}

# Function to complete setup
complete_setup() {
    echo -e "${BLUE}🚀 Starting complete project setup...${NC}"
    
    # Check Docker
    if ! check_docker; then
        echo -e "${RED}❌ Docker is required but not installed.${NC}"
        echo "Run: $0 install-docker"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker is available${NC}"
    
    # Create necessary files
    create_docker_compose
    create_nginx_conf
    create_env_file
    
    # Create necessary directories
    echo -e "${BLUE}📁 Creating necessary directories...${NC}"
    mkdir -p logs media staticfiles ssl
    echo -e "${GREEN}✅ Directories created${NC}"
    
    # Build and start services
    echo -e "${BLUE}🔨 Building Docker images...${NC}"
    $COMPOSE_CMD build
    
    echo -e "${BLUE}🚀 Starting services...${NC}"
    $COMPOSE_CMD up -d
    
    # Wait for services to be healthy
    echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"
    sleep 15
    
    # Check service health
    echo -e "${BLUE}🏥 Checking service health...${NC}"
    $COMPOSE_CMD ps
    
    # Run database migrations
    echo -e "${BLUE}🔄 Running database migrations...${NC}"
    $COMPOSE_CMD exec web python manage.py migrate
    
    # Create superuser
    echo -e "${BLUE}👤 Creating superuser...${NC}"
    $COMPOSE_CMD exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
    
    # Test the application
    echo -e "${BLUE}🧪 Testing the application...${NC}"
    sleep 5
    
    # Test health endpoint
    if curl -f http://localhost:8000/health/ &> /dev/null; then
        echo -e "${GREEN}✅ Health check passed${NC}"
    else
        echo -e "${RED}❌ Health check failed${NC}"
    fi
    
    # Test API documentation
    if curl -f http://localhost:8000/api/docs/ &> /dev/null; then
        echo -e "${GREEN}✅ API documentation accessible${NC}"
    else
        echo -e "${RED}❌ API documentation not accessible${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Complete setup finished successfully!${NC}"
    echo ""
    echo -e "${BLUE}📋 Access Points:${NC}"
    echo "  🌐 Application: http://localhost:8000"
    echo "  🔀 Nginx Proxy: http://localhost:8080"
    echo "  🔧 Admin Panel: http://localhost:8080/admin"
    echo "  📚 API Docs: http://localhost:8080/api/docs/"
    echo "  🏥 Health Check: http://localhost:8080/health/"
    echo "  📊 Metrics: http://localhost:8080/metrics/"
    echo ""
    echo -e "${BLUE}🔑 Default Credentials:${NC}"
    echo "  Email: admin@example.com"
    echo "  Password: admin123"
    echo ""
    echo -e "${BLUE}🛠️ Management Commands:${NC}"
    echo "  Start services: ${YELLOW}$0 start${NC}"
    echo "  Stop services: ${YELLOW}$0 stop${NC}"
    echo "  View logs: ${YELLOW}$0 logs${NC}"
    echo "  Check status: ${YELLOW}$0 status${NC}"
    echo "  Check health: ${YELLOW}$0 health${NC}"
    echo ""
    echo -e "${BLUE}📊 Service Status:${NC}"
    $COMPOSE_CMD ps
}

# Function to start services
start_services() {
    echo -e "${BLUE}🚀 Starting services...${NC}"
    $COMPOSE_CMD up -d
    echo -e "${GREEN}✅ Services started${NC}"
    $COMPOSE_CMD ps
}

# Function to stop services
stop_services() {
    echo -e "${BLUE}🛑 Stopping services...${NC}"
    $COMPOSE_CMD down
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to restart services
restart_services() {
    echo -e "${BLUE}🔄 Restarting services...${NC}"
    $COMPOSE_CMD restart
    echo -e "${GREEN}✅ Services restarted${NC}"
    $COMPOSE_CMD ps
}

# Function to build images
build_images() {
    echo -e "${BLUE}🔨 Building images...${NC}"
    $COMPOSE_CMD build
    echo -e "${GREEN}✅ Images built${NC}"
}

# Function to rebuild images
rebuild_images() {
    echo -e "${BLUE}🔨 Rebuilding images (no cache)...${NC}"
    $COMPOSE_CMD build --no-cache
    echo -e "${GREEN}✅ Images rebuilt${NC}"
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📋 Showing logs...${NC}"
    $COMPOSE_CMD logs -f
}

# Function to show specific service logs
show_service_logs() {
    local service=$1
    echo -e "${BLUE}📋 Showing $service logs...${NC}"
    $COMPOSE_CMD logs -f $service
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    $COMPOSE_CMD ps
    echo ""
    echo -e "${BLUE}📈 Resource Usage:${NC}"
    docker stats --no-stream
}

# Function to access web shell
access_shell() {
    echo -e "${BLUE}🐚 Accessing web container shell...${NC}"
    $COMPOSE_CMD exec web bash
}

# Function to access database shell
access_db_shell() {
    echo -e "${BLUE}🐚 Accessing database shell...${NC}"
    $COMPOSE_CMD exec db psql -U postgres -d headless_backend_db
}

# Function to run migrations
run_migrations() {
    echo -e "${BLUE}🔄 Running database migrations...${NC}"
    $COMPOSE_CMD exec web python manage.py migrate
    echo -e "${GREEN}✅ Migrations completed${NC}"
}

# Function to create superuser
create_superuser() {
    echo -e "${BLUE}👤 Creating superuser...${NC}"
    $COMPOSE_CMD exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
    echo -e "${GREEN}✅ Superuser creation completed${NC}"
}

# Function to collect static files
collect_static() {
    echo -e "${BLUE}📦 Collecting static files...${NC}"
    $COMPOSE_CMD exec web python manage.py collectstatic --noinput
    echo -e "${GREEN}✅ Static files collected${NC}"
}

# Function to run tests
run_tests() {
    echo -e "${BLUE}🧪 Running Django tests...${NC}"
    $COMPOSE_CMD exec web python manage.py test
    echo -e "${GREEN}✅ Tests completed${NC}"
}

# Function to check health
check_health() {
    echo -e "${BLUE}🏥 Checking application health...${NC}"
    
    # Check if services are running
    if ! $COMPOSE_CMD ps | grep -q "Up"; then
        echo -e "${RED}❌ Services are not running${NC}"
        return 1
    fi
    
    # Check health endpoint
    if curl -f http://localhost:8080/health/ &> /dev/null; then
        echo -e "${GREEN}✅ Health check passed${NC}"
        curl -s http://localhost:8080/health/ | python -m json.tool
    else
        echo -e "${RED}❌ Health check failed${NC}"
        return 1
    fi
}

# Function to clean up
clean_up() {
    echo -e "${BLUE}🧹 Cleaning up containers and volumes...${NC}"
    read -p "This will remove all containers, volumes, and data. Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $COMPOSE_CMD down -v --remove-orphans
        docker system prune -f
        echo -e "${GREEN}✅ Cleanup completed${NC}"
    else
        echo -e "${YELLOW}⚠️  Cleanup cancelled${NC}"
    fi
}

# Function to backup database
backup_database() {
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    echo -e "${BLUE}💾 Backing up database...${NC}"
    $COMPOSE_CMD exec db pg_dump -U postgres headless_backend_db > $backup_file
    echo -e "${GREEN}✅ Database backed up to $backup_file${NC}"
}

# Function to restore database
restore_database() {
    local backup_file=$1
    if [ -z "$backup_file" ]; then
        echo -e "${RED}❌ Please provide backup file path${NC}"
        echo "Usage: $0 restore <backup_file>"
        return 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        echo -e "${RED}❌ Backup file not found: $backup_file${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔄 Restoring database from $backup_file...${NC}"
    $COMPOSE_CMD exec -T db psql -U postgres -d headless_backend_db < $backup_file
    echo -e "${GREEN}✅ Database restored${NC}"
}

# Main script logic
case "${1:-}" in
    install-docker)
        install_docker
        ;;
    setup)
        complete_setup
        ;;
    quick-setup)
        if check_docker; then
            complete_setup
        else
            echo -e "${RED}❌ Docker is required. Run: $0 install-docker${NC}"
            exit 1
        fi
        ;;
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    build)
        build_images
        ;;
    rebuild)
        rebuild_images
        ;;
    logs)
        show_logs
        ;;
    logs-web)
        show_service_logs web
        ;;
    logs-db)
        show_service_logs db
        ;;
    logs-redis)
        show_service_logs redis
        ;;
    logs-celery)
        show_service_logs celery
        ;;
    status)
        show_status
        ;;
    shell)
        access_shell
        ;;
    db-shell)
        access_db_shell
        ;;
    migrate)
        run_migrations
        ;;
    createsuperuser)
        create_superuser
        ;;
    collectstatic)
        collect_static
        ;;
    test)
        run_tests
        ;;
    health)
        check_health
        ;;
    clean)
        clean_up
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database $2
        ;;
    *)
        show_usage
        ;;
esac
