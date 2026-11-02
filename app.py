from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from collections import deque
from datetime import datetime, timedelta
import threading
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

app = Flask(__name__)
app.secret_key = "smart_campus_food_preorder_secret_key"

# =====================================================
# DATA MODELS & IN-MEMORY STATE
# =====================================================

# Food Menu with icons and descriptions
menu = {
    1: {"name": "Burger", "price": 60, "icon": "🍔", "desc": "Crispy veg patty with fresh veggies and zesty sauce", "category": "Snacks"},
    2: {"name": "Pizza", "price": 100, "icon": "🍕", "desc": "Loaded cheese and herb-infused personal crust", "category": "Meals"},
    3: {"name": "Sandwich", "price": 50, "icon": "🥪", "desc": "Grilled multi-layer sandwich with green chutney", "category": "Snacks"},
    4: {"name": "Samosa", "price": 20, "icon": "🥟", "desc": "Crispy golden crust filled with spiced potatoes & peas", "category": "Snacks"},
    5: {"name": "Chole Bhature", "price": 80, "icon": "🍛", "desc": "Authentic Punjabi chole with 2 fluffy bhature", "category": "Meals"},
    6: {"name": "Cold Drink", "price": 40, "icon": "🥤", "desc": "Chilled refreshing beverage (300 ml)", "category": "Beverages"},
    7: {"name": "Coffee", "price": 30, "icon": "☕", "desc": "Freshly brewed hot cappuccino with frothy milk", "category": "Beverages"},
    8: {"name": "Tea", "price": 20, "icon": "🫖", "desc": "Traditional desi adrak-elaichi masala chai", "category": "Beverages"}
}

# Queue for live orders
order_queue = deque()

# Storage for all orders (history & cancelled)
all_orders = {}

# Order number counter
order_number = 1000
order_lock = threading.Lock()


def get_queue_info(target_token):
    """Calculate dynamic position and wait time for a given token in the queue."""
    for idx, ord_item in enumerate(order_queue, start=1):
        if ord_item["token"] == target_token:
            people_ahead = idx - 1
            estimated_wait = idx * 5
            return {
                "position": idx,
                "people_ahead": people_ahead,
                "estimated_wait_minutes": estimated_wait
            }
    return None


# =====================================================
# WEB ROUTES
# =====================================================

@app.route("/")
def index():
    """Home page displaying menu, ordering system, and active queue count."""
    active_count = len(order_queue)
    return render_template("index.html", menu=menu, active_count=active_count)


@app.route("/place-order", methods=["POST"])
def place_order():
    """Processes order placement and redirects to receipt."""
    global order_number

    student_name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()

    cart = []
    subtotal = 0

    for item_id, item_data in menu.items():
        qty_str = request.form.get(f"qty_{item_id}", "0")
        try:
            qty = int(qty_str)
        except ValueError:
            qty = 0

        if qty > 0:
            item_total = item_data["price"] * qty
            subtotal += item_total
            cart.append({
                "id": item_id,
                "name": item_data["name"],
                "price": item_data["price"],
                "quantity": qty,
                "total": item_total
            })

    if not cart:
        flash("Please select at least one food item with quantity greater than 0.", "warning")
        return redirect(url_for("index"))

    # Calculate discount (10% if subtotal >= 300)
    discount = (subtotal * 0.10) if subtotal >= 300 else 0.0
    final_total = subtotal - discount

    with order_lock:
        order_number += 1
        token = order_number

        # If name or roll_no are not provided, auto-assign friendly real-time identifiers
        if not student_name:
            student_name = f"Quick Student #{token}"
        if not roll_no:
            roll_no = f"TOKEN-{token}"

        position = len(order_queue) + 1
        waiting_time = position * 5
        order_time = datetime.now()
        pickup_time = (order_time + timedelta(minutes=waiting_time)).strftime("%I:%M %p")

        order = {
            "token": token,
            "name": student_name,
            "roll_no": roll_no,
            "items": cart,
            "order_items": cart,
            "subtotal": subtotal,
            "discount": discount,
            "total": final_total,
            "status": "Preparing",
            "position": position,
            "order_time": order_time.strftime("%I:%M %p, %d %b %Y"),
            "pickup": pickup_time
        }

        order_queue.append(order)
        all_orders[token] = order

    flash(f"Order #{token} placed successfully!", "success")
    return redirect(url_for("receipt", token=token))


@app.route("/receipt/<int:token>")
def receipt(token):
    """Displays receipt for a placed order."""
    order = all_orders.get(token)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("index"))

    queue_info = get_queue_info(token)
    return render_template("receipt.html", order=order, queue_info=queue_info)


@app.route("/status", methods=["GET", "POST"])
def status():
    """Allows checking status of any token."""
    searched_token = None
    order = None
    queue_info = None

    if request.method == "POST":
        token_input = request.form.get("token", "").strip()
        if token_input.isdigit():
            searched_token = int(token_input)
            order = all_orders.get(searched_token)
            if order:
                queue_info = get_queue_info(searched_token)
            else:
                flash(f"No order found with Token #{searched_token}", "danger")
        else:
            flash("Please enter a valid numeric token number.", "warning")
    elif request.args.get("token"):
        token_param = request.args.get("token", "").strip()
        if token_param.isdigit():
            searched_token = int(token_param)
            order = all_orders.get(searched_token)
            if order:
                queue_info = get_queue_info(searched_token)

    return render_template("status.html", order=order, queue_info=queue_info, searched_token=searched_token)


@app.route("/cancel/<int:token>", methods=["POST"])
def cancel(token):
    """Cancels an order by token number."""
    with order_lock:
        target_order = None
        for ord_item in list(order_queue):
            if ord_item["token"] == token:
                target_order = ord_item
                order_queue.remove(ord_item)
                break

        if target_order:
            target_order["status"] = "Cancelled"
            all_orders[token]["status"] = "Cancelled"
            flash(f"Order #{token} has been cancelled successfully.", "info")
        else:
            flash(f"Order #{token} could not be found or is already completed/cancelled.", "danger")

    # Redirect to referer or status
    ref = request.referrer or url_for("status")
    return redirect(ref)


@app.route("/admin")
def admin():
    """Kitchen / Canteen Admin dashboard to view live queue, update statuses and cancel."""
    queue_list = list(order_queue)
    total_orders = len(all_orders)
    active_orders = len(queue_list)
    total_revenue = sum(o["total"] for o in all_orders.values() if o["status"] != "Cancelled")

    return render_template(
        "admin.html",
        queue=queue_list,
        all_orders=all_orders,
        total_orders=total_orders,
        active_orders=active_orders,
        total_revenue=total_revenue
    )


@app.route("/admin/update-status/<int:token>/<new_status>", methods=["POST"])
def update_status(token, new_status):
    """Admin route to update order status (Preparing, Ready, Completed)."""
    with order_lock:
        if token in all_orders:
            all_orders[token]["status"] = new_status

            if new_status == "Completed":
                # Remove from live queue
                for ord_item in list(order_queue):
                    if ord_item["token"] == token:
                        order_queue.remove(ord_item)
                        break
            flash(f"Order #{token} status changed to '{new_status}'.", "success")
        else:
            flash(f"Order #{token} not found.", "danger")

    return redirect(url_for("admin"))


# =====================================================
# REST API (FOR AJAX/LIVE UPDATES)
# =====================================================

@app.route("/api/queue-status")
def api_queue_status():
    """JSON API to fetch live queue count, wait time and current time."""
    count = len(order_queue)
    now = datetime.now()
    wait_mins = (count + 1) * 5
    pickup_time = (now + timedelta(minutes=wait_mins)).strftime("%I:%M %p")
    return jsonify({
        "active_orders": count,
        "estimated_wait_next": wait_mins,
        "current_time": now.strftime("%I:%M:%S %p"),
        "estimated_pickup": pickup_time
    })


@app.route("/api/order/<int:token>")
def api_order(token):
    """JSON API for order details."""
    order = all_orders.get(token)
    if not order:
        return jsonify({"success": False, "message": "Order not found"}), 404

    q_info = get_queue_info(token)
    return jsonify({
        "success": True,
        "order": order,
        "queue_info": q_info
    })


if __name__ == "__main__":
    port = 5000
    print("\n" + "=" * 60)
    print(" [OK] SMART CAMPUS FOOD PRE-ORDER SYSTEM RUNNING")
    print(f" Access Web Interface at: http://127.0.0.1:{port}")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
