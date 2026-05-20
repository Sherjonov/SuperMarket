"""
SuperMarket - Savat va Buyurtmalar moduli
To'liq savat, buyurtma berish, to'lov usullari, lokatsiya
"""
import random
from flask import Blueprint, request, jsonify

from .checkout_validate import (
    card_brand_ok,
    expiry_ok,
    luhn_valid,
    uz_id_card_ok,
    uz_passport_series_number_ok,
)
from .database import get_db, rows_to_list

orders_bp = Blueprint('orders', __name__)

# ============ SAVAT ============

@orders_bp.route('/api/cart', methods=['POST'])
def add_to_cart():
    """Savatga mahsulot qo'shish"""
    data = request.json or {}
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    size = (data.get('size') or '').strip()

    if not user_id or not product_id:
        return jsonify({'error': "Ma'lumotlar to'liq emas"}), 400
    if quantity < 1:
        return jsonify({'error': "Miqdor kamida 1 bo'lishi kerak"}), 400
    if quantity > 20:
        return jsonify({'error': "Bitta mahsulotdan 20 tadan ko'p bo'lmaydi"}), 400

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT * FROM carts WHERE user_id=? AND product_id=?", (user_id, product_id)
        ).fetchone()
        if existing:
            new_quantity = int(existing['quantity']) + quantity
            if new_quantity > 20:
                return jsonify({'error': "Bitta mahsulotdan 20 tadan ko'p bo'lmaydi"}), 400
            conn.execute(
                "UPDATE carts SET quantity=?, size=? WHERE id=?",
                (new_quantity, size or existing['size'], existing['id'])
            )
        else:
            conn.execute(
                "INSERT INTO carts (user_id,product_id,quantity,size) VALUES (?,?,?,?)",
                (user_id, product_id, quantity, size)
            )
        conn.commit()
        return jsonify({'message': "Savatga qo'shildi", 'success': True})
    finally:
        conn.close()

@orders_bp.route('/api/cart/<int:cid>', methods=['PUT'])
def update_cart_quantity(cid):
    """Savatdagi miqdorni yangilash"""
    data = request.json or {}
    quantity = int(data.get('quantity', 1))

    if quantity < 1:
        return jsonify({'error': "Miqdor kamida 1 bo'lishi kerak"}), 400
    if quantity > 20:
        return jsonify({'error': "Bitta mahsulotdan 20 tadan ko'p bo'lmaydi"}), 400

    conn = get_db()
    try:
        row = conn.execute("SELECT id FROM carts WHERE id=?", (cid,)).fetchone()
        if not row:
            return jsonify({'error': "Savat elementi topilmadi"}), 404
        conn.execute("UPDATE carts SET quantity=? WHERE id=?", (quantity, cid))
        conn.commit()
        return jsonify({'message': "Savat yangilandi", 'success': True})
    finally:
        conn.close()

@orders_bp.route('/api/cart/<int:uid>', methods=['GET'])
def get_cart(uid):
    """Savatdagi mahsulotlarni olish"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT c.id AS cart_id, c.quantity, c.size,
                p.*,
                CASE WHEN d.discount_percent IS NOT NULL
                     THEN CAST(ROUND(p.price*(1.0-d.discount_percent/100.0)) AS INTEGER)
                     ELSE p.price END AS discounted_price,
                d.discount_percent
            FROM carts c
            JOIN products p ON c.product_id = p.id
            LEFT JOIN discounts d ON d.product_id = p.id
            WHERE c.user_id=?
            ORDER BY c.id DESC
        """, (uid,)).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()

@orders_bp.route('/api/cart/<int:cid>', methods=['DELETE'])
def remove_from_cart(cid):
    """Savatdan o'chirish"""
    conn = get_db()
    try:
        conn.execute("DELETE FROM carts WHERE id=?", (cid,))
        conn.commit()
        return jsonify({'message': "Savatdan o'chirildi"})
    finally:
        conn.close()

@orders_bp.route('/api/cart/<int:uid>/clear', methods=['DELETE'])
def clear_cart(uid):
    """Savatni tozalash"""
    conn = get_db()
    try:
        conn.execute("DELETE FROM carts WHERE user_id=?", (uid,))
        conn.commit()
        return jsonify({'message': "Savat tozalandi"})
    finally:
        conn.close()

# ============ BUYURTMA BERISH ============

@orders_bp.route('/api/orders/checkout', methods=['POST'])
def checkout():
    """
    Buyurtma berish:
    - To'lov usuli
    - Karta ma'lumotlari (agar karta bo'lsa)
    - Lokatsiya
    - Yetkazib berish vaqti
    """
    data = request.json or {}
    user_id = data.get('user_id')
    payment_method = data.get('payment_method', '')  # 'card', 'cash', 'payme', 'click'
    delivery_address = data.get('delivery_address', '')
    recipient_name = (data.get('recipient_name') or '').strip()
    recipient_last_name = (data.get('recipient_last_name') or '').strip()
    recipient_phone = (data.get('recipient_phone') or '').strip()
    recipient_doc_type = (data.get('recipient_doc_type') or '').strip()
    recipient_passport_number = (data.get('recipient_passport_number') or '').strip()
    latitude = data.get('latitude', '')
    longitude = data.get('longitude', '')

    if not user_id:
        return jsonify({'error': "Foydalanuvchi aniqlanmadi"}), 400
    if not payment_method:
        return jsonify({'error': "To'lov usulini tanlang"}), 400
    if len(recipient_name) < 2:
        return jsonify({'error': "Ismni to'g'ri kiriting"}), 400
    if len(recipient_last_name) < 2:
        return jsonify({'error': "Familiyani to'g'ri kiriting"}), 400
    if len(recipient_phone) < 7:
        return jsonify({'error': "Telefon raqamni to'g'ri kiriting"}), 400
    if not delivery_address:
        return jsonify({'error': "Manzilni kiriting"}), 400

    if recipient_doc_type not in ('passport_uz', 'id_card_uz'):
        return jsonify({'error': "Hujjat turini tanlang"}), 400
    if recipient_doc_type == 'passport_uz' and not uz_passport_series_number_ok(recipient_passport_number):
        return jsonify({'error': "Pasport seriya va raqami noto'g'ri (masalan: AA1234567)"}), 400
    if recipient_doc_type == 'id_card_uz' and not uz_id_card_ok(recipient_passport_number):
        return jsonify({'error': "ID karta raqami noto'g'ri"}), 400

    if payment_method == 'card':
        cn = ''.join(c for c in (data.get('card_number') or '') if c.isdigit())
        ce = (data.get('card_expiry') or '').strip()
        cv = (data.get('card_cvv') or '').strip()
        if len(cn) < 13 or not luhn_valid(cn):
            return jsonify({'error': "Bank karta raqami haqiqiy emas (Luhn tekshiruvi)"}), 400
        if not card_brand_ok(cn):
            return jsonify({'error': "Karta turi qo'llab-quvvatlanmaydi (Visa/MC/Humo/Uzcard)"}), 400
        if not expiry_ok(ce):
            return jsonify({'error': "Karta muddati noto'g'ri yoki o'tgan"}), 400
        if len(cv) not in (3, 4):
            return jsonify({'error': "CVV noto'g'ri"}), 400

    # Yetkazib berish vaqtini hisoblash (random 20-60 daqiqa)
    delivery_minutes = random.randint(20, 60)
    full_address = delivery_address
    if latitude and longitude:
        full_address = f"{delivery_address} (Koordinatalar: {latitude}, {longitude})"

    conn = get_db()
    try:
        cart_items = conn.execute("""
            SELECT c.id AS cart_id, c.quantity, c.size, p.id AS product_id,
                p.name, p.price
            FROM carts c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id=?
        """, (user_id,)).fetchall()

        if not cart_items:
            return jsonify({'error': "Savat bo'sh"}), 400

        order_ids = []
        total_sum = 0
        for item in cart_items:
            total = item['price'] * item['quantity']
            total_sum += total
            cur = conn.execute("""
                INSERT INTO orders
                (user_id, product_id, product_name, quantity, price_per_unit, total_price,
                 size, payment_method, delivery_address, delivery_time, recipient_name,
                 recipient_last_name, recipient_phone, recipient_doc_type,
                 recipient_passport_number)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                user_id, item['product_id'], item['name'],
                item['quantity'], item['price'], total,
                item['size'], payment_method, full_address, delivery_minutes,
                recipient_name, recipient_last_name, recipient_phone,
                recipient_doc_type, recipient_passport_number
            ))
            order_ids.append(cur.lastrowid)
            conn.execute("DELETE FROM carts WHERE id=?", (item['cart_id'],))

        conn.commit()
        return jsonify({
            'success': True,
            'message': "Buyurtma muvaffaqiyatli berildi!",
            'delivery_minutes': delivery_minutes,
            'total_sum': total_sum,
            'order_ids': order_ids,
            'payment_method': payment_method,
            'delivery_address': full_address
        })
    finally:
        conn.close()

# ============ ADMIN BUYURTMALAR ============

@orders_bp.route('/api/orders', methods=['GET'])
def get_orders():
    """Barcha buyurtmalarni olish (Admin)"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT o.*, u.name, u.last_name, u.username
            FROM orders o
            JOIN users u ON u.id = o.user_id
            ORDER BY o.order_date DESC
        """).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()


# ============ BUYURTMA STATUS UPDATE ============

@orders_bp.route('/api/orders/<int:oid>/status', methods=['PUT'])
def update_order_status(oid):
    """Buyurtma holatini yangilash (Admin tomonidan)"""
    data = request.json or {}
    status = (data.get('status') or '').strip()
    allowed = ['Yangi', 'Tasdiqlangan', 'Yetkazilmoqda', 'Yetkazildi', 'Bekor qilindi']
    if status not in allowed:
        return jsonify({'error': f"Status noto'g'ri. Mumkin statuslar: {', '.join(allowed)}"}), 400

    conn = get_db()
    try:
        row = conn.execute("SELECT id FROM orders WHERE id=?", (oid,)).fetchone()
        if not row:
            return jsonify({'error': 'Buyurtma topilmadi'}), 404
        conn.execute("UPDATE orders SET status=? WHERE id=?", (status, oid))
        conn.commit()
        return jsonify({'success': True, 'message': f"Buyurtma #{oid} statusi '{status}' ga o'zgartirildi"})
    finally:
        conn.close()


@orders_bp.route('/api/orders/user/<int:uid>', methods=['GET'])
def get_user_orders(uid):
    """Foydalanuvchining barcha buyurtmalari"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT
                o.id, o.user_id, o.product_id, o.product_name,
                o.quantity, o.price_per_unit, o.total_price,
                o.payment_method, o.delivery_address, o.status,
                o.order_date,
                p.image_url
            FROM orders o
            LEFT JOIN products p ON p.id = o.product_id
            WHERE o.user_id = ?
            ORDER BY o.order_date DESC
        """, (uid,)).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()
