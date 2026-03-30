# Tejasri_Ecommerce_Order_Engine_Hackathon
# Distributed E-Commerce Order Engine Hackathon

## 📌 Project Description

This project is a **CLI-based Distributed E-Commerce Order Engine** developed in **Python** to simulate how real-world e-commerce platforms handle product catalog management, multi-user carts, inventory reservation, secure order placement, payment processing, rollback recovery, and concurrency.

The system follows a **microservice-inspired modular design** where each service is responsible for a specific business function such as product handling, cart operations, payments, inventory updates, and order lifecycle management.

### ✅ Project Overview

The main objective of this project is to build a robust backend simulation that demonstrates:

* real-time stock reservation
* concurrent user handling using thread locks
* safe payment rollback on failures
* fraud detection for suspicious orders
* coupon and discount engine
* event-driven order processing
* immutable audit logging

This project mimics backend engineering concepts used in large-scale systems like Amazon, Flipkart, Zepto, and Blinkit.

### ✅ Features Implemented

* Product management (add/view products)
* Multi-user cart management
* Real-time stock reservation
* Order placement with payment simulation
* Rollback on payment failure
* Order cancellation
* Partial return and refund
* Coupon and discount engine
* Low-stock alert system
* Fraud detection rules
* Event queue simulation
* Idempotency for duplicate clicks
* Concurrency handling with threading
* Immutable audit logs

### ✅ Design Approach

The project is designed using **service-based modular architecture**:

* **ProductService** → product catalog + stock handling
* **CartService** → user cart operations
* **OrderService** → order lifecycle + state transitions
* **PaymentService** → payment success/failure simulation
* **AuditLogger** → immutable event logs

This approach improves:

* maintainability
* readability
* scalability
* separation of concerns
* extensibility

### ✅ Assumptions

* Uses **in-memory Python dictionaries** instead of database
* Payment gateway is simulated randomly
* CLI-based execution instead of web UI
* Users are identified by `user_id`
* Coupon codes are predefined
* Threading simulates concurrent users
* Failure scenarios are intentionally injected for testing rollback

### ✅ How to Run the Project

1. Open the project folder in VS Code
2. Save the source code as `ecommerce_order_engine.py`
3. Open terminal inside VS Code
4. Run:

```bash
python ecommerce_order_engine.py
```

5. Use the CLI menu to test all features

## 📌 Project Overview

This project is a **CLI-based Distributed E-Commerce Order Engine** built in **Python**.
It simulates how modern e-commerce systems manage products, carts, orders, payments, inventory, logging, fraud checks, and failure recovery.

The system is designed using a **microservice-inspired modular architecture**:

* Product Service
* Cart Service
* Order Service
* Payment Service
* Inventory Service
* Audit Log Service

The goal is to demonstrate:

* Clean architecture
* Loose coupling
* Scalability
* Fault tolerance
* Concurrency handling
* Real-world order lifecycle management

---

# 🚀 Features Implemented

## ✅ Core Features

* Add products
* View products
* Add/remove items from cart
* View cart
* Place order
* Cancel order
* Return product
* View all orders

## ✅ Order State Machine

Valid order states:

* CREATED
* PENDING_PAYMENT
* PAID
* SHIPPED
* DELIVERED
* FAILED
* CANCELLED

Invalid transitions are blocked.

## ✅ Discount & Coupon Engine

Supported rules:

* Total > ₹1000 → 10% discount
* Quantity > 3 → extra 5%
* Coupon `SAVE10` → 10% off
* Coupon `FLAT200` → ₹200 off

## ✅ Inventory Alert System

* Low stock alert
* Prevent purchase when stock = 0
* Automatic stock restore on cancellation/return

## ✅ Return & Refund System

* Partial returns supported
* Stock updated after return
* Order total recalculated

## ✅ Event-Driven Workflow

Event queue simulation:

* ORDER_CREATED
* PAYMENT_SUCCESS
* INVENTORY_UPDATED

Events execute sequentially.
Failure stops next events.

## ✅ Audit Logging

Immutable logs maintained for:

* Product additions
* Cart updates
* Orders
* Payments
* Returns
* Failures

## ✅ Fraud Detection

Flags suspicious users if:

* 3 orders placed within 1 minute
* High-value order detected

## ✅ Failure Injection

Simulated failures in:

* Payment
* Order creation
* Inventory update

System safely rolls back.

## ✅ Idempotency Handling

Duplicate order prevention when user clicks **Place Order** multiple times.

## ✅ Concurrency Simulation

* Multiple users simulated
* Thread-safe stock updates
* Locking used to prevent race conditions

---

# 🏗️ Design Approach

The project follows **service-based modular design**.

Each service has a single responsibility:

### Product Service

Handles:

* product creation
* stock view
* stock updates

### Cart Service

Handles:

* add to cart
* remove from cart
* view cart

### Order Service

Handles:

* order lifecycle
* order states
* cancellation
* returns

### Payment Service

Handles:

* payment success/failure
* rollback logic

### Inventory Service

Handles:

* stock reservation
* low stock alerts
* release expired reservations

### Audit Service

Handles:

* immutable logs
* user activity trace

This keeps the system:

* maintainable
* scalable
* loosely coupled
* easy to extend

---

# 📝 Assumptions

* Single machine CLI simulation
* In-memory data structures used instead of database
* Users identified by user_id
* Coupon codes are predefined
* Payment gateway is simulated
* Threading simulates concurrent users
* Failure mode is random/manual trigger

---

# ▶️ How to Run the Project

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Teja290604/Tejasri_Ecommerce_Order_Engine_Hackathon.git
cd Tejasri_Ecommerce_Order_Engine_Hackathon
```

## 2️⃣ Run Python File

```bash
python ecommerce_order_engine.py
```

## 3️⃣ Use CLI Menu

```text
1. Add Product
2. View Products
3. Add to Cart
4. Remove from Cart
5. View Cart
6. Apply Coupon
7. Place Order
8. Cancel Order
9. View Orders
10. Low Stock Alert
11. Return Product
12. Simulate Concurrent Users
13. View Logs
14. Trigger Failure Mode
0. Exit
```

