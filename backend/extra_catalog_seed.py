"""Qo‘shimcha kategoriyalar: O‘yinchoqlar, Futbol kiyimlari, Futbol toplari."""
from __future__ import annotations


def _insert_products(conn, rows: list[tuple]) -> None:
    c = conn.cursor()
    c.executemany(
        "INSERT INTO products (name,category,subcategory,price,sizes,stock,image_url) VALUES (?,?,?,?,?,?,?)",
        rows,
    )
    conn.commit()


def seed_extra_catalog(conn) -> None:
    """Bir marta qo‘shiladi — mavjud bo‘lsa o‘tkazib yuboriladi."""
    c = conn.cursor()

    def exists_cat(cat: str) -> bool:
        n = c.execute(
            "SELECT COUNT(*) as n FROM products WHERE category=?", (cat,)
        ).fetchone()["n"]
        return n > 0

    # --- Futbol kiyimlari (55+) ---
    if c.execute(
        "SELECT COUNT(*) as n FROM products WHERE subcategory=?",
        ("Futbol kiyimlari",),
    ).fetchone()["n"] == 0:
        teams = [
            "Real Madrid", "Barselona", "Manchester United", "Liverpool", "Chelsi",
            "PSJ", "Bayern Munich", "Yuventus", "Inter Milan", "AC Milan",
            "Arsenal", "Manchester Siti", "Tottenham", "Atletiko Madrid", "Sevilya",
            "Napoli", "Roma", "Latsio", "Portu", "Benfika",
            "Ayaks", "PSV", "Sporting", "Seltik", "Rangers",
            "Galatasaray", "Fenerbahche", "Besiktas", "Shalke", "Bayer Leverkusen",
            "Borussiya Dortmund", "Frankfurt", "Lion", "Monako", "Marsel",
            "Zenit", "Spartak", "Selta Vigo", "Valensiya", "Betis",
            "Villyareal", "YEverton", "Aston Villa", "Nyukasl", "Brighton",
            "O‘zbekiston terma jamoasi", "Argentina terma", "Braziliya terma", "Fransiya terma",
            "Italiya terma", "Ispaniya terma", "Germaniya terma", "Angliya terma",
            "Portugaliya terma", "Niderland terma",
        ]
        img_kit = "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&q=80"
        rows = []
        for i, team in enumerate(teams):
            variant = "Uy formasi" if i % 2 == 0 else "Mehmon formasi"
            price = 280000 + (i * 3500)
            rows.append(
                (
                    f"{team} {variant} 2024/25",
                    "Kiyimlar",
                    "Futbol kiyimlari",
                    price,
                    "S,M,L,XL,XXL",
                    40,
                    img_kit,
                )
            )
        _insert_products(conn, rows)

    # --- O‘yinchoqlar (35+) ---
    if not exists_cat("O'yinchoqlar"):
        toy_urls = [
            "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&q=80",
            "https://images.unsplash.com/photo-1558060370-d644479cb07f?w=400&q=80",
            "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&q=80",
            "https://images.unsplash.com/photo-1594787317357-30da06db3679?w=400&q=80",
            "https://images.unsplash.com/photo-1560857617-d57ade61ad69?w=400&q=80",
            "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&q=80",
            "https://images.unsplash.com/photo-1516979187457-637abb02f3f7?w=400&q=80",
        ]
        toys = [
            ("Lego klassik to‘plam (500 detal)", 420000),
            ("Qo‘g‘irchoq (matryoshka)", 85000),
            ("Temir yo‘l poezdi (battery)", 195000),
            ("Radioboshqariladigan mashina", 220000),
            ("Rubik kubigi 3x3", 45000),
            ("Shaxmat to‘plami (daraxt)", 180000),
            ("Damalari to‘plami", 95000),
            ("Bolalar velosiped (16\")", 890000),
            ("Skuter bolalar", 320000),
            ("Yo‘lovchi samalyot", 120000),
            ("Velosiped dubulg‘asi", 145000),
            ("Kompyuter o‘yin konsoli (portativ)", 2100000),
            ("Puzzle 1000 parça", 75000),
            ("Yo‘lboshlovchi konstruktor", 68000),
            ("Bolalar musiqiy pianochasi", 245000),
            ("Ovoz chiqaradigan hayvonlar to‘plami", 95000),
            ("Lego city majmuasi", 380000),
            ("Suv pistolesi (summer)", 115000),
            ("Bolalar xavfsizligi uchun kemasi", 78000),
            ("Futzon Topqo‘llik robot", 520000),
            ("Magnitli konstruktor", 135000),
            ("Bolalar rasm devori", 165000),
            ("Jonivorlar farmasi to‘plami", 92000),
            ("Komiks qahramonlari figuralari", 145000),
            ("Sport bowling to‘plami", 210000),
            ("Bolalar qum sandiq + aksessuar", 185000),
            ("Ovozi chiqadigan temir yo‘l stansiyasi", 295000),
            ("Ovozi chiqadigan pianochalar kichik", 88000),
            ("Bolalar qog‘oz kitobi (interaktiv)", 55000),
            ("Yozgi suv havzasi (shisha)", 420000),
            ("Sport basketbol halqasi (bolalar)", 320000),
            ("Komiks bilan Lego majmuasi", 510000),
            ("Bolalar laboratoriya to‘plami", 175000),
            ("Jonli hayvonlar zo‘rg‘aliklari", 67000),
            ("Bolalar mini futbol darvozasi", 145000),
            ("Qo‘yilgan mahpuslar labirinti", 98000),
        ]
        rows = []
        for i, (name, price) in enumerate(toys):
            rows.append(
                (
                    name,
                    "O'yinchoqlar",
                    "O'yinchoqlar",
                    price,
                    "OneSize",
                    35,
                    toy_urls[i % len(toy_urls)],
                )
            )
        _insert_products(conn, rows)

    # --- Futbol toplari (28+) ---
    if c.execute(
        "SELECT COUNT(*) as n FROM products WHERE subcategory=?",
        ("Futbol toplari",),
    ).fetchone()["n"] == 0:
        ball_imgs = [
            "https://images.unsplash.com/photo-1614632537423-81e12856442d?w=400&q=80",
            "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&q=80",
            "https://images.unsplash.com/photo-1575367473936-f227f52e7d8e?w=400&q=80",
            "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=400&q=80",
        ]
        balls = [
            ("Adidas Telstar FIFA rasmiy", 890000),
            ("Nike Strike Team", 420000),
            ("Puma La Liga rasmiy", 510000),
            ("Select Brilliant Super", 680000),
            ("Mikasa futsal professional", 380000),
            ("Wilson NCAA futbol topi", 295000),
            ("Derbystar Bundesliga", 720000),
            ("Molten Vantaggio", 450000),
            ("Umbro Neo Trainer", 210000),
            ("Kipsta Decathlon training", 145000),
            ("Joma Gold match", 520000),
            ("Lotto Stadio top", 310000),
            ("O‘zbekiston terma jamoasi commemorative", 650000),
            ("UEFA Champions League final top (kollektsiya)", 1200000),
            ("Premier League rasmiy mini", 185000),
            ("Serie A training #5", 275000),
            ("La Liga junior size 4", 220000),
            ("Bundesliga winter ball", 490000),
            ("Rossiya Premier liga match", 560000),
            ("Turkiya Superliga training", 340000),
            ("Japan J-League official", 610000),
            ("MLS North America match", 540000),
            ("Afrika kubogi commemorative", 430000),
            ("Copa America limited", 980000),
            ("World Cup Qatar commemorative", 1500000),
            ("Beach soccer padded", 260000),
            ("Street futbol rubber", 175000),
            ("Indoor low-bounce futsal", 320000),
        ]
        rows = []
        for i, (name, price) in enumerate(balls):
            rows.append(
                (
                    name,
                    "O'yinchoqlar",
                    "Futbol toplari",
                    price,
                    "OneSize",
                    45,
                    ball_imgs[i % len(ball_imgs)],
                )
            )
        _insert_products(conn, rows)

    # --- iPhone 17 qatori (agar yo‘q bo‘lsa) ---
    if (
        c.execute(
            "SELECT COUNT(*) as n FROM products WHERE name LIKE ?", ("%iPhone 17%",)
        ).fetchone()["n"]
        == 0
    ):
        iphone_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/IPhone_15_Pro_Vector.svg/280px-IPhone_15_Pro_Vector.svg.png"
        extra_phones = [
            ("iPhone 17 Pro Max 256GB", 18500000),
            ("iPhone 17 Pro 512GB", 16800000),
            ("iPhone 17 128GB", 12200000),
        ]
        rows = [
            (
                n,
                "Gadjetlar",
                "Telefonlar",
                p,
                "",
                25,
                iphone_img,
            )
            for n, p in extra_phones
        ]
        _insert_products(conn, rows)
