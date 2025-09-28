

# E-Commerce Backend API

A **RESTful E-Commerce Backend API** built with **Django REST Framework**.
This API handles products, collections, carts, customers, orders, and nested resources like reviews and product images.

---

## 🔹 Features

* **Products**: Create, update, delete, list products
* **Collections**: Manage product collections/categories
* **Carts**: Add items, view cart details, manage cart items
* **Customers**: Manage customer profiles
* **Orders**: Create and track orders
* **Nested Resources**:

  * Product **reviews** (`/products/{id}/reviews/`)
  * Product **images** (`/products/{id}/images/`)
  * Cart **items** (`/carts/{id}/items/`)

---

## 🔹 Technologies Used

* **Backend:** Python, Django, Django REST Framework
* **Database:** SQLite (default) / MySQL (optional)
* **Version Control:** Git & GitHub
* **Authentication:** JWT (optional, can be added for security)

---

## 🔹 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ecommerce-backend.git
```

2. Navigate to the project folder:

```bash
cd ecommerce-backend
```

3. Create a virtual environment:

```bash
python -m venv env
```

4. Activate the environment:

* **Windows:** `env\Scripts\activate`
* **Linux/Mac:** `source env/bin/activate`

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Apply migrations:

```bash
python manage.py migrate
```

7. Run the server:

```bash
python manage.py runserver
```

8. API is now accessible at: `http://127.0.0.1:8000/`

---

## 🔹 API Endpoints

### Products

* `GET /products/` – List all products
* `POST /products/` – Create a new product
* `GET /products/{id}/` – Retrieve product details
* `PUT/PATCH /products/{id}/` – Update product
* `DELETE /products/{id}/` – Delete product

**Nested Routes:**

* `GET /products/{id}/reviews/` – List reviews of a product
* `POST /products/{id}/reviews/` – Add a review
* `GET /products/{id}/images/` – List product images
* `POST /products/{id}/images/` – Add product image

---

### Collections

* `GET /collections/` – List all collections
* `POST /collections/` – Create a collection

---

### Carts

* `GET /carts/` – List all carts
* `POST /carts/` – Create a cart
* `GET /carts/{id}/items/` – List items in a cart
* `POST /carts/{id}/items/` – Add item to cart

---

### Customers

* `GET /customers/` – List customers
* `POST /customers/` – Add a customer

---

### Orders

* `GET /orders/` – List all orders
* `POST /orders/` – Create a new order
* `GET /orders/{id}/` – Get order details

---

## 🔹 Usage

* Use tools like **Postman** or **Swagger** to test API endpoints
* Create products, collections, carts, and orders programmatically or via frontend integration

---

## 🔹 Contributing

* Contributions, bug reports, and feature requests are welcome

---

## 🔹 License

This project is licensed under the **MIT License**

---

Do you want me to do that?
