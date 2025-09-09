# 🏥 Health & Monitoring Postman Collection

This collection provides comprehensive testing for all health monitoring, system metrics, and production features of the Headless SaaS Platform.

## 📋 **Collection Overview**

### **🔐 Authentication**

- **Login**: Get JWT access and refresh tokens
- **Refresh Token**: Refresh expired access tokens
- **Logout**: Invalidate refresh tokens
- **Get Current User**: Retrieve authenticated user info

### **🏥 Health Monitoring**

- **Health Check - All Services**: Complete system health status
- **Health Check - Database**: PostgreSQL connection status
- **Health Check - Cache**: Redis connection status
- **Health Check - Storage**: File storage system status
- **Health Check - System**: System resource status

### **📊 System Metrics**

- **System Metrics - All**: Complete system metrics
- **System Metrics - CPU**: CPU usage and performance
- **System Metrics - Memory**: Memory usage and statistics
- **System Metrics - Disk**: Disk usage and I/O statistics
- **System Metrics - Network**: Network interface statistics
- **System Metrics - Processes**: Running processes information

### **⚡ Rate Limiting Tests**

- **Rate Limit Test - Login**: Test login rate limits (5 requests)
- **Rate Limit Test - Register**: Test registration rate limits (5 requests)
- **Rate Limit Test - API Endpoints**: Test API rate limits (100 requests)

### **💾 Cache Management**

- **Cache Status**: Check cache connection and statistics
- **Cache Clear All**: Clear all cached data
- **Cache Clear Pattern**: Clear cache by pattern
- **Cache Get Key**: Retrieve specific cache value
- **Cache Set Key**: Set cache value with TTL

### **📁 File Storage Tests**

- **Upload Test File**: Upload files to cloud storage
- **List Files**: List uploaded files
- **Download File**: Download files from storage
- **Delete File**: Delete files from storage

### **📧 Email Service Tests**

- **Send Test Email**: Send test emails
- **Send Verification Email**: Trigger email verification
- **Send Password Reset Email**: Trigger password reset emails

### **🔄 Celery Task Tests**

- **Trigger Email Verification Task**: Background email verification
- **Trigger Welcome Email Task**: Background welcome emails
- **Trigger Password Reset Task**: Background password reset emails
- **Get Task Status**: Check task execution status

### **🔍 API Documentation**

- **OpenAPI Schema**: Get API schema
- **Swagger UI**: Access Swagger documentation
- **ReDoc UI**: Access ReDoc documentation

### **🧪 Performance Tests**

- **Load Test - Health Check**: 100 concurrent health checks
- **Load Test - Metrics**: 50 concurrent metrics requests
- **Load Test - API Endpoints**: 25 concurrent API requests

### **🛡️ Security Tests**

- **Test CORS Headers**: Verify CORS configuration
- **Test Invalid Token**: Test authentication security
- **Test SQL Injection Protection**: Test input sanitization

## 🚀 **Setup Instructions**

### **1. Import Collection**

1. Open Postman
2. Click "Import" button
3. Select `postman_health_monitoring_collection.json`
4. Click "Import"

### **2. Configure Environment Variables**

The collection uses these variables:

- `base_url`: http://localhost:8000 (default)
- `access_token`: Auto-populated after login
- `refresh_token`: Auto-populated after login

### **3. Start Development Server**

```bash
# Activate virtual environment
source venv/bin/activate

# Start development server
python manage.py runserver
```

### **4. Run Authentication First**

1. Execute "Login" request
2. Tokens will be automatically saved
3. All subsequent requests will use the access token

## 📊 **Health Monitoring Endpoints**

### **Health Check Responses**

```json
{
  "status": "healthy",
  "timestamp": 1757373755.0443306,
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    "cache": {
      "status": "healthy",
      "message": "Cache connection successful"
    },
    "storage": {
      "status": "healthy",
      "message": "Storage connection successful"
    },
    "system": {
      "status": "healthy",
      "message": "System metrics retrieved",
      "metrics": {
        "cpu_percent": 36.0,
        "memory_percent": 48.5,
        "memory_used_mb": 8210.51,
        "memory_total_mb": 19785.91,
        "disk_percent": 90.65,
        "disk_used_gb": 211.38
      }
    }
  }
}
```

### **System Metrics Responses**

```json
{
  "timestamp": 1757373755.0443306,
  "cpu": {
    "percent": 36.0,
    "count": 8,
    "frequency": 2400.0
  },
  "memory": {
    "total": 19785912320,
    "available": 10188800000,
    "percent": 48.5,
    "used": 9597111232,
    "free": 10188800000
  },
  "disk": {
    "total": 233000000000,
    "used": 211000000000,
    "free": 22000000000,
    "percent": 90.65
  }
}
```

## ⚡ **Rate Limiting Tests**

### **Rate Limit Headers**

When rate limits are exceeded, you'll see:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1757374200
X-RateLimit-Window: 3600
```

### **Rate Limit Response**

```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Try again later.",
  "retry_after": 3600,
  "limit": 100,
  "window": 3600
}
```

## 💾 **Cache Management**

### **Cache Operations**

```json
// Set cache value
{
  "key": "test_key",
  "value": "test_value",
  "timeout": 300
}

// Clear cache by pattern
{
  "pattern": "user_*"
}
```

## 📁 **File Storage**

### **File Upload**

- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: file + folder parameter
- **Response**: File metadata with URLs

### **File Download**

- **Method**: GET
- **Response**: File content with appropriate headers
- **Headers**: Content-Disposition, Content-Type

## 📧 **Email Service**

### **Email Templates**

- **test**: Basic test email
- **verification**: Email verification
- **welcome**: Welcome email
- **password_reset**: Password reset email

### **Email Response**

```json
{
  "success": true,
  "message": "Email sent successfully",
  "task_id": "celery_task_id_here"
}
```

## 🔄 **Celery Tasks**

### **Task Status**

```json
{
  "task_id": "celery_task_id_here",
  "status": "SUCCESS",
  "result": "Email sent successfully",
  "traceback": null
}
```

## 🧪 **Performance Testing**

### **Load Test Results**

- **Health Check**: Should handle 100+ concurrent requests
- **Metrics**: Should handle 50+ concurrent requests
- **API Endpoints**: Should handle 25+ concurrent requests

### **Performance Benchmarks**

- **Response Time**: < 5000ms (configured in collection)
- **Throughput**: 100+ requests/second
- **Concurrent Users**: 25+ simultaneous users

## 🛡️ **Security Testing**

### **CORS Headers**

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

### **Authentication Security**

- **Invalid Token**: Should return 401 Unauthorized
- **Expired Token**: Should return 401 Unauthorized
- **Missing Token**: Should return 401 Unauthorized

## 📈 **Monitoring Best Practices**

### **Health Check Frequency**

- **Production**: Every 30 seconds
- **Staging**: Every 60 seconds
- **Development**: Every 5 minutes

### **Metrics Collection**

- **CPU Usage**: Monitor for spikes > 80%
- **Memory Usage**: Monitor for usage > 85%
- **Disk Usage**: Monitor for usage > 90%
- **Response Time**: Monitor for latency > 2 seconds

### **Alert Thresholds**

- **Critical**: Health check fails
- **Warning**: Metrics exceed thresholds
- **Info**: Performance degradation detected

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Health Check Fails**

```bash
# Check database connection
python manage.py dbshell

# Check Redis connection
redis-cli ping

# Check file storage
python manage.py shell -c "from django.core.files.storage import default_storage; print(default_storage.exists('test.txt'))"
```

#### **2. Metrics Not Available**

```bash
# Check psutil installation
pip install psutil==5.9.6

# Check system permissions
python manage.py shell -c "import psutil; print(psutil.cpu_percent())"
```

#### **3. Rate Limiting Issues**

```bash
# Check Redis connection
redis-cli ping

# Clear rate limit data
redis-cli FLUSHDB
```

#### **4. Cache Issues**

```bash
# Check Redis connection
redis-cli ping

# Test cache operations
python manage.py shell -c "from django.core.cache import cache; cache.set('test', 'value', 300); print(cache.get('test'))"
```

## 📚 **Additional Resources**

- [Django Health Check Documentation](https://github.com/roverdotcom/django-health-check)
- [Redis Monitoring](https://redis.io/docs/management/monitoring/)
- [PostgreSQL Monitoring](https://www.postgresql.org/docs/current/monitoring.html)
- [Celery Monitoring](https://docs.celeryq.dev/en/stable/userguide/monitoring.html)

---

**Happy Monitoring! 🚀**
