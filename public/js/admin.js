/* SuperMarket - Admin panel */
const SUBCATS={
  'Kiyimlar':['Issiq kiyimlar','Yozgi kiyimlar','Bolalar kiyimi','Futbol kiyimlari'],
  'Oziq-ovqat':['Mevalar','Fastfood','Milliy taomlar','Ichimliklar','Shirinliklar'],
  'Gadjetlar':['Telefonlar','Noutbuklar','Planshetlar'],
  "O'yinchoqlar":["O'yinchoqlar",'Futbol toplari'],
};

async function onAdminImagePick(ev) {
  const f = ev.target.files && ev.target.files[0];
  const prev = document.getElementById('addImagePreview');
  const hid = document.getElementById('addImageUrl');
  if (!f) return;
  const fd = new FormData();
  fd.append('file', f);
  try {
    const res = await fetch('/api/upload/product-image', { method: 'POST', body: fd });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Yuklash xatosi');
    if (hid) hid.value = data.url;
    if (prev) {
      prev.src = data.url;
      prev.classList.remove('hidden');
    }
    showToast('Rasm saqlandi','success');
  } catch (e) {
    showToast(e.message,'error');
  }
}

async function loadAdminDashboard() {
  try {
    const d=await apiFetch('/api/admin/overview');
    const el=document.getElementById('adminStats');
    if(el) el.innerHTML=`
      <div class="stat-card"><div class="stat-icon">👥</div><div class="stat-value">${d.users}</div><div class="stat-label">Foydalanuvchilar</div></div>
      <div class="stat-card"><div class="stat-icon">📦</div><div class="stat-value">${d.products}</div><div class="stat-label">Mahsulotlar</div></div>
      <div class="stat-card"><div class="stat-icon">🛒</div><div class="stat-value">${d.orders}</div><div class="stat-label">Buyurtmalar</div></div>
      <div class="stat-card"><div class="stat-icon">❤️</div><div class="stat-value">${d.likes}</div><div class="stat-label">Yoqtirishlar</div></div>
      <div class="stat-card"><div class="stat-icon">🏷️</div><div class="stat-value">${d.discounts}</div><div class="stat-label">Chegirmalar</div></div>
      <div class="stat-card"><div class="stat-icon">💰</div><div class="stat-value">${formatPrice(d.total_revenue)}</div><div class="stat-label">Umumiy daromad</div></div>`;
  } catch(e){showToast(e.message,'error');}
}

function setupAdminAdd(){}

function updateSubcategoryOptions() {
  const cat=document.getElementById('addCategory').value;
  const sub=document.getElementById('addSubcategory');
  const subs=SUBCATS[cat]||[];
  if(sub) sub.innerHTML=`<option value="">Subkategoriya tanlang</option>`+subs.map(s=>`<option value="${s}">${s}</option>`).join('');
}

async function doAddProduct() {
  const name=(document.getElementById('addName').value||'').trim();
  const price=document.getElementById('addPrice').value;
  const category=document.getElementById('addCategory').value;
  const subcategory=document.getElementById('addSubcategory').value;
  const sizes=(document.getElementById('addSizes').value||'').trim();
  const stock=document.getElementById('addStock').value||50;
  const image_url=(document.getElementById('addImageUrl').value||'').trim();
  const msg=document.getElementById('addProductMsg');
  if(!name||!price||!category||!subcategory){
    msg.textContent='❌ Barcha majburiy maydonlarni to\'ldiring'; msg.className='form-msg error'; return;
  }
  try {
    await apiFetch('/api/products','POST',{name,price,category,subcategory,sizes,stock,image_url});
    await refreshProducts();
    msg.textContent='✅ Mahsulot qo\'shildi!'; msg.className='form-msg success';
    showToast('Mahsulot qo\'shildi!','success');
    ['addName','addPrice','addSizes'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
    const fi=document.getElementById('addImageFile'); if(fi) fi.value='';
    const hid=document.getElementById('addImageUrl'); if(hid) hid.value='';
    const prev=document.getElementById('addImagePreview'); if(prev){ prev.src=''; prev.classList.add('hidden');}
    document.getElementById('addStock').value='50';
  } catch(e){msg.textContent='❌ '+e.message;msg.className='form-msg error';}
}

function renderAdminDelete(filter='') {
  const prods=filter?STATE.products.filter(p=>p.name.toLowerCase().includes(filter.toLowerCase())):STATE.products;
  const el=document.getElementById('adminDeleteGrid');
  if(el) el.innerHTML=prods.map(p=>productCardHTML(p,{showDelete:true})).join('');
}
function filterAdminDelete(){renderAdminDelete((document.getElementById('adminDeleteSearch')||{}).value||'');}

async function doDeleteProduct(id) {
  if(!confirm('Mahsulotni o\'chirishni tasdiqlaysizmi?')) return;
  try {
    await apiFetch('/api/products/'+id,'DELETE');
    await refreshProducts();
    renderAdminDelete((document.getElementById('adminDeleteSearch')||{}).value||'');
    showToast('Mahsulot o\'chirildi','error');
  } catch(e){showToast(e.message,'error');}
}

async function loadAdminDiscounts() {
  const sel=document.getElementById('discountProduct');
  if(sel) sel.innerHTML=`<option value="">Mahsulotni tanlang</option>`+
    STATE.products.map(p=>`<option value="${p.id}">${p.name} — ${formatPrice(p.price)}</option>`).join('');
  try {
    const discounts=await apiFetch('/api/discounts');
    const el=document.getElementById('discountsList');
    if(!el) return;
    if(!discounts.length){el.innerHTML='<p class="empty-text" style="padding:16px">Chegirmalar yo\'q</p>';return;}
    el.innerHTML=`<table><thead><tr>
      <th>#</th><th>Mahsulot</th><th>Kategoriya</th><th>Asl narx</th>
      <th>Chegirma</th><th>Chegirmali narx</th><th>Qo'shilgan vaqt</th><th>Amal</th>
    </tr></thead><tbody>${discounts.map((d,i)=>`<tr>
      <td>${i+1}</td><td><strong>${d.product_name}</strong></td>
      <td>${d.category} › ${d.subcategory}</td>
      <td>${formatPrice(d.price)}</td>
      <td><span class="badge-discount">-${d.discount_percent}%</span></td>
      <td class="price-col">${formatPrice(Math.round(d.price*(1-d.discount_percent/100)))}</td>
      <td>${formatDate(d.created_at)}</td>
      <td><button class="btn-sm btn-danger-sm" onclick="removeDiscount(${d.product_id})">🗑️ O'chirish</button></td>
    </tr>`).join('')}</tbody></table>`;
  } catch(e){showToast(e.message,'error');}
}

async function doAddDiscount() {
  const pid=(document.getElementById('discountProduct')||{}).value;
  const pct=(document.getElementById('discountPercent')||{}).value;
  const msg=document.getElementById('discountMsg');
  if(!pid||!pct){msg.textContent='❌ Mahsulot va foizni kiriting';msg.className='form-msg error';return;}
  try {
    await apiFetch('/api/discounts','POST',{product_id:pid,discount_percent:pct});
    await refreshProducts();
    msg.textContent='✅ Chegirma qo\'shildi!';msg.className='form-msg success';
    showToast('Chegirma qo\'shildi!','success');
    document.getElementById('discountPercent').value='';
    loadAdminDiscounts();
  } catch(e){msg.textContent='❌ '+e.message;msg.className='form-msg error';}
}

async function removeDiscount(pid) {
  if(!confirm('Chegirmani olib tashlaysizmi?')) return;
  try {
    await apiFetch('/api/discounts/'+pid,'DELETE');
    await refreshProducts(); showToast('Chegirma olib tashlandi'); loadAdminDiscounts();
  } catch(e){showToast(e.message,'error');}
}

async function loadAdminLogs() {
  try {
    const logs=await apiFetch('/api/logs');
    const el=document.getElementById('logsTable');
    if(!el) return;
    if(!logs.length){el.innerHTML='<p class="empty-text" style="padding:16px">Qaydlar yo\'q</p>';return;}
    el.innerHTML=`<table><thead><tr>
      <th>#</th><th>Ism</th><th>Familiya</th><th>Username</th>
      <th>Harakat</th><th>Yil</th><th>Oy</th><th>Kun</th><th>Soat</th><th>IP</th>
    </tr></thead><tbody>${logs.map((l,i)=>{
      const d=new Date(l.time); const p=x=>String(x).padStart(2,'0');
      return `<tr>
        <td>${i+1}</td><td>${l.name||'-'}</td><td>${l.last_name||'-'}</td>
        <td><strong>${l.username}</strong></td>
        <td><span class="badge-${l.action==='login'?'login':'logout'}">${l.action==='login'?'🟢 Kirdi':'🔴 Chiqdi'}</span></td>
        <td>${d.getFullYear()}</td><td>${p(d.getMonth()+1)}</td><td>${p(d.getDate())}</td>
        <td>${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}</td>
        <td>${l.ip_address||'-'}</td>
      </tr>`;}).join('')}</tbody></table>`;
  } catch(e){showToast(e.message,'error');}
}

async function loadAdminOrders() {
  try {
    const orders=await apiFetch('/api/orders');
    const el=document.getElementById('ordersTable');
    if(!el) return;
    if(!orders.length){el.innerHTML='<p class="empty-text" style="padding:16px">Buyurtmalar yo\'q</p>';return;}
    const statusColors={'Yangi':'#6c63ff','Tasdiqlangan':'#2196F3','Yetkazilmoqda':'#FF9800','Yetkazildi':'#4CAF50','Bekor qilindi':'#F44336'};
    el.innerHTML=`<table><thead><tr>
      <th>#</th><th>Ism</th><th>Username</th>
      <th>Mahsulot</th><th>Soni</th><th>Jami</th>
      <th>To'lov</th><th>Manzil</th><th>Status</th><th>Tasdiqlash</th><th>Vaqt</th>
    </tr></thead><tbody>${orders.map((o,i)=>{
      const sc=statusColors[o.status]||'#888';
      return `<tr>
        <td>${i+1}</td>
        <td>${o.name||'-'} ${o.last_name||''}</td>
        <td><strong>${o.username}</strong></td>
        <td><strong>${o.product_name}</strong></td>
        <td>${o.quantity}</td>
        <td class="price-col">${formatPrice(o.total_price)}</td>
        <td><span class="badge-pay">${o.payment_method||'-'}</span></td>
        <td style="max-width:120px;font-size:11px">${o.delivery_address||'-'}</td>
        <td><span style="background:${sc};color:#fff;padding:3px 8px;border-radius:12px;font-size:11px;font-weight:600">${o.status||'Yangi'}</span></td>
        <td>
          <div class="order-action-btns">
            ${o.status!=='Tasdiqlangan'?`<button class="btn-sm btn-approve" onclick="approveOrder(${o.id},'Tasdiqlangan')">✅ Tasdiqlash</button>`:''}
            ${o.status==='Tasdiqlangan'?`<button class="btn-sm btn-deliver" onclick="approveOrder(${o.id},'Yetkazilmoqda')">🚚 Yetkazish</button>`:''}
            ${o.status==='Yetkazilmoqda'?`<button class="btn-sm btn-done" onclick="approveOrder(${o.id},'Yetkazildi')">🎉 Yetdi</button>`:''}
            ${o.status!=='Bekor qilindi'&&o.status!=='Yetkazildi'?`<button class="btn-sm btn-cancel" onclick="approveOrder(${o.id},'Bekor qilindi')">❌ Bekor</button>`:''}
          </div>
        </td>
        <td style="white-space:nowrap;font-size:11px">${formatDate(o.order_date)}</td>
      </tr>`;
    }).join('')}</tbody></table>`;
  } catch(e){showToast(e.message,'error');}
}

async function loadAdminUsers() {
  try {
    const users=await apiFetch('/api/users');
    const el=document.getElementById('usersTable');
    if(!el) return;
    if(!users.length){el.innerHTML='<p class="empty-text" style="padding:16px">Foydalanuvchilar yo\'q</p>';return;}
    el.innerHTML=`<table><thead><tr>
      <th>#</th><th>Ism</th><th>Familiya</th><th>Username</th>
      <th>Email</th><th>Tel</th><th>Rol</th><th>Qo'shilgan</th><th>Amal</th>
    </tr></thead><tbody>${users.map((u,i)=>`<tr>
      <td>${i+1}</td><td>${u.name}</td><td>${u.last_name}</td>
      <td><strong>${u.username}</strong></td>
      <td>${u.email}</td><td>${u.tel||'-'}</td>
      <td><span class="${u.isAdmin?'badge-login':'badge-logout'}">${u.isAdmin?'👑 Admin':'👤 User'}</span></td>
      <td>${formatDate(u.created_at)}</td>
      <td>${!u.isAdmin?`<button class="btn-sm btn-danger-sm" onclick="doDeleteUser(${u.id})">🗑️</button>`:'—'}</td>
    </tr>`).join('')}</tbody></table>`;
  } catch(e){showToast(e.message,'error');}
}

async function doDeleteUser(id) {
  if(!confirm('Foydalanuvchini o\'chirishni tasdiqlaysizmi?')) return;
  try {
    await apiFetch('/api/users/'+id,'DELETE');
    showToast('Foydalanuvchi o\'chirildi'); loadAdminUsers();
  } catch(e){showToast(e.message,'error');}
}

async function doChangeUsername() {
  const msg=document.getElementById('usernameMsg');
  try {
    const res=await apiFetch('/api/settings/username','PUT',{
      user_id:STATE.user.id,
      username:(document.getElementById('newUsername').value||'').trim(),
      email:(document.getElementById('settingsEmail').value||'').trim(),
    });
    STATE.user.username=(document.getElementById('newUsername').value||'').trim();
    const un=document.getElementById('userName'); if(un) un.textContent=STATE.user.username;
    msg.textContent='✅ '+res.message; msg.className='form-msg success';
  } catch(e){msg.textContent='❌ '+e.message;msg.className='form-msg error';}
}

async function doChangePassword() {
  const msg=document.getElementById('passwordMsg');
  try {
    const res=await apiFetch('/api/settings/password','PUT',{
      user_id:STATE.user.id,
      old_password:(document.getElementById('oldPassword').value||''),
      new_password:(document.getElementById('newPassword').value||''),
      confirm_password:(document.getElementById('confirmPassword').value||''),
    });
    msg.textContent='✅ '+res.message; msg.className='form-msg success';
    ['oldPassword','newPassword','confirmPassword'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
  } catch(e){msg.textContent='❌ '+e.message;msg.className='form-msg error';}
}

// ============ BUYURTMA TASDIQLASH (ADMIN) ============
async function approveOrder(oid, status) {
  const labels = {'Tasdiqlangan':'✅ Tasdiqlandi','Yetkazilmoqda':'🚚 Yetkazilmoqda','Yetkazildi':'🎉 Yetkazildi','Bekor qilindi':'❌ Bekor qilindi'};
  try {
    await apiFetch('/api/orders/'+oid+'/status','PUT',{status});
    showToast(labels[status]||'Status yangilandi','success');
    loadAdminOrders();
  } catch(e){showToast(e.message,'error');}
}
