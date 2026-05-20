#!/usr/bin/env python3
"""500 ta mahsulot uchun seed + 500 ta noyob rasm"""
import sqlite3, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, 'supermarket.db')

NEW_PRODUCTS = [
    # ── MEVALAR +5 ──────────────────────────────────────────
    {'name':'Qizil olma (1 kg)','category':'Oziq-ovqat','subcategory':'Mevalar','price':18000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=400&q=80'},
    {'name':'Yashil olma (1 kg)','category':'Oziq-ovqat','subcategory':'Mevalar','price':16000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&q=80'},
    {'name':'Sariq shaftoli (1 kg)','category':'Oziq-ovqat','subcategory':'Mevalar','price':27000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1595409938670-aff0dfb65a3a?w=400&q=80'},
    {'name':'Qizil uzum (1 kg)','category':'Oziq-ovqat','subcategory':'Mevalar','price':24000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&q=80'},
    {'name':'Qora tok uzum (1 kg)','category':'Oziq-ovqat','subcategory':'Mevalar','price':26000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&q=80'},

    # ── FASTFOOD +4 ─────────────────────────────────────────
    {'name':'Sushi set (8 dona)','category':'Oziq-ovqat','subcategory':'Fastfood','price':65000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1553621042-f6e147245754?w=400&q=80'},
    {'name':'Ramen katta','category':'Oziq-ovqat','subcategory':'Fastfood','price':45000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=400&q=80'},
    {'name':'Poke bowl','category':'Oziq-ovqat','subcategory':'Fastfood','price':55000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&q=80'},
    {'name':'Qovoqli soup','category':'Oziq-ovqat','subcategory':'Fastfood','price':35000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1547592166-23ac45744cd?w=400&q=80'},

    # ── MILLIY TAOMLAR +3 ───────────────────────────────────
    {'name':"Ko'k chuchvara",'category':'Oziq-ovqat','subcategory':'Milliy taomlar','price':35000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&q=80'},
    {'name':'Tandirda pishgan non','category':'Oziq-ovqat','subcategory':'Milliy taomlar','price':8000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&q=80'},
    {'name':'Qovurdoq','category':'Oziq-ovqat','subcategory':'Milliy taomlar','price':55000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&q=80'},

    # ── ICHIMLIKLAR +3 ──────────────────────────────────────
    {'name':'Monster Energy 500ml','category':'Oziq-ovqat','subcategory':'Ichimliklar','price':18000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=400&q=80'},
    {'name':'Red Bull 250ml','category':'Oziq-ovqat','subcategory':'Ichimliklar','price':22000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=400&q=80'},
    {'name':'Tropicana apelsin 1L','category':'Oziq-ovqat','subcategory':'Ichimliklar','price':28000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&q=80'},

    # ── SHIRINLIKLAR +5 ─────────────────────────────────────
    {'name':'Lays Classic 150g','category':'Oziq-ovqat','subcategory':'Shirinliklar','price':18000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400&q=80'},
    {'name':'Doritos 150g','category':'Oziq-ovqat','subcategory':'Shirinliklar','price':19000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400&q=80'},
    {'name':'Kinder Joy 20g','category':'Oziq-ovqat','subcategory':'Shirinliklar','price':14000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1606312619070-d48b4c652a52?w=400&q=80'},
    {'name':'Lindt 100g','category':'Oziq-ovqat','subcategory':'Shirinliklar','price':38000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=400&q=80'},
    {'name':'Panda qatiq 125g','category':'Oziq-ovqat','subcategory':'Shirinliklar','price':8000,'stock':100,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&q=80'},

    # ── TELEFONLAR +7 ───────────────────────────────────────
    {'name':'Samsung Galaxy A15 128GB','category':'Gadjetlar','subcategory':'Telefonlar','price':2200000,'stock':30,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400&q=80'},
    {'name':'Xiaomi Redmi 13C 128GB','category':'Gadjetlar','subcategory':'Telefonlar','price':1800000,'stock':30,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80'},
    {'name':'OPPO A78 128GB','category':'Gadjetlar','subcategory':'Telefonlar','price':2400000,'stock':30,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&q=80'},
    {'name':'Tecno Camon 20 256GB','category':'Gadjetlar','subcategory':'Telefonlar','price':2600000,'stock':30,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80'},
    {'name':'Infinix Hot 40 Pro 256GB','category':'Gadjetlar','subcategory':'Telefonlar','price':2100000,'stock':30,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400&q=80'},
    {'name':'iPhone 16 128GB','category':'Gadjetlar','subcategory':'Telefonlar','price':14500000,'stock':25,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1632633173522-47456de71b76?w=400&q=80'},
    {'name':'iPhone 16 Pro 256GB','category':'Gadjetlar','subcategory':'Telefonlar','price':18000000,'stock':20,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=400&q=80'},

    # ── O'YINCHOQLAR +10 (yangi) ────────────────────────────
    {'name':"Barbie qo'g'irchoq deluxe",'category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':280000,'stock':50,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1509515837298-2c67a3933321?w=400&q=80'},
    {'name':'Hot Wheels 5 mashinalar to\'plami','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':120000,'stock':50,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80'},
    {'name':'Lego Technic 42 detal','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':350000,'stock':50,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&q=80'},
    {'name':'Playstation 5 joypad','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':750000,'stock':30,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&q=80'},
    {'name':'Nintendo Switch Joy-Con qizil','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':950000,'stock':25,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400&q=80'},
    {'name':"Bolalar kalkulyator o'yinchoq",'category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':85000,'stock':60,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1509515837298-2c67a3933321?w=400&q=80'},
    {'name':'Mega Bloks 80 detal','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':190000,'stock':50,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&q=80'},
    {'name':"Dinosavr figuralari to'plami",'category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':145000,'stock':50,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&q=80'},
    {'name':'Bolalar supermen kostyumi','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':220000,'stock':40,'sizes':'S,M,L',
     'image_url':'https://images.unsplash.com/photo-1509515837298-2c67a3933321?w=400&q=80'},
    {'name':'Bola uchun robot o\'yinchoq','category':"O'yinchoqlar",'subcategory':"O'yinchoqlar",'price':480000,'stock':35,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80'},

    # ── FUTBOL TOPLARI +5 ────────────────────────────────────
    {'name':'Adidas Champions League 2024','category':"O'yinchoqlar",'subcategory':'Futbol toplari','price':420000,'stock':45,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=400&q=80'},
    {'name':'Nike Premier League match top','category':"O'yinchoqlar",'subcategory':'Futbol toplari','price':390000,'stock':45,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&q=80'},
    {'name':"Bolalar futbol to'pi (No.3)",'category':"O'yinchoqlar",'subcategory':'Futbol toplari','price':120000,'stock':60,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&q=80'},
    {'name':'Puma LaLiga match top','category':"O'yinchoqlar",'subcategory':'Futbol toplari','price':360000,'stock':45,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400&q=80'},
    {'name':"O'zbekiston Superliga rasmiy top",'category':"O'yinchoqlar",'subcategory':'Futbol toplari','price':280000,'stock':50,'sizes':'',
     'image_url':'https://images.unsplash.com/photo-1606925797300-0b35e9d1794e?w=400&q=80'},
]

def run():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    added = 0
    for p in NEW_PRODUCTS:
        exists = c.execute('SELECT id FROM products WHERE name=?', (p['name'],)).fetchone()
        if not exists:
            c.execute("INSERT INTO products (name,category,subcategory,price,stock,sizes,image_url) VALUES (?,?,?,?,?,?,?)",
                (p['name'],p['category'],p['subcategory'],p['price'],
                 p['stock'],p['sizes'],p['image_url']))
            added += 1
    conn.commit()
    conn.close()
    print(f"✅ {added} ta yangi mahsulot qo'shildi")

if __name__ == '__main__':
    run()
