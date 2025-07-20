from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User
from categories.models import Category
from products.models import Product
from cart.models import CartItem
from orders.models import Order, OrderProduct
from reviews.models import Review
from wishlist.models import WishlistItem
from decimal import Decimal
import random
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with mock data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before adding mock data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            # Clear in correct order to avoid foreign key constraints
            OrderProduct.objects.all().delete()
            Order.objects.all().delete()
            Review.objects.all().delete()
            CartItem.objects.all().delete()
            WishlistItem.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()  # Keep superuser
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write('Creating mock data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets',
                'imageCategory': 'electronics.jpg'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for all ages',
                'imageCategory': 'clothing.jpg'
            },
            {
                'name': 'Books',
                'description': 'Books, magazines, and reading materials',
                'imageCategory': 'books.jpg'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and gardening supplies',
                'imageCategory': 'home_garden.jpg'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment and outdoor gear',
                'imageCategory': 'sports.jpg'
            },
            {
                'name': 'Beauty & Health',
                'description': 'Beauty products and health supplements',
                'imageCategory': 'beauty.jpg'
            },
            {
                'name': 'Toys & Games',
                'description': 'Toys and games for children and adults',
                'imageCategory': 'toys.jpg'
            },
            {
                'name': 'Automotive',
                'description': 'Car parts and automotive accessories',
                'imageCategory': 'automotive.jpg'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create users (buyers, sellers, admin)
        users_data = [
            # Admin users
            {
                'username': 'admin1',
                'email': 'admin1@smartsouq.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phoneNumber': '+1234567890',
                'address': {'City': 'New York', 'Country': 'USA', 'Street': '123 Admin St'},
                'profileImage': 'admin_profile.jpg',
                'isVerified': True,
                'IsActive': True,
                'permissions': ['create', 'read', 'update', 'delete', 'manage_users', 'manage_orders']
            },
            # Seller users
            {
                'username': 'electronics_store',
                'email': 'seller1@smartsouq.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'seller',
                'phoneNumber': '+1234567891',
                'address': {'City': 'Los Angeles', 'Country': 'USA', 'Street': '456 Seller Ave'},
                'profileImage': 'john_profile.jpg',
                'storeName': 'TechHub Electronics',
                'storeDescription': 'Your one-stop shop for the latest electronics and gadgets',
                'rating': Decimal('4.5'),
                'isVerified': True,
                'IsActive': True,
                'permissions': ['create', 'read', 'update', 'delete']
            },
            {
                'username': 'fashion_boutique',
                'email': 'seller2@smartsouq.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'seller',
                'phoneNumber': '+1234567892',
                'address': {'City': 'Miami', 'Country': 'USA', 'Street': '789 Fashion Blvd'},
                'profileImage': 'sarah_profile.jpg',
                'storeName': 'Chic Boutique',
                'storeDescription': 'Trendy fashion for modern lifestyle',
                'rating': Decimal('4.8'),
                'isVerified': True,
                'IsActive': True,
                'permissions': ['create', 'read', 'update', 'delete']
            },
            {
                'username': 'bookworm_store',
                'email': 'seller3@smartsouq.com',
                'first_name': 'Michael',
                'last_name': 'Brown',
                'role': 'seller',
                'phoneNumber': '+1234567893',
                'address': {'City': 'Chicago', 'Country': 'USA', 'Street': '321 Book Lane'},
                'profileImage': 'michael_profile.jpg',
                'storeName': 'The Book Nook',
                'storeDescription': 'Rare and popular books for all readers',
                'rating': Decimal('4.3'),
                'isVerified': True,
                'IsActive': True,
                'permissions': ['create', 'read', 'update', 'delete']
            },
            # Buyer users
            {
                'username': 'alice_buyer',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Wilson',
                'role': 'buyer',
                'phoneNumber': '+1234567894',
                'address': {'City': 'Seattle', 'Country': 'USA', 'Street': '111 Buyer St'},
                'profileImage': 'alice_profile.jpg',
                'isVerified': True,
                'IsActive': True,
                'permissions': ['read']
            },
            {
                'username': 'bob_customer',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Davis',
                'role': 'buyer',
                'phoneNumber': '+1234567895',
                'address': {'City': 'Denver', 'Country': 'USA', 'Street': '222 Customer Ave'},
                'profileImage': 'bob_profile.jpg',
                'isVerified': True,
                'IsActive': True,
                'permissions': ['read']
            },
            {
                'username': 'carol_shopper',
                'email': 'carol@example.com',
                'first_name': 'Carol',
                'last_name': 'Miller',
                'role': 'buyer',
                'phoneNumber': '+1234567896',
                'address': {'City': 'Boston', 'Country': 'USA', 'Street': '333 Shopper Rd'},
                'profileImage': 'carol_profile.jpg',
                'isVerified': True,
                'IsActive': True,
                'permissions': ['read']
            },
            {
                'username': 'david_user',
                'email': 'david@example.com',
                'first_name': 'David',
                'last_name': 'Garcia',
                'role': 'buyer',
                'phoneNumber': '+1234567897',
                'address': {'City': 'Phoenix', 'Country': 'USA', 'Street': '444 User Blvd'},
                'profileImage': 'david_profile.jpg',
                'isVerified': True,
                'IsActive': True,
                'permissions': ['read']
            }
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')  # Default password for all mock users
                # Set passwordChanagedAt for some users to simulate password changes
                if random.choice([True, False]):
                    user.passwordChanagedAt = timezone.now() - timedelta(days=random.randint(1, 90))
                user.save()
                self.stdout.write(f'Created user: {user.username} ({user.role})')
            users.append(user)

        # Get seller and buyer users for product and order creation
        sellers = [u for u in users if u.role == 'seller']
        buyers = [u for u in users if u.role == 'buyer']

        # Create products
        products_data = [
            # Electronics
            {
                'name': 'iPhone 15 Pro',
                'description': 'Latest iPhone with advanced camera system and A17 Pro chip',
                'price': Decimal('999.99'),
                'quantity': 25,
                'category': categories[0],  # Electronics
                'imageProduct': 'iphone15pro.jpg'
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Flagship Android phone with AI features',
                'price': Decimal('899.99'),
                'quantity': 30,
                'category': categories[0],
                'imageProduct': 'galaxy_s24.jpg'
            },
            {
                'name': 'MacBook Air M3',
                'description': 'Ultra-thin laptop with M3 chip for professionals',
                'price': Decimal('1299.99'),
                'quantity': 15,
                'category': categories[0],
                'imageProduct': 'macbook_air_m3.jpg'
            },
            {
                'name': 'AirPods Pro 2',
                'description': 'Wireless earbuds with active noise cancellation',
                'price': Decimal('249.99'),
                'quantity': 50,
                'category': categories[0],
                'imageProduct': 'airpods_pro2.jpg'
            },
            # Clothing
            {
                'name': 'Designer Jeans',
                'description': 'Premium denim jeans with perfect fit',
                'price': Decimal('89.99'),
                'quantity': 40,
                'category': categories[1],  # Clothing
                'imageProduct': 'designer_jeans.jpg'
            },
            {
                'name': 'Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt in various colors',
                'price': Decimal('24.99'),
                'quantity': 100,
                'category': categories[1],
                'imageProduct': 'cotton_tshirt.jpg'
            },
            {
                'name': 'Winter Jacket',
                'description': 'Waterproof winter jacket for cold weather',
                'price': Decimal('159.99'),
                'quantity': 20,
                'category': categories[1],
                'imageProduct': 'winter_jacket.jpg'
            },
            # Books
            {
                'name': 'Python Programming',
                'description': 'Complete guide to Python programming for beginners',
                'price': Decimal('39.99'),
                'quantity': 60,
                'category': categories[2],  # Books
                'imageProduct': 'python_book.jpg'
            },
            {
                'name': 'The Great Novel',
                'description': 'Award-winning fiction novel',
                'price': Decimal('19.99'),
                'quantity': 35,
                'category': categories[2],
                'imageProduct': 'great_novel.jpg'
            },
            # Home & Garden
            {
                'name': 'Smart Home Hub',
                'description': 'Control all your smart devices from one place',
                'price': Decimal('129.99'),
                'quantity': 25,
                'category': categories[3],  # Home & Garden
                'imageProduct': 'smart_hub.jpg'
            },
            {
                'name': 'Garden Tool Set',
                'description': 'Complete set of essential gardening tools',
                'price': Decimal('79.99'),
                'quantity': 18,
                'category': categories[3],
                'imageProduct': 'garden_tools.jpg'
            },
            # Sports & Outdoors
            {
                'name': 'Running Shoes',
                'description': 'Professional running shoes with cushioned sole',
                'price': Decimal('119.99'),
                'quantity': 45,
                'category': categories[4],  # Sports & Outdoors
                'imageProduct': 'running_shoes.jpg'
            },
            {
                'name': 'Yoga Mat',
                'description': 'Non-slip yoga mat for home workouts',
                'price': Decimal('29.99'),
                'quantity': 70,
                'category': categories[4],
                'imageProduct': 'yoga_mat.jpg'
            },
            # Beauty & Health
            {
                'name': 'Skincare Set',
                'description': 'Complete skincare routine for healthy skin',
                'price': Decimal('69.99'),
                'quantity': 30,
                'category': categories[5],  # Beauty & Health
                'imageProduct': 'skincare_set.jpg'
            },
            # Toys & Games
            {
                'name': 'Board Game Classic',
                'description': 'Family-friendly board game for all ages',
                'price': Decimal('34.99'),
                'quantity': 25,
                'category': categories[6],  # Toys & Games
                'imageProduct': 'board_game.jpg'
            }
        ]

        products = []
        for i, product_data in enumerate(products_data):
            # Assign products to different sellers
            seller = sellers[i % len(sellers)]
            product_data['seller'] = seller
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                products.append(product)
                # Add product to seller's Products ManyToMany field
                seller.Products.add(product)
                self.stdout.write(f'Created product: {product.name} by {seller.storeName}')

        # Create reviews
        review_texts = [
            "Great product! Highly recommended.",
            "Excellent quality and fast shipping.",
            "Good value for money.",
            "Perfect! Exactly what I needed.",
            "Amazing product, will buy again.",
            "Fast delivery and good packaging.",
            "Satisfied with the purchase.",
            "Could be better but overall good.",
            "Excellent customer service.",
            "Product as described, very happy."
        ]

        for product in products[:10]:  # Add reviews for first 10 products
            # Add 2-4 reviews per product
            num_reviews = random.randint(2, 4)
            reviewed_buyers = random.sample(buyers, min(num_reviews, len(buyers)))
            
            for buyer in reviewed_buyers:
                Review.objects.get_or_create(
                    user=buyer,
                    product=product,
                    defaults={
                        'rating': random.randint(3, 5),
                        'review': random.choice(review_texts)
                    }
                )

        # Create cart items
        for buyer in buyers[:3]:  # First 3 buyers have items in cart
            cart_products = random.sample(products[:8], random.randint(1, 3))
            for product in cart_products:
                CartItem.objects.get_or_create(
                    user=buyer,
                    product=product,
                    defaults={'quantity': random.randint(1, 3)}
                )

        # Create wishlist items
        for buyer in buyers:
            wishlist_products = random.sample(products[:10], random.randint(1, 4))
            for product in wishlist_products:
                WishlistItem.objects.get_or_create(
                    user=buyer,
                    product=product
                )

        # Create orders
        order_statuses = ["Pending", "Paid", "Shipped", "Delivered"]
        payment_methods = ["COD", "CARD"]

        for i in range(12):  # Create 12 orders
            buyer = random.choice(buyers)
            # Select 1-3 products from the same seller for each order
            seller = random.choice(sellers)
            seller_products = [p for p in products if p.seller == seller]
            if seller_products:
                order_products = random.sample(seller_products, min(random.randint(1, 3), len(seller_products)))
                
                total_price = Decimal('0')
                order_items = []
                
                for product in order_products:
                    quantity = random.randint(1, 3)
                    item_total = product.price * quantity
                    total_price += item_total
                    order_items.append({
                        'product': product,
                        'quantity': quantity
                    })
                
                # Create order
                created_at = timezone.now() - timedelta(days=random.randint(0, 30))
                order = Order.objects.create(
                    user=buyer,
                    seller=seller,
                    totalPrice=total_price,
                    paymentMethod=random.choice(payment_methods),
                    status=random.choice(order_statuses),
                    created_at=created_at
                )
                
                # Create order products
                for item in order_items:
                    OrderProduct.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity']
                    )
                
                self.stdout.write(f'Created order #{order.id} for {buyer.username} from {seller.storeName}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created mock data:\n'
                f'- {len(categories)} categories\n'
                f'- {len(users)} users (sellers, buyers, admin)\n'
                f'- {len(products)} products\n'
                f'- Reviews, cart items, wishlist items, and orders'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nDefault password for all users: password123\n'
                'Admin users have staff privileges.'
            )
        )
