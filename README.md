# SmartSouq Django REST API

SmartSouq is a modern e-commerce platform built with Django and Django REST Framework (DRF). It provides a robust backend for user authentication, product management, categories, orders, cart, wishlist, and reviews, following best practices for modular Django apps and RESTful API design.

---

## 1. Project Structure

- **accounts/**: User authentication, registration, profile, and admin endpoints
- **products/**: Product CRUD, image update, and product listing
- **categories/**: Category CRUD, image update, and category-product listing
- **orders/**: Order placement, status updates, and order queries
- **cart/**: User cart management
- **wishlist/**: User wishlist management
- **reviews/**: Product reviews
- **commerce/**: Django project settings and main URL routing

Each app contains its own models, serializers, views, urls, and tests for maintainability and scalability.

---

## 2. API Endpoints

The API is organized under `/api/v1/` and follows RESTful conventions. Key endpoints include:

- **Authentication & User**: Register, login, profile, admin user management
- **Product**: CRUD, image update, list
- **Category**: CRUD, image update, list, products by category
- **Order**: Place, list, update status, delete, filter by user/product/status
- **Cart**: Add/remove/clear/list cart items
- **Wishlist**: Add/remove/list wishlist items
- **Review**: Add/list/update/delete product reviews

See the codebase for detailed endpoint paths and request/response formats.

---

## 3. How to Set Up and Run the Application

### **Prerequisites:**
- Python 3.10+
- Django 5+
- Django REST Framework
- (Optional) Docker

### **Setup Steps:**

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd <project-directory>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser (for Django admin)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/v1/`

---

## 4. Running Tests

Each app includes a test suite for its API endpoints. To run all tests:

```bash
python manage.py test
```

You can also test a specific app:
```bash
python manage.py test accounts
python manage.py test products
# etc.
```

---

## 5. API Usage

- Use tools like **Postman** or **cURL** to interact with the API.
- For authentication, use session-based login/logout or token authentication as configured.
- All endpoints require appropriate permissions (e.g., only authenticated users can create orders, only admins can manage categories).

---

## 6. Django Admin

- Access the Django admin at `/admin/` for manual management of users, products, categories, etc.

---

## 7. Contributing & Extending

- The project is modular and easy to extend. Add new apps or endpoints as needed.
- Follow the existing testing and API design patterns for consistency.

---

## 🎉 Happy Coding with Django REST Framework!
