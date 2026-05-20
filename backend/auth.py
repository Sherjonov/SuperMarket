"""
SuperMarket - Autentifikatsiya moduli
Ro'yxatdan o'tish, kirish, chiqish
"""
import re
from flask import Blueprint, request, jsonify
from .database import get_db, hash_password, check_password, random_code, rows_to_list, row_to_dict

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register/send-code', methods=['POST'])
def register_send_code():
    """Ro'yxatdan o'tish - email kod yuborish"""
    data = request.json or {}
    name = (data.get('name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    username = (data.get('username') or '').strip()
    tel = (data.get('tel') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '')

    # Validatsiya
    if len(name) < 2:
        return jsonify({'error': "Ism kamida 2 ta harf bo'lishi kerak"}), 400
    if len(last_name) < 2:
        return jsonify({'error': "Familiya kamida 2 ta harf bo'lishi kerak"}), 400
    if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
        return jsonify({'error': "Username 5-20 ta lotin harfi yoki raqam bo'lishi kerak"}), 400
    if not re.match(r'^\S+@\S+\.\S+$', email):
        return jsonify({'error': "Email format noto'g'ri"}), 400
    if len(password) < 6:
        return jsonify({'error': "Parol kamida 6 ta belgi bo'lishi kerak"}), 400

    conn = get_db()
    try:
        # Username tekshirish
        if conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone():
            return jsonify({'error': "Bu username allaqachon band"}), 400
        # Email tekshirish
        if conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
            return jsonify({'error': "Bu email allaqachon ro'yxatdan o'tgan"}), 400

        code = random_code(6)
        conn.execute(
            "INSERT INTO users (name,last_name,username,tel,email,email_code,password,is_admin) VALUES (?,?,?,?,?,?,?,0)",
            (name, last_name, username, tel, email, code, hash_password(password))
        )
        conn.commit()
        return jsonify({
            'message': f"Kod emailingizga yuborildi",
            'code': code,  # Real loyihada bu yerda email yuboriladi
            'success': True
        })
    finally:
        conn.close()

@auth_bp.route('/api/register/verify', methods=['POST'])
def register_verify():
    """Email kodni tasdiqlash"""
    data = request.json or {}
    email = (data.get('email') or '').strip().lower()
    code = (data.get('email_code') or '').strip()

    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not user:
            return jsonify({'error': "Foydalanuvchi topilmadi"}), 404
        if user['email_code'] != code:
            return jsonify({'error': "Kod noto'g'ri. Qaytadan urinib ko'ring"}), 400
        return jsonify({'message': "Email tasdiqlandi!", 'success': True})
    finally:
        conn.close()

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Kirish"""
    data = request.json or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '')

    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE LOWER(username)=LOWER(?)", (username,)).fetchone()
        if not user:
            return jsonify({'error': "Username topilmadi"}), 404
        if not check_password(password, user['password']):
            return jsonify({'error': "Parol noto'g'ri"}), 400

        ip = request.remote_addr or 'unknown'
        conn.execute(
            "INSERT INTO session_logs (user_id,name,last_name,username,action,ip_address) VALUES (?,?,?,?,'login',?)",
            (user['id'], user['name'], user['last_name'], user['username'], ip)
        )
        conn.commit()
        return jsonify({
            'id': user['id'],
            'name': user['name'],
            'last_name': user['last_name'],
            'username': user['username'],
            'isAdmin': bool(user['is_admin']),
            'email': user['email'],
            'tel': user['tel']
        })
    finally:
        conn.close()

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """Chiqish"""
    data = request.json or {}
    conn = get_db()
    try:
        ip = request.remote_addr or 'unknown'
        conn.execute(
            "INSERT INTO session_logs (user_id,name,last_name,username,action,ip_address) VALUES (?,?,?,?,'logout',?)",
            (data.get('user_id', 0), data.get('name', ''), data.get('last_name', ''), data.get('username', ''), ip)
        )
        conn.commit()
        return jsonify({'message': "Chiqish muvaffaqiyatli"})
    finally:
        conn.close()

@auth_bp.route('/api/settings/username', methods=['PUT'])
def change_username():
    """Username o'zgartirish"""
    data = request.json or {}
    new_username = (data.get('username') or '').strip()
    if not re.match(r'^[a-zA-Z0-9_]{5,20}$', new_username):
        return jsonify({'error': "Username format xato"}), 400

    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE id=? AND email=?",
                            (data.get('user_id'), data.get('email', '').lower())).fetchone()
        if not user:
            return jsonify({'error': "Email tasdiqlanmadi"}), 400
        dup = conn.execute("SELECT id FROM users WHERE username=? AND id!=?",
                           (new_username, data.get('user_id'))).fetchone()
        if dup:
            return jsonify({'error': "Bu username band"}), 400
        conn.execute("UPDATE users SET username=? WHERE id=?", (new_username, data.get('user_id')))
        conn.commit()
        return jsonify({'message': "Username muvaffaqiyatli yangilandi"})
    finally:
        conn.close()

@auth_bp.route('/api/settings/password', methods=['PUT'])
def change_password():
    """Parol o'zgartirish"""
    data = request.json or {}
    if len(data.get('new_password', '')) < 6:
        return jsonify({'error': "Yangi parol kamida 6 ta belgi bo'lishi kerak"}), 400
    if data.get('new_password') != data.get('confirm_password'):
        return jsonify({'error': "Parollar mos kelmaydi"}), 400

    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE id=?", (data.get('user_id'),)).fetchone()
        if not user:
            return jsonify({'error': "Foydalanuvchi topilmadi"}), 404
        if not check_password(data.get('old_password', ''), user['password']):
            return jsonify({'error': "Eski parol noto'g'ri"}), 400
        conn.execute("UPDATE users SET password=? WHERE id=?",
                     (hash_password(data['new_password']), data['user_id']))
        conn.commit()
        return jsonify({'message': "Parol muvaffaqiyatli yangilandi"})
    finally:
        conn.close()
