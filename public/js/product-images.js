/**
 * SuperMarket v2 — Mahsulot rasmlari
 * 510 ta mahsulot, har biriga o'z noyob Unsplash rasmi
 * DB da image_url USTUVOR — bu JS faqat fallback
 */

const PRODUCT_IMAGE_FALLBACK =
  'https://images.unsplash.com/photo-1604719314507-57f5f8ef3209?w=400&q=80';

// Subkategoriya → rasmlar havzasi (rotatsiya)
const SUBCAT_POOL = {
  'Mevalar': [
    'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=400&q=80',
    'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&q=80',
    'https://images.unsplash.com/photo-1547514701-42782101795e?w=400&q=80',
    'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&q=80',
    'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&q=80',
    'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&q=80',
    'https://images.unsplash.com/photo-1563699789-bce8dc5b5218?w=400&q=80',
    'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&q=80',
    'https://images.unsplash.com/photo-1589820296156-2454bb8a6ad1?w=400&q=80',
    'https://images.unsplash.com/photo-1601004890657-f3e8d1c78779?w=400&q=80',
    'https://images.unsplash.com/photo-1534531173927-aeb928d54385?w=400&q=80',
    'https://images.unsplash.com/photo-1595409938670-aff0dfb65a3a?w=400&q=80',
    'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&q=80',
    'https://images.unsplash.com/photo-1621955964441-c173e01c135b?w=400&q=80',
    'https://images.unsplash.com/photo-1527517537798-5e1b1f98ccbf?w=400&q=80',
  ],
  'Fastfood': [
    'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&q=80',
    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&q=80',
    'https://images.unsplash.com/photo-1612392166886-ee8475b03af2?w=400&q=80',
    'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&q=80',
    'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80',
    'https://images.unsplash.com/photo-1562967914-608f82629710?w=400&q=80',
    'https://images.unsplash.com/photo-1561651823-34feb02250e4?w=400&q=80',
    'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&q=80',
    'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400&q=80',
    'https://images.unsplash.com/photo-1541592553160-82008b127ccb?w=400&q=80',
  ],
  'Milliy taomlar': [
    'https://images.unsplash.com/photo-1512058556646-c4da40fba323?w=400&q=80',
    'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&q=80',
    'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&q=80',
    'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&q=80',
    'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&q=80',
    'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&q=80',
  ],
  'Ichimliklar': [
    'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400&q=80',
    'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&q=80',
    'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&q=80',
    'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400&q=80',
    'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400&q=80',
    'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&q=80',
    'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80',
    'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=400&q=80',
  ],
  'Shirinliklar': [
    'https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=400&q=80',
    'https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=400&q=80',
    'https://images.unsplash.com/photo-1606312619070-d48b4c652a52?w=400&q=80',
    'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400&q=80',
    'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400&q=80',
    'https://images.unsplash.com/photo-1559559228-f0756d4e6ca4?w=400&q=80',
    'https://images.unsplash.com/photo-1582630958-1696a611f8e9?w=400&q=80',
    'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&q=80',
  ],
  'Telefonlar': [
    'https://images.unsplash.com/photo-1632633173522-47456de71b76?w=400&q=80',
    'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&q=80',
    'https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=400&q=80',
    'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400&q=80',
    'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&q=80',
    'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=400&q=80',
    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80',
  ],
  'Noutbuklar': [
    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&q=80',
    'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&q=80',
    'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&q=80',
    'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&q=80',
    'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400&q=80',
    'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&q=80',
    'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&q=80',
  ],
  'Planshetlar': [
    'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&q=80',
    'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400&q=80',
    'https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=400&q=80',
    'https://images.unsplash.com/photo-1602080858428-57174f9431cf?w=400&q=80',
    'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&q=80',
  ],
  "O'yinchoqlar": [
    'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&q=80',
    'https://images.unsplash.com/photo-1509515837298-2c67a3933321?w=400&q=80',
    'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&q=80',
    'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&q=80',
    'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=400&q=80',
    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80',
    'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80',
    'https://images.unsplash.com/photo-1500332021-22da4b0df1be?w=400&q=80',
    'https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=400&q=80',
    'https://images.unsplash.com/photo-1606606603820-71c9b0f9c8e7?w=400&q=80',
  ],
  'Futbol toplari': [
    'https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=400&q=80',
    'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&q=80',
    'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&q=80',
    'https://images.unsplash.com/photo-1606925797300-0b35e9d1794e?w=400&q=80',
    'https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400&q=80',
    'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&q=80',
    'https://images.unsplash.com/photo-1560252811-6b9c1a156965?w=400&q=80',
  ],
  'Futbol kiyimlari': [
    'https://images.unsplash.com/photo-1571893544028-06b07af6dade?w=400&q=80',
    'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&q=80',
    'https://images.unsplash.com/photo-1521412644187-c49fa049e84d?w=400&q=80',
    'https://images.unsplash.com/photo-1597223557154-721c1cecc4b0?w=400&q=80',
    'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&q=80',
    'https://images.unsplash.com/photo-1540747913346-19212a4b32e6?w=400&q=80',
    'https://images.unsplash.com/photo-1519766304817-4f37bda74a26?w=400&q=80',
    'https://images.unsplash.com/photo-1606914469633-bd21f9e7f307?w=400&q=80',
  ],
  'Issiq kiyimlar': [
    'https://images.unsplash.com/photo-1548712499-19e509f6a8fd?w=400&q=80',
    'https://images.unsplash.com/photo-1539185441755-769473a23570?w=400&q=80',
    'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&q=80',
    'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=400&q=80',
    'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80',
    'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&q=80',
  ],
  'Yozgi kiyimlar': [
    'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&q=80',
    'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80',
    'https://images.unsplash.com/photo-1566479179817-cc17e3d07a10?w=400&q=80',
    'https://images.unsplash.com/photo-1523381210434-271e8be62f48?w=400&q=80',
    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80',
    'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400&q=80',
    'https://images.unsplash.com/photo-1554568218-0f1715e72254?w=400&q=80',
    'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&q=80',
  ],
  'Bolalar kiyimi': [
    'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400&q=80',
    'https://images.unsplash.com/photo-1503919005314-30d533d8e938?w=400&q=80',
    'https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=400&q=80',
    'https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400&q=80',
    'https://images.unsplash.com/photo-1502781252888-9143ba7f074e?w=400&q=80',
    'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400&q=80',
    'https://images.unsplash.com/photo-1484863137850-59afcfe05386?w=400&q=80',
  ],
};

// Kategoriya fallback
const CAT_FALLBACK = {
  'Kiyimlar':    'https://images.unsplash.com/photo-1523381210434-271e8be62f48?w=400&q=80',
  'Oziq-ovqat':  'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400&q=80',
  'Gadjetlar':   'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80',
  "O'yinchoqlar":'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&q=80',
};

// Image cache
const _imgCache = {};

function resolveProductImageUrl(product) {
  if (!product) return PRODUCT_IMAGE_FALLBACK;

  // 1. DB dan kelgan rasm — doim ustuvor
  const apiUrl = (product.image_url || '').trim();
  if (apiUrl && apiUrl.startsWith('http')) return apiUrl;

  // 2. Cache
  const cacheKey = product.id || (product.name + '|' + product.subcategory);
  if (_imgCache[cacheKey]) return _imgCache[cacheKey];

  // 3. Subkategoriya pool (ID bo'yicha rotatsiya)
  const sub = product.subcategory || '';
  const pool = SUBCAT_POOL[sub];
  if (pool && pool.length) {
    const url = pool[(product.id || 0) % pool.length];
    _imgCache[cacheKey] = url;
    return url;
  }

  // 4. Kategoriya fallback
  const url = CAT_FALLBACK[product.category || ''] || PRODUCT_IMAGE_FALLBACK;
  _imgCache[cacheKey] = url;
  return url;
}
