/* Dynamic Product Properties widget for Django admin.
 *
 * Workflow:
 *   1. On page load, fetch the global CatalogProperty list from the API.
 *   2. Render any pre-existing product_properties as labelled rows with
 *      native <datalist> autocomplete seeded from the global values.
 *   3. "＋ Add Property" opens a picker that shows:
 *        a) A dropdown of existing global properties (if any are not yet added).
 *        b) A text input + "Add" button to create a brand-new property name.
 *   4. The hidden textarea stays in sync so the normal Django form submit
 *      carries the JSON without any extra API calls.
 *   5. New property names / values are persisted server-side in
 *      ProductAdmin.save_model() via CatalogProperty.objects.get_or_create().
 */

'use strict';

(function () {
  var API_URL = '/api/v1/catalog/properties/';
  var globalProperties = []; // [{id, property_name, property_values:[...]}]

  /* ── Bootstrap ──────────────────────────────────────────────────── */

  function init() {
    var textarea = document.getElementById('id_product_properties');
    if (!textarea) return;
    fetchProperties().then(function () { renderWidget(textarea); });
  }

  function fetchProperties() {
    return fetch(API_URL)
      .then(function (res) { return res.ok ? res.json() : []; })
      .then(function (data) {
        globalProperties = Array.isArray(data) ? data : (data.results || []);
      })
      .catch(function () { globalProperties = []; });
  }

  /* ── Widget render ───────────────────────────────────────────────── */

  function renderWidget(textarea) {
    var current = {};
    try { current = JSON.parse(textarea.value || '{}'); } catch (e) {}

    textarea.style.display = 'none';

    var container = document.createElement('div');
    container.className = 'dpw-container';

    var rows = document.createElement('div');
    rows.id = 'dpw-rows';
    container.appendChild(rows);

    // Render pre-existing property rows
    Object.keys(current).forEach(function (name) {
      rows.appendChild(createRow(name, String(current[name]), textarea));
    });

    var addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'dpw-add-btn';
    addBtn.textContent = '＋ Add Property';
    addBtn.addEventListener('click', function () {
      showPicker(rows, textarea, container, addBtn);
    });
    container.appendChild(addBtn);

    textarea.parentNode.insertBefore(container, textarea);
  }

  /* ── Property row ────────────────────────────────────────────────── */

  function createRow(propName, propValue, textarea) {
    var propDef = findProp(propName) || { property_values: [] };
    // Use a timestamp suffix so rows added quickly get unique datalist ids
    var listId = 'dpw-list-' + propName.replace(/\W/g, '_') + '-' + Date.now();

    var row = document.createElement('div');
    row.className = 'dpw-row';
    row.dataset.prop = propName;

    var label = document.createElement('label');
    label.className = 'dpw-label';
    label.textContent = propName;

    var input = document.createElement('input');
    input.type = 'text';
    input.className = 'dpw-input';
    input.value = propValue;
    input.setAttribute('list', listId);
    input.setAttribute('placeholder', 'Type or pick a value…');
    input.addEventListener('input', function () { syncJSON(textarea); });

    var datalist = document.createElement('datalist');
    datalist.id = listId;
    (propDef.property_values || []).forEach(function (v) {
      var opt = document.createElement('option');
      opt.value = String(v);
      datalist.appendChild(opt);
    });

    var del = document.createElement('button');
    del.type = 'button';
    del.className = 'dpw-del';
    del.title = 'Remove';
    del.innerHTML = '&times;';
    del.addEventListener('click', function () { row.remove(); syncJSON(textarea); });

    row.appendChild(label);
    row.appendChild(input);
    row.appendChild(datalist);
    row.appendChild(del);
    return row;
  }

  /* ── Picker ──────────────────────────────────────────────────────── */

  function showPicker(rowsEl, textarea, container, addBtn) {
    if (document.getElementById('dpw-picker')) return;

    var usedNames = new Set(
      Array.from(rowsEl.querySelectorAll('.dpw-row')).map(function (r) {
        return r.dataset.prop;
      })
    );
    var available = globalProperties.filter(function (p) {
      return !usedNames.has(p.property_name);
    });

    var picker = document.createElement('div');
    picker.id = 'dpw-picker';
    picker.className = 'dpw-picker';

    /* ── Section A: existing global properties ─────────────────────── */
    if (available.length > 0) {
      var existingSection = document.createElement('div');
      existingSection.className = 'dpw-section';

      var existingHeading = document.createElement('div');
      existingHeading.className = 'dpw-section-heading';
      existingHeading.textContent = 'Existing properties';

      var sel = document.createElement('select');
      sel.className = 'dpw-picker-select';

      var ph = document.createElement('option');
      ph.value = '';
      ph.textContent = '— Choose a property —';
      sel.appendChild(ph);

      available.forEach(function (p) {
        var opt = document.createElement('option');
        opt.value = p.property_name;
        opt.textContent = p.property_name;
        sel.appendChild(opt);
      });

      sel.addEventListener('change', function () {
        if (!sel.value) return;
        rowsEl.appendChild(createRow(sel.value, '', textarea));
        syncJSON(textarea);
        picker.remove();
      });

      existingSection.appendChild(existingHeading);
      existingSection.appendChild(sel);
      picker.appendChild(existingSection);

      // Divider
      var divider = document.createElement('div');
      divider.className = 'dpw-divider';
      divider.innerHTML = '<span>or create a new property</span>';
      picker.appendChild(divider);
    }

    /* ── Section B: create brand-new property ──────────────────────── */
    var newSection = document.createElement('div');
    newSection.className = 'dpw-section dpw-new-section';

    if (available.length === 0) {
      var newHeading = document.createElement('div');
      newHeading.className = 'dpw-section-heading';
      newHeading.textContent = 'New property name';
      newSection.appendChild(newHeading);
    }

    var newRow = document.createElement('div');
    newRow.className = 'dpw-new-row';

    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.className = 'dpw-new-input';
    newInput.placeholder = 'Property name, e.g. Material';

    var addNewBtn = document.createElement('button');
    addNewBtn.type = 'button';
    addNewBtn.className = 'dpw-add-new-btn';
    addNewBtn.textContent = 'Add';

    var errorMsg = document.createElement('span');
    errorMsg.className = 'dpw-error';

    function confirmNew() {
      var name = newInput.value.trim();
      errorMsg.textContent = '';
      newInput.classList.remove('dpw-input-error');

      if (!name) {
        newInput.focus();
        errorMsg.textContent = 'Please enter a property name.';
        return;
      }
      if (usedNames.has(name)) {
        newInput.classList.add('dpw-input-error');
        errorMsg.textContent = '"' + name + '" is already added to this product.';
        return;
      }
      // Allow even if it doesn't exist in globalProperties yet —
      // save_model() will create it via get_or_create on the server.
      rowsEl.appendChild(createRow(name, '', textarea));
      syncJSON(textarea);
      picker.remove();
    }

    addNewBtn.addEventListener('click', confirmNew);
    newInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); confirmNew(); }
    });

    newRow.appendChild(newInput);
    newRow.appendChild(addNewBtn);
    newSection.appendChild(newRow);
    newSection.appendChild(errorMsg);
    picker.appendChild(newSection);

    /* ── Cancel ────────────────────────────────────────────────────── */
    var cancelRow = document.createElement('div');
    cancelRow.className = 'dpw-cancel-row';
    var cancel = document.createElement('button');
    cancel.type = 'button';
    cancel.className = 'dpw-cancel';
    cancel.textContent = 'Cancel';
    cancel.addEventListener('click', function () { picker.remove(); });
    cancelRow.appendChild(cancel);
    picker.appendChild(cancelRow);

    container.insertBefore(picker, addBtn);

    // Auto-focus the right input
    if (available.length === 0) {
      newInput.focus();
    }
  }

  /* ── JSON sync ───────────────────────────────────────────────────── */

  function syncJSON(textarea) {
    var props = {};
    document.querySelectorAll('#dpw-rows .dpw-row').forEach(function (row) {
      var name = row.dataset.prop;
      var input = row.querySelector('.dpw-input');
      if (name && input && input.value.trim()) {
        props[name] = input.value.trim();
      }
    });
    textarea.value = JSON.stringify(props);
  }

  /* ── Helper ──────────────────────────────────────────────────────── */

  function findProp(name) {
    return globalProperties.find(function (p) { return p.property_name === name; }) || null;
  }

  /* ── Entry point ─────────────────────────────────────────────────── */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
