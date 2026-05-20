/* SuperMarket - UI yordamchi funksiyalar v2 */

function showToast(msg, type = '') {
  let toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.className = 'toast' + (type ? ' toast-' + type : '');
  toast.classList.remove('hidden');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.add('hidden'), 3500);
}

function formatPrice(n) {
  if (!n && n !== 0) return "0 so'm";
  return Number(n).toLocaleString('uz-UZ') + " so'm";
}

function formatDate(str) {
  if (!str) return '-';
  const d = new Date(str);
  const p = x => String(x).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

function getProductEmoji(p) {
  const name = (p?.name || '').toLowerCase();
  const key = `${p?.subcategory||''}|${p?.category||''}`.toLowerCase();
  const emojiByWord = [
    ['olma','🍎'],['banan','🍌'],['apelsin','🍊'],['uzum','🍇'],['kivi','🥝'],
    ['nok','🍐'],['shaftoli','🍑'],['gilos','🍒'],['limon','🍋'],['tarvuz','🍉'],
    ['qulupnay','🍓'],['malina','🍓'],['ananas','🍍'],['mango','🥭'],['avokado','🥑'],
    ['cola','🥤'],['fanta','🥤'],['sprite','🥤'],['suv','💧'],['sharbat','🧃'],['choy','🍵'],['qahva','☕'],
    ['pizza','🍕'],['burger','🍔'],['hot-dog','🌭'],['sendvich','🥪'],['shaorma','🌯'],['fri','🍟'],
    ['osh','🍚'],['manti','🥟'],['somsa','🥟'],['shashlik','🍢'],
    ['shokolad','🍫'],['chips','🥔'],['oreo','🍪'],['donuts','🍩'],['keks','🧁'],
    ['iphone','📱'],['samsung','📱'],['xiaomi','📱'],['huawei','📱'],['oppo','📱'],
    ['macbook','💻'],['noutbuk','💻'],['thinkpad','💻'],
    ['ipad','📟'],['planshet','📟'],
    ['kurtka','🧥'],['palto','🧥'],['pufka','🧥'],['sviter','🧶'],['futbolka','👕'],
    ['shim','👖'],['short','🩳'],['sandali','👡'],['krossovka','👟'],['etik','🥾'],
  ];
  for (const [word, emoji] of emojiByWord) {
    if (name.includes(word)) return emoji;
  }
  if (key.includes('issiq')) return '🧥';
  if (key.includes('yozgi')) return '👕';
  if (key.includes('meva')) return '🍎';
  if (key.includes('fastfood')) return '🍔';
  if (key.includes('milliy')) return '🍲';
  if (key.includes('ichimlik')) return '🥤';
  if (key.includes('shirin')) return '🍫';
  if (key.includes('telefon')) return '📱';
  if (key.includes('noutbuk')) return '💻';
  if (key.includes('planshet')) return '📟';
  return '🛒';
}

function toggleUserMenu(event) {
  if (event) event.stopPropagation();
  const menu = document.getElementById('userMenu');
  if (!menu) return;
  menu.classList.toggle('hidden');
}
function closeUserMenu() {
  const menu = document.getElementById('userMenu');
  if (menu) menu.classList.add('hidden');
}
function openSettingsFromMenu() { closeUserMenu(); showPage('settings'); }
function logoutFromMenu() { closeUserMenu(); doLogout(); }

document.addEventListener('click', function(event) {
  const wrap = document.querySelector('.user-menu-wrap');
  if (!wrap) return;
  if (!wrap.contains(event.target)) closeUserMenu();
});

document.addEventListener('languagechange', function() {
  const auth = document.getElementById('authScreen');
  if (auth && !auth.classList.contains('hidden')) return;
  const active = document.querySelector('#mainApp .page.active');
  if (!active || !active.id) return;
  const name = active.id.replace(/^page-/, '');
  if (typeof showPage === 'function') showPage(name, false);
});

const SUBCATEGORIES = {
  'Kiyimlar': [
    {name:'Issiq kiyimlar', icon:'🧥', desc:'Qishki, palto, pufkalar'},
    {name:'Yozgi kiyimlar', icon:'👕', desc:'Futbolka, shim, sandal'},
    {name:'Bolalar kiyimi', icon:'👶', desc:'3-14 yoshgacha'},
    {name:'Futbol kiyimlari', icon:'⚽', desc:'Klub va terma formalari'},
  ],
  'Oziq-ovqat': [
    {name:'Mevalar', icon:'🍎', desc:'Yangi va mazali mevalar'},
    {name:'Fastfood', icon:'🍔', desc:'Burger, pizza, shaorma'},
    {name:'Milliy taomlar', icon:'🍲', desc:"Osh, manti, lag'mon"},
    {name:'Ichimliklar', icon:'🥤', desc:'Sharbat, choy, qahva'},
    {name:'Shirinliklar', icon:'🍫', desc:'Shokolad, chips, keks'},
  ],
  'Gadjetlar': [
    {name:'Telefonlar', icon:'📱', desc:'iPhone, Samsung, Xiaomi'},
    {name:'Noutbuklar', icon:'💻', desc:"Gaming, ish, o'qish"},
    {name:'Planshetlar', icon:'📟', desc:'iPad, Samsung Tab'},
  ],
  "O'yinchoqlar": [
    {name:"O'yinchoqlar", icon:'🧸', desc:"Lego, qo'g'irchoq, transport"},
    {name:'Futbol toplari', icon:'⚽', desc:'Professional va mashq uchun'},
  ],
};

function showPage(name, push=true) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById('page-'+name);
  if (target) { target.classList.add('active'); if (push) STATE.pageHistory.push(name); }
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector('[data-page="'+name+'"]');
  if (btn) btn.classList.add('active');
  const loaders = {
    'home':renderHome, 'favorites':renderFavorites, 'cart':renderCart,
    'discounts':renderDiscountsPage, 'my-orders':renderMyOrders,
    'admin-dashboard':loadAdminDashboard,
    'admin-add':setupAdminAdd, 'admin-delete':renderAdminDelete,
    'admin-logs':loadAdminLogs, 'admin-orders':loadAdminOrders,
    'admin-users':loadAdminUsers, 'admin-discounts':loadAdminDiscounts,
  };
  if (loaders[name]) loaders[name]();
  // Mobile: close sidebar on page change
  if (window.innerWidth <= 900) {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.add('closed');
  }
}

function goBack() {
  STATE.pageHistory.pop();
  const prev = STATE.pageHistory[STATE.pageHistory.length-1];
  if (STATE.currentSubcategory && prev === 'catalog') {
    STATE.currentSubcategory = '';
    renderSubcategories(STATE.currentCategory);
    const cf = document.getElementById('catalogFilters'); if (cf) cf.classList.add('hidden');
    const cp = document.getElementById('catalogProducts'); if (cp) cp.innerHTML = '';
    const sc = document.getElementById('subCatContainer'); if (sc) sc.style.display = '';
    // Restore category title
    const titles = {'Kiyimlar':t('clothes'),'Oziq-ovqat':t('food'),'Gadjetlar':t('gadgets'),"O'yinchoqlar":t('toys')};
    const ct = document.getElementById('catalogTitle');
    if (ct) ct.textContent = titles[STATE.currentCategory] || STATE.currentCategory;
    return;
  }
  showPage(prev||'home', false);
}

function openCategory(cat) {
  STATE.currentCategory = cat; STATE.currentSubcategory = '';
  showPage('catalog');
  const titles = {'Kiyimlar':t('clothes'),'Oziq-ovqat':t('food'),'Gadjetlar':t('gadgets'),"O'yinchoqlar":t('toys')};
  const el = document.getElementById('catalogTitle'); if (el) el.textContent = titles[cat]||cat;
  renderSubcategories(cat);
  const cf = document.getElementById('catalogFilters'); if (cf) cf.classList.add('hidden');
  const cp = document.getElementById('catalogProducts'); if (cp) cp.innerHTML = '';
}

function renderSubcategories(cat) {
  const subs = SUBCATEGORIES[cat] || [];
  const el = document.getElementById('subCatContainer');
  if (!el) return;
  el.style.display = '';
  // Use data-idx to avoid HTML quote conflicts with apostrophes in names (O\'yinchoqlar etc)
  window._currentSubcats = subs;
  el.innerHTML = subs.map((s, i) => {
    const safeName = s.name.replace(/&/g,'&amp;').replace(/"/g,'&quot;');
    return `<div class="subcat-card" data-subidx="${i}" data-subname="${safeName}" onclick="handleSubcatClick(this)"><div class="sub-icon">${s.icon}</div><h4>${s.name}</h4><p>${s.desc}</p></div>`;
  }).join('');
}

function handleSubcatClick(el) {
  const idx = parseInt(el.getAttribute('data-subidx'));
  const subs = window._currentSubcats || [];
  if (subs[idx]) openSubcategory(subs[idx].name);
}

function openSubcategory(sub) {
  STATE.currentSubcategory = sub;
  const sc = document.getElementById('subCatContainer'); if (sc) sc.style.display = 'none';
  const cf = document.getElementById('catalogFilters'); if (cf) cf.classList.remove('hidden');
  const ct = document.getElementById('catalogTitle'); if (ct) ct.textContent = sub;
  const prods = STATE.products.filter(p => p.subcategory === sub);
  const sizes = new Set();
  prods.forEach(p => { if (p.sizes) p.sizes.split(',').forEach(s => sizes.add(s.trim())); });
  const sf = document.getElementById('catalogSizeFilter');
  if (sf) sf.innerHTML = `<option value="">${t('filterSizes')}</option>`+[...sizes].filter(Boolean).map(s=>`<option value="${s}">${s}</option>`).join('');
  filterCatalog();
}

function filterCatalog() {
  const q = (document.getElementById('catalogSearch')||{}).value||'';
  const size = (document.getElementById('catalogSizeFilter')||{}).value||'';
  const sort = (document.getElementById('catalogPriceFilter')||{}).value||'';
  let prods = STATE.products.filter(p => p.subcategory === STATE.currentSubcategory);
  if (q) prods = prods.filter(p => p.name.toLowerCase().includes(q.toLowerCase()));
  if (size) prods = prods.filter(p => p.sizes && p.sizes.split(',').map(s=>s.trim()).includes(size));
  if (sort==='asc') prods.sort((a,b)=>(a.discounted_price||a.price)-(b.discounted_price||b.price));
  if (sort==='desc') prods.sort((a,b)=>(b.discounted_price||b.price)-(a.discounted_price||a.price));
  const grid = document.getElementById('catalogProducts');
  if (grid) grid.innerHTML = prods.length ? prods.map(p=>productCardHTML(p)).join('') : '<p class="empty-text">Mahsulot topilmadi</p>';
}

function productCardHTML(p, opts={}) {
  const isLiked = STATE.myLikeIds.includes(p.id);
  const dp = (p.discounted_price && p.discounted_price < p.price) ? p.discounted_price : p.price;
  const hasDis = p.discount_percent > 0;
  const imgSrc = resolveProductImageUrl(p);
  const fb = PRODUCT_IMAGE_FALLBACK;
  return `<div class="product-card" onclick="openProductDetail(${p.id})">
    <div class="product-img-wrap">
      <img class="product-img" src="${imgSrc}" alt="${p.name}" loading="lazy"
           onerror="this.onerror=null;this.src='${fb}'"/>
      ${hasDis ? `<div class="discount-tag">-${p.discount_percent}%</div>` : ''}
      <button class="like-btn ${isLiked?'liked':''}" onclick="toggleLike(${p.id},event)">
        ${isLiked?'❤️':'🤍'}
      </button>
    </div>
    <div class="product-body">
      <div class="product-name">${p.name}</div>
      <div class="product-cat">${p.subcategory}</div>
      <div class="product-price-row">
        <span class="product-price">${formatPrice(dp)}</span>
        ${hasDis ? `<span class="product-old-price">${formatPrice(p.price)}</span>` : ''}
      </div>
      <div class="product-stock ${(p.stock||0)>0?'':'out-of-stock'}">
        ${(p.stock||0)>0 ? `✅ ${p.stock} dona` : '❌ Tugagan'}
      </div>
      <div class="product-actions" onclick="event.stopPropagation()">
        ${opts.showDelete ? `<button class="btn-delete-sm" onclick="doDeleteProduct(${p.id})">🗑️</button>` : ''}
        <button class="btn-cart" onclick="handleAddToCart(${p.id})">🛒 Savat</button>
      </div>
    </div>
  </div>`;
}

// ============ PRODUCT DETAIL MODAL ============
function openProductDetail(pid) {
  const p = STATE.products.find(pr => pr.id === pid);
  if (!p) return;
  const imgSrc = resolveProductImageUrl(p);
  const fb = PRODUCT_IMAGE_FALLBACK;
  const dp = (p.discounted_price && p.discounted_price < p.price) ? p.discounted_price : p.price;
  const hasDis = p.discount_percent > 0;
  const isLiked = STATE.myLikeIds.includes(p.id);
  const sizesHtml = p.sizes ? p.sizes.split(',').filter(Boolean).map(s=>`<span class="size-chip">${s.trim()}</span>`).join('') : '';
  const modal = document.getElementById('productDetailModal');
  if (!modal) return;
  modal.innerHTML = `
    <div class="modal-box modal-product" onclick="event.stopPropagation()">
      <button class="modal-close product-detail-close" onclick="closeProductDetail()">✕</button>
      <div class="product-detail-inner">
        <div class="product-detail-img-side">
          <img src="${imgSrc}" alt="${p.name}" loading="lazy" onerror="this.onerror=null;this.src='${fb}'" class="product-detail-img"/>
          ${hasDis ? `<div class="detail-discount-badge">-${p.discount_percent}% Chegirma</div>` : ''}
        </div>
        <div class="product-detail-info">
          <div class="detail-breadcrumb">${p.category} › ${p.subcategory}</div>
          <h2 class="detail-name">${p.name}</h2>
          <div class="detail-price-wrap">
            <span class="detail-price">${formatPrice(dp)}</span>
            ${hasDis ? `<span class="detail-old-price">${formatPrice(p.price)}</span>` : ''}
          </div>
          ${sizesHtml ? `<div class="detail-section"><strong>O'lchamlar:</strong><div class="detail-sizes">${sizesHtml}</div></div>` : ''}
          <div class="detail-section detail-meta">
            <div class="detail-meta-row"><span>📦 Kategoriya:</span><strong>${p.category}</strong></div>
            <div class="detail-meta-row"><span>📂 Sub:</span><strong>${p.subcategory}</strong></div>
            <div class="detail-meta-row"><span>📊 Mavjud:</span>
              <strong class="${(p.stock||0)>0?'stock-ok':'stock-out'}">${(p.stock||0)>0?'✅ '+p.stock+' dona':'❌ Tugagan'}</strong>
            </div>
            ${hasDis ? `<div class="detail-meta-row"><span>💥 Tejamkorlik:</span><strong class="price-green">${formatPrice(p.price-dp)} tejaysiz</strong></div>` : ''}
          </div>
          <div class="detail-actions">
            <button class="btn-primary btn-detail-cart" onclick="handleAddToCart(${p.id});closeProductDetail()">🛒 Savatga qo'shish</button>
            <button class="btn-like-detail ${isLiked?'liked':''}" onclick="toggleLike(${p.id},event)">
              ${isLiked ? "❤️ Yoqtirganlarimda" : "🤍 Yoqtirganlarimga qo'shish"}
            </button>
          </div>
        </div>
      </div>
    </div>`;
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeProductDetail() {
  const modal = document.getElementById('productDetailModal');
  if (modal) modal.classList.add('hidden');
  document.body.style.overflow = '';
}

function renderHome() {
  const disc = STATE.products.filter(p => p.discount_percent > 0).slice(0, 8);
  const hd = document.getElementById('homeDiscountedProducts');
  if (hd) hd.innerHTML = disc.length ? disc.map(p=>productCardHTML(p)).join('') : '<p class="empty-text">Hozircha chegirmalar yo\'q</p>';
  const newest = [...STATE.products].reverse().slice(0, 16);
  const hp = document.getElementById('homeProducts');
  if (hp) hp.innerHTML = newest.map(p=>productCardHTML(p)).join('');
}

function globalSearchProducts() {
  const q = (document.getElementById('globalSearch')||{}).value||'';
  if (!q.trim()) return;
  STATE.currentSubcategory = '__search__'; STATE.currentCategory = '';
  showPage('catalog');
  const ct = document.getElementById('catalogTitle'); if (ct) ct.textContent = '🔍 "'+q+'"';
  const sc = document.getElementById('subCatContainer'); if (sc) sc.style.display = 'none';
  const cf = document.getElementById('catalogFilters'); if (cf) cf.classList.add('hidden');
  const prods = STATE.products.filter(p => p.name.toLowerCase().includes(q.toLowerCase()));
  const grid = document.getElementById('catalogProducts');
  if (grid) grid.innerHTML = prods.length ? prods.map(p=>productCardHTML(p)).join('') : '<p class="empty-text">Hech narsa topilmadi</p>';
}

function renderFavorites() {
  const grid = document.getElementById('favoritesGrid');
  if (!grid) return;
  grid.innerHTML = STATE.likes.length ? STATE.likes.map(p=>productCardHTML(p)).join('')
    : `<div class="empty-state"><div class="empty-icon">❤️</div><p>Yoqtirgan mahsulotlar yo'q</p></div>`;
}

function renderDiscountsPage() {
  const disc = STATE.products.filter(p => p.discount_percent > 0);
  const grid = document.getElementById('discountsGrid');
  if (!grid) return;
  grid.innerHTML = disc.length ? disc.map(p=>productCardHTML(p)).join('')
    : `<div class="empty-state"><div class="empty-icon">🏷️</div><p>Chegirmali mahsulotlar yo'q</p></div>`;
}

// ============ MY ORDERS ============
async function renderMyOrders() {
  const grid = document.getElementById('myOrdersList');
  if (!grid || !STATE.user) return;
  grid.innerHTML = '<div style="padding:24px;text-align:center">⏳ Yuklanmoqda...</div>';
  try {
    const orders = await apiFetch('/api/orders/user/'+STATE.user.id);
    if (!orders.length) {
      grid.innerHTML = `<div class="empty-state"><div class="empty-icon">📦</div><p>Hozircha buyurtmalar yo'q</p></div>`;
      return;
    }
    const statusColors = {'Yangi':'#6c63ff','Tasdiqlangan':'#2196F3','Yetkazilmoqda':'#FF9800','Yetkazildi':'#4CAF50','Bekor qilindi':'#F44336'};
    const statusIcons = {'Yangi':'🆕','Tasdiqlangan':'✅','Yetkazilmoqda':'🚚','Yetkazildi':'🎉','Bekor qilindi':'❌'};
    grid.innerHTML = orders.map(o => {
      const color = statusColors[o.status] || '#888';
      const icon = statusIcons[o.status] || '📦';
      return `<div class="order-card">
        <div class="order-card-header">
          <div class="order-info-left">
            ${o.image_url ? `<img src="${o.image_url}" class="order-thumb" onerror="this.style.display='none'">` : ''}
            <div>
              <div class="order-product-name">${o.product_name}</div>
              <div class="order-date">${formatDate(o.order_date)}</div>
            </div>
          </div>
          <span class="order-status-badge" style="background:${color}">${icon} ${o.status||'Yangi'}</span>
        </div>
        <div class="order-card-body">
          <div class="order-detail-row"><span>Miqdor:</span><strong>${o.quantity} ta</strong></div>
          <div class="order-detail-row"><span>Narx:</span><strong>${formatPrice(o.price_per_unit)}</strong></div>
          <div class="order-detail-row"><span>Jami:</span><strong class="price-green">${formatPrice(o.total_price)}</strong></div>
          <div class="order-detail-row"><span>To'lov:</span><strong>${o.payment_method||'-'}</strong></div>
          <div class="order-detail-row"><span>Manzil:</span><span style="font-size:12px">${o.delivery_address||'-'}</span></div>
        </div>
        ${(o.status==='Tasdiqlangan'||o.status==='Yetkazilmoqda') ? `<div class="order-delivery-notice">🚚 Buyurtmangiz tasdiqlandi! Tez orada yetkazib boriladi.</div>` : ''}
        ${o.status==='Yetkazildi' ? `<div class="order-delivery-notice success-notice">🎉 Buyurtmangiz yetkazildi! Xaridingiz uchun rahmat.</div>` : ''}
      </div>`;
    }).join('');
  } catch(e) {
    grid.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><p>${e.message}</p></div>`;
  }
}
