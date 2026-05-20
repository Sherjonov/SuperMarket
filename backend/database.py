"""
SuperMarket - Database moduli
SQLite database yaratish, jadvallar va seed data
"""
import sqlite3
import hashlib
import os
import random

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'supermarket.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def hash_password(pwd):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def check_password(pwd, hashed):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest() == hashed

def random_code(n=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(n)])

def rows_to_list(rows):
    return [dict(r) for r in rows]

def row_to_dict(row):
    return dict(row) if row else None

def create_tables(conn):
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        tel TEXT DEFAULT '',
        email TEXT UNIQUE NOT NULL,
        email_code TEXT DEFAULT '',
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS session_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT DEFAULT '',
        last_name TEXT DEFAULT '',
        username TEXT NOT NULL,
        action TEXT NOT NULL,
        ip_address TEXT DEFAULT '',
        time TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        price INTEGER NOT NULL,
        sizes TEXT DEFAULT '',
        image_url TEXT DEFAULT '',
        likes_count INTEGER DEFAULT 0,
        stock INTEGER DEFAULT 50,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS discounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL UNIQUE,
        discount_percent INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        liked_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price_per_unit INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        size TEXT DEFAULT '',
        payment_method TEXT DEFAULT '',
        delivery_address TEXT DEFAULT '',
        delivery_time INTEGER DEFAULT 30,
        recipient_name TEXT DEFAULT '',
        recipient_last_name TEXT DEFAULT '',
        recipient_phone TEXT DEFAULT '',
        recipient_doc_type TEXT DEFAULT '',
        recipient_passport_number TEXT DEFAULT '',
        status TEXT DEFAULT 'Yangi',
        order_date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        size TEXT DEFAULT '',
        UNIQUE(user_id, product_id)
    )''')

    # Real loyihadagi kabi tezkor ishlash uchun indekslar
    c.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category, subcategory)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_date ON orders(user_id, order_date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_user_time ON session_logs(user_id, time)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_likes_user_product ON likes(user_id, product_id)")

    conn.commit()

def seed_admin(conn):
    c = conn.cursor()
    admin = c.execute("SELECT id FROM users WHERE LOWER(username)=LOWER(?)", ('Sherjanov',)).fetchone()
    if admin:
        # Mavjud admin account oddiy user bo'lib qolgan bo'lsa ham admin qilib qo'yamiz
        c.execute("UPDATE users SET is_admin=1 WHERE id=?", (admin['id'],))
    else:
        c.execute("""INSERT INTO users (name,last_name,username,tel,email,email_code,password,is_admin)
                     VALUES (?,?,?,?,?,?,?,1)""",
                  ('Sherjanov', 'Abduaziz', 'Sherjanov',
                   '+998 90 000 00 00', 'admin@supermarket.uz',
                   '000000', hash_password('qwerty123321')))
    conn.commit()

def seed_products(conn):
    c = conn.cursor()
    count = c.execute("SELECT COUNT(*) as n FROM products").fetchone()['n']
    if count > 0:
        return

    imgs = {
        'issiq': [
            "https://images.unsplash.com/photo-1544923246-77307dd654cb?w=400",
            "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
            "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400",
            "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
        ],
        'yozgi': [
            "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400",
            "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
            "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400",
        ],
        'bolalar': [
            "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400",
            "https://images.unsplash.com/photo-1503919005314-30d533d8e938?w=400",
        ],
        'meva': [
            "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400",
            "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400",
            "https://images.unsplash.com/photo-1547514701-42782101795e?w=400",
            "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400",
            "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400",
        ],
        'fast': [
            "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
            "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
            "https://images.unsplash.com/photo-1562802378-063ec186a863?w=400",
            "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400",
            "https://images.unsplash.com/photo-1561043433-aaf687c4cf04?w=400",
        ],
        'milliy': [
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400",
            "https://images.unsplash.com/photo-1547592180-85f173990554?w=400",
            "https://images.unsplash.com/photo-1544025162-d76694265947?w=400",
            "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400",
        ],
        'ichimlik': [
            "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400",
            "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400",
            "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=400",
            "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",
            "https://images.unsplash.com/photo-1564890369478-c89ca3d9cde1?w=400",
        ],
        'shirin': [
            "https://images.unsplash.com/photo-1599599810694-b5b37304c041?w=400",
            "https://images.unsplash.com/photo-1571167366136-b57e069b5c99?w=400",
            "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400",
            "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400",
            "https://images.unsplash.com/photo-1582716401301-b2407dc7563d?w=400",
        ],
        'telefon': [
            "https://images.unsplash.com/photo-1696446702183-cbd44df63e73?w=400",
            "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400",
            "https://images.unsplash.com/photo-1578345628641-5a6a1a70f92a?w=400",
        ],
        'noutbuk': [
            "https://images.unsplash.com/photo-1611186871525-47de4bda9ddd?w=400",
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400",
            "https://images.unsplash.com/photo-1542393545-10f5cde2c810?w=400",
            "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400",
        ],
        'planshet': [
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
            "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=400",
        ],
    }

    def img(key, i): return imgs[key][i % len(imgs[key])]

    products = []

    # ===== KIYIMLAR - Issiq kiyimlar (35 ta) =====
    issiq_kiyimlar = [
        ("Erkaklar qora pufka", 350000, "S,M,L,XL,XXL"),
        ("Ayollar oq pufka", 360000, "XS,S,M,L,XL"),
        ("Unisex ko'k pufka", 340000, "S,M,L,XL"),
        ("Jigarrang qishki palto", 650000, "S,M,L,XL,XXL"),
        ("Qora qishki palto ayollar", 700000, "XS,S,M,L,XL"),
        ("Kulrang trikotaj sviter", 120000, "S,M,L,XL,XXL"),
        ("Ko'k trikotaj sviter", 130000, "XS,S,M,L,XL"),
        ("Erkaklar termo ichki kiyim", 80000, "S,M,L,XL,XXL"),
        ("Ayollar termo ichki kiyim", 85000, "XS,S,M,L,XL"),
        ("Teri qo'lqop (qora)", 45000, "S,M,L"),
        ("Jun qizil sharf", 35000, "OneSize"),
        ("Kulrang quloqchin shapka", 55000, "OneSize"),
        ("Erkaklar qishki etigi", 280000, "40,41,42,43,44,45"),
        ("Ayollar qishki etigi", 260000, "36,37,38,39,40,41"),
        ("Jun paypoq (3 juft)", 25000, "S,M,L"),
        ("Erkaklar flanes ko'ylak", 95000, "S,M,L,XL,XXL"),
        ("Yostiqli qishki kurtka", 320000, "S,M,L,XL,XXL,XXXL"),
        ("Balaclava nimcha", 40000, "OneSize"),
        ("Qishki sport kostyum", 180000, "S,M,L,XL,XXL"),
        ("Qishki uyqu kiyimi", 95000, "S,M,L,XL"),
        ("Ayollar jun ko'ylak", 145000, "XS,S,M,L,XL"),
        ("Qishki sport poyabzal", 220000, "38,39,40,41,42,43,44"),
        ("Erkaklar yostiqchalı kurtka qizil", 310000, "S,M,L,XL,XXL"),
        ("Ayollar yostiqchalı kurtka binafsha", 330000, "XS,S,M,L,XL"),
        ("Qishki gilam ko'ylak", 155000, "S,M,L,XL"),
        ("Erkaklar qishki shim", 180000, "28,30,32,34,36"),
        ("Ayollar qishki shim", 175000, "24,26,28,30,32"),
        ("Qo'lqop-sharf to'plam", 65000, "OneSize"),
        ("Erkaklar qishki sport shim", 120000, "S,M,L,XL,XXL"),
        ("Ayollar qishki sport shim", 125000, "XS,S,M,L,XL"),
        ("Qishki erkaklar jemperi", 160000, "S,M,L,XL,XXL"),
        ("Qishki ayollar jemperi", 165000, "XS,S,M,L,XL"),
        ("Qalin fleece kostyum", 200000, "S,M,L,XL,XXL"),
        ("Qishki to'n (erkaklar)", 850000, "S,M,L,XL"),
        ("Qishki to'n (ayollar)", 870000, "XS,S,M,L"),
    ]
    for i, (name, price, sizes) in enumerate(issiq_kiyimlar):
        products.append((name, "Kiyimlar", "Issiq kiyimlar", price, sizes, 50, img('issiq', i)))

    # ===== KIYIMLAR - Yozgi kiyimlar (35 ta) =====
    yozgi_kiyimlar = [
        ("Erkaklar oq futbolka", 35000, "S,M,L,XL,XXL"),
        ("Ayollar qora futbolka", 38000, "XS,S,M,L,XL"),
        ("Jinsi shorti", 65000, "S,M,L,XL"),
        ("Ipak ayollar ko'ylak", 150000, "XS,S,M,L,XL"),
        ("Panama shapka", 30000, "S,M,L"),
        ("Erkaklar sandali", 70000, "40,41,42,43,44,45"),
        ("Ayollar sandali", 65000, "36,37,38,39,40"),
        ("Sport mayfa", 25000, "S,M,L,XL,XXL"),
        ("Yengil sviter", 65000, "S,M,L,XL"),
        ("To'r krossovka", 120000, "38,39,40,41,42,43,44"),
        ("Quyosh ko'zoynagi", 45000, "OneSize"),
        ("Ayollar jinsi kalta", 75000, "XS,S,M,L,XL"),
        ("Sport shorti", 40000, "S,M,L,XL,XXL"),
        ("Polo ko'ylak", 75000, "S,M,L,XL,XXL"),
        ("Erkaklar jinsi shim", 145000, "28,30,32,34,36"),
        ("Ayollar jinsi shim", 140000, "24,26,28,30,32"),
        ("Erkaklar yozgi ko'ylak", 85000, "S,M,L,XL,XXL"),
        ("Ayollar kaftan", 110000, "S,M,L,XL"),
        ("Yozgi sport kostyum", 130000, "S,M,L,XL,XXL"),
        ("Yozgi poyabzal", 95000, "36,37,38,39,40,41,42"),
        ("Plyaj futbolkasi", 30000, "S,M,L,XL"),
        ("Erkaklar yozgi kurtka", 180000, "S,M,L,XL,XXL"),
        ("Ayollar yozgi ko'ylak (qisqa)", 95000, "XS,S,M,L,XL"),
        ("Erkaklar klassik shim", 160000, "28,30,32,34,36"),
        ("Ayollar yubka (uzun)", 120000, "XS,S,M,L,XL"),
        ("Erkaklar piyodalik", 55000, "40,41,42,43,44,45"),
        ("Ayollar piyodalik", 60000, "36,37,38,39,40"),
        ("Erkaklar sport majmuasi", 180000, "S,M,L,XL,XXL"),
        ("Ayollar sport majmuasi", 175000, "XS,S,M,L,XL"),
        ("Erkaklar kamzul", 250000, "S,M,L,XL,XXL"),
        ("Ayollar bluzka", 85000, "XS,S,M,L,XL"),
        ("Erkaklar ruboshka (oq)", 95000, "S,M,L,XL,XXL"),
        ("Ayollar yozgi to'n", 200000, "S,M,L,XL"),
        ("Erkaklar bermuda shorti", 70000, "S,M,L,XL,XXL"),
        ("Ayollar yozgi shim (nozik)", 130000, "XS,S,M,L,XL"),
    ]
    for i, (name, price, sizes) in enumerate(yozgi_kiyimlar):
        products.append((name, "Kiyimlar", "Yozgi kiyimlar", price, sizes, 50, img('yozgi', i)))

    # ===== KIYIMLAR - Bolalar kiyimi (35 ta) =====
    bolalar_sizes = ["3Y,4Y,5Y", "5Y,6Y,7Y", "7Y,8Y,9Y", "9Y,10Y,11Y", "3-4Y,5-6Y,7-8Y",
                     "5Y,6Y,7Y,8Y", "26,27,28,29", "30,31,32,33", "S,M,L"]
    bolalar_kiyim = [
        ("Bolalar qizil pufkasi (3-5 yosh)", 180000),
        ("Bolalar futbolkasi (5-7 yosh)", 25000),
        ("Bolalar sport kostyum (7-9 yosh)", 95000),
        ("Qizlar ko'ylagi (5-7 yosh)", 65000),
        ("Bolalar jinsi (9-11 yosh)", 85000),
        ("Bolalar poyabzali (26-29)", 75000),
        ("Bolalar poyabzali (30-33)", 85000),
        ("Bolalar qishki shlyapasi", 20000),
        ("Bolalar paypoq (5 juft)", 15000),
        ("Bolalar ichki kiyim to'plam", 35000),
        ("Bolalar yomg'irli paltosi", 55000),
        ("Bolalar kepchalari", 18000),
        ("Bolalar pijamasi", 45000),
        ("Bolalar qo'lqopchasi", 12000),
        ("Bolalar termal kiyimi", 60000),
        ("Bolalar sport shorti", 22000),
        ("Qizlar ko'ylak-shimcha", 75000),
        ("Bolalar sandali", 45000),
        ("Bolalar printli futbolka", 28000),
        ("Bolalar qishki palto", 145000),
        ("Bolalar dengiz kostyumi", 35000),
        ("Bolalar sport krossovkasi", 95000),
        ("Bolalar libosi (to'y)", 180000),
        ("O'g'il bolalar klassik kiyimi", 160000),
        ("Qizlar bayram ko'ylagi", 150000),
        ("Bolalar sport poyabzali", 85000),
        ("Bolalar yozgi shorti", 25000),
        ("Bolalar maykasi (3 ta)", 30000),
        ("Bolalar qishki kombinezon", 200000),
        ("Bolalar galosha", 25000),
        ("Bolalar sport ko'ylagi", 40000),
        ("Bolalar kigiz kiyim", 55000),
        ("O'g'il bolalar jinsi shimi", 75000),
        ("Qizlar sport kostyumi", 90000),
        ("Bolalar yozgi kepka", 15000),
    ]
    for i, (name, price) in enumerate(bolalar_kiyim):
        sizes = bolalar_sizes[i % len(bolalar_sizes)]
        products.append((name, "Kiyimlar", "Bolalar kiyimi", price, sizes, 50, img('bolalar', i)))

    # ===== OZIQ-OVQAT - Mevalar (30 ta) =====
    mevalar = [
        ("Olma (1 kg)", 12000), ("Banan (1 kg)", 18000), ("Apelsin (1 kg)", 15000),
        ("Uzum (1 kg)", 22000), ("Anor (1 kg)", 25000), ("Xurmo (1 kg)", 30000),
        ("Kivi (1 kg)", 20000), ("Nok (1 kg)", 14000), ("Shaftoli (1 kg)", 28000),
        ("Gilos (1 kg)", 35000), ("Limon (1 kg)", 16000), ("Mandarin (1 kg)", 18000),
        ("Tarvuz (kg)", 8000), ("Qovun (1 dona)", 15000), ("Malina (250g)", 22000),
        ("Qulupnay (500g)", 28000), ("Anjir (500g)", 32000), ("O'rik (1 kg)", 20000),
        ("Mango (1 dona)", 25000), ("Ananas (1 dona)", 45000), ("Papaya (1 kg)", 35000),
        ("Olcha (1 kg)", 18000), ("Kokoс (1 dona)", 30000), ("Avokado (1 dona)", 20000),
        ("Xurmo (Medjool, 500g)", 45000), ("Nektarin (1 kg)", 26000), ("Lichy (200g)", 35000),
        ("Pitaya (1 dona)", 28000), ("Marakuya (500g)", 32000), ("Xurmo (qo'ng'ir, 1 kg)", 22000),
    ]
    for i, (name, price) in enumerate(mevalar):
        products.append((name, "Oziq-ovqat", "Mevalar", price, "", 100, img('meva', i)))

    # ===== OZIQ-OVQAT - Fastfood (30 ta) =====
    fastfood = [
        ("Gamburger klassik", 25000), ("Chizburger qo'sh", 32000), ("Fri kartoshka katta", 15000),
        ("Hot-dog klassik", 15000), ("Sendvich tovuqli", 22000), ("Nuggets 8 dona", 28000),
        ("Shaorma katta", 32000), ("Qanotchalar 8 dona", 35000), ("Pitsa kichik pishloqli", 38000),
        ("Pitsa o'rta qo'shimchali", 55000), ("Spicy burger", 35000), ("Donuts 6 dona", 22000),
        ("Burrito go'shtli", 30000), ("Taco 2 dona", 25000), ("Nacho katta", 20000),
        ("Caesar salad", 28000), ("Wrap tovuqli", 24000), ("Milkshake katta", 18000),
        ("Garlic bread", 14000), ("Fish & Chips", 35000), ("Corndog", 12000),
        ("Hotdog pishloqli", 18000), ("Qovurilgan tovuq", 45000), ("Pitsa katta (4 qo'shimcha)", 75000),
        ("Club sandwich", 30000), ("Qo'zi kabob roll", 35000), ("Vegetarian burger", 28000),
        ("BBQ wings (10 dona)", 42000), ("Loaded fries", 22000), ("Cheese sticks (6 dona)", 20000),
    ]
    for i, (name, price) in enumerate(fastfood):
        products.append((name, "Oziq-ovqat", "Fastfood", price, "", 100, img('fast', i)))

    # ===== OZIQ-OVQAT - Milliy taomlar (30 ta) =====
    milliy = [
        ("Osh katta", 30000), ("Manti 6 dona", 25000), ("Sho'rva katta", 22000),
        ("Lag'mon katta", 28000), ("Somsa go'shtli 2 dona", 12000), ("Dimlama", 35000),
        ("Norin", 28000), ("Xonim katta", 20000), ("Qozonkabob", 40000),
        ("Mastava katta", 18000), ("Dolma 4 dona", 22000), ("Shashlik 1 tayoq", 25000),
        ("Shashlik 3 tayoq", 65000), ("Chuchvara go'shtli", 20000), ("Nona katta", 8000),
        ("Samsa qatlamali 2 dona", 14000), ("Kabob tovuqli", 30000), ("Tandir go'sht", 55000),
        ("Guruch oshi vegetarian", 22000), ("Qurt-qurt paket", 5000), ("Suzma 500g", 12000),
        ("Qovoq zichisi", 15000), ("Qo'zi osh", 45000), ("Baliq oshi", 40000),
        ("Tuxum qovurma", 18000), ("Jigar qovurma", 28000), ("Kazin oshi", 35000),
        ("Xamir tvorog bilan", 20000), ("Tandirda pishirilgan tovuq", 50000), ("Dushbara 20 dona", 25000),
    ]
    for i, (name, price) in enumerate(milliy):
        products.append((name, "Oziq-ovqat", "Milliy taomlar", price, "", 100, img('milliy', i)))

    # ===== OZIQ-OVQAT - Ichimliklar (30 ta) =====
    ichimliklari = [
        ("Coca-Cola 1.5L", 12000), ("Coca-Cola 0.5L", 6000), ("Fanta apelsin 1L", 10000),
        ("Sprite 1L", 10000), ("Mineral suv 1.5L", 5000), ("Multifruit sharbat 1L", 12000),
        ("Qora choy 100 paket", 25000), ("Yashil choy 100 paket", 28000), ("Qahva 3in1 20 dona", 18000),
        ("Energy drink 0.5L", 9000), ("Pepsi 1.5L", 11000), ("7Up 1L", 9000),
        ("Lipton Ice Tea 0.5L", 8000), ("Mango-ananas smoothie", 15000), ("Qoq sut 1L", 8000),
        ("Kefir 1L", 9000), ("Espresso qahva paket", 35000), ("Monster energy 0.5L", 12000),
        ("Latte tayyor 240ml", 14000), ("Tarvuz sharbati 1L", 12000), ("Kakao 250ml", 10000),
        ("Qovoq sharbati 1L", 11000), ("Olma sharbati 1L", 10000), ("Uzum sharbati 1L", 13000),
        ("Apelsin sharbati 1L", 11000), ("Anor sharbati 500ml", 18000), ("Ajinomoto choy 50 paket", 22000),
        ("Nesquik kakao paket", 20000), ("Nescafe klassik 95g", 45000), ("Ayron 500ml", 7000),
    ]
    for i, (name, price) in enumerate(ichimliklari):
        products.append((name, "Oziq-ovqat", "Ichimliklar", price, "", 100, img('ichimlik', i)))

    # ===== OZIQ-OVQAT - Shirinliklar (30 ta) =====
    shirinlik = [
        ("Snickers 50g", 8000), ("Kit Kat 42g", 7000), ("Twix 50g", 8000),
        ("Bounty 57g", 8000), ("Milka shokolad 100g", 22000), ("Halva 500g", 25000),
        ("Novvot 500g", 18000), ("Karamel 200g", 12000), ("Zefir 200g", 15000),
        ("Marmelad 250g", 12000), ("M&Ms 75g", 12000), ("Pringles 165g", 22000),
        ("Lay's chips 70g", 9000), ("Oreo 440g", 28000), ("Tarvuzli keks 300g", 15000),
        ("Wafer tort 300g", 18000), ("Gummy bears 250g", 14000), ("Nutella 350g", 55000),
        ("Chupa Chups 1 dona", 3000), ("Ferrero Rocher 8 dona", 55000), ("Ritter Sport 100g", 28000),
        ("Alpen Gold 95g", 18000), ("Raffaello 8 dona", 45000), ("After Eight 200g", 35000),
        ("Kinder Bueno 43g", 12000), ("Haribo gummies 100g", 10000), ("Maltesers 85g", 18000),
        ("Toblerone 100g", 30000), ("Milkybar 100g", 20000), ("Kindershoko 20g", 5000),
    ]
    for i, (name, price) in enumerate(shirinlik):
        products.append((name, "Oziq-ovqat", "Shirinliklar", price, "", 100, img('shirin', i)))

    # ===== GADJETLAR - Telefonlar (30 ta) =====
    telefonlar = [
        ("iPhone 15 128GB qora", 12500000), ("iPhone 15 Pro 256GB", 16000000),
        ("iPhone 15 Plus 256GB", 14000000), ("iPhone 14 128GB", 9800000),
        ("Samsung Galaxy S24 256GB", 10500000), ("Samsung Galaxy S24+ 512GB", 13500000),
        ("Samsung Galaxy A55 128GB", 4200000), ("Samsung Galaxy A35 128GB", 3200000),
        ("Samsung Galaxy M34 128GB", 2800000), ("Xiaomi 14 256GB", 8500000),
        ("Xiaomi Redmi Note 13 Pro", 3800000), ("Xiaomi POCO X6 Pro 256GB", 3500000),
        ("Xiaomi 13T Pro 256GB", 7500000), ("OPPO Reno 11 Pro 256GB", 5500000),
        ("OnePlus 12 256GB", 9500000), ("Google Pixel 8 Pro 256GB", 11000000),
        ("Realme GT 5 Pro 256GB", 4500000), ("Nokia G60 128GB", 2200000),
        ("Infinix Note 30 Pro", 2500000), ("Motorola Edge 50 Pro", 4000000),
        ("Honor Magic6 Pro", 7800000), ("Huawei Nova 12 256GB", 4800000),
        ("Vivo V30 Pro 256GB", 5200000), ("ZTE Blade V40 Pro", 2000000),
        ("Tecno Phantom V Fold", 7500000), ("iPhone 13 128GB", 7500000),
        ("Samsung Galaxy Z Flip5", 15000000), ("Samsung Galaxy Z Fold5", 28000000),
        ("Xiaomi Redmi 12 128GB", 2200000), ("OPPO A98 128GB", 3000000),
    ]
    for i, (name, price) in enumerate(telefonlar):
        products.append((name, "Gadjetlar", "Telefonlar", price, "", 30, img('telefon', i)))

    # ===== GADJETLAR - Noutbuklar (30 ta) =====
    noutbuklar = [
        ("MacBook Air M3 13\" 8GB", 18000000), ("MacBook Pro M3 14\" 16GB", 28000000),
        ("MacBook Air M2 13\" 8GB", 15000000), ("Dell XPS 15 Core i7 16GB", 20000000),
        ("HP Pavilion 15 Ryzen 5", 8500000), ("Lenovo IdeaPad 5 Ryzen 7", 9500000),
        ("ASUS ZenBook 14 Core i5", 11000000), ("Acer Aspire 5 Core i5", 7500000),
        ("MSI GF63 Thin Gaming", 13000000), ("ROG Zephyrus G14 Gaming", 22000000),
        ("Samsung Galaxy Book3 Pro", 16000000), ("Microsoft Surface Laptop 5", 18500000),
        ("HP EliteBook 840 G10", 17000000), ("Lenovo ThinkPad X1 Carbon", 21000000),
        ("Dell Inspiron 15 Ryzen 5", 8000000), ("Acer Predator Helios 300", 19000000),
        ("ASUS TUF Gaming F15", 15000000), ("Huawei MateBook D16 Ryzen 7", 12000000),
        ("Razer Blade 15 Gaming", 32000000), ("LG Gram 14 Core i5", 14000000),
        ("HP Spectre x360 Core i7", 19500000), ("Xiaomi Notebook Pro 14", 10500000),
        ("Gigabyte Aorus 15 Gaming", 23000000), ("Dell XPS 13 Core i7", 17000000),
        ("Lenovo Legion 5 Ryzen 7", 16500000), ("ASUS ROG Strix G15", 20000000),
        ("HP Omen 16 Core i7", 18000000), ("Acer Swift 3 Core i5", 9000000),
        ("MSI Prestige 14 Core i7", 16000000), ("Toshiba Portege Z30", 14500000),
    ]
    for i, (name, price) in enumerate(noutbuklar):
        products.append((name, "Gadjetlar", "Noutbuklar", price, "", 20, img('noutbuk', i)))

    # ===== GADJETLAR - Planshetlar (30 ta) =====
    planshetlar = [
        ("iPad Air M2 11\" 256GB", 9800000), ("iPad Pro M4 13\" 256GB", 18000000),
        ("iPad mini 6 64GB", 6500000), ("iPad 10th gen 64GB WiFi", 7200000),
        ("Samsung Galaxy Tab S9 256GB", 8500000), ("Samsung Galaxy Tab S9 FE 128GB", 4200000),
        ("Samsung Galaxy Tab A9+ 128GB", 3200000), ("Samsung Galaxy Tab S9 Ultra", 16000000),
        ("Xiaomi Pad 6 Pro 256GB", 5500000), ("Xiaomi Redmi Pad SE 128GB", 2500000),
        ("Xiaomi Pad 6 128GB", 4500000), ("Huawei MatePad Pro 13.2\"", 7500000),
        ("Huawei MatePad 11.5\"", 4500000), ("Huawei MatePad T10s", 2800000),
        ("Lenovo Tab P12 Pro 256GB", 5800000), ("Lenovo Tab M10 Plus 128GB", 2200000),
        ("Lenovo Tab P11 Pro 128GB", 4000000), ("Microsoft Surface Pro 10", 14000000),
        ("OPPO Pad 2 256GB", 5200000), ("Realme Pad X 128GB", 2800000),
        ("Nokia T21 64GB", 1800000), ("Amazon Fire HD 10 32GB", 1500000),
        ("Blackview Tab 18 256GB", 3000000), ("Vivo Pad 2 256GB", 4800000),
        ("Teclast P40HD 128GB", 1200000), ("Tecno Megapad 10 64GB", 1000000),
        ("Chuwi HiPad X Pro 128GB", 1800000), ("Alldocube iPlay 50 Pro", 2200000),
        ("Doogee T30 Pro 256GB", 3500000), ("Itel Pad 1 64GB", 900000),
    ]
    for i, (name, price) in enumerate(planshetlar):
        products.append((name, "Gadjetlar", "Planshetlar", price, "", 25, img('planshet', i)))

    c.executemany(
        "INSERT INTO products (name,category,subcategory,price,sizes,stock,image_url) VALUES (?,?,?,?,?,?,?)",
        products
    )
    conn.commit()
    print(f"✅ {len(products)} ta mahsulot qo'shildi")

def apply_smart_product_images(conn):
    """Mahsulot nomiga mos rasmlarni yozadi (/uploads/ dan tashqari)."""
    from .product_image_rules import match_image_url

    c = conn.cursor()
    rows = c.execute("SELECT id, name, image_url FROM products").fetchall()
    for r in rows:
        cur = (r["image_url"] or "").strip()
        if cur.startswith("/uploads/"):
            continue
        hit = match_image_url(r["name"] or "")
        if hit:
            c.execute("UPDATE products SET image_url=? WHERE id=?", (hit, r["id"]))
    conn.commit()


def init_db():
    """Database ni ishga tushiradi"""
    conn = get_db()
    create_tables(conn)
    # Eski bazalar uchun kerakli ustunlarni migratsiya qilamiz
    try:
        conn.execute("ALTER TABLE orders ADD COLUMN recipient_name TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        conn.execute("ALTER TABLE orders ADD COLUMN recipient_last_name TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        conn.execute("ALTER TABLE orders ADD COLUMN recipient_phone TEXT DEFAULT ''")
    except Exception:
        pass
    for col in (
        "recipient_doc_type TEXT DEFAULT ''",
        "recipient_passport_number TEXT DEFAULT ''",
    ):
        try:
            conn.execute(f"ALTER TABLE orders ADD COLUMN {col}")
        except Exception:
            pass

    # Matnlarni tozalash: "jinsi" so'zini tabiiyroq "shim" bilan almashtirish
    conn.execute("UPDATE products SET name = REPLACE(name, 'jinsi', 'shim') WHERE name LIKE '%jinsi%'")
    conn.execute("UPDATE products SET name = REPLACE(name, 'Jinsi', 'Shim') WHERE name LIKE '%Jinsi%'")
    conn.commit()
    seed_admin(conn)
    seed_products(conn)
    # Qo‘shimcha katalog + rasmlar
    from .extra_catalog_seed import seed_extra_catalog

    seed_extra_catalog(conn)
    apply_smart_product_images(conn)
    conn.close()
    print(f"✅ Database: {DB_PATH}")
