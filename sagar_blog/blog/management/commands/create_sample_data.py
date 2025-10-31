from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Create sample blog data'
    
    def add_arguments(self, parser):
        parser.add_argument('--posts', type=int, default=10, help='Number of posts to create')
    
    def handle(self, *args, **options):
        # Create superuser if doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user (username: admin, password: admin123)')
        
        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Latest tech trends and news'},
            {'name': 'Travel', 'description': 'Travel guides and experiences'},
            {'name': 'Food', 'description': 'Recipes and food reviews'},
            {'name': 'Lifestyle', 'description': 'Lifestyle tips and advice'},
            {'name': 'Health', 'description': 'Health and wellness articles'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Get admin user
        admin_user = User.objects.get(username='admin')
        categories = Category.objects.all()
        
        # Sample post content
        sample_posts = [
            {
                'title': 'Getting Started with Django',
                'content': 'Django is a high-level Python web framework that encourages rapid development...',
                'excerpt': 'Learn the basics of Django web framework'
            },
            {
                'title': '10 Best Travel Destinations for 2024',
                'content': 'Discover amazing places around the world that should be on your travel list...',
                'excerpt': 'Explore the most beautiful destinations for your next adventure'
            },
            {
                'title': 'Healthy Eating Habits for Busy People',
                'content': 'Maintaining a healthy diet can be challenging when you have a busy schedule...',
                'excerpt': 'Simple tips to eat healthy even with a busy lifestyle'
            },
        ]
        
        # Create posts
        posts_created = 0
        for i in range(options['posts']):
            sample_post = random.choice(sample_posts)
            title = f"{sample_post['title']} #{i+1}"
            
            post, created = Post.objects.get_or_create(
                title=title,
                defaults={
                    'author': admin_user,
                    'category': random.choice(categories),
                    'content': sample_post['content'] * 3,  # Make content longer
                    'excerpt': sample_post['excerpt'],
                    'status': 'published',
                    'published_at': timezone.now(),
                    'views': random.randint(10, 1000),
                    'featured': random.choice([True, False]) if i < 3 else False,
                }
            )
            
            if created:
                # Add some tags
                tags = ['django', 'python', 'web development', 'tutorial', 'tips']
                post.tags.add(*random.sample(tags, random.randint(1, 3)))
                posts_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {posts_created} sample posts')
        )
