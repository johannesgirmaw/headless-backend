# 🚀 Headless SaaS Platform - Postman Collection

This repository contains a comprehensive Postman collection for testing the Django DRF headless SaaS platform API.

## 📋 Collection Overview

The Postman collection includes complete CRUD operations for:

- **🔐 Authentication** - Login, Register, Token Management
- **🏢 Accounts** - Account management and features
- **🏢 Organizations** - Organization management within accounts
- **👤 Users** - User management and permissions
- **👥 Teams** - Team management and member operations
- **👥 Team Members** - Team membership management

## 🛠️ Setup Instructions

### 1. Import the Collection

1. Open Postman
2. Click **Import** button
3. Select the `postman_collection_complete.json` file
4. The collection will be imported with all endpoints

### 2. Configure Environment Variables

The collection uses the following variables that are automatically set:

- `base_url` - API base URL (default: `http://127.0.0.1:8000`)
- `access_token` - JWT access token (auto-set after login)
- `refresh_token` - JWT refresh token (auto-set after login)
- `account_id` - Current account ID (auto-set from responses)
- `organization_id` - Current organization ID (auto-set from responses)
- `user_id` - Current user ID (auto-set from responses)
- `team_id` - Current team ID (auto-set from responses)

### 3. Start the Django Server

```bash
# Navigate to project directory
cd /path/to/headless-backend

# Activate virtual environment
source venv/bin/activate

# Start Django development server
python manage.py runserver
```

## 🔐 Authentication Flow

### Step 1: Login

1. Use the **Login** request in the Authentication folder
2. Default credentials:
   ```json
   {
     "email": "admin@example.com",
     "password": "admin123"
   }
   ```
3. The access token will be automatically saved for subsequent requests

### Step 2: Test Protected Endpoints

- All other endpoints will automatically use the saved access token
- No need to manually set authorization headers

## 📊 API Endpoints Overview

### Authentication Endpoints

- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/refresh/` - Token refresh
- `POST /api/v1/auth/logout/` - User logout
- `GET /api/v1/auth/me/` - Current user details
- `POST /api/v1/auth/change-password/` - Change password

### Account Endpoints

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

### Organization Endpoints

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

### User Endpoints

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

### Team Endpoints

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

### Team Member Endpoints

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

## 🧪 Testing Workflow

### Recommended Testing Order:

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

## 🔍 Features Tested

### Multi-tenant Architecture

- Account isolation
- Organization isolation
- User access control

### Soft Delete Functionality

- All entities support soft delete
- Restore functionality available

### Feature Management

- Account-level features
- Organization-level features
- Team-level features

### Role-based Permissions

- Account administrators
- Organization administrators
- Team owners/admins/members

### JWT Authentication

- Token-based authentication
- Automatic token refresh
- Secure logout with token blacklisting

## 📝 Notes

- All DELETE operations perform soft delete (data is preserved)
- Feature flags can be set at account, organization, and team levels
- User preferences are stored as JSON
- Team member permissions are granular and role-based
- All endpoints support filtering, searching, and pagination
- API documentation is available at `/api/docs/` when server is running

## 🐛 Troubleshooting

### Common Issues:

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

## 📚 Additional Resources

- Django REST Framework Documentation: https://www.django-rest-framework.org/
- JWT Authentication: https://django-rest-framework-simplejwt.readthedocs.io/
- Postman Documentation: https://learning.postman.com/docs/

---

**Happy Testing! 🎉**
