"""
SuperMarket - Flask Application Factory
Barcha blueprintlarni ulaydi
"""
import os
from flask import Flask, send_file, send_from_directory, jsonify
from flask_cors import CORS

from .auth import auth_bp
from .products import products_bp
from .orders import orders_bp
from .admin import admin_bp

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public')

def create_app():
    """Flask applicationni yaratadi va sozlaydi"""
    # Static fayllarni manual boshqaramiz - Flask built-in static ni o'chiramiz
    app = Flask(__name__, static_folder=None)
    CORS(app)

    # Blueprintlarni ro'yxatdan o'tkazish
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    # CSS, JS, images - static fayllar
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(PUBLIC_DIR, 'css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(PUBLIC_DIR, 'js'), filename)

    @app.route('/images/<path:filename>')
    def serve_images(filename):
        return send_from_directory(os.path.join(PUBLIC_DIR, 'images'), filename)

    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(os.path.join(PUBLIC_DIR, 'uploads'), filename)

    # Bosh sahifa va barcha SPA route'lari
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_index(path):
        # API so'rovlari bu yerga kelmasin
        if path.startswith('api/'):
            return jsonify({'error': 'API endpoint topilmadi'}), 404
        # Boshqa barcha so'rovlar uchun index.html
        return send_file(os.path.join(PUBLIC_DIR, 'index.html'))

    # 404 handler
    @app.errorhandler(404)
    def not_found(e):
        if '/api/' in str(e):
            return jsonify({'error': 'Topilmadi'}), 404
        return send_file(os.path.join(PUBLIC_DIR, 'index.html'))

    # 500 handler
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Server xatosi: ' + str(e)}), 500

    return app
