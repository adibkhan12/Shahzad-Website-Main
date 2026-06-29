/* Color-Variants admin widget for Django admin (django-unfold compatible).
 *
 * What it does
 * ────────────
 * 1. Reads the "Enable color variants" checkbox (id_has_color_variants).
 * 2. When OFF  → hides the Color Variants inline + "Is price same?" row +
 *                the Color column in the Images inline.
 * 3. When ON   → shows all of the above.
 * 4. "Is price same?" (id_is_price_same)
 *      ON  → hides the Price column in the Color Variants inline.
 *      OFF → shows it so each row can have its own price.
 * 5. A MutationObserver watches both inlines so newly added rows (via
 *    Django's "Add another" link) automatically get the correct visibility.
 */

'use strict';

(function () {

  /* ── Entry point ─────────────────────────────────────────────────── */

  function init() {
    var hasVariants = document.getElementById('id_has_color_variants');
    if (!hasVariants) return;

    var isPriceSame = document.getElementById('id_is_price_same');

    // Apply the initial saved state immediately.
    applyAll(hasVariants.checked, isPriceSame ? isPriceSame.checked : true);

    // React to checkbox changes.
    hasVariants.addEventListener('change', function () {
      applyAll(hasVariants.checked, isPriceSame ? isPriceSame.checked : true);
    });

    if (isPriceSame) {
      isPriceSame.addEventListener('change', function () {
        if (hasVariants.checked) applyPriceSame(isPriceSame.checked);
      });
    }

    // Re-apply visibility whenever Django adds new inline rows.
    watchInlineChanges(hasVariants, isPriceSame);
  }

  /* ── Master toggle ───────────────────────────────────────────────── */

  function applyAll(variantsOn, priceSameOn) {
    var variantGroup = getVariantGroup();
    var priceSameRow = getPriceSameRow();

    // Show / hide the whole Color Variants inline.
    if (variantGroup) variantGroup.style.display = variantsOn ? '' : 'none';

    // Show / hide the "Is price same?" field row.
    if (priceSameRow) priceSameRow.style.display = variantsOn ? '' : 'none';

    // Show / hide the "Color variant" column in the Images inline.
    eachColorVariantCol(function (el) {
      el.style.display = variantsOn ? '' : 'none';
    });

    // Show / hide the Price column inside the Color Variants inline.
    if (variantsOn) applyPriceSame(priceSameOn);
  }

  function applyPriceSame(priceSameOn) {
    eachPriceCol(function (el) {
      // Price column visible only when "Is price same?" is OFF.
      el.style.display = priceSameOn ? 'none' : '';
    });
  }

  /* ── Column helpers ──────────────────────────────────────────────── */

  function eachColorVariantCol(fn) {
    document.querySelectorAll(
      '.column-color_variant, .field-color_variant'
    ).forEach(fn);
  }

  function eachPriceCol(fn) {
    var group = getVariantGroup();
    if (!group) return;
    group.querySelectorAll('.column-price, .field-price').forEach(fn);
  }

  /* ── DOM finders ─────────────────────────────────────────────────── */

  function getVariantGroup() {
    // Django generates the inline group id from the related_name on the FK.
    // ColorVariant.product FK has related_name='color_variants_data'
    // → prefix: color_variants_data → group id: color_variants_data-group
    return (
      document.getElementById('color_variants_data-group') ||
      document.getElementById('colorvariant_set-group') ||
      findGroupByHeading('color variant')
    );
  }

  function getImageGroup() {
    // ProductImage.product FK has related_name='uploaded_images'
    return (
      document.getElementById('uploaded_images-group') ||
      document.getElementById('productimage_set-group') ||
      findGroupByHeading('product image')
    );
  }

  function getPriceSameRow() {
    var el = document.getElementById('id_is_price_same');
    if (!el) return null;
    // Walk up until we hit a Django form-row wrapper.
    var node = el;
    for (var i = 0; i < 6; i++) {
      node = node.parentElement;
      if (!node) break;
      var cls = node.className || '';
      if (
        cls.includes('form-row') ||
        cls.includes('field-box') ||
        node.tagName === 'P'
      ) return node;
    }
    return el.parentElement;
  }

  function findGroupByHeading(text) {
    var headings = document.querySelectorAll('h2, caption, .tabular h2');
    for (var i = 0; i < headings.length; i++) {
      if (headings[i].textContent.trim().toLowerCase().includes(text)) {
        var node = headings[i];
        for (var j = 0; j < 10; j++) {
          node = node.parentElement;
          if (!node) break;
          if (
            node.classList.contains('inline-group') ||
            (node.id && node.id.endsWith('-group'))
          ) return node;
        }
      }
    }
    return null;
  }

  /* ── MutationObserver — keep new rows in sync ────────────────────── */

  function watchInlineChanges(hasVariantsEl, isPriceSameEl) {
    var targets = [getVariantGroup(), getImageGroup()];

    targets.forEach(function (target) {
      if (!target) return;

      var obs = new MutationObserver(function () {
        if (!hasVariantsEl.checked) return;
        // Re-apply column visibility for any newly added rows.
        eachColorVariantCol(function (el) { el.style.display = ''; });
        var priceSame = isPriceSameEl ? isPriceSameEl.checked : true;
        applyPriceSame(priceSame);
      });

      obs.observe(target, { childList: true, subtree: true });
    });
  }

  /* ── Boot ────────────────────────────────────────────────────────── */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
