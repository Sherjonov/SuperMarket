/* SuperMarket - Savat va Buyurtma */

// ============ SAVAT ============
function renderCart() {
  const list=document.getElementById('cartItems');
  const summary=document.getElementById('cartSummary');
  const empty=document.getElementById('cartEmpty');
  if (!STATE.cart||!STATE.cart.length) {
    if(list) list.innerHTML='';
    if(summary) summary.classList.add('hidden');
    if(empty) empty.classList.remove('hidden');
    return;
  }
  if(empty) empty.classList.add('hidden');
  if(summary) summary.classList.remove('hidden');
  let total=0;
  if(list) list.innerHTML=STATE.cart.map(item=>{
    const p=(item.discounted_price&&item.discounted_price<item.price)?item.discounted_price:item.price;
    const sub=p*item.quantity; total+=sub;
    const imgSrc = resolveProductImageUrl(item);
    const fb = PRODUCT_IMAGE_FALLBACK;
    return `<div class="cart-item">
      <img class="cart-thumb" src="${imgSrc}" alt="" loading="lazy"
           onerror="this.onerror=null;this.src='${fb}'"/>
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        ${item.size?`<div class="cart-item-size">📐 Razmer: <strong>${item.size}</strong></div>`:''}
        <div class="cart-item-price">${formatPrice(p)} × ${item.quantity}</div>
        <div class="cart-item-sub">Jami: <strong>${formatPrice(sub)}</strong></div>
      </div>
      <div class="cart-item-actions">
        <button class="btn-qty" onclick="changeCartQty(${item.cart_id},${item.quantity-1})">−</button>
        <span class="cart-qty">${item.quantity}</span>
        <button class="btn-qty" onclick="changeCartQty(${item.cart_id},${item.quantity+1})">+</button>
        <button class="btn-remove" onclick="removeFromCart(${item.cart_id})">🗑️</button>
      </div>
    </div>`;
  }).join('');
  const ct=document.getElementById('cartTotal');
  if(ct) ct.textContent=formatPrice(total);
  updateCartBadge();
}

async function changeCartQty(cartId,newQty) {
  if(newQty<=0){await removeFromCart(cartId);return;}
  if(newQty>20){showToast('Bitta mahsulotdan 20 tadan ko\'p bo\'lmaydi','error');return;}
  try {
    await apiFetch('/api/cart/'+cartId,'PUT',{quantity:newQty});
    await refreshCart(); renderCart();
  } catch(e){showToast(e.message,'error');}
}

async function removeFromCart(cartId) {
  try {
    await apiFetch('/api/cart/'+cartId,'DELETE');
    await refreshCart(); renderCart();
    showToast('Savatdan o\'chirildi');
  } catch(e){showToast(e.message,'error');}
}

// ============ LIKE ============
async function toggleLike(productId,event) {
  if(event) event.stopPropagation();
  if(!STATE.user){showLoginRequiredModal();return;}
  try {
    const res=await apiFetch('/api/likes','POST',{user_id:STATE.user.id,product_id:productId});
    await refreshLikes();
    showToast(res.liked?'❤️ Yoqtirganlarimga qo\'shildi':'💔 Olib tashlandi');
    const ap=document.querySelector('.page.active');
    if(ap){
      if(ap.id==='page-home') renderHome();
      else if(ap.id==='page-catalog') filterCatalog();
      else if(ap.id==='page-favorites') renderFavorites();
      else if(ap.id==='page-discounts') renderDiscountsPage();
    }
  } catch(e){showToast(e.message,'error');}
}

// ============ SAVATGA QO'SHISH ============
function handleAddToCart(productId) {
  if(!STATE.user){showLoginRequiredModal();return;}
  const product=STATE.products.find(p=>p.id===productId);
  if(!product) return;
  const sizes=(product.sizes||'').split(',').map(s=>s.trim()).filter(Boolean);
  const hasReal=sizes.length>0&&!(sizes.length===1&&sizes[0]==='OneSize');
  if(hasReal){
    STATE.pendingCartProductId=productId;
    openSizeModal(product,sizes);
  } else {
    addToCartDirect(productId,sizes[0]==='OneSize'?'':(sizes[0]||''));
  }
}

function openSizeModal(product,sizes) {
  document.getElementById('sizeOptions').innerHTML=sizes.map(s=>
    `<div class="size-chip" onclick="selectSizeChip(this,'${s}')">${s}</div>`
  ).join('');
  const spn=document.getElementById('sizeProductName');
  if(spn) spn.textContent=product.name;
  STATE.pendingCartSize='';
  document.getElementById('sizeModal').classList.remove('hidden');
}

function selectSizeChip(el,size) {
  document.querySelectorAll('.size-chip').forEach(c=>c.classList.remove('selected'));
  el.classList.add('selected');
  STATE.pendingCartSize=size;
}

function closeSizeModal() {
  document.getElementById('sizeModal').classList.add('hidden');
  STATE.pendingCartProductId=null; STATE.pendingCartSize='';
}

async function addToCartWithSize() {
  if(!STATE.pendingCartSize){showToast('Razmer tanlang!','error');return;}
  const current = STATE.cart.find(
    i => i.product_id===STATE.pendingCartProductId && (i.size||'')===STATE.pendingCartSize
  );
  if (current) {
    const ok = confirm(`${STATE.pendingCartSize} razmerdan yana qo'shasizmi?`);
    if (!ok) return;
  }
  await addToCartDirect(STATE.pendingCartProductId,STATE.pendingCartSize);
  closeSizeModal();
}

async function addToCartDirect(productId,size) {
  try {
    const current = STATE.cart.find(
      i => i.product_id===productId && (i.size||'')===(size||'')
    );
    if (current && current.quantity>=20) {
      showToast('Bitta mahsulotdan 20 tadan ko\'p bo\'lmaydi','error');
      return;
    }
    await apiFetch('/api/cart','POST',{user_id:STATE.user.id,product_id:productId,quantity:1,size:size||''});
    await refreshCart();
    showToast(typeof t === 'function' ? t('cartAdded') : 'Savatga qo\'shildi','success');
  } catch(e){showToast(e.message,'error');}
}

// ============ CHECKOUT ============
let selectedPayment='';
let locationData={lat:null,lng:null,address:''};

function openCheckoutModal() {
  if(!STATE.user){showLoginRequiredModal();return;}
  if(!STATE.cart||!STATE.cart.length){showToast('Savat bo\'sh!','error');return;}
  selectedPayment='';
  locationData={lat:null,lng:null,address:''};
  let total=0;
  const items=STATE.cart.map(i=>{
    const p=(i.discounted_price&&i.discounted_price<i.price)?i.discounted_price:i.price;
    total+=p*i.quantity;
    return `<div class="checkout-item"><span>${i.name} × ${i.quantity}</span><span>${formatPrice(p*i.quantity)}</span></div>`;
  }).join('');
  const ci=document.getElementById('checkoutItems'); if(ci) ci.innerHTML=items;
  const ct=document.getElementById('checkoutTotal'); if(ct) ct.textContent=formatPrice(total);
  document.querySelectorAll('.payment-btn').forEach(b=>b.classList.remove('selected'));
  const cs=document.getElementById('cardSection'); if(cs) cs.classList.add('hidden');
  const ls=document.getElementById('locationStatus'); if(ls) ls.textContent='';
  const da=document.getElementById('deliveryAddress'); if(da) da.value='';
  const n=document.getElementById('checkoutName'); if(n) n.value=STATE.user?.name||'';
  const ln=document.getElementById('checkoutLastName'); if(ln) ln.value=STATE.user?.last_name||'';
  const ph=document.getElementById('checkoutPhone'); if(ph) ph.value=STATE.user?.tel||'';
  const dt=document.getElementById('checkoutDocType'); if(dt) dt.value='passport_uz';
  const pp=document.getElementById('checkoutPassport'); if(pp) pp.value='';
  const slb=document.getElementById('sendLocationBtn');
  if(slb){slb.textContent='📍 Lokatsiyani yuborish';slb.style.background='';slb.disabled=false;}
  const pb=document.getElementById('placeOrderBtn');
  if(pb){pb.disabled=false;pb.innerHTML='✅ <span>Buyurtmani tasdiqlash</span>';}
  document.getElementById('checkoutModal').classList.remove('hidden');
}

function closeCheckoutModal() {
  document.getElementById('checkoutModal').classList.add('hidden');
}

function selectPayment(method) {
  selectedPayment=method;
  document.querySelectorAll('.payment-btn').forEach(b=>b.classList.remove('selected'));
  const btn=document.querySelector('[data-payment="'+method+'"]');
  if(btn) btn.classList.add('selected');
  const cs=document.getElementById('cardSection');
  if(cs) cs.classList.toggle('hidden',method!=='card');
}

function sendLocation() {
  const btn=document.getElementById('sendLocationBtn');
  if(btn){btn.textContent='📡 Aniqlanmoqda...';btn.disabled=true;}
  const done=(lat,lng,label)=>{
    locationData={lat,lng,address:label};
    const ls=document.getElementById('locationStatus');
    if(ls) ls.innerHTML=`<span class="location-ok">✅ Lokatsiya yuborildi! (${lat.toFixed(4)}, ${lng.toFixed(4)})</span>`;
    if(btn){btn.textContent='✅ Lokatsiya yuborildi!';btn.style.background='var(--accent2)';btn.disabled=false;}
  };
  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(
      pos=>done(pos.coords.latitude,pos.coords.longitude,'GPS lokatsiya'),
      ()=>done(41.2995,69.2401,'Toshkent, O\'zbekiston'),
      {timeout:5000}
    );
  } else {
    done(41.2995,69.2401,'Toshkent, O\'zbekiston');
  }
}

async function placeOrder() {
  if(!selectedPayment){showToast('To\'lov usulini tanlang!','error');return;}
  const da=document.getElementById('deliveryAddress');
  const recipientName=((document.getElementById('checkoutName')||{}).value||'').trim();
  const recipientLastName=((document.getElementById('checkoutLastName')||{}).value||'').trim();
  const recipientPhone=((document.getElementById('checkoutPhone')||{}).value||'').trim();
  const docType=((document.getElementById('checkoutDocType')||{}).value||'').trim();
  const passportVal=((document.getElementById('checkoutPassport')||{}).value||'').trim();
  const address=(da?da.value:'').trim();
  if(recipientName.length<2){showToast('Ismni kiriting!','error');return;}
  if(recipientLastName.length<2){showToast('Familiyani kiriting!','error');return;}
  if(recipientPhone.length<7){showToast('Telefon raqamni kiriting!','error');return;}
  if(!address){showToast('Manzilni kiriting!','error');return;}
  const idCheck = validateCheckoutIdentity(docType, passportVal);
  if (!idCheck.ok) { showToast(idCheck.msg,'error'); return; }
  if(selectedPayment==='card'){
    const ch=(document.getElementById('cardHolder')||{}).value||'';
    const cardCheck = validateCheckoutCard();
    if (!cardCheck.ok) { showToast(cardCheck.msg,'error'); return; }
    if(!ch.trim()){showToast('Karta egasining ismini kiriting!','error');return;}
  }
  const btn=document.getElementById('placeOrderBtn');
  if(btn){btn.disabled=true;btn.textContent='⏳ Buyurtma berilmoqda...';}
  try {
    const payload={
      user_id:STATE.user.id,
      payment_method:selectedPayment,
      delivery_address:address,
      recipient_name:recipientName,
      recipient_last_name:recipientLastName,
      recipient_phone:recipientPhone,
      recipient_doc_type:docType,
      recipient_passport_number:passportVal,
      latitude:locationData.lat,
      longitude:locationData.lng,
    };
    if (selectedPayment==='card') {
      payload.card_number=(document.getElementById('cardNumber')||{}).value||'';
      payload.card_expiry=(document.getElementById('cardExpiry')||{}).value||'';
      payload.card_cvv=(document.getElementById('cardCvv')||{}).value||'';
    }
    const result=await apiFetch('/api/orders/checkout','POST',payload);
    closeCheckoutModal();
    await refreshCart(); renderCart();
    const sd=document.getElementById('successDelivery'); if(sd) sd.textContent=result.delivery_minutes;
    const st=document.getElementById('successTotal'); if(st) st.textContent=formatPrice(result.total_sum);
    const sp=document.getElementById('successPayment');
    if(sp) sp.textContent={card:'💳 Bank kartasi',cash:'💵 Naqd pul',payme:'📱 Payme',click:'📲 Click'}[selectedPayment]||selectedPayment;
    document.getElementById('orderSuccessModal').classList.remove('hidden');
  } catch(e) {
    showToast(e.message,'error');
    if(btn){btn.disabled=false;btn.innerHTML='✅ <span>Buyurtmani tasdiqlash</span>';}
  }
}

function closeOrderSuccess() {
  document.getElementById('orderSuccessModal').classList.add('hidden');
  showPage('home');
}

function formatCardNumber(input) {
  let val=input.value.replace(/\D/g,'').slice(0,19);
  input.value=val.replace(/(.{4})/g,'$1 ').trim();
}

function formatExpiry(input) {
  let val=input.value.replace(/\D/g,'').slice(0,4);
  if(val.length>=2) val=val.slice(0,2)+'/'+val.slice(2);
  input.value=val;
}

// ============ LOGIN KERAK ============
function showLoginRequiredModal() {
  document.getElementById('loginRequiredModal').classList.remove('hidden');
}
function closeLoginRequiredModal() {
  document.getElementById('loginRequiredModal').classList.add('hidden');
}
function goToRegisterFromModal() {
  closeLoginRequiredModal();
  document.getElementById('mainApp').classList.add('hidden');
  document.getElementById('authScreen').classList.remove('hidden');
  switchAuthTab('register');
}
