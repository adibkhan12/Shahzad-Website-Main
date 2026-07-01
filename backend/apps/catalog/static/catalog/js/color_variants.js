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

    // Pills must be set up BEFORE applyAll() so getPriceSameRow() correctly
    // targets the individual is_price_same pill instead of the whole shared row.
    setupOptionsPills();

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

    // Inject the "Save Color Variants" button.
    addSaveButton();
  }

  /* ── Options pill layout ─────────────────────────────────────────── */

  var BOOL_NAMES = ['is_active', 'is_featured', 'is_box_packed', 'has_color_variants', 'is_price_same'];

  function findPillWrapper(name) {
    var input = document.getElementById('id_' + name);
    if (!input) return null;
    var section = document.querySelector('.product-toggles');
    // IDs of the OTHER boolean inputs — used to detect "shared" wrappers.
    var otherSels = BOOL_NAMES
      .filter(function (n) { return n !== name; })
      .map(function (n) { return '#id_' + n; });

    // Walk UP from the input; stop at the smallest element that contains
    // ONLY this boolean (no other boolean inputs inside it).
    var node = input.parentElement;
    while (node && node !== section && node !== document.body) {
      var containsOther = otherSels.some(function (sel) {
        return !!node.querySelector(sel);
      });
      if (!containsOther) return node;
      node = node.parentElement;
    }
    return input.parentElement; // last-resort fallback
  }

  function setupOptionsPills() {
    var section = document.querySelector('.product-toggles');
    if (!section || section.dataset.pillsSetup) return;
    section.dataset.pillsSetup = '1';

    var flexParents = new Set();

    BOOL_NAMES.forEach(function (name) {
      var wrapper = findPillWrapper(name);
      if (!wrapper) return;

      wrapper.classList.add('cv-toggle-pill');
      if (name === 'is_price_same') wrapper.classList.add('cv-price-same-pill');

      // Remove any empty <p> help-text nodes Django may still emit.
      wrapper.querySelectorAll('p, small').forEach(function (el) {
        if (!el.querySelector('input, label, select')) el.remove();
      });

      if (wrapper.parentElement) flexParents.add(wrapper.parentElement);
    });

    // Make each container that holds pills into a horizontal flex row.
    flexParents.forEach(function (parent) {
      parent.style.cssText += 'display:flex!important;flex-wrap:wrap!important;gap:16px!important;align-items:center!important;border-bottom:none!important;padding:8px 0!important;';
    });
  }

  /* ── Save Color Variants button ──────────────────────────────────── */

  function getProductId() {
    var m = window.location.pathname.match(/\/(\d+)\/change\//);
    return m ? m[1] : null;
  }

  function addSaveButton() {
    var group = getVariantGroup();
    if (!group || group.dataset.cvSaveBtnAdded) return;
    group.dataset.cvSaveBtnAdded = '1';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'cv-save-btn';
    btn.textContent = 'Save Color Variants';
    btn.title = 'Saves new / edited color variants so the image section can reference them. Use the main Save button to delete variants.';
    btn.style.cssText = [
      'display:inline-block',
      'margin-left:14px',
      'padding:5px 16px',
      'border-radius:6px',
      'background:#4f46e5',
      'color:#fff',
      'border:none',
      'font-size:12px',
      'font-weight:600',
      'cursor:pointer',
      'vertical-align:middle',
      'transition:background 0.2s',
    ].join(';');

    btn.addEventListener('click', handleSaveClick);

    // Try multiple selectors — unfold uses tr.add-row inside tfoot,
    // stock Django admin uses p.add-row. Fall back to appending to the group.
    var anchor =
      group.querySelector('p.add-row') ||
      group.querySelector('tr.add-row td') ||
      group.querySelector('tr.add-row') ||
      group.querySelector('.add-row') ||
      group.querySelector('tfoot td') ||
      group.querySelector('tfoot tr') ||
      null;

    if (anchor) {
      anchor.appendChild(btn);
    } else {
      // Last resort: create a dedicated wrapper and append to group.
      var wrap = document.createElement('div');
      wrap.style.cssText = 'padding:8px 14px;margin-top:4px';
      wrap.appendChild(btn);
      group.appendChild(wrap);
    }
  }

  function handleSaveClick() {
    var btn = this;
    var productId = getProductId();
    if (!productId) {
      setBtnState(btn, 'error', 'Save product first');
      return;
    }

    var prefix = 'color_variants_data';
    var formData = new FormData();

    // Management form fields.
    ['TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS'].forEach(function (k) {
      var el = document.querySelector('input[name="' + prefix + '-' + k + '"]');
      if (el) formData.append(el.name, el.value);
    });

    // Collect each non-empty variant row. Skip new rows the user has already
    // marked for deletion (they were never persisted — no need to send them).
    var group = getVariantGroup();
    var rows = group
      ? group.querySelectorAll('tr.form-row:not(.empty-form), .form-row:not(.empty-form)')
      : [];

    rows.forEach(function (row) {
      var idInput     = row.querySelector('[name$="-id"]');
      var deleteInput = row.querySelector('[name$="-DELETE"]');
      var isNew       = !idInput || !idInput.value;
      var isDeleted   = deleteInput && deleteInput.checked;

      // New + deleted → skip entirely (never persisted).
      if (isNew && isDeleted) return;

      ['id', 'color_name', 'price', 'order'].forEach(function (field) {
        var el = row.querySelector('[name$="-' + field + '"]');
        if (el) formData.append(el.name, el.value);
      });

      // The product FK is resolved server-side via instance=product,
      // but send it if present to satisfy any validation.
      var productEl = row.querySelector('[name$="-product"]');
      if (productEl && productEl.value) formData.append(productEl.name, productEl.value);

      // For existing rows being deleted, DO NOT include DELETE so the
      // AJAX save skips deletion (full Save handles that). For new rows
      // (not deleted above) also skip DELETE.
      // Only include DELETE for existing rows that are marked → this lets
      // the endpoint actually remove them so dropdowns stay accurate.
      if (!isNew && isDeleted) {
        formData.append(idInput.name.replace(/-id$/, '-DELETE'), 'on');
      }
    });

    var csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfEl) formData.append('csrfmiddlewaretoken', csrfEl.value);

    setBtnState(btn, 'loading', 'Saving…');

    fetch('/admin/catalog/product/' + productId + '/save-color-variants/', {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrfEl ? csrfEl.value : '' },
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.ok) {
          setBtnState(btn, 'success', '✓ Saved');
          afterSaveSuccess(data.variants);
          setTimeout(function () { setBtnState(btn, 'idle', 'Save Color Variants'); }, 2500);
        } else {
          setBtnState(btn, 'error', 'Error — check fields');
          setTimeout(function () { setBtnState(btn, 'idle', 'Save Color Variants'); }, 3000);
        }
      })
      .catch(function () {
        setBtnState(btn, 'error', 'Network error');
        setTimeout(function () { setBtnState(btn, 'idle', 'Save Color Variants'); }, 3000);
      });
  }

  function setBtnState(btn, state, label) {
    btn.textContent = label;
    btn.disabled = (state === 'loading');
    var colors = { idle: '#4f46e5', success: '#059669', error: '#dc2626', loading: '#6366f1' };
    btn.style.background = colors[state] || colors.idle;
  }

  function afterSaveSuccess(variants) {
    var prefix = 'color_variants_data';
    var group = getVariantGroup();

    // 1. Update id hidden inputs for newly-created variants (match by color_name).
    //    Also hide rows that were marked for deletion.
    if (group) {
      var rows = group.querySelectorAll('tr.form-row:not(.empty-form), .form-row:not(.empty-form)');
      rows.forEach(function (row) {
        var deleteInput = row.querySelector('[name$="-DELETE"]');
        var idInput     = row.querySelector('[name$="-id"]');
        var colorInput  = row.querySelector('[name$="-color_name"]');

        if (deleteInput && deleteInput.checked) {
          // Row was deleted — visually hide it.
          row.style.display = 'none';
          return;
        }

        if (!colorInput || !idInput) return;
        var colorName = colorInput.value.trim();
        if (!colorName) return;

        var match = variants.find(function (v) { return v.color_name === colorName; });
        if (match) idInput.value = match.id;
      });

      // 2. Update INITIAL_FORMS to reflect how many variants now exist in DB.
      var initialFormsEl = document.querySelector('input[name="' + prefix + '-INITIAL_FORMS"]');
      if (initialFormsEl) initialFormsEl.value = variants.length;
    }

    // 3. Rebuild color_variant dropdowns in the image inline.
    updateImageDropdowns(variants);
  }

  function updateImageDropdowns(variants) {
    var optsHtml = '<option value="">---------</option>' +
      variants.map(function (v) {
        return '<option value="' + v.id + '">' + v.color_name + '</option>';
      }).join('');

    var imageGroup = getImageGroup();
    if (!imageGroup) return;

    // Update existing rows.
    imageGroup.querySelectorAll('select[name$="-color_variant"]').forEach(function (sel) {
      var current = sel.value;
      sel.innerHTML = optsHtml;
      // Restore previously selected value if it still exists.
      if (current && sel.querySelector('option[value="' + current + '"]')) {
        sel.value = current;
      }
    });

    // Also patch the empty-form template so new image rows get the right options.
    var emptyForm = imageGroup.querySelector('.empty-form');
    if (emptyForm) {
      var emptySel = emptyForm.querySelector('select[name$="-color_variant"]');
      if (emptySel) emptySel.innerHTML = optsHtml;
    }
  }

  /* ── Master toggle ───────────────────────────────────────────────── */

  function applyAll(variantsOn, priceSameOn) {
    var variantGroup = getVariantGroup();
    var priceSameRow = getPriceSameRow();

    // Show / hide the whole Color Variants inline.
    if (variantGroup) variantGroup.style.display = variantsOn ? '' : 'none';

    // Show / hide the "Is price same?" field row.
    // Use setProperty/removeProperty so the inline style can beat the CSS
    // `display: none !important` on .cv-price-same-pill.
    if (priceSameRow) {
      if (variantsOn) {
        priceSameRow.style.setProperty('display', 'inline-flex', 'important');
      } else {
        priceSameRow.style.removeProperty('display');
      }
    }

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
    // Use findPillWrapper so we always get the same individual wrapper that
    // setupOptionsPills() tagged — even if pills haven't run yet.
    return findPillWrapper('is_price_same');
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
