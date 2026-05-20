#!/usr/bin/env python3
"""SuperMarket v2 - Main Entry Point"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from backend.app import create_app
from backend.database import init_db

def run_seeds():
    try:
        from backend.seed_500 import run as seed_run
        seed_run()
    except Exception as e:
        print(f"  Seed: {e}")
    try:
        from backend.fix_images_v2 import run as img_run
        img_run()
    except Exception as e:
        print(f"  Images: {e}")

if __name__ == '__main__':
    print("=" * 55)
    print("  🛒  SuperMarket v2 - Server ishga tushmoqda")
    print("=" * 55)
    init_db()
    print("✅ Database tayyor")
    run_seeds()
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🌐 Brauzerda oching: http://localhost:{port}")
    print("👤 Admin: Sherjanov / qwerty123321")
    print("🔴 To'xtatish: Ctrl+C")
    print("=" * 55)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
