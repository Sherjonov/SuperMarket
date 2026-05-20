/* SuperMarket - API moduli */

// Asosiy API funksiyasi - barcha JS fayllarida ishlatiladi
async function apiFetch(url, method='GET', body=null) {
  const opts = { method, headers:{'Content-Type':'application/json'} };
  if (body) opts.body = JSON.stringify(body);
  let res;
  try {
    res = await fetch(url, opts);
  } catch(netErr) {
    throw new Error('Server bilan aloqa yo\'q');
  }
  const text = await res.text();
  if (!text || text.trim() === '') {
    if (!res.ok) throw new Error('Server xatosi: ' + res.status);
    return {};
  }
  let data;
  try {
    data = JSON.parse(text);
  } catch(e) {
    throw new Error('Server noto\'g\'ri javob qaytardi');
  }
  if (!res.ok) throw new Error(data.error || 'Xatolik: ' + res.status);
  return data;
}

// Mahsulotlarni yangilash
async function refreshProducts() {
  STATE.products = await apiFetch('/api/products');
}

// Savatni yangilash
async function refreshCart() {
  if (!STATE.user) { STATE.cart=[]; updateCartBadge(); return; }
  try { STATE.cart = await apiFetch('/api/cart/'+STATE.user.id); }
  catch(e) { STATE.cart=[]; }
  updateCartBadge();
}

// Like larni yangilash
async function refreshLikes() {
  if (!STATE.user) { STATE.likes=[]; STATE.myLikeIds=[]; updateLikesBadge(); return; }
  try {
    const [liked, ids] = await Promise.all([
      apiFetch('/api/likes/'+STATE.user.id),
      apiFetch('/api/myLikes/'+STATE.user.id)
    ]);
    STATE.likes = liked;
    STATE.myLikeIds = ids;
  } catch(e) { STATE.likes=[]; STATE.myLikeIds=[]; }
  updateLikesBadge();
}

// Hammasini yangilash
async function refreshAll() {
  await Promise.all([refreshProducts(), refreshCart(), refreshLikes()]);
}
