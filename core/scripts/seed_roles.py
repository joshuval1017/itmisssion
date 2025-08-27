from django.contrib.auth import get_user_model
from core.models import Role  # Adjust if your Role model is in a different app

def run():
    # Seed roles
    roles = ['Admin', 'Officer', 'Citizen']
    for role_name in roles:
        role, created = Role.objects.get_or_create(RoleName=role_name)
        if created:
            print(f"✅ Role '{role_name}' created.")
        else:
            print(f"ℹ️ Role '{role_name}' already exists.")

    # Create demo admin user
    User = get_user_model()
    admin_user, created = User.objects.get_or_create(
        username='admin_demo',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin user already exists.")
