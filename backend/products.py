"""
SuperMarket - Mahsulotlar moduli
Mahsulotlar, chegirmalar, yoqtirishlar
"""
import os
import uuid

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from .database import get_db, rows_to_list, row_to_dict

products_bp = Blueprint('products', __name__)

PUBLIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public')
UPLOAD_DIR = os.path.join(PUBLIC_ROOT, 'uploads')
ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

# ============ MAHSULOTLAR ============

@products_bp.route('/api/products', methods=['GET'])
def get_products():
    """Barcha mahsulotlarni olish (chegirmalar bilan)"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT p.*,
                d.discount_percent,
                CASE WHEN d.discount_percent IS NOT NULL
                     THEN CAST(ROUND(p.price * (1.0 - d.discount_percent / 100.0)) AS INTEGER)
                     ELSE p.price END AS discounted_price
            FROM products p
            LEFT JOIN discounts d ON d.product_id = p.id
            ORDER BY p.category, p.subcategory, p.name
        """).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()

@products_bp.route('/api/upload/product-image', methods=['POST'])
def upload_product_image():
    """Mahsulot rasmini kompyuterdan yuklash — serverda saqlanadi."""
    if 'file' not in request.files:
        return jsonify({'error': "Rasm faylini tanlang"}), 400
    f = request.files['file']
    if not f or not f.filename:
        return jsonify({'error': "Rasm faylini tanlang"}), 400
    ext = secure_filename(f.filename).rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_IMAGE_EXT:
        return jsonify({'error': "Faqat PNG, JPG, JPEG, WEBP, GIF"}), 400
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(UPLOAD_DIR, fname)
    f.save(path)
    return jsonify({'url': f'/uploads/{fname}', 'success': True})


@products_bp.route('/api/products', methods=['POST'])
def add_product():
    """Yangi mahsulot qo'shish (Admin)"""
    data = request.json or {}
    name = (data.get('name') or '').strip()
    category = (data.get('category') or '').strip()
    subcategory = (data.get('subcategory') or '').strip()
    price = data.get('price')
    sizes = (data.get('sizes') or '').strip()
    stock = data.get('stock', 50)
    image_url = (data.get('image_url') or '').strip()

    if not name or not category or not subcategory or not price:
        return jsonify({'error': "Barcha majburiy maydonlarni to'ldiring"}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO products (name,category,subcategory,price,sizes,stock,image_url) VALUES (?,?,?,?,?,?,?)",
            (name, category, subcategory, int(price), sizes, int(stock), image_url)
        )
        conn.commit()
        return jsonify({'message': "Mahsulot muvaffaqiyatli qo'shildi"})
    finally:
        conn.close()

@products_bp.route('/api/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    """Mahsulotni o'chirish (Admin)"""
    conn = get_db()
    try:
        conn.execute("DELETE FROM discounts WHERE product_id=?", (pid,))
        conn.execute("DELETE FROM likes WHERE product_id=?", (pid,))
        conn.execute("DELETE FROM carts WHERE product_id=?", (pid,))
        conn.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
        return jsonify({'message': "Mahsulot o'chirildi"})
    finally:
        conn.close()

# ============ CHEGIRMALAR ============

@products_bp.route('/api/discounts', methods=['GET'])
def get_discounts():
    """Barcha chegirmalarni olish"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT d.*, p.name AS product_name, p.price, p.category, p.subcategory, p.image_url
            FROM discounts d
            JOIN products p ON d.product_id = p.id
            ORDER BY d.created_at DESC
        """).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()

@products_bp.route('/api/discounts', methods=['POST'])
def add_discount():
    """Chegirma qo'shish (Admin)"""
    data = request.json or {}
    product_id = data.get('product_id')
    discount_percent = data.get('discount_percent')

    if not product_id or not discount_percent:
        return jsonify({'error': "Mahsulot va chegirma foizini kiriting"}), 400
    if not (1 <= int(discount_percent) <= 99):
        return jsonify({'error': "Chegirma 1-99% oralig'ida bo'lishi kerak"}), 400

    conn = get_db()
    try:
        existing = conn.execute("SELECT id FROM discounts WHERE product_id=?", (product_id,)).fetchone()
        if existing:
            conn.execute(
                "UPDATE discounts SET discount_percent=?, created_at=CURRENT_TIMESTAMP WHERE product_id=?",
                (int(discount_percent), product_id)
            )
        else:
            conn.execute(
                "INSERT INTO discounts (product_id, discount_percent) VALUES (?,?)",
                (product_id, int(discount_percent))
            )
        conn.commit()
        return jsonify({'message': "Chegirma muvaffaqiyatli qo'shildi"})
    finally:
        conn.close()

@products_bp.route('/api/discounts/<int:pid>', methods=['DELETE'])
def delete_discount(pid):
    """Chegirmani o'chirish (Admin)"""
    conn = get_db()
    try:
        conn.execute("DELETE FROM discounts WHERE product_id=?", (pid,))
        conn.commit()
        return jsonify({'message': "Chegirma olib tashlandi"})
    finally:
        conn.close()

# ============ YOQTIRGANLARIM ============

@products_bp.route('/api/likes', methods=['POST'])
def toggle_like():
    """Like qo'shish/olib tashlash"""
    data = request.json or {}
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not user_id or not product_id:
        return jsonify({'error': "Ma'lumotlar to'liq emas"}), 400

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM likes WHERE user_id=? AND product_id=?", (user_id, product_id)
        ).fetchone()
        if existing:
            conn.execute("DELETE FROM likes WHERE id=?", (existing['id'],))
            conn.execute("UPDATE products SET likes_count=MAX(0,likes_count-1) WHERE id=?", (product_id,))
            conn.commit()
            return jsonify({'liked': False, 'message': "Like olib tashlandi"})
        else:
            conn.execute("INSERT INTO likes (user_id, product_id) VALUES (?,?)", (user_id, product_id))
            conn.execute("UPDATE products SET likes_count=likes_count+1 WHERE id=?", (product_id,))
            conn.commit()
            return jsonify({'liked': True, 'message': "Yoqtirganlarimga qo'shildi"})
    finally:
        conn.close()

@products_bp.route('/api/likes/<int:uid>', methods=['GET'])
def get_liked_products(uid):
    """Foydalanuvchi yoqtirgan mahsulotlar"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT p.*,
                d.discount_percent,
                CASE WHEN d.discount_percent IS NOT NULL
                     THEN CAST(ROUND(p.price*(1.0-d.discount_percent/100.0)) AS INTEGER)
                     ELSE p.price END AS discounted_price
            FROM likes l
            JOIN products p ON l.product_id = p.id
            LEFT JOIN discounts d ON d.product_id = p.id
            WHERE l.user_id=?
            ORDER BY l.liked_at DESC
        """, (uid,)).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()

@products_bp.route('/api/myLikes/<int:uid>', methods=['GET'])
def get_my_like_ids(uid):
    """Foydalanuvchi like bosgan mahsulot IDlari"""
    conn = get_db()
    try:
        rows = conn.execute("SELECT product_id FROM likes WHERE user_id=?", (uid,)).fetchall()
        return jsonify([r['product_id'] for r in rows])
    finally:
        conn.close()
