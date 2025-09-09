# **Agents Platform API Specifications**

This document outlines the RESTful API endpoints for managing the core resources of the Agents Platform, including accounts, organizations, users, subscriptions, and the product catalog.

-----

## **1. Accounts**

### **`POST /accounts`**

  * **Description:** Creates a new top-level account.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "Acme Corporation",
      "description": "Enterprise customer account.",
      "contactEmail": "admin@acmecorp.com",
      "isActive": true
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "accountId": 101,
      "name": "Acme Corporation",
      "description": "Enterprise customer account.",
      "contactEmail": "admin@acmecorp.com",
      "isActive": true,
      "createdBy": 12345,
      "createdAt": "2025-08-19T10:00:00Z",
      "updatedAt": "2025-08-19T10:00:00Z"
    }
    ```

### **`GET /accounts`**

  * **Description:** Retrieves a paginated list of all accounts.
  * **Authorization:** SaaS Administrator only.
  * **Query Parameters:** `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "page": 1,
      "pageSize": 25,
      "totalPages": 1,
      "totalItems": 2,
      "items": [
        {
          "accountId": 101,
          "name": "Acme Corporation",
          "description": "Enterprise customer account.",
          "contactEmail": "admin@acmecorp.com",
          "isActive": true,
          "createdBy": 12345,
          "createdAt": "2025-08-19T10:00:00Z",
          "updatedAt": "2025-08-19T10:00:00Z"
        }
      ]
    }
    ```

### **`GET /accounts/{accountId}`**

  * **Description:** Retrieves a single account by its ID.
  * **Authorization:** SaaS Administrator only.
  * **Response:** `200 OK`
    ```json
    {
      "accountId": 101,
      "name": "Acme Corporation",
      "description": "Enterprise customer account.",
      "contactEmail": "admin@acmecorp.com",
      "isActive": true,
      "createdBy": 12345,
      "createdAt": "2025-08-19T10:00:00Z",
      "updatedAt": "2025-08-19T10:00:00Z"
    }
    ```

### **`PUT /accounts/{accountId}`**

  * **Description:** Updates an existing account.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "isActive": false,
      "description": "Deactivated and updated description."
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "accountId": 101,
      "name": "Acme Corporation",
      "description": "Deactivated and updated description.",
      "contactEmail": "admin@acmecorp.com",
      "isActive": false,
      "createdBy": 12345,
      "createdAt": "2025-08-19T10:00:00Z",
      "updatedAt": "2025-08-19T11:00:00Z"
    }
    ```

### **`DELETE /accounts/{accountId}`**

  * **Description:** Deletes an account.
  * **Authorization:** SaaS Administrator only.
  * **Response:** `204 No Content`

-----

## **2. Organizations**

### **`POST /accounts/{accountId}/organizations`**

  * **Description:** Creates a new organization within a specific account.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "Marketing Department",
      "description": "Handles all marketing-related activities.",
      "logoUrl": "https://example.com/logos/marketing-dept.png"
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "organizationId": 201,
      "accountId": 101,
      "name": "Marketing Department",
      "description": "Handles all marketing-related activities.",
      "logoUrl": "https://example.com/logos/marketing-dept.png",
      "createdAt": "2025-08-20T09:00:00Z",
      "updatedAt": "2025-08-20T09:00:00Z"
    }
    ```

### **`GET /accounts/{accountId}/organizations`**

  * **Description:** Retrieves a paginated list of all organizations for a specific account.
  * **Authorization:** SaaS Administrator, SaaS Account Manager.
  * **Query Parameters:** `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "organizationId": 201,
          "accountId": 101,
          "name": "Marketing Department",
          "description": "...",
          "logoUrl": "...",
          "createdAt": "...",
          "updatedAt": "..."
        }
      ]
    }
    ```

### **`GET /accounts/{accountId}/organizations/{organizationId}`**

  * **Description:** Retrieves a single organization by its ID.
  * **Authorization:** SaaS Administrator, SaaS Account Manager, Organization Administrator.
  * **Response:** `200 OK`
    ```json
    {
      "organizationId": 201,
      "accountId": 101,
      "name": "Marketing Department",
      "description": "...",
      "logoUrl": "...",
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`PUT /accounts/{accountId}/organizations/{organizationId}`**

  * **Description:** Updates an existing organization.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "description": "Updated description for the Marketing Department.",
      "logoUrl": "https://example.com/logos/marketing-dept-new.png"
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "organizationId": 201,
      "accountId": 101,
      "name": "Marketing Department",
      "description": "Updated description...",
      "logoUrl": "...",
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`DELETE /accounts/{accountId}/organizations/{organizationId}`**

  * **Description:** Deletes an organization.
  * **Authorization:** SaaS Administrator only.
  * **Response:** `204 No Content`

-----

## **3. Users**

### **`POST /organizations/{organizationId}/users`**

  * **Description:** Creates a new user within an organization.
  * **Authorization:** Organization Administrator only.
  * **Request Body:**
    ```json
    {
      "fullName": "Jane Doe",
      "email": "jane.doe@example.com",
      "password": "strongPassword123!",
      "profileImage": "https://example.com/images/janeDoe.png",
      "userPreferences": {}
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "userId": 301,
      "organizationId": 201,
      "fullName": "Jane Doe",
      "email": "jane.doe@example.com",
      "status": "active",
      "createdBy": 12345,
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`GET /organizations/{organizationId}/users`**

  * **Description:** Retrieves a paginated list of all users.
  * **Authorization:** Organization Administrator, Team Manager.
  * **Query Parameters:** `status`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "userId": 301,
          "organizationId": 201,
          "fullName": "Jane Doe",
          "email": "jane.doe@example.com",
          "status": "active",
          "createdBy": 12345,
          "createdAt": "...",
          "updatedAt": "..."
        }
      ]
    }
    ```

### **`GET /organizations/{organizationId}/users/{userId}`**

  * **Description:** Retrieves a single user by their ID.
  * **Authorization:** Organization Administrator, Team Manager.
  * **Response:** `200 OK`
    ```json
    {
      "userId": 301,
      "organizationId": 201,
      "fullName": "Jane Doe",
      "email": "jane.doe@example.com",
      "status": "active",
      "createdBy": 12345,
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`PUT /organizations/{organizationId}/users/{userId}`**

  * **Description:** Updates an existing user's information.
  * **Authorization:** Organization Administrator, Team Manager.
  * **Request Body:**
    ```json
    {
      "profileImage": "https://example.com/images/janeNew.png",
      "userPreferences": {},
      "status": "inactive"
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "userId": 301,
      "organizationId": 201,
      "fullName": "Jane Doe",
      "email": "jane.doe@example.com",
      "status": "inactive",
      "createdBy": 12345,
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`DELETE /organizations/{organizationId}/users/{userId}`**

  * **Description:** Deletes a user (soft delete).
  * **Authorization:** Organization Administrator only.
  * **Response:** `204 No Content`

-----

## **4. Teams**

### **`POST /organizations/{organizationId}/teams`**

  * **Description:** Creates a new team within an organization.
  * **Authorization:** Organization Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "Customer Support",
      "description": "Team responsible for handling customer inquiries.",
      "configurations": {}
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "teamId": 401,
      "organizationId": 201,
      "name": "Customer Support",
      "description": "...",
      "configurations": {},
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`GET /organizations/{organizationId}/teams`**

  * **Description:** Retrieves a paginated list of all teams.
  * **Authorization:** Organization Administrator, Team Manager.
  * **Query Parameters:** `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "teamId": 401,
          "organizationId": 201,
          "name": "Customer Support",
          "description": "...",
          "configurations": {},
          "createdAt": "...",
          "updatedAt": "..."
        }
      ]
    }
    ```

### **`GET /organizations/{organizationId}/teams/{teamId}`**

  * **Description:** Retrieves a single team by its ID.
  * **Authorization:** Organization Administrator, Team Manager.
  * **Response:** `200 OK`
    ```json
    {
      "teamId": 401,
      "organizationId": 201,
      "name": "Customer Support",
      "description": "...",
      "configurations": {},
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`PUT /organizations/{organizationId}/teams/{teamId}`**

  * **Description:** Updates an existing team's information.
  * **Authorization:** Organization Administrator only.
  * **Request Body:**
    ```json
    {
      "description": "Updated description for the customer support team.",
      "configurations": {
        "isActive": true
      }
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "teamId": 401,
      "organizationId": 201,
      "name": "Customer Support",
      "description": "...",
      "configurations": {},
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`DELETE /organizations/{organizationId}/teams/{teamId}`**

  * **Description:** Deletes a team.
  * **Authorization:** Organization Administrator only.
  * **Response:** `204 No Content`

-----

## **5. Roles & Permissions**

### **`POST /organizations/{organizationId}/roles`**

  * **Description:** Creates a new custom role.
  * **Authorization:** Organization Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "Team Lead",
      "description": "A role with elevated permissions for team management.",
      "permissions": [
        "teams:read",
        "teams:update",
        "users:read"
      ]
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "roleId": 501,
      "organizationId": 201,
      "name": "Team Lead",
      "description": "...",
      "isCustom": true,
      "permissions": ["..."],
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`GET /organizations/{organizationId}/roles`**

  * **Description:** Retrieves a list of all predefined and custom roles.
  * **Authorization:** Organization Administrator.
  * **Response:** `200 OK`
    ```json
    [
      {
        "roleId": 1,
        "name": "Organization Admin",
        "description": "Full administrative access...",
        "isCustom": false
      },
      {
        "roleId": 501,
        "organizationId": 201,
        "name": "Team Lead",
        "description": "...",
        "isCustom": true
      }
    ]
    ```

### **`PUT /organizations/{organizationId}/roles/{roleId}`**

  * **Description:** Updates a custom role's information.
  * **Authorization:** Organization Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "Team Manager",
      "permissions": ["teams:read", "users:read", "users:update"]
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "roleId": 501,
      "organizationId": 201,
      "name": "Team Manager",
      "description": "...",
      "isCustom": true,
      "permissions": ["..."],
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`DELETE /organizations/{organizationId}/roles/{roleId}`**

  * **Description:** Deletes a custom role.
  * **Authorization:** Organization Administrator only.
  * **Response:** `204 No Content`

### **`GET /organizations/{organizationId}/permissions`**

  * **Description:** Retrieves a list of all available permissions.
  * **Authorization:** Organization Administrator only.
  * **Response:** `200 OK`
    ```json
    [
      "accounts:read",
      "organizations:read",
      "users:read",
      "users:create",
      "teams:read",
      "roles:read"
    ]
    ```

### **`POST /organizations/{organizationId}/users/{userId}/roles`**

  * **Description:** Assigns one or more roles to a user.
  * **Authorization:** Organization Administrator only.
  * **Request Body:**
    ```json
    {
      "roleIds": [501, 502]
    }
    ```
  * **Response:** `204 No Content`

### **`GET /organizations/{organizationId}/users/{userId}/roles`**

  * **Description:** Retrieves the list of roles assigned to a user.
  * **Authorization:** Organization Administrator, Team Manager.
  * **Response:** `200 OK`
    ```json
    [
      { "roleId": 501, "name": "Team Lead" },
      { "roleId": 502, "name": "Project Manager" }
    ]
    ```

### **`DELETE /organizations/{organizationId}/users/{userId}/roles/{roleId}`**

  * **Description:** Removes a specific role from a user.
  * **Authorization:** Organization Administrator only.
  * **Response:** `204 No Content`

### **`GET /organizations/{organizationId}/users/{userId}/permissions`**

  * **Description:** Retrieves all permissions granted to a specific user through their assigned roles.
  * **Authorization:** Organization Administrator, Team Manager, or the user themselves.
  * **Response:** `200 OK`
    ```json
    {
      "userId": 301,
      "permissions": [
        "teams:read",
        "teams:update", 
        "users:read",
        "users:create",
        "roles:read"
      ],
      "grantedBy": [
        {
          "roleId": 501,
          "roleName": "Team Lead",
          "permissions": ["teams:read", "teams:update", "users:read"]
        },
        {
          "roleId": 502,
          "roleName": "Project Manager", 
          "permissions": ["users:create", "roles:read"]
        }
      ]
    }
    ```

-----

## **6. Product Catalog**

### **`GET /productCatalog/products`**

  * **Description:** Retrieves a list of all products in the catalog.
  * **Authorization:** All authenticated users.
  * **Response:** `200 OK`
    ```json
    [
      {
        "productId": 701,
        "name": "Agents Platform",
        "description": "The flagship platform...",
        "status": "active",
        "modules": [{"moduleId": 1, "isIncluded": true}]
      }
    ]
    ```

### **`GET /productCatalog/products/{productId}`**

  * **Description:** Retrieves a single product by its ID.
  * **Authorization:** All authenticated users.
  * **Response:** `200 OK`
    ```json
    {
      "productId": 701,
      "name": "Agents Platform",
      "description": "The flagship platform...",
      "status": "active",
      "modules": [{"moduleId": 1, "isIncluded": true}]
    }
    ```

-----

## **7. Subscriptions**

### **`POST /organizations/{organizationId}/subscriptions`**

  * **Description:** Creates a new subscription for an organization.
  * **Authorization:** SaaS Administrator, SaaS Account Manager.
  * **Request Body:**
    ```json
    {
      "productId": 701,
      "startDate": "...",
      "endDate": "...",
      "status": "active",
      "planConfiguration": { "maxUsers": 50 }
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "subscriptionId": 801,
      "organizationId": 201,
      "productId": 701,
      "startDate": "...",
      "endDate": "...",
      "status": "active",
      "planConfiguration": {},
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`GET /organizations/{organizationId}/subscriptions`**

  * **Description:** Retrieves a list of all subscriptions for an organization.
  * **Authorization:** SaaS Administrator, SaaS Account Manager, Organization Administrator.
  * **Query Parameters:** `status`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "subscriptionId": 801,
          "organizationId": 201,
          "productId": 701,
          "startDate": "...",
          "endDate": "...",
          "status": "active",
          "planConfiguration": {}
        }
      ]
    }
    ```

### **`GET /organizations/{organizationId}/subscriptions/{subscriptionId}`**

  * **Description:** Retrieves a single subscription by its ID.
  * **Authorization:** SaaS Administrator, SaaS Account Manager, Organization Administrator.
  * **Response:** `200 OK`
    ```json
    {
      "subscriptionId": 801,
      "organizationId": 201,
      "productId": 701,
      "startDate": "...",
      "endDate": "...",
      "status": "active",
      "planConfiguration": {}
    }
    ```

### **`PUT /organizations/{organizationId}/subscriptions/{subscriptionId}`**

  * **Description:** Updates an existing subscription.
  * **Authorization:** SaaS Administrator, SaaS Account Manager.
  * **Request Body:**
    ```json
    {
      "endDate": "...",
      "status": "active",
      "planConfiguration": { "maxUsers": 75 }
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "subscriptionId": 801,
      "organizationId": 201,
      "productId": 701,
      "startDate": "...",
      "endDate": "...",
      "status": "active",
      "planConfiguration": {},
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

-----

## **8. Catalogs & Resources**

### **`POST /organizations/{organizationId}/catalogs`**

  * **Description:** Creates a new catalog within an organization.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Request Body:**
    ```json
    {
      "name": "Customer Documentation",
      "description": "Catalog containing help articles..."
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "catalogId": 901,
      "organizationId": 201,
      "name": "Customer Documentation",
      "description": "...",
      "status": "draft",
      "createdAt": "...",
      "updatedAt": "..."
    }
    ```

### **`GET /organizations/{organizationId}/catalogs`**

  * **Description:** Retrieves a list of all catalogs.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "catalogId": 901,
          "organizationId": 201,
          "name": "Customer Documentation",
          "description": "...",
          "status": "live"
        }
      ]
    }
    ```

### **`GET /organizations/{organizationId}/catalogs/{catalogId}`**

  * **Description:** Retrieves a single catalog by its ID.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Response:** `200 OK`
    ```json
    {
      "catalogId": 901,
      "organizationId": 201,
      "name": "Customer Documentation",
      "description": "...",
      "status": "live"
    }
    ```

### **`PUT /organizations/{organizationId}/catalogs/{catalogId}`**

  * **Description:** Updates the metadata for a catalog.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Request Body:**
    ```json
    {
      "name": "Customer Help Center",
      "description": "Updated name and description..."
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "catalogId": 901,
      "organizationId": 201,
      "name": "Customer Help Center",
      "description": "...",
      "status": "live"
    }
    ```

### **`DELETE /organizations/{organizationId}/catalogs/{catalogId}`**

  * **Description:** Deletes a catalog and its resources.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Response:** `204 No Content`

### **`POST /organizations/{organizationId}/catalogs/{catalogId}/resources`**

  * **Description:** Uploads a new resource to a catalog.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Request Body:** `multipart/form-data` or JSON with a URL.
    ```json
    {
      "resourceUrl": "https://example.com/docs/policy.pdf",
      "sourceType": "url",
      "metadata": { "title": "Refund Policy" }
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "resourceId": 951,
      "catalogId": 901,
      "resourceUrl": "...",
      "status": "processing",
      "metadata": {}
    }
    ```

### **`DELETE /organizations/{organizationId}/catalogs/{catalogId}/resources/{resourceId}`**

  * **Description:** Deletes a resource from a catalog.
  * **Authorization:** Organization Administrator, Catalog Manager.
  * **Response:** `204 No Content`

Of course. It's a good idea to document our progress. I will generate the complete specifications for the new modules we've designed in this session.

Here are the API specifications for the LLMs, Tools, and Agents modules, incorporating all of the revisions and enhancements we discussed.

-----

## **9. LLMs**

### `POST /llms`

  * **Description:** Adds a new LLM to the platform's central catalog.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "GPT-4 Turbo",
      "provider": "OpenAI",
      "modelIdentifier": "gpt-4-1106-preview",
      "description": "The latest GPT-4 model with a 128k context window.",
      "status": "active",
      "configurations": {
        "maxTokens": 4096,
        "supportsVision": true
      }
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "llmId": 1001,
      "name": "GPT-4 Turbo",
      "provider": "OpenAI",
      "modelIdentifier": "gpt-4-1106-preview",
      "description": "The latest GPT-4 model with a 128k context window.",
      "status": "active",
      "configurations": {
        "maxTokens": 4096,
        "supportsVision": true
      },
      "createdAt": "2025-08-21T11:00:00Z",
      "updatedAt": "2025-08-21T11:00:00Z"
    }
    ```

### `GET /llms`

  * **Description:** Retrieves a paginated list of all available LLMs. This is the read-only list that users will see when creating an agent.
  * **Authorization:** SaaS Administrator, Organization Administrator.
  * **Query Parameters:** `status`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "page": 1,
      "pageSize": 25,
      "totalPages": 1,
      "totalItems": 1,
      "items": [
        {
          "llmId": 1001,
          "name": "GPT-4 Turbo",
          "provider": "OpenAI",
          "modelIdentifier": "gpt-4-1106-preview",
          "description": "The latest GPT-4 model with a 128k context window.",
          "status": "active",
          "configurations": {
            "maxTokens": 4096,
            "supportsVision": true
          }
        }
      ]
    }
    ```

### `GET /llms/{llmId}`

  * **Description:** Retrieves a single LLM by its ID.
  * **Authorization:** SaaS Administrator, Organization Administrator.
  * **Response:** `200 OK`
    ```json
    {
      "llmId": 1001,
      "name": "GPT-4 Turbo",
      "provider": "OpenAI",
      "modelIdentifier": "gpt-4-1106-preview",
      "description": "The latest GPT-4 model with a 128k context window.",
      "status": "active",
      "configurations": {
        "maxTokens": 4096,
        "supportsVision": true
      },
      "createdAt": "2025-08-21T11:00:00Z",
      "updatedAt": "2025-08-21T11:00:00Z"
    }
    ```

### `PUT /llms/{llmId}`

  * **Description:** Updates an existing LLM's information.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "description": "Updated model description.",
      "status": "inactive",
      "configurations": {
        "maxTokens": 8192,
        "supportsVision": true
      }
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "llmId": 1001,
      "name": "GPT-4 Turbo",
      "provider": "OpenAI",
      "modelIdentifier": "gpt-4-1106-preview",
      "description": "Updated model description.",
      "status": "inactive",
      "configurations": {
        "maxTokens": 8192,
        "supportsVision": true
      },
      "createdAt": "2025-08-21T11:00:00Z",
      "updatedAt": "2025-08-21T12:30:00Z"
    }
    ```

### `DELETE /llms/{llmId}`

  * **Description:** Deletes an LLM from the platform.
  * **Authorization:** SaaS Administrator only.
  * **Response:** `204 No Content`

## **10. Tools**

This section is divided into two parts: managing the global catalog of tools and managing which tools are enabled for each organization.

### **10.1. Tool Catalog Management (SaaS Admin)**

These endpoints are for managing the master list of tools available on the platform.

#### `POST /tools`

  * **Description:** Adds a new tool to the platform's central catalog.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "name": "Internal CRM Lookup",
      "description": "A tool to look up customer information from the internal CRM.",
      "status": "active",
      "configurationsSchema": {
        "type": "object",
        "properties": {
          "api_key": { "type": "string", "description": "API Key for the CRM" },
          "base_url": { "type": "string", "description": "Base URL of the CRM API" }
        },
        "required": ["api_key", "base_url"]
      }
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "toolId": 2001,
      "name": "Internal CRM Lookup",
      "description": "A tool to look up customer information from the internal CRM.",
      "status": "active",
      "configurationsSchema": { "...": "..." },
      "createdAt": "2025-08-22T09:00:00Z",
      "updatedAt": "2025-08-22T09:00:00Z"
    }
    ```

#### `GET /tools`

  * **Description:** Retrieves a paginated list of all tools in the central catalog.
  * **Authorization:** SaaS Administrator only.
  * **Query Parameters:** `page`, `pageSize`
  * **Response:** `200 OK` with a paginated list of tool objects.

#### `PUT /tools/{toolId}`

  * **Description:** Updates an existing tool in the central catalog.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "description": "An updated description for the CRM lookup tool.",
      "status": "inactive"
    }
    ```
  * **Response:** `200 OK` with the updated tool object.

### **10.2. Organization Tool Access**

#### `PUT /organizations/{organizationId}/tools`

  * **Description:** Sets the complete list of enabled tools for a specific organization. This single endpoint is used to add, update, and remove tool access. To disable a tool, simply omit it from the `toolIds` array in the request.
  * **Authorization:** SaaS Administrator only.
  * **Request Body:**
    ```json
    {
      "toolIds": [2001, 2005]
    }
    ```
  * **Response:** `204 No Content`

#### `GET /organizations/{organizationId}/tools`

  * **Description:** Retrieves a list of all tools currently enabled and available for a specific organization. This is the list users will see.
  * **Authorization:** Organization Administrator, Team Manager, User.
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "toolId": 2001,
          "name": "Internal CRM Lookup",
          "description": "A tool to look up customer information from the internal CRM.",
          "configurationsSchema": { "...": "..." }
        },
        {
          "toolId": 2005,
          "name": "Google Search",
          "description": "A tool to perform a web search.",
          "configurationsSchema": { "...": "..." }
        }
      ]
    }
    ```

## **11. Agents**

### `POST /organizations/{organizationId}/agents`

  * **Description:** Creates a new AI agent (Version 1) within an organization.
  * **Authorization:** All authenticated users within the organization.
  * **Request Body:**
    ```json
    {
      "name": "Customer Support Agent",
      "description": "Handles initial customer support inquiries.",
      "prompt": "You are a friendly and helpful customer support agent for our company. Use the provided knowledge base to answer questions accurately.",
      "llmId": 1001,
      "llmSettings": {
        "temperature": 0.7,
        "maxTokens": 2048
      },
      "selectedTools": [
        {
          "toolId": 2001,
          "configurations": {
            "api_key": "user_provided_crm_key",
            "base_url": "https://crm.example.com/api"
          }
        }
      ]
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "agentId": 3001,
      "organizationId": 201,
      "version": 1,
      "name": "Customer Support Agent",
      "description": "Handles initial customer support inquiries.",
      "prompt": "You are a friendly and helpful customer support agent...",
      "llmId": 1001,
      "llmSettings": {
        "temperature": 0.7,
        "maxTokens": 2048
      },
      "selectedTools": [
        {
          "toolId": 2001,
          "configurations": {
            "api_key": "user_provided_crm_key",
            "base_url": "https://crm.example.com/api"
          }
        }
      ],
      "createdBy": 301,
      "createdAt": "2025-08-19T15:30:00Z",
      "updatedAt": "2025-08-19T15:30:00Z"
    }
    ```

### `GET /organizations/{organizationId}/agents`

  * **Description:** Retrieves a paginated list of the latest versions of all agents within an organization.
  * **Authorization:** All authenticated users within the organization.
  * **Query Parameters:** `page`, `pageSize`
  * **Response:** `200 OK` with a paginated list of agent objects.

### `GET /organizations/{organizationId}/agents/{agentId}`

  * **Description:** Retrieves the latest version of a single agent by its ID.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK` with the full agent object, including the current version number.

### `PUT /organizations/{organizationId}/agents/{agentId}`

  * **Description:** Updates an existing agent. This action creates a new version of the agent. The request **must** include the current version number to prevent conflicts.
  * **Authorization:** All authenticated users within the organization.
  * **Request Body:**
    ```json
    {
      "version": 1,
      "name": "Advanced Customer Agent",
      "prompt": "You are an advanced support agent. You are direct and concise.",
      "llmSettings": {
        "temperature": 0.5
      }
    }
    ```
  * **Success Response:** `200 OK` with the updated agent object and the new, incremented version number (e.g., `version: 2`).
  * **Error Response:** `409 Conflict` if the provided `version` in the request body does not match the current version of the agent in the database.

### `DELETE /organizations/{organizationId}/agents/{agentId}`

  * **Description:** Deletes an agent and all its version history.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `204 No Content`

### **Agent Versioning**

#### `GET /organizations/{organizationId}/agents/{agentId}/versions`

  * **Description:** Retrieves a list of all saved versions for a specific agent, showing metadata for each version.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "version": 2,
          "updatedAt": "2025-08-20T10:00:00Z",
          "updatedBy": 301
        },
        {
          "version": 1,
          "updatedAt": "2025-08-19T15:30:00Z",
          "updatedBy": 301
        }
      ]
    }
    ```

#### `POST /organizations/{organizationId}/agents/{agentId}/versions/{versionNumber}/restore`

  * **Description:** Restores a previous version of an agent, making it the new latest version. This will create a new version (e.g., restoring version 1 will create a new version 3 with the content of version 1).
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK` with the newly created agent version object.

----

Of course. After a thorough review of the existing API specifications and the product requirement documents, the next logical resource to specify is the **Channels** module. This module is essential for deploying the agents you've defined.

Here are the complete API endpoint specifications for the Channels module, continuing the format and quality from your existing work.

-----

## **12. Channels**

### **12.1. Channel Types**

#### `GET /channel-types`

  * **Description:** Retrieves a list of all available channel types supported by the platform (e.g., WhatsApp, Web Chat). This is a global, read-only list.
  * **Authorization:** All authenticated users.
  * **Response:** `200 OK`
    ```json
    [
      {
        "channelTypeId": 1,
        "name": "Web Chat",
        "description": "Deploy an agent to a customizable chat widget on your website."
      },
      {
        "channelTypeId": 2,
        "name": "WhatsApp",
        "description": "Connect an agent to a WhatsApp business number."
      }
    ]
    ```

### **12.2. Organization Channel Instances**

#### `POST /organizations/{organizationId}/channels`

  * **Description:** Creates a new channel instance for an organization. The request body will vary based on the `channelTypeId`.
  * **Authorization:** Organization Administrator.
  * **Request Body (for Web Chat):**
    ```json
    {
      "channelTypeId": 1,
      "name": "Main Website Chat",
      "configurations": {
        "logoUrl": "https://example.com/logos/main-chat.png",
        "primaryColor": "#3B82F6",
        "welcomeMessage": "Hello! How can I help you today?"
      }
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "channelId": 4001,
      "organizationId": 201,
      "channelTypeId": 1,
      "name": "Main Website Chat",
      "status": "active",
      "configurations": {
        "logoUrl": "https://example.com/logos/main-chat.png",
        "primaryColor": "#3B82F6",
        "welcomeMessage": "Hello! How can I help you today?",
        "widgetScript": "<script src='https://cdn.agents-platform.com/widget/4001.js'></script>"
      },
      "createdAt": "2025-08-23T10:00:00Z",
      "updatedAt": "2025-08-23T10:00:00Z"
    }
    ```

#### `GET /organizations/{organizationId}/channels`

  * **Description:** Retrieves a list of all channel instances configured for a specific organization.
  * **Authorization:** Organization Administrator.
  * **Query Parameters:** `status`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "channelId": 4001,
          "organizationId": 201,
          "channelTypeId": 1,
          "name": "Main Website Chat",
          "status": "active",
          "createdAt": "2025-08-23T10:00:00Z"
        }
      ]
    }
    ```

#### `GET /organizations/{organizationId}/channels/{channelId}`

  * **Description:** Retrieves a single channel instance by its ID.
  * **Authorization:** Organization Administrator.
  * **Response:** `200 OK`
    ```json
    {
      "channelId": 4001,
      "organizationId": 201,
      "channelTypeId": 1,
      "name": "Main Website Chat",
      "status": "active",
      "configurations": {
        "logoUrl": "https://example.com/logos/main-chat.png",
        "primaryColor": "#3B82F6",
        "welcomeMessage": "Hello! How can I help you today?",
        "widgetScript": "<script src='https://cdn.agents-platform.com/widget/4001.js'></script>"
      },
      "createdAt": "2025-08-23T10:00:00Z",
      "updatedAt": "2025-08-23T10:00:00Z"
    }
    ```

#### `PUT /organizations/{organizationId}/channels/{channelId}`

  * **Description:** Updates an existing channel instance's configuration.
  * **Authorization:** Organization Administrator.
  * **Request Body:**
    ```json
    {
      "name": "Primary Website Chat Widget",
      "configurations": {
        "primaryColor": "#000000",
        "welcomeMessage": "Welcome to our website! Ask me anything."
      }
    }
    ```
  * **Response:** `200 OK` with the updated channel instance object.

#### `DELETE /organizations/{organizationId}/channels/{channelId}`

  * **Description:** Deletes a channel instance.
  * **Authorization:** Organization Administrator.
  * **Response:** `204 No Content`

-----

## **13. Integrations**

The Integrations module enables users to connect their agents and flows to external systems through webhooks and REST API calls. This module supports both incoming webhooks (for receiving data) and outgoing API calls (for sending data to external systems).

### **13.1. Webhook Integrations**

Webhook integrations allow external systems to send data to the platform, which can then be processed by flows and agents.

#### `POST /organizations/{organizationId}/webhooks`

  * **Description:** Creates a new webhook integration for receiving data from external systems.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Request Body:**
    ```json
    {
      "name": "Customer Order Webhook",
      "description": "Receives order notifications from the e-commerce system.",
      "channelId": 4001,
      "samplePayload": "{\n  \"orderId\": \"ORD-12345\",\n  \"customerEmail\": \"customer@example.com\",\n  \"orderTotal\": 299.99,\n  \"items\": [\n    {\n      \"productId\": \"PROD-001\",\n      \"quantity\": 2,\n      \"price\": 149.99\n    }\n  ]\n}",
      "jsonPathMappings": [
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.customerEmail",
          "description": "Extract customer email for personalization"
        },
        {
          "key": "orderTotal",
          "name": "Order Amount",
          "jsonPath": "$.orderTotal",
          "description": "Extract order total for notifications"
        }
      ],
      "isActive": true
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "webhookId": 5001,
      "organizationId": 201,
      "channelId": 4001,
      "name": "Customer Order Webhook",
      "description": "Receives order notifications from the e-commerce system.",
      "webhookUrl": "https://api.agents-platform.com/webhooks/5001/abc123def456",
      "secretKey": "whsec_abc123def456",
      "samplePayload": "{\n  \"orderId\": \"ORD-12345\",\n  \"customerEmail\": \"customer@example.com\",\n  \"orderTotal\": 299.99,\n  \"items\": [\n    {\n      \"productId\": \"PROD-001\",\n      \"quantity\": 2,\n      \"price\": 149.99\n    }\n  ]\n}",
      "jsonPathMappings": [
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.customerEmail",
          "description": "Extract customer email for personalization"
        },
        {
          "key": "orderTotal",
          "name": "Order Amount",
          "jsonPath": "$.orderTotal",
          "description": "Extract order total for notifications"
        }
      ],
      "isActive": true,
      "createdBy": 301,
      "createdAt": "2025-08-24T14:30:00Z",
      "updatedAt": "2025-08-24T14:30:00Z"
    }
    ```

#### `GET /organizations/{organizationId}/webhooks`

  * **Description:** Retrieves a paginated list of all webhook integrations for an organization.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Query Parameters:** `isActive`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "page": 1,
      "pageSize": 25,
      "totalPages": 1,
      "totalItems": 2,
      "items": [
        {
          "webhookId": 5001,
          "organizationId": 201,
          "channelId": 4001,
          "name": "Customer Order Webhook",
          "description": "Receives order notifications from the e-commerce system.",
          "webhookUrl": "https://api.agents-platform.com/webhooks/5001/abc123def456",
          "isActive": true,
          "createdAt": "2025-08-24T14:30:00Z"
        },
        {
          "webhookId": 5002,
          "organizationId": 201,
          "channelId": 4002,
          "name": "Support Ticket Webhook",
          "description": "Receives new support ticket notifications.",
          "webhookUrl": "https://api.agents-platform.com/webhooks/5002/def456ghi789",
          "isActive": false,
          "createdAt": "2025-08-25T09:15:00Z"
        }
      ]
    }
    ```

#### `GET /organizations/{organizationId}/webhooks/{webhookId}`

  * **Description:** Retrieves a single webhook integration by its ID.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Response:** `200 OK`
    ```json
    {
      "webhookId": 5001,
      "organizationId": 201,
      "channelId": 4001,
      "name": "Customer Order Webhook",
      "description": "Receives order notifications from the e-commerce system.",
      "webhookUrl": "https://api.agents-platform.com/webhooks/5001/abc123def456",
      "secretKey": "whsec_abc123def456",
      "samplePayload": "{\n  \"orderId\": \"ORD-12345\",\n  \"customerEmail\": \"customer@example.com\",\n  \"orderTotal\": 299.99,\n  \"items\": [\n    {\n      \"productId\": \"PROD-001\",\n      \"quantity\": 2,\n      \"price\": 149.99\n    }\n  ]\n}",
      "jsonPathMappings": [
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.customerEmail",
          "description": "Extract customer email for personalization"
        },
        {
          "key": "orderTotal",
          "name": "Order Amount",
          "jsonPath": "$.orderTotal",
          "description": "Extract order total for notifications"
        }
      ],
      "isActive": true,
      "createdBy": 301,
      "createdAt": "2025-08-24T14:30:00Z",
      "updatedAt": "2025-08-24T14:30:00Z"
    }
    ```

#### `PUT /organizations/{organizationId}/webhooks/{webhookId}`

  * **Description:** Updates an existing webhook integration's configuration.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Request Body:**
    ```json
    {
      "name": "Updated Order Webhook",
      "description": "Updated description for the order webhook.",
      "channelId": 4001,
      "samplePayload": "{\n  \"orderId\": \"ORD-12345\",\n  \"customerEmail\": \"customer@example.com\",\n  \"orderTotal\": 299.99,\n  \"status\": \"confirmed\"\n}",
      "jsonPathMappings": [
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.customerEmail",
          "description": "Extract customer email for personalization"
        },
        {
          "key": "orderStatus",
          "name": "Order Status",
          "jsonPath": "$.status",
          "description": "Extract order status for notifications"
        }
      ],
      "isActive": false
    }
    ```
  * **Response:** `200 OK` with the updated webhook integration object.

#### `DELETE /organizations/{organizationId}/webhooks/{webhookId}`

  * **Description:** Deletes a webhook integration.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Response:** `204 No Content`

#### `POST /organizations/{organizationId}/webhooks/{webhookId}/regenerate-secret`

  * **Description:** Regenerates the secret key for a webhook integration. This invalidates the previous secret key.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Response:** `200 OK`
    ```json
    {
      "webhookId": 5001,
      "secretKey": "whsec_new123secret456",
      "updatedAt": "2025-08-24T16:45:00Z"
    }
    ```

### **13.2. REST API Integrations**

REST API integrations allow the platform to make outgoing calls to external systems, which can be used within flows and agent tools. Each integration represents a single API endpoint with unified parameter and response mapping structures.

#### `POST /organizations/{organizationId}/api-integrations`

  * **Description:** Creates a new REST API integration for making calls to external systems.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Request Body:**
    ```json
    {
      "name": "CRM Customer Lookup",
      "description": "Retrieve customer information from the CRM system by ID.",
      "url": "https://crm.example.com/api/v1/customers/{customerId}",
      "method": "GET",
      "headers": [
        {
          "key": "Authorization",
          "value": "Bearer crm_api_token_12345"
        },
        {
          "key": "Content-Type",
          "value": "application/json"
        }
      ],
      "parameters": [
        {
          "key": "customerId",
          "name": "Customer ID",
          "type": "path",
          "required": true,
          "description": "The customer ID to look up"
        }
      ],
      "requestBody": null,
      "responseMappings": [
        {
          "key": "customerName",
          "name": "Customer Name",
          "jsonPath": "$.name",
          "description": "Extract customer name from response"
        },
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.email",
          "description": "Extract customer email from response"
        },
        {
          "key": "customerPhone",
          "name": "Customer Phone",
          "jsonPath": "$.phone",
          "description": "Extract customer phone from response"
        }
      ],
      "isActive": true
    }
    ```

**Additional Examples for Different HTTP Methods:**
```json
{
  "name": "Create Customer",
  "description": "Create a new customer in the CRM system.",
  "url": "https://crm.example.com/api/v1/customers",
  "method": "POST",
  "headers": [
    {
      "key": "Authorization",
      "value": "Bearer crm_api_token_12345"
    },
    {
      "key": "Content-Type",
      "value": "application/json"
    }
  ],
  "parameters": [],
  "requestBody": "{\n  \"name\": \"{customerName}\",\n  \"email\": \"{customerEmail}\",\n  \"phone\": \"{customerPhone}\"\n}",
  "responseMappings": [
    {
      "key": "customerId",
      "name": "Customer ID",
      "jsonPath": "$.id",
      "description": "Extract the created customer ID"
    },
    {
      "key": "status",
      "name": "Status",
      "jsonPath": "$.status",
      "description": "Extract the creation status"
    }
  ]
}
```

**GET with Query Parameters:**
```json
{
  "name": "Search Customers",
  "description": "Search customers by email or name.",
  "url": "https://crm.example.com/api/v1/customers/search",
  "method": "GET",
  "headers": [
    {
      "key": "Authorization",
      "value": "Bearer crm_api_token_12345"
    }
  ],
  "parameters": [
    {
      "key": "email",
      "name": "Email",
      "type": "query",
      "required": false,
      "description": "Search by customer email"
    },
    {
      "key": "name",
      "name": "Name",
      "type": "query",
      "required": false,
      "description": "Search by customer name"
    }
  ],
  "requestBody": null,
  "responseMappings": [
    {
      "key": "customers",
      "name": "Customers",
      "jsonPath": "$.customers",
      "description": "Extract the list of customers"
    },
    {
      "key": "totalCount",
      "name": "Total Count",
      "jsonPath": "$.totalCount",
      "description": "Extract the total number of results"
    }
  ]
}
```

**PUT with Path and Query Parameters:**
```json
{
  "name": "Update Customer",
  "description": "Update customer information by ID.",
  "url": "https://crm.example.com/api/v1/customers/{customerId}?version={version}",
  "method": "PUT",
  "headers": [
    {
      "key": "Authorization",
      "value": "Bearer crm_api_token_12345"
    },
    {
      "key": "Content-Type",
      "value": "application/json"
    }
  ],
  "parameters": [
    {
      "key": "customerId",
      "name": "Customer ID",
      "type": "path",
      "required": true,
      "description": "The customer ID to update"
    },
    {
      "key": "version",
      "name": "Version",
      "type": "query",
      "required": false,
      "description": "API version for optimistic locking"
    }
  ],
  "requestBody": "{\n  \"name\": \"{customerName}\",\n  \"email\": \"{customerEmail}\"\n}",
  "responseMappings": [
    {
      "key": "updatedAt",
      "name": "Updated At",
      "jsonPath": "$.updatedAt",
      "description": "Extract the update timestamp"
    },
    {
      "key": "version",
      "name": "New Version",
      "jsonPath": "$.version",
      "description": "Extract the new version number"
    }
  ]
}
```

  * **Response:** `201 Created`
    ```json
    {
      "apiIntegrationId": 6001,
      "organizationId": 201,
      "name": "CRM Customer Lookup",
      "description": "Retrieve customer information from the CRM system by ID.",
      "url": "https://crm.example.com/api/v1/customers/{customerId}",
      "method": "GET",
      "headers": [
        {
          "key": "Authorization",
          "value": "Bearer crm_api_token_12345"
        },
        {
          "key": "Content-Type",
          "value": "application/json"
        }
      ],
      "parameters": [
        {
          "key": "customerId",
          "name": "Customer ID",
          "type": "path",
          "required": true,
          "description": "The customer ID to look up"
        }
      ],
      "requestBody": null,
      "responseMappings": [
        {
          "key": "customerName",
          "name": "Customer Name",
          "jsonPath": "$.name",
          "description": "Extract customer name from response"
        },
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.email",
          "description": "Extract customer email from response"
        },
        {
          "key": "customerPhone",
          "name": "Customer Phone",
          "jsonPath": "$.phone",
          "description": "Extract customer phone from response"
        }
      ],
      "isActive": true,
      "createdBy": 301,
      "createdAt": "2025-08-24T15:00:00Z",
      "updatedAt": "2025-08-24T15:00:00Z"
    }
    ```

#### `GET /organizations/{organizationId}/api-integrations`

  * **Description:** Retrieves a paginated list of all REST API integrations for an organization.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Query Parameters:** `isActive`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "page": 1,
      "pageSize": 25,
      "totalPages": 1,
      "totalItems": 2,
      "items": [
        {
          "apiIntegrationId": 6001,
          "organizationId": 201,
          "name": "CRM Customer Lookup",
          "description": "Retrieve customer information from the CRM system by ID.",
          "url": "https://crm.example.com/api/v1/customers/{customerId}",
          "method": "GET",
          "isActive": true,
          "createdAt": "2025-08-24T15:00:00Z"
        },
        {
          "apiIntegrationId": 6002,
          "organizationId": 201,
          "name": "Create Customer",
          "description": "Create a new customer in the CRM system.",
          "url": "https://crm.example.com/api/v1/customers",
          "method": "POST",
          "isActive": true,
          "createdAt": "2025-08-25T10:30:00Z"
        }
      ]
    }
    ```

#### `GET /organizations/{organizationId}/api-integrations/{apiIntegrationId}`

  * **Description:** Retrieves a single REST API integration by its ID.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Response:** `200 OK`
    ```json
    {
      "apiIntegrationId": 6001,
      "organizationId": 201,
      "name": "CRM Customer Lookup",
      "description": "Retrieve customer information from the CRM system by ID.",
      "url": "https://crm.example.com/api/v1/customers/{customerId}",
      "method": "GET",
      "headers": [
        {
          "key": "Authorization",
          "value": "Bearer crm_api_token_12345"
        },
        {
          "key": "Content-Type",
          "value": "application/json"
        }
      ],
      "parameters": [
        {
          "key": "customerId",
          "name": "Customer ID",
          "type": "path",
          "required": true,
          "description": "The customer ID to look up"
        }
      ],
      "requestBody": null,
      "responseMappings": [
        {
          "key": "customerName",
          "name": "Customer Name",
          "jsonPath": "$.name",
          "description": "Extract customer name from response"
        },
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.email",
          "description": "Extract customer email from response"
        },
        {
          "key": "customerPhone",
          "name": "Customer Phone",
          "jsonPath": "$.phone",
          "description": "Extract customer phone from response"
        }
      ],
      "isActive": true,
      "createdBy": 301,
      "createdAt": "2025-08-24T15:00:00Z",
      "updatedAt": "2025-08-24T15:00:00Z"
    }
    ```

#### `PUT /organizations/{organizationId}/api-integrations/{apiIntegrationId}`

  * **Description:** Updates an existing REST API integration's configuration.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Request Body:**
    ```json
    {
      "name": "Updated CRM Integration",
      "description": "Updated description for the CRM integration.",
      "url": "https://crm.example.com/api/v1/customers/{customerId}",
      "method": "GET",
      "headers": [
        {
          "key": "Authorization",
          "value": "Bearer new_crm_api_token_67890"
        },
        {
          "key": "Content-Type",
          "value": "application/json"
        }
      ],
      "parameters": [
        {
          "key": "customerId",
          "name": "Customer ID",
          "type": "path",
          "required": true,
          "description": "The customer ID to look up"
        }
      ],
      "requestBody": null,
      "responseMappings": [
        {
          "key": "customerName",
          "name": "Customer Name",
          "jsonPath": "$.name",
          "description": "Extract customer name from response"
        },
        {
          "key": "customerEmail",
          "name": "Customer Email",
          "jsonPath": "$.email",
          "description": "Extract customer email from response"
        },
        {
          "key": "customerPhone",
          "name": "Customer Phone",
          "jsonPath": "$.phone",
          "description": "Extract customer phone from response"
        },
        {
          "key": "customerStatus",
          "name": "Customer Status",
          "jsonPath": "$.status",
          "description": "Extract customer status from response"
        }
      ],
      "isActive": false
    }
    ```
  * **Response:** `200 OK` with the updated API integration object.

#### `DELETE /organizations/{organizationId}/api-integrations/{apiIntegrationId}`

  * **Description:** Deletes a REST API integration.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Response:** `204 No Content`

### **13.3. API Testing & Validation**

#### `POST /organizations/{organizationId}/api-integrations/{apiIntegrationId}/test`

  * **Description:** Tests an API integration with provided parameters and request body.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Request Body:**
    ```json
    {
      "parameters": {
        "customerId": "CUST-12345"
      },
      "requestBody": null
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "success": true,
      "statusCode": 200,
      "responseHeaders": {
        "content-type": "application/json",
        "x-rate-limit-remaining": "999"
      },
      "responseBody": {
        "id": "CUST-12345",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "status": "active"
      },
      "extractedData": {
        "customerName": "John Doe",
        "customerEmail": "john.doe@example.com",
        "customerPhone": "+1234567890"
      },
      "executionTime": 245
    }
    ```

#### `POST /organizations/{organizationId}/api-integrations/{apiIntegrationId}/validate`

  * **Description:** Validates the configuration of an API integration without making actual API calls.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Response:** `200 OK`
    ```json
    {
      "valid": true,
      "validationResults": {
        "url": {
          "valid": true,
          "issues": []
        },
        "headers": {
          "valid": true,
          "issues": []
        },
        "parameters": {
          "valid": true,
          "issues": []
        },
        "requestBody": {
          "valid": true,
          "issues": []
        },
        "responseMappings": {
          "valid": true,
          "issues": []
        }
      }
    }
    ```

### **13.4. Integration Analytics**

#### `GET /organizations/{organizationId}/integrations/analytics`

  * **Description:** Retrieves analytics data for all integrations within an organization.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Query Parameters:** `startDate`, `endDate`, `integrationType` (webhook|api)
  * **Response:** `200 OK`
    ```json
    {
      "period": {
        "startDate": "2025-08-01T00:00:00Z",
        "endDate": "2025-08-31T23:59:59Z"
      },
      "webhooks": {
        "totalCalls": 1250,
        "successfulCalls": 1180,
        "failedCalls": 70,
        "averageResponseTime": 145
      },
      "apiIntegrations": {
        "totalCalls": 890,
        "successfulCalls": 845,
        "failedCalls": 45,
        "averageResponseTime": 320
      },
      "topIntegrations": [
        {
          "integrationId": 5001,
          "name": "Customer Order Webhook",
          "type": "webhook",
          "callCount": 450,
          "successRate": 96.2
        },
        {
          "integrationId": 6001,
          "name": "CRM Customer Lookup",
          "type": "api",
          "callCount": 320,
          "successRate": 94.8
        }
      ]
    }
    ```

#### `GET /organizations/{organizationId}/integrations/{integrationId}/analytics`

  * **Description:** Retrieves detailed analytics for a specific integration.
  * **Authorization:** Organization Administrator, Integration Manager.
  * **Query Parameters:** `startDate`, `endDate`
  * **Response:** `200 OK`
    ```json
    {
      "integrationId": 5001,
      "name": "Customer Order Webhook",
      "type": "webhook",
      "period": {
        "startDate": "2025-08-01T00:00:00Z",
        "endDate": "2025-08-31T23:59:59Z"
      },
      "metrics": {
        "totalCalls": 450,
        "successfulCalls": 433,
        "failedCalls": 17,
        "successRate": 96.2,
        "averageResponseTime": 145,
        "peakHour": 14,
        "peakDay": "Monday"
      },
      "recentActivity": [
        {
          "timestamp": "2025-08-31T15:30:00Z",
          "status": "success",
          "responseTime": 120,
          "payloadSize": 1024
        },
        {
          "timestamp": "2025-08-31T15:25:00Z",
          "status": "failed",
          "error": "Invalid JSON payload",
          "responseTime": 50
        }
      ]
    }
    ```

-----

## **14. Flows**

**TODO: The `flowJson` structure in this specification is a conceptual representation. It should be adapted to match the actual structure implemented by the frontend visual workflow builder (e.g., React Flow, Node-RED, or similar library). The current structure serves as a reference for the expected data format.**

The Flows module provides a visual workflow builder for designing multi-channel conversation logic. Flows enable users to create complex automated workflows that combine agents, channels, and integrations into cohesive conversation experiences.

### **14.1. Flow Management**

#### `POST /organizations/{organizationId}/flows`

  * **Description:** Creates a new flow (Version 1) within an organization.
  * **Authorization:** All authenticated users within the organization.
  * **Request Body:**
    ```json
    {
      "name": "Customer Support Flow",
      "description": "Handles initial customer inquiries and routes to appropriate agents.",
      "channelId": 4001,
      "status": "draft",
      "flowJson": {
        "nodes": [
          {
            "id": "node-1",
            "type": "trigger",
            "position": { "x": 100, "y": 100 },
            "data": {
              "triggerType": "webhook",
              "webhookId": 5001,
              "eventType": "message_received"
            }
          },
          {
            "id": "node-2",
            "type": "condition",
            "position": { "x": 300, "y": 100 },
            "data": {
              "conditionType": "text_contains",
              "field": "message",
              "value": "support",
              "operator": "contains"
            }
          },
          {
            "id": "node-3",
            "type": "action",
            "position": { "x": 500, "y": 50 },
            "data": {
              "actionType": "send_message",
              "message": "Welcome to our support! How can I help you today?",
              "channelId": 4001
            }
          },
          {
            "id": "node-4",
            "type": "action",
            "position": { "x": 500, "y": 150 },
            "data": {
              "actionType": "call_agent",
              "agentId": 3001,
              "inputMapping": {
                "customerMessage": "message",
                "customerEmail": "customerEmail"
              }
            }
          }
        ],
        "edges": [
          {
            "id": "edge-1",
            "source": "node-1",
            "target": "node-2",
            "sourceHandle": "output",
            "targetHandle": "input"
          },
          {
            "id": "edge-2",
            "source": "node-2",
            "target": "node-3",
            "sourceHandle": "true",
            "targetHandle": "input"
          },
          {
            "id": "edge-3",
            "source": "node-2",
            "target": "node-4",
            "sourceHandle": "false",
            "targetHandle": "input"
          }
        ],
        "viewport": { "x": 0, "y": 0, "zoom": 1 }
      }
    }
    ```
  * **Response:** `201 Created`
    ```json
    {
      "flowId": 7001,
      "organizationId": 201,
      "version": 1,
      "name": "Customer Support Flow",
      "description": "Handles initial customer inquiries and routes to appropriate agents.",
      "channelId": 4001,
      "status": "draft",
      "flowJson": {
        "nodes": [...],
        "edges": [...],
        "viewport": { "x": 0, "y": 0, "zoom": 1 }
      },
      "createdBy": 301,
      "createdAt": "2025-08-26T10:00:00Z",
      "updatedAt": "2025-08-26T10:00:00Z"
    }
    ```

#### `GET /organizations/{organizationId}/flows`

  * **Description:** Retrieves a paginated list of the latest versions of all flows within an organization.
  * **Authorization:** All authenticated users within the organization.
  * **Query Parameters:** `status`, `channelId`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "page": 1,
      "pageSize": 25,
      "totalPages": 1,
      "totalItems": 2,
      "items": [
        {
          "flowId": 7001,
          "organizationId": 201,
          "version": 2,
          "name": "Customer Support Flow",
          "description": "Handles initial customer inquiries and routes to appropriate agents.",
          "channelId": 4001,
          "status": "live",
          "createdAt": "2025-08-26T10:00:00Z",
          "updatedAt": "2025-08-26T15:30:00Z"
        },
        {
          "flowId": 7002,
          "organizationId": 201,
          "version": 1,
          "name": "Lead Qualification Flow",
          "description": "Automated lead qualification and routing.",
          "channelId": 4002,
          "status": "draft",
          "createdAt": "2025-08-27T09:15:00Z",
          "updatedAt": "2025-08-27T09:15:00Z"
        }
      ]
    }
    ```

#### `GET /organizations/{organizationId}/flows/{flowId}`

  * **Description:** Retrieves the latest version of a single flow by its ID.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK`
    ```json
    {
      "flowId": 7001,
      "organizationId": 201,
      "version": 2,
      "name": "Customer Support Flow",
      "description": "Handles initial customer inquiries and routes to appropriate agents.",
      "channelId": 4001,
      "status": "live",
      "flowJson": {
        "nodes": [
          {
            "id": "node-1",
            "type": "trigger",
            "position": { "x": 100, "y": 100 },
            "data": {
              "triggerType": "webhook",
              "webhookId": 5001,
              "eventType": "message_received"
            }
          },
          {
            "id": "node-2",
            "type": "condition",
            "position": { "x": 300, "y": 100 },
            "data": {
              "conditionType": "text_contains",
              "field": "message",
              "value": "support",
              "operator": "contains"
            }
          },
          {
            "id": "node-3",
            "type": "action",
            "position": { "x": 500, "y": 50 },
            "data": {
              "actionType": "send_message",
              "message": "Welcome to our support! How can I help you today?",
              "channelId": 4001
            }
          },
          {
            "id": "node-4",
            "type": "action",
            "position": { "x": 500, "y": 150 },
            "data": {
              "actionType": "call_agent",
              "agentId": 3001,
              "inputMapping": {
                "customerMessage": "message",
                "customerEmail": "customerEmail"
              }
            }
          }
        ],
        "edges": [
          {
            "id": "edge-1",
            "source": "node-1",
            "target": "node-2",
            "sourceHandle": "output",
            "targetHandle": "input"
          },
          {
            "id": "edge-2",
            "source": "node-2",
            "target": "node-3",
            "sourceHandle": "true",
            "targetHandle": "input"
          },
          {
            "id": "edge-3",
            "source": "node-2",
            "target": "node-4",
            "sourceHandle": "false",
            "targetHandle": "input"
          }
        ],
        "viewport": { "x": 0, "y": 0, "zoom": 1 }
      },
      "createdBy": 301,
      "createdAt": "2025-08-26T10:00:00Z",
      "updatedAt": "2025-08-26T15:30:00Z"
    }
    ```

#### `PUT /organizations/{organizationId}/flows/{flowId}`

  * **Description:** Updates an existing flow. This action creates a new version of the flow. The request **must** include the current version number to prevent conflicts.
  * **Authorization:** All authenticated users within the organization.
  * **Request Body:**
    ```json
    {
      "version": 2,
      "name": "Enhanced Customer Support Flow",
      "description": "Updated customer support flow with improved routing logic.",
      "status": "live",
      "flowJson": {
        "nodes": [
          {
            "id": "node-1",
            "type": "trigger",
            "position": { "x": 100, "y": 100 },
            "data": {
              "triggerType": "webhook",
              "webhookId": 5001,
              "eventType": "message_received"
            }
          },
          {
            "id": "node-2",
            "type": "condition",
            "position": { "x": 300, "y": 100 },
            "data": {
              "conditionType": "text_contains",
              "field": "message",
              "value": "support",
              "operator": "contains"
            }
          },
          {
            "id": "node-3",
            "type": "action",
            "position": { "x": 500, "y": 50 },
            "data": {
              "actionType": "send_message",
              "message": "Welcome to our enhanced support! How can I help you today?",
              "channelId": 4001
            }
          },
          {
            "id": "node-4",
            "type": "action",
            "position": { "x": 500, "y": 150 },
            "data": {
              "actionType": "call_agent",
              "agentId": 3001,
              "inputMapping": {
                "customerMessage": "message",
                "customerEmail": "customerEmail"
              }
            }
          },
          {
            "id": "node-5",
            "type": "action",
            "position": { "x": 700, "y": 100 },
            "data": {
              "actionType": "call_api",
              "apiIntegrationId": 6001,
              "parameters": {
                "customerId": "customerId"
              },
              "outputMapping": {
                "customerName": "customerName",
                "customerStatus": "customerStatus"
              }
            }
          }
        ],
        "edges": [
          {
            "id": "edge-1",
            "source": "node-1",
            "target": "node-2",
            "sourceHandle": "output",
            "targetHandle": "input"
          },
          {
            "id": "edge-2",
            "source": "node-2",
            "target": "node-3",
            "sourceHandle": "true",
            "targetHandle": "input"
          },
          {
            "id": "edge-3",
            "source": "node-2",
            "target": "node-4",
            "sourceHandle": "false",
            "targetHandle": "input"
          },
          {
            "id": "edge-4",
            "source": "node-4",
            "target": "node-5",
            "sourceHandle": "output",
            "targetHandle": "input"
          }
        ],
        "viewport": { "x": 0, "y": 0, "zoom": 1 }
      }
    }
    ```
  * **Success Response:** `200 OK` with the updated flow object and the new, incremented version number (e.g., `version: 3`).
  * **Error Response:** `409 Conflict` if the provided `version` in the request body does not match the current version of the flow in the database.

#### `DELETE /organizations/{organizationId}/flows/{flowId}`

  * **Description:** Deletes a flow and all its version history.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `204 No Content`

### **14.2. Flow Versioning**

#### `GET /organizations/{organizationId}/flows/{flowId}/versions`

  * **Description:** Retrieves a list of all saved versions for a specific flow, showing metadata for each version.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK`
    ```json
    {
      "items": [
        {
          "version": 3,
          "name": "Enhanced Customer Support Flow",
          "status": "live",
          "updatedAt": "2025-08-26T15:30:00Z",
          "updatedBy": 301
        },
        {
          "version": 2,
          "name": "Customer Support Flow",
          "status": "draft",
          "updatedAt": "2025-08-26T12:00:00Z",
          "updatedBy": 301
        },
        {
          "version": 1,
          "name": "Customer Support Flow",
          "status": "draft",
          "updatedAt": "2025-08-26T10:00:00Z",
          "updatedBy": 301
        }
      ]
    }
    ```

#### `GET /organizations/{organizationId}/flows/{flowId}/versions/{versionNumber}`

  * **Description:** Retrieves a specific version of a flow by its version number.
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK`
    ```json
    {
      "flowId": 7001,
      "organizationId": 201,
      "version": 2,
      "name": "Customer Support Flow",
      "description": "Handles initial customer inquiries and routes to appropriate agents.",
      "channelId": 4001,
      "status": "draft",
      "flowJson": {
        "nodes": [...],
        "edges": [...],
        "viewport": { "x": 0, "y": 0, "zoom": 1 }
      },
      "createdBy": 301,
      "createdAt": "2025-08-26T10:00:00Z",
      "updatedAt": "2025-08-26T12:00:00Z"
    }
    ```

#### `POST /organizations/{organizationId}/flows/{flowId}/versions/{versionNumber}/restore`

  * **Description:** Restores a previous version of a flow, making it the new latest version. This will create a new version (e.g., restoring version 1 will create a new version 4 with the content of version 1).
  * **Authorization:** All authenticated users within the organization.
  * **Response:** `200 OK` with the newly created flow version object.

### **14.3. Flow Status Management**

#### `PUT /organizations/{organizationId}/flows/{flowId}/status`

  * **Description:** Updates the status of a flow (Draft, Live, Paused, Deleted).
  * **Authorization:** All authenticated users within the organization.
  * **Request Body:**
    ```json
    {
      "status": "live"
    }
    ```
  * **Response:** `200 OK`
    ```json
    {
      "flowId": 7001,
      "status": "live",
      "updatedAt": "2025-08-26T16:00:00Z"
    }
    ```

### **14.4. Flow Analytics**

#### `GET /organizations/{organizationId}/flows/{flowId}/analytics`

  * **Description:** Retrieves analytics data for a specific flow.
  * **Authorization:** All authenticated users within the organization.
  * **Query Parameters:** `startDate`, `endDate`
  * **Response:** `200 OK`
    ```json
    {
      "flowId": 7001,
      "name": "Enhanced Customer Support Flow",
      "period": {
        "startDate": "2025-08-01T00:00:00Z",
        "endDate": "2025-08-31T23:59:59Z"
      },
      "metrics": {
        "totalExecutions": 1250,
        "successfulExecutions": 1180,
        "failedExecutions": 70,
        "averageExecutionTime": 2450,
        "peakHour": 14,
        "peakDay": "Monday"
      },
      "nodeAnalytics": [
        {
          "nodeId": "node-1",
          "nodeType": "trigger",
          "executionCount": 1250,
          "successRate": 100.0,
          "averageExecutionTime": 50
        },
        {
          "nodeId": "node-2",
          "nodeType": "condition",
          "executionCount": 1250,
          "successRate": 100.0,
          "averageExecutionTime": 100,
          "conditionResults": {
            "true": 800,
            "false": 450
          }
        },
        {
          "nodeId": "node-3",
          "nodeType": "action",
          "executionCount": 800,
          "successRate": 98.5,
          "averageExecutionTime": 500
        }
      ],
      "recentExecutions": [
        {
          "executionId": "exec-12345",
          "timestamp": "2025-08-31T15:30:00Z",
          "status": "success",
          "executionTime": 2300,
          "triggerData": {
            "message": "I need support",
            "customerEmail": "customer@example.com"
          }
        }
      ]
    }
    ```

-----

## **15. File Management**

The File Management module provides a unified file upload system with configurable presets for different use cases across the platform. This module handles file validation, processing, storage, and access control.

### **15.1. File Upload**

#### `POST /files/upload`

  * **Description:** Uploads one or more files using a specific preset configuration. The preset determines the allowed file types, sizes, and processing options.
  * **Authorization:** All authenticated users within the organization.
  * **Query Parameters:** `preset` (required) - The preset ID to use for validation and processing
  * **Request Body:** `multipart/form-data`
    * `files[]` (required) - The files to upload
    * `metadata` (optional) - JSON string with additional metadata
  * **Response:** `201 Created`
    ```json
    {
      "uploadId": "upl_12345",
      "preset": {
        "presetId": "user-profile-image",
        "name": "User Profile Image"
      },
      "files": [
        {
          "fileId": "file_67890",
          "originalName": "profile.jpg",
          "mimeType": "image/jpeg",
          "size": 245760,
          "url": "https://cdn.example.com/files/file_67890.jpg",
          "thumbnailUrl": "https://cdn.example.com/files/thumbnails/file_67890.jpg",
          "metadata": {
            "width": 400,
            "height": 400,
            "format": "webp"
          },
          "createdAt": "2025-08-27T10:00:00Z"
        }
      ],
      "uploadedAt": "2025-08-27T10:00:00Z"
    }
    ```

**Available Presets:**

* **`user-profile-image`** - Profile images for user accounts
  * Allowed: JPEG, PNG, WebP
  * Max size: 5MB
  * Max files: 1
  * Processing: Auto-resize to 400x400px, convert to WebP

* **`organization-logo`** - Logos for organizations
  * Allowed: JPEG, PNG, SVG
  * Max size: 2MB
  * Max files: 1
  * Processing: Auto-resize to 200x200px

* **`catalog-resources`** - Knowledge base resources
  * Allowed: PDF, DOCX, XLSX, CSV
  * Max size: 50MB
  * Max files: 10
  * Processing: None

### **15.2. File Management**

#### `GET /files/{fileId}`

  * **Description:** Retrieves metadata for a specific file.
  * **Authorization:** Users with access to the file (based on organization and permissions).
  * **Response:** `200 OK`
    ```json
    {
      "fileId": "file_67890",
      "originalName": "profile.jpg",
      "mimeType": "image/jpeg",
      "size": 245760,
      "url": "https://cdn.example.com/files/file_67890.jpg",
      "thumbnailUrl": "https://cdn.example.com/files/thumbnails/file_67890.jpg",
      "metadata": {
        "width": 400,
        "height": 400,
        "format": "webp"
      },
      "organizationId": 201,
      "uploadedBy": 301,
      "createdAt": "2025-08-27T10:00:00Z",
      "updatedAt": "2025-08-27T10:00:00Z"
    }
    ```

#### `GET /files/{fileId}/download`

  * **Description:** Downloads a file with appropriate headers for browser download.
  * **Authorization:** Users with access to the file (based on organization and permissions).
  * **Response:** `200 OK` with file content and appropriate headers:
    * `Content-Disposition: attachment; filename="original-name.jpg"`
    * `Content-Type: {mimeType}`
    * `Content-Length: {fileSize}`

#### `DELETE /files/{fileId}`

  * **Description:** Deletes a file from storage. This action is irreversible.
  * **Authorization:** Users who uploaded the file or have appropriate permissions.
  * **Response:** `204 No Content`

### **15.3. Organization File Management**

#### `GET /organizations/{organizationId}/files`

  * **Description:** Retrieves a paginated list of all files uploaded by the organization.
  * **Authorization:** Organization Administrator, appropriate team members.
  * **Query Parameters:** `preset`, `uploadedBy`, `startDate`, `endDate`, `page`, `pageSize`
  * **Response:** `200 OK`
    ```json
    {
      "page": 1,
      "pageSize": 25,
      "totalPages": 1,
      "totalItems": 3,
      "items": [
        {
          "fileId": "file_67890",
          "originalName": "profile.jpg",
          "mimeType": "image/jpeg",
          "size": 245760,
          "url": "https://cdn.example.com/files/file_67890.jpg",
          "thumbnailUrl": "https://cdn.example.com/files/thumbnails/file_67890.jpg",
          "preset": {
            "presetId": "user-profile-image",
            "name": "User Profile Image"
          },
          "uploadedBy": 301,
          "createdAt": "2025-08-27T10:00:00Z"
        },
        {
          "fileId": "file_67891",
          "originalName": "company-logo.png",
          "mimeType": "image/png",
          "size": 156789,
          "url": "https://cdn.example.com/files/file_67891.png",
          "thumbnailUrl": "https://cdn.example.com/files/thumbnails/file_67891.png",
          "preset": {
            "presetId": "organization-logo",
            "name": "Organization Logo"
          },
          "uploadedBy": 301,
          "createdAt": "2025-08-27T11:30:00Z"
        }
      ]
    }
    ```

### **15.4. File Upload Analytics**

#### `GET /organizations/{organizationId}/files/analytics`

  * **Description:** Retrieves analytics data for file uploads within an organization.
  * **Authorization:** Organization Administrator.
  * **Query Parameters:** `startDate`, `endDate`, `preset`
  * **Response:** `200 OK`
    ```json
    {
      "organizationId": 201,
      "period": {
        "startDate": "2025-08-01T00:00:00Z",
        "endDate": "2025-08-31T23:59:59Z"
      },
      "metrics": {
        "totalUploads": 45,
        "totalFiles": 67,
        "totalSize": 15728640,
        "averageFileSize": 234756
      },
      "presetBreakdown": [
        {
          "presetId": "user-profile-image",
          "presetName": "User Profile Image",
          "uploadCount": 25,
          "fileCount": 25,
          "totalSize": 5242880
        },
        {
          "presetId": "organization-logo",
          "presetName": "Organization Logo",
          "uploadCount": 3,
          "fileCount": 3,
          "totalSize": 2097152
        },
        {
          "presetId": "catalog-resources",
          "presetName": "Catalog Resources",
          "uploadCount": 17,
          "fileCount": 39,
          "totalSize": 8388608
        }
      ],
      "recentUploads": [
        {
          "fileId": "file_67890",
          "originalName": "profile.jpg",
          "preset": "user-profile-image",
          "uploadedBy": 301,
          "uploadedAt": "2025-08-27T10:00:00Z"
        }
      ]
    }
    ```

### **15.5. Error Responses**

#### **File Upload Validation Errors**

When file upload validation fails, the API returns `400 Bad Request` with detailed error information:

```json
{
  "error": "VALIDATION_ERROR",
  "message": "File upload validation failed",
  "details": [
    {
      "file": "document.pdf",
      "errors": [
        {
          "code": "FILE_TOO_LARGE",
          "message": "File size (75MB) exceeds maximum allowed size (50MB)"
        }
      ]
    },
    {
      "file": "image.gif",
      "errors": [
        {
          "code": "INVALID_FILE_TYPE",
          "message": "File type 'image/gif' is not allowed for this preset"
        }
      ]
    }
  ]
}
```

#### **Common Error Codes:**

* `INVALID_PRESET` - The specified preset does not exist or is inactive
* `FILE_TOO_LARGE` - File size exceeds the preset's maximum size limit
* `INVALID_FILE_TYPE` - File MIME type is not allowed for the preset
* `TOO_MANY_FILES` - Number of files exceeds the preset's maximum limit
* `FILE_PROCESSING_ERROR` - Error occurred during file processing (resizing, format conversion)
* `STORAGE_ERROR` - Error occurred while storing the file
* `ACCESS_DENIED` - User does not have permission to access the file
* `FILE_NOT_FOUND` - The requested file does not exist

-----