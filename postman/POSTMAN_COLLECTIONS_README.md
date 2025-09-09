# 🚀 Complete Postman Collections for Headless SaaS Platform

This repository contains comprehensive Postman collections for testing all API endpoints of the Django DRF headless SaaS platform.

## 📦 **Available Collections:**

### 1. **`postman_collection_final.json`** - Main Collection
- **🔐 Authentication** - Login, Register, Token Management
- **🏢 Accounts** - Complete Account CRUD operations

### 2. **`postman_organizations_collection.json`** - Organizations Collection
- **🏢 Organizations** - Complete Organization CRUD operations
- **📊 Organization Features** - Feature management and limits
- **👥 Organization Users & Teams** - Related data access

### 3. **`postman_users_collection.json`** - Users Collection
- **👤 Users** - Complete User CRUD operations
- **🔑 User Management** - Roles, permissions, preferences
- **⚙️ User Settings** - Preferences and team memberships

### 4. **`postman_teams_collection.json`** - Teams Collection
- **👥 Teams** - Complete Team CRUD operations
- **👥 Team Members** - Team membership management
- **🎯 Team Features** - Feature flags and member management

## 🛠️ **Setup Instructions:**

### **Step 1: Import Collections**
1. Open Postman
2. Click **Import** button
3. Select the collection files you want to import:
   - `postman_collection_final.json` (Main + Auth + Accounts)
   - `postman_organizations_collection.json` (Organizations)
   - `postman_users_collection.json` (Users)
   - `postman_teams_collection.json` (Teams)

### **Step 2: Configure Environment Variables**
Each collection uses these variables (automatically set):

- `base_url` - API base URL (default: `http://127.0.0.1:8000`)
- `access_token` - JWT access token (auto-set after login)
- `account_id` - Current account ID (auto-set from responses)
- `organization_id` - Current organization ID (auto-set from responses)
- `user_id` - Current user ID (auto-set from responses)
- `team_id` - Current team ID (auto-set from responses)

### **Step 3: Start Django Server**
```bash
cd /path/to/headless-backend
source venv/bin/activate
python manage.py runserver
```

## 🔐 **Authentication Flow:**

### **Step 1: Login**
Use the **Login** request in the Authentication folder:
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

### **Step 2: Test Protected Endpoints**
- All other endpoints automatically use the saved access token
- No need to manually set authorization headers

## 📊 **API Endpoints Overview:**

### **🔐 Authentication Endpoints**
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/refresh/` - Token refresh
- `POST /api/v1/auth/logout/` - User logout
- `GET /api/v1/auth/me/` - Current user details
- `POST /api/v1/auth/change-password/` - Change password

### **🏢 Account Endpoints**
- `GET /api/v1/accounts/` - List accounts
- `POST /api/v1/accounts/` - Create account
- `GET /api/v1/accounts/{id}/` - Get account details
- `PUT /api/v1/accounts/{id}/` - Update account
- `DELETE /api/v1/accounts/{id}/` - Delete account (soft delete)
- `POST /api/v1/accounts/{id}/activate/` - Activate account
- `POST /api/v1/accounts/{id}/deactivate/` - Deactivate account
- `POST /api/v1/accounts/{id}/set_feature/` - Set account feature
- `GET /api/v1/accounts/{id}/get_feature/` - Get account feature
- `GET /api/v1/accounts/{id}/organizations/` - Get account organizations
- `GET /api/v1/accounts/{id}/users/` - Get account users
- `GET /api/v1/accounts/stats/` - Account statistics

### **🏢 Organization Endpoints**
- `GET /api/v1/organizations/` - List organizations
- `POST /api/v1/organizations/` - Create organization
- `GET /api/v1/organizations/{id}/` - Get organization details
- `PUT /api/v1/organizations/{id}/` - Update organization
- `DELETE /api/v1/organizations/{id}/` - Delete organization (soft delete)
- `POST /api/v1/organizations/{id}/activate/` - Activate organization
- `POST /api/v1/organizations/{id}/suspend/` - Suspend organization
- `POST /api/v1/organizations/{id}/set_feature/` - Set organization feature
- `GET /api/v1/organizations/{id}/limits/` - Get organization limits
- `GET /api/v1/organizations/{id}/users/` - Get organization users
- `GET /api/v1/organizations/{id}/teams/` - Get organization teams
- `GET /api/v1/organizations/stats/` - Organization statistics

### **👤 User Endpoints**
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}/` - Get user details
- `PUT /api/v1/users/{id}/` - Update user
- `DELETE /api/v1/users/{id}/` - Delete user
- `POST /api/v1/users/{id}/activate/` - Activate user
- `POST /api/v1/users/{id}/deactivate/` - Deactivate user
- `POST /api/v1/users/{id}/verify/` - Verify user
- `POST /api/v1/users/{id}/make_organization_admin/` - Make organization admin
- `POST /api/v1/users/{id}/make_account_admin/` - Make account admin
- `POST /api/v1/users/{id}/change_password/` - Change user password
- `POST /api/v1/users/{id}/set_preference/` - Set user preference
- `GET /api/v1/users/{id}/get_preference/` - Get user preference
- `GET /api/v1/users/{id}/teams/` - Get user teams
- `GET /api/v1/users/stats/` - User statistics

### **👥 Team Endpoints**
- `GET /api/v1/teams/` - List teams
- `POST /api/v1/teams/` - Create team
- `GET /api/v1/teams/{id}/` - Get team details
- `PUT /api/v1/teams/{id}/` - Update team
- `DELETE /api/v1/teams/{id}/` - Delete team (soft delete)
- `POST /api/v1/teams/{id}/activate/` - Activate team
- `POST /api/v1/teams/{id}/deactivate/` - Deactivate team
- `POST /api/v1/teams/{id}/archive/` - Archive team
- `GET /api/v1/teams/{id}/members/` - Get team members
- `POST /api/v1/teams/{id}/add_member/` - Add team member
- `POST /api/v1/teams/{id}/remove_member/` - Remove team member
- `POST /api/v1/teams/{id}/set_feature/` - Set team feature
- `GET /api/v1/teams/{id}/get_feature/` - Get team feature
- `GET /api/v1/teams/{id}/limits/` - Get team limits
- `GET /api/v1/teams/stats/` - Team statistics

### **👥 Team Member Endpoints**
- `GET /api/v1/team-members/` - List team members
- `POST /api/v1/team-members/` - Create team member
- `GET /api/v1/team-members/{id}/` - Get team member details
- `PUT /api/v1/team-members/{id}/` - Update team member
- `DELETE /api/v1/team-members/{id}/` - Delete team member
- `POST /api/v1/team-members/{id}/activate/` - Activate team member
- `POST /api/v1/team-members/{id}/deactivate/` - Deactivate team member
- `POST /api/v1/team-members/{id}/change_role/` - Change team member role
- `POST /api/v1/team-members/{id}/set_permission/` - Set team member permission
- `GET /api/v1/team-members/{id}/get_permission/` - Get team member permission
- `POST /api/v1/team-members/{id}/set_setting/` - Set team member setting
- `GET /api/v1/team-members/{id}/get_setting/` - Get team member setting

## 🧪 **Testing Workflow:**

### **Recommended Testing Order:**

1. **Authentication**
   - Login to get access token
   - Test token refresh
   - Test logout

2. **Account Management**
   - List accounts
   - Create new account
   - Update account
   - Test account features
   - Test account statistics

3. **Organization Management**
   - List organizations
   - Create new organization
   - Update organization
   - Test organization features
   - Test organization limits

4. **User Management**
   - List users
   - Create new user
   - Update user
   - Test user roles and permissions
   - Test user preferences

5. **Team Management**
   - List teams
   - Create new team
   - Add team members
   - Test team features
   - Test team member management

## 🔍 **Features Tested:**

### **Multi-tenant Architecture**
- Account isolation
- Organization isolation
- User access control

### **Soft Delete Functionality**
- All entities support soft delete
- Restore functionality available

### **Feature Management**
- Account-level features
- Organization-level features
- Team-level features

### **Role-based Permissions**
- Account administrators
- Organization administrators
- Team owners/admins/members

### **JWT Authentication**
- Token-based authentication
- Automatic token refresh
- Secure logout with token blacklisting

## 📝 **Test Data Available:**

### **Pre-configured Test Data:**
- **Account ID**: `2d9efae8-e6ea-4e3b-91e8-a307bdfa81be` (test-company)
- **Organization ID**: `b332c686-003b-4403-8503-756d09933c56` (engineering)
- **Admin User**: `admin@example.com` / `admin123`
- **Test User**: `newuser@example.com` / `password123`

### **Sample Request Bodies:**
All collections include comprehensive request bodies with realistic test data for:
- Account creation and updates
- Organization management
- User registration and management
- Team creation and member management

## 🐛 **Troubleshooting:**

### **Common Issues:**

1. **401 Unauthorized**
   - Ensure you're logged in and have a valid access token
   - Check if the token has expired

2. **404 Not Found**
   - Verify the server is running on the correct port
   - Check if the endpoint URL is correct

3. **400 Bad Request**
   - Validate the request body format
   - Check required fields are provided

4. **500 Internal Server Error**
   - Check Django server logs
   - Verify database is properly configured

## 📚 **Additional Resources:**

- Django REST Framework Documentation: https://www.django-rest-framework.org/
- JWT Authentication: https://django-rest-framework-simplejwt.readthedocs.io/
- Postman Documentation: https://learning.postman.com/docs/

---

**Happy Testing! 🎉**

All collections are production-ready and include comprehensive error handling, automatic variable management, and realistic test data.
