"""
SuperMarket - Admin panel moduli
Statistika, loglar, foydalanuvchilar boshqaruvi
"""
from flask import Blueprint, request, jsonify
from .database import get_db, rows_to_list

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/overview', methods=['GET'])
def admin_overview():
    """Dashboard statistikasi"""
    conn = get_db()
    try:
        users = conn.execute("SELECT COUNT(*) as n FROM users").fetchone()['n']
        products = conn.execute("SELECT COUNT(*) as n FROM products").fetchone()['n']
        orders = conn.execute("SELECT COUNT(*) as n FROM orders").fetchone()['n']
        likes = conn.execute("SELECT COUNT(*) as n FROM likes").fetchone()['n']
        discounts = conn.execute("SELECT COUNT(*) as n FROM discounts").fetchone()['n']
        total_revenue = conn.execute(
            "SELECT COALESCE(SUM(total_price),0) as s FROM orders"
        ).fetchone()['s']
        return jsonify({
            'users': users,
            'products': products,
            'orders': orders,
            'likes': likes,
            'discounts': discounts,
            'total_revenue': total_revenue
        })
    finally:
        conn.close()

@admin_bp.route('/api/logs', methods=['GET'])
def get_logs():
    """Kirish/Chiqish jadvali"""
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM session_logs ORDER BY time DESC"
        ).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()

@admin_bp.route('/api/users', methods=['GET'])
def get_users():
    """Barcha foydalanuvchilar"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT id, name, last_name, username, email, tel, is_admin as isAdmin, created_at
            FROM users ORDER BY id DESC
        """).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()

@admin_bp.route('/api/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    """Foydalanuvchini o'chirish (Admin bo'lmaganlar)"""
    conn = get_db()
    try:
        user = conn.execute("SELECT is_admin FROM users WHERE id=?", (uid,)).fetchone()
        if user and user['is_admin']:
            return jsonify({'error': "Adminni o'chirib bo'lmaydi"}), 403
        conn.execute("DELETE FROM users WHERE id=? AND is_admin=0", (uid,))
        conn.commit()
        return jsonify({'message': "Foydalanuvchi o'chirildi"})
    finally:
        conn.close()

@admin_bp.route('/api/admin/likes', methods=['GET'])
def admin_likes():
    """Kim qaysi mahsulotni yoqtirgani"""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT l.id, l.liked_at,
                u.name, u.last_name, u.username,
                p.name AS product_name, p.category, p.subcategory, p.price
            FROM likes l
            JOIN users u ON u.id = l.user_id
            JOIN products p ON p.id = l.product_id
            ORDER BY l.liked_at DESC
        """).fetchall()
        return jsonify(rows_to_list(rows))
    finally:
        conn.close()
