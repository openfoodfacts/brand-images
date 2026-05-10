# NSI Brand Match Viewer

Interactive table of all NSI brands, with matched logo images.

<div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
  <input id="search" type="text" placeholder="Filter…" style="padding:.4rem .7rem;font-size:.95rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:4px;max-width:150px">
  <select id="category-filter" style="padding:.4rem .7rem;font-size:.95rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:4px">
    <option value="">All categories</option>
    <option value="alcohol">alcohol</option>
    <option value="bakery">bakery</option>
    <option value="bar">bar</option>
    <option value="bbq">bbq</option>
    <option value="beverages">beverages</option>
    <option value="books">books</option>
    <option value="butcher">butcher</option>
    <option value="cafe">cafe</option>
    <option value="casino">casino</option>
    <option value="cheese">cheese</option>
    <option value="chemist">chemist</option>
    <option value="chocolate">chocolate</option>
    <option value="cinema">cinema</option>
    <option value="clothes">clothes</option>
    <option value="coffee">coffee</option>
    <option value="confectionery">confectionery</option>
    <option value="convenience">convenience</option>
    <option value="cosmetics">cosmetics</option>
    <option value="country_store">country_store</option>
    <option value="craft">craft</option>
    <option value="dairy">dairy</option>
    <option value="deli">deli</option>
    <option value="doityourself">doityourself</option>
    <option value="fast_food">fast_food</option>
    <option value="fishing">fishing</option>
    <option value="florist">florist</option>
    <option value="food_sharing">food_sharing</option>
    <option value="frozen_food">frozen_food</option>
    <option value="furniture">furniture</option>
    <option value="games">games</option>
    <option value="garden_centre">garden_centre</option>
    <option value="general">general</option>
    <option value="gift">gift</option>
    <option value="greengrocer">greengrocer</option>
    <option value="hardware">hardware</option>
    <option value="health_food">health_food</option>
    <option value="herbalist">herbalist</option>
    <option value="hifi">hifi</option>
    <option value="houseware">houseware</option>
    <option value="ice_cream">ice_cream</option>
    <option value="kitchen">kitchen</option>
    <option value="lighting">lighting</option>
    <option value="medical_supply">medical_supply</option>
    <option value="mobile_phone">mobile_phone</option>
    <option value="music">music</option>
    <option value="nutrition_supplements">nutrition_supplements</option>
    <option value="nuts">nuts</option>
    <option value="outdoor">outdoor</option>
    <option value="party">party</option>
    <option value="pastry">pastry</option>
    <option value="perfumery">perfumery</option>
    <option value="pet">pet</option>
    <option value="pharmacy">pharmacy</option>
    <option value="pub">pub</option>
    <option value="restaurant">restaurant</option>
    <option value="seafood">seafood</option>
    <option value="second_hand">second_hand</option>
    <option value="shoes">shoes</option>
    <option value="spices">spices</option>
    <option value="sports">sports</option>
    <option value="supermarket">supermarket</option>
    <option value="tea">tea</option>
    <option value="tobacco">tobacco</option>
    <option value="trade">trade</option>
    <option value="variety_store">variety_store</option>
    <option value="video_games">video_games</option>
    <option value="wholesale">wholesale</option>
    <option value="wine">wine</option>
  </select>
  <select id="status-filter" style="padding:.4rem .7rem;font-size:.95rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:4px">
    <option value="">All statuses</option>
    <option value="both">Both (SVG + PNG)</option>
    <option value="only_svg">SVG only</option>
    <option value="only_png">PNG only</option>
    <option value="no">No match</option>
  </select>
</div>

<div>
  <span id="count" style="font-size:.85rem;color:var(--md-default-fg-color--light)"></span>
</div>

<div id="table-wrap" style="overflow-x:auto">
  <table id="brand-table" style="width:100%;border-collapse:collapse;font-size:.9rem">
    <thead>
      <tr>
        <th style="text-align:left;padding:.5rem .7rem;border-bottom:2px solid var(--md-default-fg-color--lightest)">Brand</th>
        <th style="text-align:left;padding:.5rem .7rem;border-bottom:2px solid var(--md-default-fg-color--lightest)">Category</th>
        <th style="text-align:center;padding:.5rem .7rem;border-bottom:2px solid var(--md-default-fg-color--lightest)">Status</th>
        <th style="text-align:center;padding:.5rem .7rem;border-bottom:2px solid var(--md-default-fg-color--lightest)">SVG</th>
        <th style="text-align:center;padding:.5rem .7rem;border-bottom:2px solid var(--md-default-fg-color--lightest)">PNG</th>
      </tr>
    </thead>
    <tbody id="table-body">
      <tr><td colspan="5" style="padding:1rem;text-align:center">Loading...</td></tr>
    </tbody>
  </table>
</div>

<script>
(function () {
  const configuredBase = (window.BRAND_MATCH_LOGO_BASE || '../../xx/stores/').trim();
  const LOGO_BASE = new URL(configuredBase, window.location.href).toString();
  const CSV_URL = new URL('../brand-match.csv', window.location.href).toString();
  const STATUS_COLOR = {
    both: '#2e7d32',
    only_svg: '#1565c0',
    only_png: '#ef6c00',
    no: '#b71c1c'
  };
  const STATUS_BG = {
    both: '#e8f5e9',
    only_svg: '#e3f2fd',
    only_png: '#fff3e0',
    no: '#ffebee'
  };

  let allRows = [];

  function parseCSV(text) {
    const lines = text.trim().split(/\r?\n/);
    const headers = lines[0].split(',').map(h => h.trim().replace(/^\uFEFF/, ''));
    return lines.slice(1).map(line => {
      const vals = line.split(',').map(v => v.trim());
      return Object.fromEntries(headers.map((h, i) => [h, vals[i] || '']));
    });
  }

  function safe(value) {
    return value || '';
  }

  function imgCell(filename) {
    if (!filename) return '<td style="text-align:center;padding:.3rem .7rem">-</td>';
    const encoded = encodeURIComponent(filename);
    const logoUrl = LOGO_BASE + encoded;
    return `<td style="text-align:center;padding:.3rem .7rem">
      <a href="${logoUrl}" target="_blank" title="${filename}">
        <span style="width:50px;height:50px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--md-default-fg-color--lightest);border-radius:4px;background:var(--md-default-bg-color)">
          <img src="${logoUrl}" alt="${filename}" style="width:50px;height:50px;object-fit:contain" loading="lazy">
        </span>
      </a>
    </td>`;
  }

  function statusBadge(status) {
    const color = STATUS_COLOR[status] || '#555';
    const bg = STATUS_BG[status] || '#eee';
    return `<span style="background:${bg};color:${color};border-radius:3px;padding:.15rem .45rem;font-size:.8rem;font-weight:600">${status}</span>`;
  }

  function render(rows) {
    const tbody = document.getElementById('table-body');
    document.getElementById('count').textContent = `${rows.length} brands`;
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="5" style="padding:1rem;text-align:center">No results.</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map((r, i) => {
      const bg = i % 2 === 0 ? '' : 'background:var(--md-code-bg-color)';
      const brand = safe(r.tags_brand) || safe(r.display_name);
      return `<tr style="${bg}">
        <td style="padding:.4rem .7rem">${brand}</td>
        <td style="padding:.4rem .7rem">${safe(r.source_category)}</td>
        <td style="text-align:center;padding:.4rem .7rem">${statusBadge(safe(r.match_status))}</td>
        ${imgCell(safe(r.matched_image_svg))}
        ${imgCell(safe(r.matched_image_png))}
      </tr>`;
    }).join('');
  }

  function applyFilters() {
    const q = document.getElementById('search').value.toLowerCase();
    const status = document.getElementById('status-filter').value;
    const category = document.getElementById('category-filter').value;

    const filtered = allRows.filter(r => {
      const brand = safe(r.tags_brand) || safe(r.display_name);
      return (
        (!q || brand.toLowerCase().includes(q) || safe(r.nsi_id).toLowerCase().includes(q)) &&
        (!status || safe(r.match_status) === status) &&
        (!category || safe(r.source_category) === category)
      );
    });

    render(filtered);
  }

  fetch(CSV_URL)
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.text();
    })
    .then(text => {
      allRows = parseCSV(text);
      applyFilters();
      document.getElementById('search').addEventListener('input', applyFilters);
      document.getElementById('status-filter').addEventListener('change', applyFilters);
      document.getElementById('category-filter').addEventListener('change', applyFilters);
    })
    .catch(() => {
      document.getElementById('table-body').innerHTML =
        '<tr><td colspan="5" style="padding:1rem;text-align:center;color:red">Failed to load CSV.</td></tr>';
    });
})();
</script>
