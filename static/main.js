let cartCount = 0;

function addToCart(productName) {
    cartCount++;

    const badge = document.getElementById('cart-count');
    if (badge) {
        badge.textContent = cartCount;
    }

    alert(productName + ' has been added to your cart!');
}
