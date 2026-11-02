/* Demo mode for the Shammah owner panel: admin.html?demo
   Replaces the database with fictitious data kept in this browser tab only.
   Nothing is read from or written to Supabase, and nothing survives a reload. */
(function () {
  if (!/[?&]demo(=|&|$)/.test(location.search)) return;
  var SB = window.SB;
  if (!SB) return;

  var today = SB.today();
  function day(n) { return SB.addDays(today, n); }
  function iso(n) { return new Date(Date.now() + n * 864e5).toISOString(); }
  function uid(p) { return p + Math.random().toString(16).slice(2, 10) + "-0000-4000-8000-" + Math.random().toString(16).slice(2, 14).padEnd(12, "0"); }
  function code() { return "SH-" + Math.random().toString(36).slice(2, 8).toUpperCase(); }
  function clone(x) { return JSON.parse(JSON.stringify(x)); }

  var DB = {
    settings: [{ id: 1, business_name: "Shammah Moving", whatsapp: "14074856775", phone: "(407) 485-6775", email: "contact@shammahmoving.com", timezone: "America/New_York",
      booking_window_days: 90, min_notice_days: 1, max_active_per_phone: 3, auto_confirm: false, work_days: [1, 2, 3, 4, 5, 6], morning_label: "8–10 AM", afternoon_label: "1–3 PM" }],
    move_types: [
      ["house", "House move", "Mudança de casa", "full", 1], ["apt", "Apartment move", "Mudança de apartamento", "full", 1], ["office", "Office move", "Mudança comercial", "full", 2],
      ["interstate", "Interstate move", "Mudança interestadual", "full", 2], ["intl", "International move", "Mudança internacional", "full", 1], ["freight", "Freight", "Frete", "half", 1],
      ["packing", "Packing", "Embalagem", "half", 1], ["piano", "Piano move", "Transporte de piano", "half", 1], ["storage", "Storage", "Guarda-móveis", "half", 1],
      ["labor", "Loading help", "Ajuda para carregar", "half", 1], ["assembly", "Furniture assembly", "Montagem de móveis", "half", 1]
    ].map(function (t, i) { return { id: t[0], label_en: t[1], label_pt: t[2], span: t[3], crews: t[4], active: true, sort: i + 1 }; }),
    crews: [{ id: 1, name: "Equipe 1", truck: "Caminhão 26 pés", active: true, sort: 1 }, { id: 2, name: "Equipe 2", truck: "Caminhão 16 pés", active: true, sort: 2 }],
    crew_off: [{ id: 1, crew_id: 2, date_from: day(6), date_to: day(6), reason: "Manutenção do caminhão" }],
    blocked_dates: [{ day: day(18), reason: "Feriado" }],
    customers: [],
    bookings: []
  };

  var people = [
    ["Laura Mendes", "14075550111", "laura@example.com", "pt"], ["Michael Grant", "14075550112", "", "en"], ["Fernanda Lima", "14075550113", "fe.lima@example.com", "pt"],
    ["Daniel Brooks", "14075550114", "dbrooks@example.com", "en"], ["Ricardo Alves", "14075550115", "", "pt"], ["Sarah Collins", "14075550116", "sarah.c@example.com", "en"],
    ["Paula Nogueira", "14075550117", "", "pt"]
  ];
  people.forEach(function (p, i) {
    DB.customers.push({ id: "c" + i + "000000-0000-4000-8000-000000000000", name: p[0], phone: p[1], email: p[2], notes: "", tags: i === 0 ? ["indicação"] : [], created_at: iso(-40 + i * 4), _lang: p[3] });
  });
  function inv(list) { return list.map(function (x) { return { room: x[0], item: x[1], item_pt: x[2], qty: x[3] }; }); }
  var INV_A = inv([["bed", "Double bed set (bed, nightstands, dresser)", "Cama de casal (cama, criados, cômoda)", 1], ["bed", "Single bed set", "Cama de solteiro", 2], ["kitchen", "Refrigerator", "Geladeira", 1],
    ["kitchen", "Dining table (4 seats)", "Mesa de jantar (4 lugares)", 1], ["living", "Sofa (2–3 seats)", "Sofá (2–3 lugares)", 1], ["living", "TV and stand", "TV e rack", 1], ["other", "Extra boxes (approx.)", "Caixas extras (aprox.)", 9]]);
  var INV_B = inv([["bed", "Double bed set (bed, nightstands, dresser)", "Cama de casal (cama, criados, cômoda)", 1], ["kitchen", "Refrigerator", "Geladeira", 1], ["living", "Large sofa (4+ seats)", "Sofá grande (4+ lugares)", 1], ["other", "Washer / dryer", "Lavadora / secadora", 1]]);
  function bk(ci, type, n, win, status, src, extra) {
    var c = DB.customers[ci], t = DB.move_types.filter(function (x) { return x.id === type; })[0];
    var b = { id: uid("b"), code: code(), token: uid("t"), customer_id: c.id, name: c.name, phone: c.phone, email: c.email, move_type: type, move_date: day(n),
      win: t.span === "full" ? "morning" : win, span: t.span, crews: t.crews, from_addr: "", to_addr: "", size_note: "", notes: "", admin_note: "", source: src, status: status,
      price_cents: null, lang: c._lang, inventory: [], created_at: iso(n < 0 ? n - 12 : -3 + ci * 0.3), updated_at: iso(-1), cancelled_at: status === "cancelled" ? iso(-2) : null };
    Object.keys(extra || {}).forEach(function (k) { b[k] = extra[k]; });
    DB.bookings.push(b);
  }
  bk(2, "labor", 0, "morning", "confirmed", "whatsapp", { from_addr: "Windermere, FL", to_addr: "Winter Garden, FL", size_note: "Carregar caminhão alugado", price_cents: 32000 });
  bk(0, "house", 3, "morning", "pending", "site", { from_addr: "Windermere, FL", to_addr: "Orlando, FL", size_note: "3 quartos", notes: "Prédio sem elevador no destino.", inventory: INV_A });
  bk(1, "apt", 5, "morning", "pending", "site", { from_addr: "Kissimmee, FL", to_addr: "Tampa, FL", size_note: "1 bedroom", inventory: INV_B });
  bk(2, "piano", 2, "afternoon", "confirmed", "whatsapp", { from_addr: "Winter Garden, FL", to_addr: "Clermont, FL", size_note: "Piano vertical", price_cents: 45000 });
  bk(3, "office", 8, "morning", "confirmed", "phone", { from_addr: "Lake Nona, FL", to_addr: "Downtown Orlando, FL", size_note: "12 estações de trabalho", price_cents: 380000 });
  bk(4, "house", 2, "morning", "confirmed", "site", { from_addr: "Orlando, FL", to_addr: "Atlanta, GA", size_note: "4 quartos", price_cents: 420000, inventory: INV_A });
  bk(5, "packing", 9, "afternoon", "pending", "site", { from_addr: "Dr. Phillips, FL", size_note: "Cozinha e sala" });
  bk(6, "interstate", 12, "morning", "confirmed", "walkin", { from_addr: "Windermere, FL", to_addr: "Charlotte, NC", size_note: "Casa de 3 quartos", price_cents: 560000 });
  bk(1, "assembly", -4, "morning", "done", "whatsapp", { from_addr: "Kissimmee, FL", size_note: "2 guarda-roupas", price_cents: 18000 });
  bk(3, "freight", -9, "afternoon", "done", "phone", { from_addr: "Ocoee, FL", to_addr: "Sanford, FL", price_cents: 25000 });
  bk(5, "apt", 6, "morning", "cancelled", "site", { from_addr: "Orlando, FL", to_addr: "Miami, FL" });

  /* ---------- tiny PostgREST look-alike ---------- */
  function parse(qs) {
    var out = { f: [], order: [], limit: 0 };
    (qs || "").split("&").forEach(function (kv) {
      if (!kv) return;
      var i = kv.indexOf("="), k = decodeURIComponent(kv.slice(0, i)), v = decodeURIComponent(kv.slice(i + 1));
      if (k === "select" || k === "on_conflict") return;
      if (k === "order") { out.order = v.split(",").map(function (o) { var p = o.split("."); return [p[0], p[1] === "desc" ? -1 : 1]; }); return; }
      if (k === "limit") { out.limit = +v; return; }
      var j = v.indexOf("."); out.f.push([k, v.slice(0, j), v.slice(j + 1)]);
    });
    return out;
  }
  function match(r, f) {
    return f.every(function (x) {
      var a = r[x[0]], op = x[1], v = x[2];
      if (op === "eq") return String(a) === v;
      if (op === "neq") return String(a) !== v;
      if (op === "in") return v.replace(/^\(|\)$/g, "").split(",").indexOf(String(a)) >= 0;
      if (op === "gte") return String(a) >= v;
      if (op === "lte") return String(a) <= v;
      if (op === "gt") return String(a) > v;
      if (op === "lt") return String(a) < v;
      return true;
    });
  }
  function query(table, qs) {
    var q = parse(qs), rows = (DB[table] || []).filter(function (r) { return match(r, q.f); });
    if (q.order.length) rows.sort(function (a, b) {
      for (var i = 0; i < q.order.length; i++) { var k = q.order[i][0], d = q.order[i][1]; if (a[k] < b[k]) return -d; if (a[k] > b[k]) return d; }
      return 0;
    });
    if (q.limit) rows = rows.slice(0, q.limit);
    return { rows: rows, q: q };
  }
  function fail(msg) { var e = new Error(msg); e.status = 400; e.code = "P0001"; return e; }

  /* ---------- capacity, like the database functions ---------- */
  function crewsOn(d) {
    var dow = new Date(d + "T12:00:00Z").getUTCDay();
    if (DB.settings[0].work_days.indexOf(dow) < 0) return 0;
    if (DB.blocked_dates.some(function (x) { return x.day === d; })) return 0;
    return DB.crews.filter(function (c) { return c.active && !DB.crew_off.some(function (o) { return o.crew_id === c.id && o.date_from <= d && o.date_to >= d; }); }).length;
  }
  function usedOn(d, w, skip) {
    return DB.bookings.filter(function (b) { return b.move_date === d && b.id !== skip && ["pending", "confirmed", "done"].indexOf(b.status) >= 0 && (b.span === "full" || b.win === w); })
      .reduce(function (s, b) { return s + b.crews; }, 0);
  }
  function fits(d, span, win, crews, skip) {
    var n = crewsOn(d);
    if (span === "full") return n - usedOn(d, "morning", skip) >= crews && n - usedOn(d, "afternoon", skip) >= crews;
    return n - usedOn(d, win, skip) >= crews;
  }

  var RPC = {
    is_admin: function () { return true; },
    admin_capacity: function (a) {
      var out = [], d = a.p_from;
      while (d <= a.p_to) { var n = crewsOn(d); out.push({ d: d, open: n > 0, crews: n, um: usedOn(d, "morning"), ua: usedOn(d, "afternoon") }); d = SB.addDays(d, 1); }
      return out;
    },
    admin_clients: function () {
      return DB.customers.map(function (c) {
        var mine = DB.bookings.filter(function (b) { return b.customer_id === c.id; });
        var dates = mine.map(function (b) { return b.move_date; }).sort();
        var next = mine.filter(function (b) { return b.move_date >= today && ["pending", "confirmed"].indexOf(b.status) >= 0; }).map(function (b) { return b.move_date; }).sort()[0] || null;
        return { id: c.id, name: c.name, phone: c.phone, email: c.email, notes: c.notes, tags: c.tags, created_at: c.created_at, total: mine.length,
          cancelled: mine.filter(function (b) { return b.status === "cancelled"; }).length, done: mine.filter(function (b) { return b.status === "done"; }).length,
          last_date: dates[dates.length - 1] || null, next_date: next };
      });
    },
    admin_create_booking: function (a) {
      var p = a.p, t = DB.move_types.filter(function (x) { return x.id === p.type; })[0];
      if (!t) throw fail("TYPE_INVALID");
      if (!p.name) throw fail("NAME_REQUIRED");
      var ph = String(p.phone || "").replace(/\D/g, ""); if (ph.length === 10) ph = "1" + ph;
      if (ph.length < 11) throw fail("PHONE_INVALID");
      var win = t.span === "full" ? "morning" : (p.win || "morning");
      if (p.status !== "cancelled" && !p.force && !fits(p.date, t.span, win, t.crews)) throw fail("DATE_TAKEN");
      var c = DB.customers.filter(function (x) { return x.phone === ph; })[0];
      if (!c) { c = { id: uid("c"), name: p.name, phone: ph, email: p.email || "", notes: "", tags: [], created_at: new Date().toISOString(), _lang: p.lang }; DB.customers.unshift(c); }
      var b = { id: uid("b"), code: code(), token: uid("t"), customer_id: c.id, name: p.name, phone: ph, email: p.email || "", move_type: t.id, move_date: p.date, win: win, span: t.span, crews: t.crews,
        from_addr: p.from || "", to_addr: p.to || "", size_note: p.size || "", notes: p.notes || "", admin_note: "", source: p.source || "whatsapp", status: p.status || "confirmed",
        price_cents: p.price_cents === "" || p.price_cents == null ? null : +p.price_cents, lang: p.lang === "pt" ? "pt" : "en", inventory: [], created_at: new Date().toISOString(), updated_at: new Date().toISOString(), cancelled_at: null };
      DB.bookings.push(b);
      return { id: b.id, code: b.code, token: b.token };
    },
    admin_move_booking: function (a) {
      var b = DB.bookings.filter(function (x) { return x.id === a.p_id; })[0];
      if (!b) throw fail("NOT_FOUND");
      var win = b.span === "full" ? "morning" : a.p_win;
      if (!a.p_force && !fits(a.p_date, b.span, win, b.crews, b.id)) throw fail("DATE_TAKEN");
      b.move_date = a.p_date; b.win = win; return true;
    }
  };

  function tableOf(path) { var m = path.match(/^\/rest\/v1\/([a-z_]+)(?:\?(.*))?$/); return m ? { t: m[1], qs: m[2] || "" } : null; }

  SB.req = function (path, opt) {
    opt = opt || {};
    var method = opt.method || "GET", body = opt.body;
    return new Promise(function (resolve, reject) {
      setTimeout(function () {
        try {
          var m = path.match(/^\/rest\/v1\/rpc\/([a-z_]+)/);
          if (m) { if (!RPC[m[1]]) throw fail("Indisponível na demonstração."); return resolve(clone(RPC[m[1]](body || {}))); }
          if (/^\/auth\//.test(path)) return resolve({});
          var x = tableOf(path);
          if (!x || !DB[x.t]) throw fail("Indisponível na demonstração.");
          var res = query(x.t, x.qs);
          if (method === "GET") return resolve(clone(res.rows));
          if (method === "PATCH") { res.rows.forEach(function (r) { Object.keys(body || {}).forEach(function (k) { r[k] = body[k]; }); r.updated_at = new Date().toISOString(); }); return resolve(clone(res.rows)); }
          if (method === "DELETE") { DB[x.t] = DB[x.t].filter(function (r) { return res.rows.indexOf(r) < 0; }); return resolve(null); }
          if (method === "POST") {
            var rows = Array.isArray(body) ? body : [body], key = x.t === "blocked_dates" ? "day" : "id";
            var out = rows.map(function (r) {
              r = clone(r);
              if (key === "id" && r.id == null) r.id = DB[x.t].reduce(function (mx, y) { return Math.max(mx, +y.id || 0); }, 0) + 1;
              var prev = DB[x.t].filter(function (y) { return y[key] === r[key]; })[0];
              if (prev) { Object.keys(r).forEach(function (k) { prev[k] = r[k]; }); return prev; }
              DB[x.t].push(r); return r;
            });
            return resolve(clone(out));
          }
          throw fail("Indisponível na demonstração.");
        } catch (e) { reject(e); }
      }, 120);
    });
  };
  SB.session = { access_token: "demo", refresh_token: "demo", expires_at: Math.floor(Date.now() / 1000) + 86400, email: "demonstracao@shammahmoving.com" };
  SB.refreshIfNeeded = function () { return Promise.resolve(); };
  SB.signIn = SB.signUp = function () { return Promise.resolve(SB.session); };
  SB.signOut = function () { location.href = "index.html"; return new Promise(function () {}); };
  SB.demo = true;

  function badge() {
    var s = document.createElement("style");
    s.textContent = ".demo-badge{display:flex;gap:9px;align-items:flex-start;margin:0 4px 10px;padding:12px 14px;border-radius:16px;background:#121214;color:#fff;font:500 11px/1.45 'Geist Mono',ui-monospace,monospace;letter-spacing:.04em}" +
      ".demo-badge i,.demo-chip i{flex:none;width:8px;height:8px;border-radius:50%;background:#ff6b1a;margin-top:3px}" +
      ".demo-chip{display:none;align-items:center;gap:6px;margin:0 10px 0 auto;padding:6px 10px;border-radius:999px;background:#121214;color:#fff;font:500 11px/1 'Geist Mono',ui-monospace,monospace;letter-spacing:.08em}" +
      ".demo-chip i{margin-top:0}" +
      "@media (max-width:900px){.demo-chip{display:inline-flex}}";
    document.head.appendChild(s);
    var who = document.getElementById("who");
    if (who) {
      var b = document.createElement("div");
      b.className = "demo-badge"; b.setAttribute("role", "note");
      b.innerHTML = "<i></i><span>DEMONSTRAÇÃO<br>Dados fictícios. Nada do que você mudar é salvo.</span>";
      who.parentNode.insertBefore(b, who);
    }
    var bar = document.querySelector(".mbar .burger");
    if (bar) {
      var c = document.createElement("span");
      c.className = "demo-chip"; c.title = "Demonstração: dados fictícios, nada é salvo";
      c.innerHTML = "<i></i>DEMO";
      bar.parentNode.insertBefore(c, bar);
    }
  }
  if (document.body) badge(); else document.addEventListener("DOMContentLoaded", badge);
})();
