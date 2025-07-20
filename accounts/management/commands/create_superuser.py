from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials for development'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superuser already exists. Skipping creation.')
            )
            return
        
        # Create superuser
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@smartsouq.com',
            password='admin123',
            first_name='Super',
            last_name='Admin',
            phoneNumber='+1000000000',
            address={'City': 'Admin City', 'Country': 'Admin Country', 'Street': 'Admin Street'},
            role='admin',
            profileImage='admin_super_profile.jpg',
            isVerified=True,
            IsActive=True,
            storeName='Admin Store',
            storeDescription='Administrative store for system management',
            rating=5.0,
            permissions=['create', 'read', 'update', 'delete', 'manage_users', 'manage_orders', 'system_admin']
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser created successfully!\n'
                f'Username: admin\n'
                f'Email: admin@smartsouq.com\n'
                f'Password: admin123'
            )
        )
