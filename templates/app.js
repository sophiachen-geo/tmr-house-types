/* Québec Residential Typologies — vanilla JS: smooth anchors, matrix sort, compare page. */
(function () {
  "use strict";
  var R = document.documentElement.getAttribute("data-root") || "";

  /* smooth in-page anchors (same behaviour as the original TMR page) */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var t = document.getElementById(a.getAttribute("href").slice(1));
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: "smooth", block: "start" }); history.replaceState(null, "", "#" + t.id); }
    });
  });

  /* matrix: toggle row order between decade and name */
  var mxBtn = document.getElementById("mx-sort");
  if (mxBtn) {
    mxBtn.addEventListener("click", function () {
      var tbody = document.querySelector("#mx-table tbody");
      var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr"));
      var byName = mxBtn.dataset.mode === "decade"; // switch to the other mode
      rows.sort(function (a, b) {
        return byName
          ? a.dataset.name.localeCompare(b.dataset.name)
          : (+a.dataset.decade - +b.dataset.decade);
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
      mxBtn.dataset.mode = byName ? "name" : "decade";
      mxBtn.textContent = byName ? "Sorted by name — click to sort by decade" : "Sorted by decade — click to sort by name";
    });
  }

  /* compare page */
  var mount = document.getElementById("cmp-mount");
  if (!mount) return;
  var picker = document.getElementById("cmp-picker");
  var search = document.getElementById("cmp-search");
  var results = document.getElementById("cmp-results");
  var status = document.getElementById("cmp-status");
  var MAX = 4, types = [], byId = {};

  var FIELDS = [
    ["Tenure / plan", function (t) { return txt(t.tenure_plan); }],
    ["Storeys", function (t) { return txt(t.storeys); }],
    ["Roof", function (t) { return txt(t.roof && t.roof.form); }],
    ["Roof pitch", function (t) { return t.roof && t.roof.pitch_deg !== null && t.roof.pitch_deg !== undefined ? t.roof.pitch_deg + "°" : "–"; }],
    ["Window proportion", function (t) { return txt(t.window_proportion); }],
    ["Cladding", function (t) { return list(t.principal_cladding); }],
    ["Roofing", function (t) { return txt(t.roofing); }],
    ["Garage", function (t) { return txt(t.garage); }],
    ["Lot width", function (t) { return t.lot_width_m ? t.lot_width_m[0] + "–" + t.lot_width_m[1] + " m" : "–"; }],
    ["Front setback", function (t) { return num(t.setback_front_m, " m"); }],
    ["Side setback", function (t) { return num(t.setback_side_m, " m"); }],
    ["Front yard green", function (t) { return num(t.front_yard_green_pct, " %"); }]
  ];
  var PROFILE = [
    ["siting_landscape", "Siting & landscape"],
    ["massing", "Massing"],
    ["articulation", "Articulation"],
    ["openings", "Openings"],
    ["materials", "Materials"]
  ];
  function txt(v) { return v === null || v === undefined || v === "" ? "–" : String(v); }
  function num(v, suffix) { return v === null || v === undefined ? "–" : v + suffix; }
  function list(v) { return v && v.length ? v.join(", ") : "–"; }
  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { if (k === "text") n.textContent = attrs[k]; else n.setAttribute(k, attrs[k]); });
    (children || []).forEach(function (c) { n.appendChild(c); });
    return n;
  }
  function ids() {
    var q = new URLSearchParams(location.search).get("ids");
    return q ? q.split(",").map(function (s) { return s.trim(); }).filter(function (s) { return byId[s]; }).slice(0, MAX) : [];
  }
  function setIds(list) {
    var q = list.length ? "?ids=" + list.join(",") : location.pathname;
    history.replaceState(null, "", list.length ? q : q);
    render();
  }
  function render() {
    var sel = ids();
    mount.textContent = "";
    status.textContent = sel.length
      ? (sel.length < 2 ? "Add another type to compare (up to " + MAX + ")." : sel.length + " of " + MAX + " selected.")
      : "Nothing selected yet — add 2–4 types.";
    if (!sel.length) return;
    var table = el("table", { "class": "members" });
    var thead = el("thead"), hrow = el("tr", null, [el("th", { text: "" })]);
    sel.forEach(function (id) {
      var t = byId[id];
      var th = el("th");
      var name = el("div", { "class": "cmp-name", text: t.name_en });
      name.appendChild(el("span", { "class": "fr", text: t.name_fr }));
      var meta = el("div", { "class": "decade", text: t.place_name + " · " + t.phase_label + " · " + t.phase_years });
      var rm = el("button", { "class": "rm", type: "button", text: "remove" });
      rm.addEventListener("click", function () { setIds(ids().filter(function (x) { return x !== id; })); });
      th.appendChild(name); th.appendChild(meta); th.appendChild(rm);
      hrow.appendChild(th);
    });
    thead.appendChild(hrow); table.appendChild(thead);
    var tbody = el("tbody");
    /* photo row */
    var prow = el("tr", null, [el("th", { text: "Photo" })]);
    sel.forEach(function (id) {
      var t = byId[id], td = el("td");
      if (t.photo) { var img = el("img", { src: R + t.photo.file, alt: t.photo.alt || t.name_en, loading: "lazy" }); td.appendChild(img); }
      else td.textContent = "–";
      prow.appendChild(td);
    });
    tbody.appendChild(prow);
    FIELDS.forEach(function (f) {
      var row = el("tr", null, [el("th", { text: f[0] })]);
      sel.forEach(function (id) { row.appendChild(el("td", { text: f[1](byId[id]) })); });
      tbody.appendChild(row);
    });
    PROFILE.forEach(function (p) {
      var row = el("tr", null, [el("th", { text: p[1] })]);
      sel.forEach(function (id) {
        var td = el("td"), items = (byId[id].profile || {})[p[0]] || [];
        if (items.length) { var ul = el("ul"); items.forEach(function (it) { ul.appendChild(el("li", { text: it })); }); td.appendChild(ul); }
        else td.textContent = "–";
        row.appendChild(td);
      });
      tbody.appendChild(row);
    });
    var srow = el("tr", null, [el("th", { text: "Styles" })]);
    sel.forEach(function (id) { srow.appendChild(el("td", { text: (byId[id].style_names || []).join(" · ") || "–" })); });
    tbody.appendChild(srow);
    table.appendChild(tbody);
    mount.appendChild(table);
  }
  function showResults(q) {
    results.textContent = "";
    var sel = ids();
    var hits = types.filter(function (t) {
      if (sel.indexOf(t.id) !== -1) return false;
      var hay = (t.name_en + " " + t.name_fr + " " + t.place_name).toLowerCase();
      return !q || hay.indexOf(q) !== -1;
    }).slice(0, 12);
    hits.forEach(function (t) {
      var li = el("li", null, []);
      li.appendChild(document.createTextNode(t.name_en));
      li.appendChild(el("span", { "class": "pl", text: t.place_name }));
      li.addEventListener("click", function () {
        var s = ids();
        if (s.length < MAX) { s.push(t.id); setIds(s); }
        search.value = ""; results.classList.remove("open");
      });
      results.appendChild(li);
    });
    results.classList.toggle("open", hits.length > 0);
  }
  fetch(R + "data.json").then(function (r) {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  }).then(function (data) {
    types = data.types;
    types.forEach(function (t) { byId[t.id] = t; });
    picker.hidden = false;
    search.addEventListener("input", function () { showResults(search.value.trim().toLowerCase()); });
    search.addEventListener("focus", function () { showResults(search.value.trim().toLowerCase()); });
    document.addEventListener("click", function (e) { if (!picker.contains(e.target)) results.classList.remove("open"); });
    render();
  }).catch(function (err) {
    status.textContent = "Could not load data.json (" + err.message + ").";
    picker.hidden = false;
  });
})();
