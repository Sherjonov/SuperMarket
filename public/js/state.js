/* SuperMarket - Global holat boshqaruvi */
const STATE = {
  user: null,
  products: [],
  cart: [],
  likes: [],
  myLikeIds: [],
  currentCategory: '',
  currentSubcategory: '',
  pageHistory: [],
  pendingCartProductId: null,
  pendingCartSize: '',
};

// Savat badge yangilash
function updateCartBadge() {
  const count = STATE.cart.reduce((s, i) => s + i.quantity, 0);
  const badge = document.getElementById('cartBadge');
  if (badge) {
    badge.textContent = count;
    badge.classList.toggle('hidden', count === 0);
  }
}

// Like badge yangilash
function updateLikesBadge() {
  const count = STATE.myLikeIds.length;
  const badge = document.getElementById('likesBadge');
  if (badge) {
    badge.textContent = count;
    badge.classList.toggle('hidden', count === 0);
  }
}
