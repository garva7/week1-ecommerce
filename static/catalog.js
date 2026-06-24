// catalog.js - live product search (DOM manipulation).
// Demonstrates: selecting elements, handling the "input" event, and
// altering elements' CSS/visibility with JavaScript.

document.addEventListener('DOMContentLoaded', function () {
    const search = document.getElementById('product-search');
    if (!search) return; // not on this page

    const cards = document.querySelectorAll('#product-grid .product-col');
    const noResults = document.getElementById('no-results');

    search.addEventListener('input', function () {
        const term = search.value.toLowerCase().trim();
        let visibleCount = 0;

        cards.forEach(function (col) {
            const name = col.querySelector('.card-title').textContent.toLowerCase();
            if (name.indexOf(term) !== -1) {
                col.style.display = '';      // show
                visibleCount++;
            } else {
                col.style.display = 'none';  // hide
            }
        });

        // Show the "no matches" message only when nothing is visible.
        noResults.classList.toggle('d-none', visibleCount > 0);
    });
});
