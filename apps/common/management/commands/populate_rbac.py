from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.common.rbac_models import Permission, Role, RolePermission

User = get_user_model()


class Command(BaseCommand):
    """Management command to populate initial permissions and roles."""

    help = 'Populate initial permissions and system roles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset existing permissions and roles',
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        if options['reset']:
            self.stdout.write('Resetting existing permissions and roles...')
            Permission.objects.all().delete()
            Role.objects.all().delete()

        self.stdout.write('Creating permissions...')
        self.create_permissions()

        self.stdout.write('Creating system roles...')
        self.create_system_roles()

        self.stdout.write(
            self.style.SUCCESS('Successfully populated permissions and roles!')
        )

    def create_permissions(self):
        """Create all system permissions."""
        permissions_data = [
            # Account permissions
            {'name': 'accounts:create', 'codename': 'accounts_create',
                'description': 'Create accounts', 'permission_type': 'create', 'model_name': 'account'},
            {'name': 'accounts:read', 'codename': 'accounts_read',
                'description': 'Read accounts', 'permission_type': 'read', 'model_name': 'account'},
            {'name': 'accounts:update', 'codename': 'accounts_update',
                'description': 'Update accounts', 'permission_type': 'update', 'model_name': 'account'},
            {'name': 'accounts:delete', 'codename': 'accounts_delete',
                'description': 'Delete accounts', 'permission_type': 'delete', 'model_name': 'account'},
            {'name': 'accounts:list', 'codename': 'accounts_list',
                'description': 'List accounts', 'permission_type': 'list', 'model_name': 'account'},

            # Organization permissions
            {'name': 'organizations:create', 'codename': 'organizations_create',
                'description': 'Create organizations', 'permission_type': 'create', 'model_name': 'organization'},
            {'name': 'organizations:read', 'codename': 'organizations_read',
                'description': 'Read organizations', 'permission_type': 'read', 'model_name': 'organization'},
            {'name': 'organizations:update', 'codename': 'organizations_update',
                'description': 'Update organizations', 'permission_type': 'update', 'model_name': 'organization'},
            {'name': 'organizations:delete', 'codename': 'organizations_delete',
                'description': 'Delete organizations', 'permission_type': 'delete', 'model_name': 'organization'},
            {'name': 'organizations:list', 'codename': 'organizations_list',
                'description': 'List organizations', 'permission_type': 'list', 'model_name': 'organization'},

            # User permissions
            {'name': 'users:create', 'codename': 'users_create', 'description': 'Create users',
                'permission_type': 'create', 'model_name': 'user'},
            {'name': 'users:read', 'codename': 'users_read', 'description': 'Read users',
                'permission_type': 'read', 'model_name': 'user'},
            {'name': 'users:update', 'codename': 'users_update', 'description': 'Update users',
                'permission_type': 'update', 'model_name': 'user'},
            {'name': 'users:delete', 'codename': 'users_delete', 'description': 'Delete users',
                'permission_type': 'delete', 'model_name': 'user'},
            {'name': 'users:list', 'codename': 'users_list', 'description': 'List users',
                'permission_type': 'list', 'model_name': 'user'},

            # Team permissions
            {'name': 'teams:create', 'codename': 'teams_create', 'description': 'Create teams',
                'permission_type': 'create', 'model_name': 'team'},
            {'name': 'teams:read', 'codename': 'teams_read', 'description': 'Read teams',
                'permission_type': 'read', 'model_name': 'team'},
            {'name': 'teams:update', 'codename': 'teams_update', 'description': 'Update teams',
                'permission_type': 'update', 'model_name': 'team'},
            {'name': 'teams:delete', 'codename': 'teams_delete', 'description': 'Delete teams',
                'permission_type': 'delete', 'model_name': 'team'},
            {'name': 'teams:list', 'codename': 'teams_list', 'description': 'List teams',
                'permission_type': 'list', 'model_name': 'team'},

            # Role permissions
            {'name': 'roles:create', 'codename': 'roles_create', 'description': 'Create roles',
                'permission_type': 'create', 'model_name': 'role'},
            {'name': 'roles:read', 'codename': 'roles_read', 'description': 'Read roles',
                'permission_type': 'read', 'model_name': 'role'},
            {'name': 'roles:update', 'codename': 'roles_update', 'description': 'Update roles',
                'permission_type': 'update', 'model_name': 'role'},
            {'name': 'roles:delete', 'codename': 'roles_delete', 'description': 'Delete roles',
                'permission_type': 'delete', 'model_name': 'role'},
            {'name': 'roles:list', 'codename': 'roles_list', 'description': 'List roles',
                'permission_type': 'list', 'model_name': 'role'},

            # Permission permissions
            {'name': 'permissions:create', 'codename': 'permissions_create',
                'description': 'Create permissions', 'permission_type': 'create', 'model_name': 'permission'},
            {'name': 'permissions:read', 'codename': 'permissions_read',
                'description': 'Read permissions', 'permission_type': 'read', 'model_name': 'permission'},
            {'name': 'permissions:update', 'codename': 'permissions_update',
                'description': 'Update permissions', 'permission_type': 'update', 'model_name': 'permission'},
            {'name': 'permissions:delete', 'codename': 'permissions_delete',
                'description': 'Delete permissions', 'permission_type': 'delete', 'model_name': 'permission'},
            {'name': 'permissions:list', 'codename': 'permissions_list',
                'description': 'List permissions', 'permission_type': 'list', 'model_name': 'permission'},

            # Group permissions
            {'name': 'groups:create', 'codename': 'groups_create',
                'description': 'Create groups', 'permission_type': 'create', 'model_name': 'group'},
            {'name': 'groups:read', 'codename': 'groups_read', 'description': 'Read groups',
                'permission_type': 'read', 'model_name': 'group'},
            {'name': 'groups:update', 'codename': 'groups_update',
                'description': 'Update groups', 'permission_type': 'update', 'model_name': 'group'},
            {'name': 'groups:delete', 'codename': 'groups_delete',
                'description': 'Delete groups', 'permission_type': 'delete', 'model_name': 'group'},
            {'name': 'groups:list', 'codename': 'groups_list', 'description': 'List groups',
                'permission_type': 'list', 'model_name': 'group'},

            # Subscription permissions
            {'name': 'subscriptions:create', 'codename': 'subscriptions_create',
                'description': 'Create subscriptions', 'permission_type': 'create', 'model_name': 'subscription'},
            {'name': 'subscriptions:read', 'codename': 'subscriptions_read',
                'description': 'Read subscriptions', 'permission_type': 'read', 'model_name': 'subscription'},
            {'name': 'subscriptions:update', 'codename': 'subscriptions_update',
                'description': 'Update subscriptions', 'permission_type': 'update', 'model_name': 'subscription'},
            {'name': 'subscriptions:delete', 'codename': 'subscriptions_delete',
                'description': 'Delete subscriptions', 'permission_type': 'delete', 'model_name': 'subscription'},
            {'name': 'subscriptions:list', 'codename': 'subscriptions_list',
                'description': 'List subscriptions', 'permission_type': 'list', 'model_name': 'subscription'},

            # Admin permissions
            {'name': 'admin:access', 'codename': 'admin_access', 'description': 'Admin access',
                'permission_type': 'manage', 'model_name': 'admin'},
            {'name': 'admin:manage', 'codename': 'admin_manage', 'description': 'Admin management',
                'permission_type': 'manage', 'model_name': 'admin'},
        ]

        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                codename=perm_data['codename'],
                defaults=perm_data
            )
            if created:
                self.stdout.write(f'  Created permission: {permission.name}')
            else:
                self.stdout.write(
                    f'  Permission already exists: {permission.name}')

    def create_system_roles(self):
        """Create system roles with appropriate permissions."""
        # SaaS Administrator role
        saas_admin_role, created = Role.objects.get_or_create(
            codename='saas_administrator',
            defaults={
                'name': 'SaaS Administrator',
                'description': 'Full platform access for managing accounts, organizations, and global configurations',
                'role_type': 'system',
                'is_system_role': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(f'  Created role: {saas_admin_role.name}')
            # Assign all permissions to SaaS Administrator
            all_permissions = Permission.objects.filter(is_active=True)
            for permission in all_permissions:
                RolePermission.objects.get_or_create(
                    role=saas_admin_role,
                    permission=permission
                )
            self.stdout.write(
                f'  Assigned {all_permissions.count()} permissions to {saas_admin_role.name}')

        # SaaS Account Manager role
        account_manager_role, created = Role.objects.get_or_create(
            codename='saas_account_manager',
            defaults={
                'name': 'SaaS Account Manager',
                'description': 'Manages multiple organizations on behalf of enterprise accounts',
                'role_type': 'system',
                'is_system_role': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(f'  Created role: {account_manager_role.name}')
            # Assign account and organization permissions
            account_permissions = Permission.objects.filter(
                model_name__in=['account', 'organization'],
                is_active=True
            )
            for permission in account_permissions:
                RolePermission.objects.get_or_create(
                    role=account_manager_role,
                    permission=permission
                )
            self.stdout.write(
                f'  Assigned {account_permissions.count()} permissions to {account_manager_role.name}')

        # Organization Administrator role
        org_admin_role, created = Role.objects.get_or_create(
            codename='organization_administrator',
            defaults={
                'name': 'Organization Administrator',
                'description': 'Full administrative access within a specific organization',
                'role_type': 'system',
                'is_system_role': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(f'  Created role: {org_admin_role.name}')
            # Assign organization-scoped permissions
            org_permissions = Permission.objects.filter(
                model_name__in=['user', 'team',
                                'role', 'group', 'subscription'],
                is_active=True
            )
            for permission in org_permissions:
                RolePermission.objects.get_or_create(
                    role=org_admin_role,
                    permission=permission
                )
            self.stdout.write(
                f'  Assigned {org_permissions.count()} permissions to {org_admin_role.name}')

        # Team Manager role
        team_manager_role, created = Role.objects.get_or_create(
            codename='team_manager',
            defaults={
                'name': 'Team Manager',
                'description': 'Manages team members and team-specific resources',
                'role_type': 'system',
                'is_system_role': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(f'  Created role: {team_manager_role.name}')
            # Assign team and user permissions
            team_permissions = Permission.objects.filter(
                model_name__in=['team', 'user'],
                permission_type__in=['read', 'update'],
                is_active=True
            )
            for permission in team_permissions:
                RolePermission.objects.get_or_create(
                    role=team_manager_role,
                    permission=permission
                )
            self.stdout.write(
                f'  Assigned {team_permissions.count()} permissions to {team_manager_role.name}')

        # User role
        user_role, created = Role.objects.get_or_create(
            codename='user',
            defaults={
                'name': 'User',
                'description': 'Standard user with basic platform access based on assigned permissions',
                'role_type': 'system',
                'is_system_role': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(f'  Created role: {user_role.name}')
            # Assign basic read permissions
            user_permissions = Permission.objects.filter(
                permission_type='read',
                is_active=True
            )
            for permission in user_permissions:
                RolePermission.objects.get_or_create(
                    role=user_role,
                    permission=permission
                )
            self.stdout.write(
                f'  Assigned {user_permissions.count()} permissions to {user_role.name}')
