"""
Mahsulot nomiga qarab mos rasm URL ini tanlash.
Ma'lumotlar bazasidagi image_url ustuni ustuvor; bu modul seed va migratsiya uchun.
Eng uzun mos keluvchi qoida tanlanadi (aniqlik uchun qoidalar uzunlik bo'yicha tartiladi).
"""
from __future__ import annotations

# Wikimedia / Unsplash — barqaror foto havolalar (mahsulot turiga mos)
RULES: list[tuple[str, str]] = [
    # Telefonlar (aniq modellar ustuvor)
    ("iphone 17 pro max", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/IPhone_15_Pro_Vector.svg/320px-IPhone_15_Pro_Vector.svg.png"),
    ("iphone 17 pro", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/IPhone_15_Pro_Vector.svg/320px-IPhone_15_Pro_Vector.svg.png"),
    ("iphone 17", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/IPhone_15_Pro_Vector.svg/280px-IPhone_15_Pro_Vector.svg.png"),
    ("iphone 16", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/IPhone_16_Pro_vector.svg/280px-IPhone_16_Pro_vector.svg.png"),
    ("iphone 15", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/IPhone_15_Pro_Vector.svg/280px-IPhone_15_Pro_Vector.svg.png"),
    ("iphone 14", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/IPhone_14_vector.svg/260px-IPhone_14_vector.svg.png"),
    ("iphone 13", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/IPhone_14_vector.svg/240px-IPhone_14_vector.svg.png"),
    ("iphone", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/IPhone_16_Pro_vector.svg/240px-IPhone_16_Pro_vector.svg.png"),
    ("samsung galaxy", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Samsung_Galaxy_S21_Vector.svg/260px-Samsung_Galaxy_S21_Vector.svg.png"),
    ("pixel", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Google_Pixel_8_%28 Hazel %29.svg/220px-Google_Pixel_8_%28_Hazel_%29.svg.png"),
    ("xiaomi", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Xiaomi_logo_%282021-%29.svg/200px-Xiaomi_logo_%282021-%29.svg.png"),
    ("oppo", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/OPPO_LOGO_2019.png/200px-OPPO_LOGO_2019.png"),
    ("macbook", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/MacBook_Pro_vector.svg/280px-MacBook_Pro_vector.svg.png"),
    ("ipad", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/IPad_Air_%284th_generation%29.svg/240px-IPad_Air_%284th_generation%29.svg.png"),
    ("noutbuk", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/MacBook_Pro_vector.svg/260px-MacBook_Pro_vector.svg.png"),
    ("planshet", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/IPad_Air_%284th_generation%29.svg/220px-IPad_Air_%284th_generation%29.svg.png"),
    # Fastfood
    ("hot-dog", "https://images.unsplash.com/photo-1612392166886-f7e5ac169527?w=400&q=80"),
    ("hotdog", "https://images.unsplash.com/photo-1612392166886-f7e5ac169527?w=400&q=80"),
    ("gamburger", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&q=80"),
    ("burger", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&q=80"),
    ("pitsa", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&q=80"),
    ("pizza", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&q=80"),
    ("shaorma", "https://images.unsplash.com/photo-1599974579688-8dbddbcdf54d?w=400&q=80"),
    ("nuggets", "https://images.unsplash.com/photo-1569058242567-93de6f36f8ee?w=400&q=80"),
    ("fri", "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&q=80"),
    ("taco", "https://images.unsplash.com/photo-1565299585323-38e0760fbbc3?w=400&q=80"),
    ("burrito", "https://images.unsplash.com/photo-1626700055535-281064fec54f?w=400&q=80"),
    ("donuts", "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400&q=80"),
    ("sendvich", "https://images.unsplash.com/photo-1539252554453-80ab360cc867?w=400&q=80"),
    ("sandwich", "https://images.unsplash.com/photo-1539252554453-80ab360cc867?w=400&q=80"),
    ("fish & chips", "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&q=80"),
    ("salad", "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&q=80"),
    ("milkshake", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&q=80"),
    # Milliy
    ("osh", "https://images.unsplash.com/photo-1547592166-23abf45744cd?w=400&q=80"),
    ("lag'mon", "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400&q=80"),
    ("manti", "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&q=80"),
    ("somsa", "https://images.unsplash.com/photo-1604908177446-13f55ce02ecb?w=400&q=80"),
    ("shashlik", "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&q=80"),
    ("dimlama", "https://images.unsplash.com/photo-1547592180-85f173990554?w=400&q=80"),
    # Mevalar
    ("olma", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&q=80"),
    ("banan", "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&q=80"),
    ("apelsin", "https://images.unsplash.com/photo-1547514701-42782101795e?w=400&q=80"),
    ("uzum", "https://images.unsplash.com/photo-1596591606975-68fbf77eae6f?w=400&q=80"),
    ("anor", "https://images.unsplash.com/photo-1547514701-42782101795e?w=400&q=80"),
    ("xurmo", "https://images.unsplash.com/photo-1605027990121-b935781665f7?w=400&q=80"),
    ("tarvuz", "https://images.unsplash.com/photo-1587049352846-4a222e2d38f8?w=400&q=80"),
    ("qovun", "https://images.unsplash.com/photo-1595475207221-195942106abd?w=400&q=80"),
    ("limon", "https://images.unsplash.com/photo-1590502593747-d42bdb46f82d?w=400&q=80"),
    ("ananas", "https://images.unsplash.com/photo-1589829075699-a339bc06bdd9?w=400&q=80"),
    ("mango", "https://images.unsplash.com/photo-1605027990121-b935781665f7?w=400&q=80"),
    ("kivi", "https://images.unsplash.com/photo-1587735243477-be89c02bc694?w=400&q=80"),
    ("gilos", "https://images.unsplash.com/photo-1528821128474-27f963b062bf?w=400&q=80"),
    ("malina", "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&q=80"),
    ("anjir", "https://images.unsplash.com/photo-1601370690297-7eca30163363?w=400&q=80"),
    ("avokado", "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=400&q=80"),
    # Ichimlik
    ("cola", "https://images.unsplash.com/photo-1629203851122-362ede94fd97?w=400&q=80"),
    ("pepsi", "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400&q=80"),
    ("sprite", "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400&q=80"),
    ("mineral", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&q=80"),
    ("suv", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&q=80"),
    ("choy", "https://images.unsplash.com/photo-1597318181412-49af564f5608?w=400&q=80"),
    ("qahva", "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=400&q=80"),
    ("energy", "https://images.unsplash.com/photo-1622543925917-763caa543e02?w=400&q=80"),
    ("sharbat", "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&q=80"),
    ("kefir", "https://images.unsplash.com/photo-1550583724-b2692bda8d8e?w=400&q=80"),
    ("sut", "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&q=80"),
    # Shirinlik
    ("snickers", "https://images.unsplash.com/photo-1599599810694-b5b37304c041?w=400&q=80"),
    ("shokolad", "https://images.unsplash.com/photo-1549007997098-8979cc3284ce?w=400&q=80"),
    ("oreo", "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=400&q=80"),
    ("chips", "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400&q=80"),
    ("novvot", "https://images.unsplash.com/photo-1616427825526-7f2e7f8c7e88?w=400&q=80"),
    # Kiyim
    ("pufka", "https://images.unsplash.com/photo-1544923246-77307dd654cb?w=400&q=80"),
    ("palto", "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400&q=80"),
    ("futbolka", "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&q=80"),
    ("short", "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&q=80"),
    ("shim", "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80"),
    ("krossovka", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80"),
    ("etik", "https://images.unsplash.com/photo-1608256246200-53e635b5e65d?w=400&q=80"),
    ("sandali", "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&q=80"),
    ("forma", "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&q=80"),
    ("futbol kiyim", "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&q=80"),
    # O'yinchoqlar va to'plar
    ("futbol to'pi", "https://images.unsplash.com/photo-1614632537423-81e12856442d?w=400&q=80"),
    ("futbol top", "https://images.unsplash.com/photo-1614632537423-81e12856442d?w=400&q=80"),
    ("top (fifa", "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&q=80"),
    ("lego", "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&q=80"),
    ("qog'irchoq", "https://images.unsplash.com/photo-1558060370-d644479cb07f?w=400&q=80"),
    ("qo'g'irchoq", "https://images.unsplash.com/photo-1558060370-d644479cb07f?w=400&q=80"),
    ("oyinchiq", "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&q=80"),
    ("machinka", "https://images.unsplash.com/photo-1594787317357-30da06db3679?w=400&q=80"),
    ("piyon", "https://images.unsplash.com/photo-1582195047927-c187f49f8158?w=400&q=80"),
]

_SORTED_RULES = sorted(RULES, key=lambda x: len(x[0]), reverse=True)


def match_image_url(product_name: str) -> str | None:
    """Mahsulot nomidan eng mos rasm URL ini qaytaradi."""
    if not product_name:
        return None
    n = product_name.strip().lower()
    for key, url in _SORTED_RULES:
        if key in n:
            return url
    return None
