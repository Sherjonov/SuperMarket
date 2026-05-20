/** Klient tomonda tekshiruv (server ham qayta tekshiradi). Pul yechilmaydi. */

function digitsOnly(s) {
  return (s || '').replace(/\D/g, '');
}

function luhnValid(cardNumber) {
  const digits = digitsOnly(cardNumber).split('').map(Number);
  if (digits.length < 13) return false;
  let s = 0;
  let alt = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = digits[i];
    if (alt) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    s += d;
    alt = !alt;
  }
  return s % 10 === 0;
}

function cardBrandAllowed(cardNumber) {
  const d = digitsOnly(cardNumber);
  if (d.length < 6) return false;
  if (d.startsWith('4')) return true;
  const p2 = parseInt(d.slice(0, 2), 10);
  if (p2 >= 51 && p2 <= 55) return true;
  const p4 = parseInt(d.slice(0, 4), 10);
  if (p4 >= 2221 && p4 <= 2720) return true;
  if (d.startsWith('62')) return true;
  if (d.startsWith('9860') || d.startsWith('8600')) return true;
  return false;
}

function expiryValid(mmYy) {
  const m = String(mmYy || '').trim().match(/^(\d{2})\/(\d{2})$/);
  if (!m) return false;
  const month = parseInt(m[1], 10);
  const year = 2000 + parseInt(m[2], 10);
  if (month < 1 || month > 12) return false;
  const now = new Date();
  const exp = new Date(year, month - 1, 1);
  const cur = new Date(now.getFullYear(), now.getMonth(), 1);
  return exp >= cur;
}

function uzPassportOk(val) {
  const v = String(val || '').trim().toUpperCase().replace(/\s/g, '');
  return /^[A-Z]{2}\d{7}$/.test(v);
}

function uzIdCardOk(val) {
  const v = String(val || '').trim().toUpperCase().replace(/\s/g, '');
  if (/^[A-Z]{2}\d{7}$/.test(v)) return true;
  return /^\d{9}$/.test(v);
}

function validateCheckoutCard() {
  const cn = digitsOnly(document.getElementById('cardNumber')?.value || '');
  const ce = document.getElementById('cardExpiry')?.value || '';
  const cv = document.getElementById('cardCvv')?.value || '';
  if (cn.length < 13 || !luhnValid(cn)) return { ok: false, msg: 'Karta raqami haqiqiy emas' };
  if (!cardBrandAllowed(cn)) return { ok: false, msg: 'Karta turi qo‘llab-quvvatlanmaydi' };
  if (!expiryValid(ce)) return { ok: false, msg: 'Muddat noto‘g‘ri yoki o‘tgan' };
  if (![3, 4].includes(cv.length)) return { ok: false, msg: 'CVV noto‘g‘ri' };
  return { ok: true };
}

function validateCheckoutIdentity(docType, passportVal) {
  if (docType === 'passport_uz') {
    return uzPassportOk(passportVal)
      ? { ok: true }
      : { ok: false, msg: 'Pasport: AA1234567 formatida kiriting' };
  }
  if (docType === 'id_card_uz') {
    return uzIdCardOk(passportVal)
      ? { ok: true }
      : { ok: false, msg: 'ID karta raqami noto‘g‘ri' };
  }
  return { ok: false, msg: 'Hujjat turini tanlang' };
}
