from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.workers.models import WorkerProfile, Service
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates demo data for the Nexus WeFix application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating demo data...')

        # 1. Create Services
        services = [
            {'name': 'General Plumbing', 'category': 'Plumbing', 'desc': 'Fix leaks, install pipes, etc.'},
            {'name': 'Pipe Installation', 'category': 'Plumbing', 'desc': 'Full new pipe installations.'},
            {'name': 'Wall Painting', 'category': 'Painting', 'desc': 'Interior and exterior wall painting.'},
            {'name': 'Furniture Assembly', 'category': 'Carpentry', 'desc': 'Assemble flat-pack furniture.'},
            {'name': 'Electrical Wiring', 'category': 'Electrical', 'desc': 'Fix or install house wiring.'},
            {'name': 'AC Maintenance', 'category': 'HVAC', 'desc': 'Regular AC cleaning and repair.'},
        ]
        
        for s in services:
            Service.objects.get_or_create(
                name=s['name'], 
                defaults={'category': s['category'], 'description': s['desc']}
            )
        self.stdout.write(self.style.SUCCESS('Services created.'))

        # 2. Create Admin
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser('admin@example.com', 'admin', user_type='admin')
            self.stdout.write(self.style.SUCCESS('Admin user created.'))

        # 3. Create Customers
        for i in range(1, 4):
            email = f'customer{i}@example.com'
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    password='password',
                    first_name=f'Customer',
                    last_name=f'{i}',
                    user_type='customer',
                    phone=f'555-010{i}'
                )
        self.stdout.write(self.style.SUCCESS('Customer users created.'))

        # 4. Create Workers
        worker_data = [
            {'email': 'worker1@example.com', 'fname': 'John', 'lname': 'Doe', 'skills': ['Plumbing'], 'rate': '45.00', 'loc': 'Downtown'},
            {'email': 'worker2@example.com', 'fname': 'Jane', 'lname': 'Smith', 'skills': ['Painting', 'Carpentry'], 'rate': '35.00', 'loc': 'Uptown'},
            {'email': 'worker3@example.com', 'fname': 'Mike', 'lname': 'Johnson', 'skills': ['Electrical', 'HVAC'], 'rate': '60.00', 'loc': 'Suburbs'},
            {'email': 'worker4@example.com', 'fname': 'Sarah', 'lname': 'Williams', 'skills': ['Carpentry'], 'rate': '40.00', 'loc': 'Downtown'},
        ]

        for w in worker_data:
            if not User.objects.filter(email=w['email']).exists():
                user = User.objects.create_user(
                    email=w['email'],
                    password='password',
                    first_name=w['fname'],
                    last_name=w['lname'],
                    user_type='worker',
                    phone=f'555-200{random.randint(1,9)}'
                )
                WorkerProfile.objects.create(
                    user=user,
                    skills=w['skills'],
                    location=w['loc'],
                    is_verified=True,
                    hourly_rate=Decimal(w['rate']),
                    availability={'mon': '9-5', 'tue': '9-5', 'wed': '9-5'}
                )
        self.stdout.write(self.style.SUCCESS('Worker users and profiles created.'))
        self.stdout.write(self.style.SUCCESS('Demo data generation complete!'))
