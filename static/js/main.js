// =====================================================
// SMART CAMPUS FOOD PRE-ORDER SYSTEM - REAL-TIME JS
// =====================================================

document.addEventListener("DOMContentLoaded", () => {
    updateCartUI();
    initRealTimeClock();
    initLiveQueuePolling();
    initOrderStatusLiveTracking();
    initReceiptCountdown();
    initAdminLiveSync();
});

// =====================================================
// 1. REAL-TIME LIVE CLOCK
// =====================================================
function initRealTimeClock() {
    function updateClock() {
        const clockEl = document.getElementById("live-clock");
        if (!clockEl) return;

        const now = new Date();
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, "0");
        const seconds = String(now.getSeconds()).padStart(2, "0");
        const ampm = hours >= 12 ? "PM" : "AM";
        hours = hours % 12 || 12;

        clockEl.innerText = `${hours}:${minutes}:${seconds} ${ampm}`;
    }

    updateClock();
    setInterval(updateClock, 1000);
}

// =====================================================
// 2. REAL-TIME QUEUE & WAIT SYNC (FETCH FROM API)
// =====================================================
function initLiveQueuePolling() {
    async function fetchQueueStatus() {
        try {
            const res = await fetch("/api/queue-status");
            if (!res.ok) return;
            const data = await res.json();

            // Update Tray widget elements
            const queueEl = document.getElementById("live-tray-queue");
            const waitEl = document.getElementById("live-tray-wait");
            const pickupEl = document.getElementById("live-tray-pickup");
            const heroQueueCount = document.getElementById("live-queue-count");

            if (queueEl) queueEl.innerText = `${data.active_orders} Orders`;
            if (waitEl) waitEl.innerText = `~${data.estimated_wait_next} min`;
            if (pickupEl) pickupEl.innerText = data.estimated_pickup;
            if (heroQueueCount) heroQueueCount.innerText = data.active_orders;
        } catch (e) {
            // Ignore temporary network glitches
        }
    }

    // Initial fetch
    fetchQueueStatus();
    // Poll every 3 seconds for real-time updates
    setInterval(fetchQueueStatus, 3000);
}

// =====================================================
// 3. REAL-TIME ORDER STATUS TRACKING (STATUS PAGE)
// =====================================================
function initOrderStatusLiveTracking() {
    const statusCard = document.querySelector(".status-card");
    const tokenBadge = document.querySelector(".token-badge");
    if (!statusCard || !tokenBadge) return;

    const tokenText = tokenBadge.innerText.replace(/[^0-9]/g, "");
    if (!tokenText) return;

    const token = parseInt(tokenText);
    let currentStatus = document.querySelector(".status-badge")?.innerText?.trim();

    // If order is already completed or cancelled, no need to poll
    if (currentStatus === "Completed" || currentStatus === "Cancelled") return;

    setInterval(async () => {
        try {
            const res = await fetch(`/api/order/${token}`);
            if (!res.ok) return;
            const data = await res.json();
            if (data.success && data.order) {
                // If status changed, reload to show new progress step & badges smoothly
                if (data.order.status !== currentStatus) {
                    window.location.reload();
                }
            }
        } catch (err) {
            // Ignore
        }
    }, 3000);
}

// =====================================================
// 4. REAL-TIME RECEIPT COUNTDOWN TIMER
// =====================================================
function initReceiptCountdown() {
    const countdownCard = document.querySelector(".live-countdown-card");
    const timerEl = document.getElementById("receipt-countdown");
    if (!countdownCard || !timerEl) return;

    const pickupStr = countdownCard.dataset.pickup; // e.g. "01:30 PM"
    if (!pickupStr) return;

    function tick() {
        const now = new Date();
        const parts = pickupStr.trim().split(" ");
        if (parts.length < 2) return;

        const timeParts = parts[0].split(":");
        let targetHours = parseInt(timeParts[0]);
        const targetMins = parseInt(timeParts[1]);
        const isPM = parts[1].toUpperCase() === "PM";

        if (isPM && targetHours < 12) targetHours += 12;
        if (!isPM && targetHours === 12) targetHours = 0;

        const targetDate = new Date();
        targetDate.setHours(targetHours, targetMins, 0, 0);

        // If pickup time has passed into next day (e.g. ordered at 11:58 PM)
        if (targetDate.getTime() < now.getTime() - 1000 * 60 * 30) {
            targetDate.setDate(targetDate.getDate() + 1);
        }

        const diffMs = targetDate.getTime() - now.getTime();
        if (diffMs <= 0) {
            timerEl.innerText = "🔔 Ready for collection at counter!";
            timerEl.style.color = "#059669";
            return;
        }

        const totalSecs = Math.floor(diffMs / 1000);
        const mins = Math.floor(totalSecs / 60);
        const secs = totalSecs % 60;

        timerEl.innerText = `${mins}m ${String(secs).padStart(2, "0")}s remaining`;
    }

    tick();
    setInterval(tick, 1000);
}

// =====================================================
// 5. ADMIN KITCHEN DASHBOARD LIVE AUTO-SYNC
// =====================================================
function initAdminLiveSync() {
    const adminTop = document.querySelector(".admin-topbar");
    if (!adminTop) return;

    const initialCountEl = document.querySelector(".admin-stat-card.active-card .stat-value");
    const initialCount = initialCountEl ? parseInt(initialCountEl.innerText) || 0 : -1;

    setInterval(async () => {
        try {
            const res = await fetch("/api/queue-status");
            if (!res.ok) return;
            const data = await res.json();
            if (typeof data.active_orders === "number" && data.active_orders !== initialCount) {
                window.location.reload();
            }
        } catch (e) {
            // Ignore
        }
    }, 4000);
}

// =====================================================
// 4. CART & MENU INTERACTIONS
// =====================================================
function getFoodData(itemId) {
    const card = document.querySelector(`.food-card[data-id="${itemId}"]`);
    if (!card) return null;
    return {
        id: itemId,
        name: card.dataset.name,
        price: parseFloat(card.dataset.price)
    };
}

function increaseQty(itemId) {
    const input = document.getElementById(`qty_${itemId}`);
    if (!input) return;
    let val = parseInt(input.value) || 0;
    if (val < 20) {
        input.value = val + 1;
        updateCartUI();
    }
}

function decreaseQty(itemId) {
    const input = document.getElementById(`qty_${itemId}`);
    if (!input) return;
    let val = parseInt(input.value) || 0;
    if (val > 0) {
        input.value = val - 1;
        updateCartUI();
    }
}

function updateCartUI() {
    const qtyInputs = document.querySelectorAll('.qty-input');
    if (!qtyInputs || qtyInputs.length === 0) return;

    const cartContainer = document.getElementById('cart-items-container');
    const badgeCount = document.getElementById('total-items-badge');
    const subtotalEl = document.getElementById('bill-subtotal');
    const discountRow = document.getElementById('discount-row');
    const discountEl = document.getElementById('bill-discount');
    const discountHint = document.getElementById('discount-hint');
    const totalEl = document.getElementById('bill-total');
    const submitBtn = document.getElementById('btn-submit-order');

    let totalItems = 0;
    let subtotal = 0;
    let selectedItems = [];

    qtyInputs.forEach(input => {
        const qty = parseInt(input.value) || 0;
        if (qty > 0) {
            const itemId = input.id.replace('qty_', '');
            const itemData = getFoodData(itemId);
            if (itemData) {
                totalItems += qty;
                const itemTotal = itemData.price * qty;
                subtotal += itemTotal;
                selectedItems.push({
                    name: itemData.name,
                    qty: qty,
                    price: itemData.price,
                    total: itemTotal
                });
            }
        }
    });

    // Update Items Count Badge
    if (badgeCount) {
        badgeCount.innerText = `${totalItems} item${totalItems === 1 ? '' : 's'}`;
    }

    // Render Cart Items
    if (cartContainer) {
        if (selectedItems.length === 0) {
            cartContainer.innerHTML = `
                <div class="empty-cart-msg">
                    <span class="empty-icon">🛒</span>
                    <p>Your tray is currently empty.</p>
                    <small>Click '+' on any food item to add.</small>
                </div>
            `;
        } else {
            cartContainer.innerHTML = selectedItems.map(item => `
                <div class="cart-item-row">
                    <div>
                        <div class="cart-item-title">${item.name}</div>
                        <div class="cart-item-calc">${item.qty} × ₹${item.price}</div>
                    </div>
                    <div class="cart-item-price">₹${item.total.toFixed(2)}</div>
                </div>
            `).join('');
        }
    }

    // Calculate Discount & Total
    let discount = 0;
    if (subtotal >= 300) {
        discount = subtotal * 0.10;
        if (discountRow) discountRow.style.display = 'flex';
        if (discountEl) discountEl.innerText = `-₹${discount.toFixed(2)}`;
        if (discountHint) {
            discountHint.innerHTML = `🎉 <strong>10% Campus Discount Applied!</strong> (You saved ₹${discount.toFixed(2)})`;
            discountHint.style.background = '#ecfdf5';
            discountHint.style.borderColor = '#a7f3d0';
            discountHint.style.color = '#065f46';
        }
    } else {
        if (discountRow) discountRow.style.display = 'none';
        const remaining = 300 - subtotal;
        if (discountHint) {
            discountHint.innerHTML = `💡 Add <strong>₹${remaining.toFixed(2)}</strong> more to unlock <strong>10% OFF</strong>!`;
            discountHint.style.background = '#fffbeb';
            discountHint.style.borderColor = '#fef3c7';
            discountHint.style.color = '#b45309';
        }
    }

    const finalTotal = subtotal - discount;

    if (subtotalEl) subtotalEl.innerText = `₹${subtotal.toFixed(2)}`;
    if (totalEl) totalEl.innerText = `₹${finalTotal.toFixed(2)}`;

    // Enable / Disable submit button
    if (submitBtn) {
        submitBtn.disabled = totalItems === 0;
    }
}
