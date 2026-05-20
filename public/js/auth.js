/* SuperMarket - Autentifikatsiya (100% ishlaydigan) */

const SESSION_KEY = 'supermarket_user_session_v1';

function saveSession() {
  if (STATE.user) localStorage.setItem(SESSION_KEY, JSON.stringify(STATE.user));
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

function restoreSession() {
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (!raw) return false;
    const user = JSON.parse(raw);
    if (!user || !user.id || !user.username) return false;
    STATE.user = user;
    return true;
  } catch (_) {
    return false;
  }
}

function switchAuthTab(tab) {
  ['login','register','adminLogin'].forEach(name => {
    const panel = document.getElementById(name + 'Panel');
    const tabEl = document.getElementById('tab_' + name);
    if (panel) panel.classList.add('hidden');
    if (tabEl) tabEl.classList.remove('active');
  });
  const target = document.getElementById(tab + 'Panel');
  const targetTab = document.getElementById('tab_' + tab);
  if (target) target.classList.remove('hidden');
  if (targetTab) targetTab.classList.add('active');
}

async function doLogin() {
  const username = (document.getElementById('loginUsername').value || '').trim();
  const password = document.getElementById('loginPassword').value || '';
  const msg = document.getElementById('loginMsg');
  msg.textContent = ''; msg.className = 'form-msg';
  if (!username || !password) { msg.textContent = 'Username va parolni kiriting'; msg.className='form-msg error'; return; }
  const btn = document.querySelector('#loginPanel .btn-primary');
  if (btn) { btn.disabled=true; btn.textContent='⏳...'; }
  try {
    const user = await apiFetch('/api/login','POST',{username,password});
    if (user.isAdmin) { msg.textContent='❌ Admin uchun "Admin" tabini bosing'; msg.className='form-msg error'; return; }
    msg.textContent='✅ Muvaffaqiyatli!'; msg.className='form-msg success';
    STATE.user=user; saveSession(); setTimeout(()=>enterApp(),500);
  } catch(e) { msg.textContent='❌ '+e.message; msg.className='form-msg error';
  } finally { if(btn){btn.disabled=false;btn.textContent='Kirish';} }
}

async function doAdminLogin() {
  const username = (document.getElementById('adminUsername').value || '').trim();
  const password = document.getElementById('adminPassword').value || '';
  const msg = document.getElementById('adminLoginMsg');
  msg.textContent=''; msg.className='form-msg';
  if (!username || !password) { msg.textContent='Username va parolni kiriting'; msg.className='form-msg error'; return; }
  const btn = document.querySelector('#adminLoginPanel .btn-primary');
  if (btn) { btn.disabled=true; btn.textContent='⏳...'; }
  try {
    const user = await apiFetch('/api/login','POST',{username,password});
    if (!user.isAdmin) { msg.textContent='❌ Siz admin emassiz'; msg.className='form-msg error'; return; }
    msg.textContent='✅ Admin sifatida kirdingiz!'; msg.className='form-msg success';
    STATE.user=user; saveSession(); setTimeout(()=>enterApp(),500);
  } catch(e) { msg.textContent='❌ '+e.message; msg.className='form-msg error';
  } finally { if(btn){btn.disabled=false;btn.textContent='Admin sifatida kirish';} }
}

async function doSendCode() {
  const data = {
    name: (document.getElementById('regName').value||'').trim(),
    last_name: (document.getElementById('regLastName').value||'').trim(),
    username: (document.getElementById('regUsername').value||'').trim(),
    tel: (document.getElementById('regTel').value||'').trim(),
    email: (document.getElementById('regEmail').value||'').trim(),
    password: document.getElementById('regPassword').value||'',
  };
  const msg = document.getElementById('regMsg');
  msg.textContent=''; msg.className='form-msg';
  if (!data.name||!data.last_name||!data.username||!data.email||!data.password) {
    msg.textContent='❌ Barcha maydonlarni to\'ldiring'; msg.className='form-msg error'; return;
  }
  const btn = document.getElementById('sendCodeBtn');
  if (btn) { btn.disabled=true; btn.textContent='⏳ Yuborilmoqda...'; }
  try {
    const res = await apiFetch('/api/register/send-code','POST',data);
    msg.textContent='✅ '+(res.message||'Kod yuborildi!'); msg.className='form-msg success';
    document.getElementById('regStep1').classList.add('hidden');
    document.getElementById('regStep2').classList.remove('hidden');
    if (res.code) {
      setTimeout(()=>{
        const ci=document.getElementById('verifyCode');
        if(ci) ci.value=res.code;
        showToast('📧 Tasdiqlash kodi: '+res.code,'success');
      },600);
    }
  } catch(e) {
    msg.textContent='❌ '+e.message; msg.className='form-msg error';
    if(btn){btn.disabled=false;btn.textContent='Kod yuborish';}
  }
}

async function doVerify() {
  const email = (document.getElementById('regEmail').value||'').trim();
  const code = (document.getElementById('verifyCode').value||'').trim();
  const msg = document.getElementById('verifyMsg');
  msg.textContent=''; msg.className='form-msg';
  if (!code) { msg.textContent='❌ Kodni kiriting'; msg.className='form-msg error'; return; }
  const btn = document.querySelector('#regStep2 .btn-primary');
  if (btn) { btn.disabled=true; btn.textContent='⏳...'; }
  try {
    await apiFetch('/api/register/verify','POST',{email,email_code:code});
    msg.textContent="✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!"; msg.className='form-msg success';
    showToast("✅ Ro'yxatdan o'tish muvaffaqiyatli!",'success');
    setTimeout(()=>{
      switchAuthTab('login');
      const uname=document.getElementById('regUsername').value;
      if(uname) document.getElementById('loginUsername').value=uname;
      document.getElementById('regStep1').classList.remove('hidden');
      document.getElementById('regStep2').classList.add('hidden');
      ['regName','regLastName','regUsername','regTel','regEmail','regPassword'].forEach(id=>{
        const el=document.getElementById(id); if(el) el.value='';
      });
      document.getElementById('verifyCode').value='';
    },1500);
  } catch(e) {
    msg.textContent='❌ '+e.message; msg.className='form-msg error';
  } finally { if(btn){btn.disabled=false;btn.textContent='Tasdiqlash';} }
}

async function enterApp() {
  document.getElementById('authScreen').classList.add('hidden');
  document.getElementById('mainApp').classList.remove('hidden');
  const el1=document.getElementById('userName'); if(el1) el1.textContent=STATE.user.username;
  const el2=document.getElementById('userAvatar'); if(el2) el2.textContent=(STATE.user.name||'U').charAt(0).toUpperCase();
  const adminNav=document.getElementById('adminNav');
  if(adminNav) adminNav.style.display=STATE.user.isAdmin?'block':'none';
  await refreshAll();
  showPage('home');
}

async function doLogout() {
  try {
    await apiFetch('/api/logout','POST',{
      user_id:STATE.user.id,username:STATE.user.username,
      name:STATE.user.name,last_name:STATE.user.last_name
    });
  } catch(e){}
  clearSession();
  STATE.user=null; STATE.products=[]; STATE.cart=[];
  STATE.likes=[]; STATE.myLikeIds=[]; STATE.pageHistory=[];
  document.getElementById('mainApp').classList.add('hidden');
  document.getElementById('authScreen').classList.remove('hidden');
  const adminNav=document.getElementById('adminNav');
  if(adminNav) adminNav.style.display='none';
  ['loginUsername','loginPassword','adminUsername','adminPassword'].forEach(id=>{
    const el=document.getElementById(id); if(el) el.value='';
  });
  ['loginMsg','adminLoginMsg'].forEach(id=>{
    const el=document.getElementById(id); if(el){el.textContent='';el.className='form-msg';}
  });
  switchAuthTab('login');
}

document.addEventListener('keydown',function(e){
  if(e.key!=='Enter') return;
  const ap=document.querySelector('.auth-panel:not(.hidden)');
  if(!ap) return;
  if(ap.id==='loginPanel') doLogin();
  else if(ap.id==='adminLoginPanel') doAdminLogin();
});

document.addEventListener('DOMContentLoaded', async function () {
  if (!restoreSession()) return;
  try {
    await enterApp();
  } catch (_) {
    clearSession();
    STATE.user = null;
  }
});
