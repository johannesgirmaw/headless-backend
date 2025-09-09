# 📁 Git Repository Structure Guide

This document outlines what files and folders should be included or excluded from the Git repository for the Headless SaaS Platform.

## ✅ **Files/Folders TO TRACK (Include in Git)**

### **🔧 Core Application Files**

- `apps/` - Django applications (accounts, organizations, users, teams, common)
- `headless_backend/` - Django project settings and configuration
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies

### **🐳 Docker Configuration**

- `Dockerfile` - Docker image build configuration
- `docker-compose.yml` - Main Docker Compose configuration
- `docker-compose.dev.yml` - Development Docker Compose configuration
- `.dockerignore` - Docker build context exclusions
- `nginx.conf` - Nginx reverse proxy configuration

### **🛠️ Setup & Management Scripts**

- `docker_setup.sh` - Automated Docker setup script
- `docker_manage.sh` - Docker management commands
- `install_docker.sh` - Docker installation script
- `setup_postgres_dev.sh` - PostgreSQL development setup
- `deploy.sh` - Deployment script

### **📚 Documentation**

- `docs/` - Project documentation
- `README.md` - Main project documentation
- `*.md` - Markdown documentation files

### **🔐 Environment Templates**

- `env.example` - Environment variables template
- `env.dev` - Development environment template

### **📋 Postman Documentation**

- `postman/*.md` - Postman collection documentation
- `postman/README.md` - Postman usage guide

## ❌ **Files/Folders NOT TO TRACK (Exclude from Git)**

### **🔐 Sensitive Configuration**

- `.env` - Local environment variables (contains secrets)
- `.env.local` - Local environment overrides
- `.env.production` - Production environment variables
- `.env.docker` - Docker environment variables
- `secrets/` - Secret files directory
- `.secrets/` - Hidden secrets directory

### **🗄️ Database & Data**

- `*.sql` - Database dump files
- `*.dump` - Database backup files
- `*.backup` - Backup files
- `db.sqlite3` - SQLite database file
- `db.sqlite3-journal` - SQLite journal file
- `postgres_data/` - PostgreSQL Docker volume
- `redis_data/` - Redis Docker volume

### **📁 Generated Directories**

- `staticfiles/` - Django collected static files
- `media/` - User uploaded media files
- `logs/` - Application log files
- `static_volume/` - Docker static files volume
- `media_volume/` - Docker media files volume
- `logs_volume/` - Docker logs volume

### **🐍 Python & Virtual Environment**

- `venv/` - Python virtual environment
- `env/` - Python virtual environment
- `ENV/` - Python virtual environment
- `__pycache__/` - Python bytecode cache
- `*.pyc` - Python compiled files
- `*.pyo` - Python optimized files
- `*.pyd` - Python extension modules
- `*.egg-info/` - Python package metadata

### **🧪 Testing & Coverage**

- `.coverage` - Coverage report data
- `htmlcov/` - HTML coverage reports
- `.pytest_cache/` - Pytest cache
- `.tox/` - Tox testing cache
- `.nox/` - Nox testing cache
- `test_*.py` - Test files (if not part of main codebase)

### **🔧 IDE & Editor Files**

- `.vscode/` - VS Code settings (except shared configs)
- `.idea/` - PyCharm/IntelliJ settings
- `*.swp` - Vim swap files
- `*.swo` - Vim swap files
- `*~` - Backup files
- `.cursor/` - Cursor IDE settings

### **💻 Operating System Files**

- `.DS_Store` - macOS directory metadata
- `Thumbs.db` - Windows thumbnail cache
- `desktop.ini` - Windows desktop configuration
- `._*` - macOS resource forks
- `.Spotlight-V100` - macOS Spotlight index
- `.Trashes` - macOS trash folder

### **📦 Dependencies & Build Artifacts**

- `node_modules/` - Node.js dependencies
- `build/` - Build output directory
- `dist/` - Distribution files
- `*.egg` - Python egg files
- `*.whl` - Python wheel files

### **🔒 SSL & Certificates**

- `ssl/` - SSL certificate directory
- `*.pem` - Certificate files
- `*.key` - Private key files
- `*.crt` - Certificate files
- `*.p12` - PKCS#12 certificate files
- `*.pfx` - Personal Information Exchange files

### **📊 Monitoring & Logs**

- `monitoring/` - Monitoring configuration
- `.monitoring/` - Hidden monitoring files
- `*.log` - Log files
- `celerybeat-schedule` - Celery beat schedule
- `celerybeat.pid` - Celery beat process ID

### **📋 Postman Collections (Sensitive Data)**

- `postman/*.json` - Postman collections (contain API keys/tokens)
- `postman/collections/` - Postman collections directory
- `postman/environments/` - Postman environments directory

### **🔄 Temporary & Cache Files**

- `tmp/` - Temporary files directory
- `temp/` - Temporary files directory
- `.tmp/` - Hidden temporary files
- `.cache/` - Cache directory
- `cache/` - Cache directory

## 🎯 **Best Practices**

### **✅ DO Track:**

- Source code and application logic
- Configuration templates and examples
- Documentation and README files
- Setup and deployment scripts
- Docker configuration files
- Requirements and dependencies lists

### **❌ DON'T Track:**

- Environment variables with secrets
- Database files and dumps
- Generated static files
- Log files and temporary data
- IDE-specific settings
- OS-generated files
- SSL certificates and keys
- Postman collections with sensitive data

### **🔐 Security Considerations:**

- Never commit `.env` files with real secrets
- Use `env.example` as a template
- Keep API keys and tokens out of version control
- Use environment variables for sensitive configuration
- Regularly audit what's being tracked

### **📝 Maintenance:**

- Regularly review `.gitignore` for completeness
- Remove accidentally committed sensitive files
- Use `git rm --cached` for files already tracked
- Keep documentation up to date

## 🚀 **Quick Commands**

### **Check What's Being Tracked:**

```bash
git status --porcelain
git ls-files
```

### **Remove Files from Tracking:**

```bash
git rm --cached <file>
git rm --cached -r <directory>
```

### **Add to .gitignore:**

```bash
echo "filename" >> .gitignore
echo "directory/" >> .gitignore
```

### **Check .gitignore Effectiveness:**

```bash
git check-ignore -v <file>
```

---

**Remember**: When in doubt, exclude it! It's better to accidentally exclude a file than to accidentally commit sensitive data. 🔒
