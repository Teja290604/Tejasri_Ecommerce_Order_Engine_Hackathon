import threading
import random
import time
from datetime import datetime
from collections import defaultdict, deque


class AuditLogger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.logs.append(entry)
        print(entry)

    def view_logs(self):
        for log in self.logs:
            print(log)


class ProductService:
    def __init__(self, logger):
        self.products = {}
        self.lock = threading.Lock()
        self.logger = logger

    def add_product(self, pid, name, price, stock):
        if pid in self.products:
            print("Product ID already exists")
            return
        self.products[pid] = {"name": name, "price": price, "stock": stock, "reserved": 0}
        self.logger.log(f"PRODUCT {pid} added")

    def view_products(self):
        for pid, p in self.products.items():
            print(pid, p)

    def reserve_stock(self, pid, qty):
        with self.lock:
            if pid not in self.products or self.products[pid]["stock"] < qty:
                return False
            self.products[pid]["stock"] -= qty
            self.products[pid]["reserved"] += qty
            return True

    def release_stock(self, pid, qty):
        with self.lock:
            self.products[pid]["stock"] += qty
            self.products[pid]["reserved"] -= qty

    def commit_reserved(self, pid, qty):
        with self.lock:
            self.products[pid]["reserved"] -= qty

    def low_stock_alert(self, threshold=2):
        print("Low stock products:")
        for pid, p in self.products.items():
            if p["stock"] <= threshold:
                print(pid, p)


class CartService:
    def __init__(self, product_service, logger):
        self.carts = defaultdict(dict)
        self.ps = product_service
        self.logger = logger

    def add_to_cart(self, user, pid, qty):
        if self.ps.reserve_stock(pid, qty):
            self.carts[user][pid] = self.carts[user].get(pid, 0) + qty
            self.logger.log(f"{user} added {pid} qty={qty}")
            print("Added to cart")
        else:
            print("Not enough stock")

    def remove_from_cart(self, user, pid):
        if pid in self.carts[user]:
            qty = self.carts[user].pop(pid)
            self.ps.release_stock(pid, qty)
            self.logger.log(f"{user} removed {pid}")

    def view_cart(self, user):
        print(self.carts[user])

    def clear_cart(self, user):
        self.carts[user].clear()


class PaymentService:
    def pay(self, amount):
        return random.choice([True, True, False])


class OrderService:
    VALID_STATES = {
        "CREATED": ["PENDING_PAYMENT", "CANCELLED"],
        "PENDING_PAYMENT": ["PAID", "FAILED"],
        "PAID": ["SHIPPED", "CANCELLED"],
        "SHIPPED": ["DELIVERED"],
        "DELIVERED": [],
        "FAILED": [],
        "CANCELLED": [],
    }

    def __init__(self, ps, cs, payment, logger):
        self.ps = ps
        self.cs = cs
        self.payment = payment
        self.logger = logger
        self.orders = {}
        self.counter = 100
        self.idempotency = set()
        self.events = deque()
        self.user_order_times = defaultdict(list)

    def apply_discount(self, items, coupon=None):
        total = sum(self.ps.products[pid]["price"] * qty for pid, qty in items.items())
        if total > 1000:
            total *= 0.9
        if any(qty > 3 for qty in items.values()):
            total *= 0.95
        if coupon == "SAVE10":
            total *= 0.9
        elif coupon == "FLAT200":
            total -= 200
        return max(total, 0)

    def place_order(self, user, coupon=None):
        cart = self.cs.carts[user]
        if not cart:
            print("Cart empty")
            return None

        idem_key = f"{user}-{sorted(cart.items())}"
        if idem_key in self.idempotency:
            print("Duplicate click prevented")
            return None
        self.idempotency.add(idem_key)

        items = cart.copy()
        total = self.apply_discount(items, coupon)
        oid = self.counter
        self.counter += 1
        self.orders[oid] = {"user": user, "items": items, "total": total, "state": "PENDING_PAYMENT"}
        self.events.append("ORDER_CREATED")
        self.logger.log(f"ORDER_{oid} created")

        now = time.time()
        self.user_order_times[user] = [t for t in self.user_order_times[user] if now - t < 60]
        self.user_order_times[user].append(now)
        if len(self.user_order_times[user]) >= 3 or total > 5000:
            self.logger.log(f"FRAUD ALERT for {user}")

        if self.payment.pay(total):
            self.orders[oid]["state"] = "PAID"
            for pid, qty in items.items():
                self.ps.commit_reserved(pid, qty)
            self.cs.clear_cart(user)
            self.events.extend(["PAYMENT_SUCCESS", "INVENTORY_UPDATED"])
            self.logger.log(f"ORDER_{oid} payment success")
        else:
            self.orders[oid]["state"] = "FAILED"
            for pid, qty in items.items():
                self.ps.release_stock(pid, qty)
            self.cs.clear_cart(user)
            self.logger.log(f"ORDER_{oid} payment failed rollback")
        return oid

    def cancel_order(self, oid):
        if oid not in self.orders:
            print("Order not found")
            return
        order = self.orders[oid]
        if order["state"] == "CANCELLED":
            print("Already cancelled")
            return
        for pid, qty in order["items"].items():
            self.ps.products[pid]["stock"] += qty
        order["state"] = "CANCELLED"
        self.logger.log(f"ORDER_{oid} cancelled")

    def return_product(self, oid, pid, qty):
        if oid not in self.orders:
            return
        order = self.orders[oid]
        if pid not in order["items"] or qty > order["items"][pid]:
            return
        refund = self.ps.products[pid]["price"] * qty
        order["items"][pid] -= qty
        order["total"] -= refund
        self.ps.products[pid]["stock"] += qty
        self.logger.log(f"RETURN processed for ORDER_{oid}, {pid}, qty={qty}")

    def view_orders(self):
        for oid, order in self.orders.items():
            print(oid, order)

    def simulate_events(self):
        while self.events:
            print(self.events.popleft())


def simulate_concurrent_users(cart_service, pid):
    def worker(user):
        cart_service.add_to_cart(user, pid, 5)

    t1 = threading.Thread(target=worker, args=("USER_A",))
    t2 = threading.Thread(target=worker, args=("USER_B",))
    t1.start(); t2.start(); t1.join(); t2.join()


def main():
    logger = AuditLogger()
    ps = ProductService(logger)
    cs = CartService(ps, logger)
    pay = PaymentService()
    os = OrderService(ps, cs, pay, logger)
    coupon = None

    while True:
        print("""\n1.Add Product
2.View Products
3.Add to Cart
4.Remove from Cart
5.View Cart
6.Apply Coupon
7.Place Order
8.Cancel Order
9.View Orders
10.Low Stock Alert
11.Return Product
12.Simulate Concurrent Users
13.View Logs
14.Trigger Failure Mode
0.Exit""")
        ch = input("Enter choice: ")

        if ch == "1":
            ps.add_product(input("PID: "), input("Name: "), float(input("Price: ")), int(input("Stock: ")))
        elif ch == "2":
            ps.view_products()
        elif ch == "3":
            cs.add_to_cart(input("User: "), input("PID: "), int(input("Qty: ")))
        elif ch == "4":
            cs.remove_from_cart(input("User: "), input("PID: "))
        elif ch == "5":
            cs.view_cart(input("User: "))
        elif ch == "6":
            coupon = input("Coupon: ")
        elif ch == "7":
            os.place_order(input("User: "), coupon)
            coupon = None
        elif ch == "8":
            os.cancel_order(int(input("Order ID: ")))
        elif ch == "9":
            os.view_orders()
        elif ch == "10":
            ps.low_stock_alert()
        elif ch == "11":
            os.return_product(int(input("Order ID: ")), input("PID: "), int(input("Qty: ")))
        elif ch == "12":
            simulate_concurrent_users(cs, input("PID: "))
        elif ch == "13":
            logger.view_logs()
        elif ch == "14":
            os.simulate_events()
        elif ch == "0":
            break


if __name__ == "__main__":
    main()
