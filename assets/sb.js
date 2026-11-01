/* Minimal Supabase client (REST + Auth) for the Shammah Moving booking system. */
(function () {
  var URL = "https://ttymforuvvbnadurpvgz.supabase.co";
  var KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR0eW1mb3J1dnZibmFkdXJwdmd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM1NDU5OTksImV4cCI6MjEwOTEyMTk5OX0.nwAPpb4KeaBls1aAxgiws1xGFbClFnqtZUbK_C5EmVU";
  var SKEY = "shammah-session";
  var TZ = "America/New_York";

  function readSession() { try { return JSON.parse(localStorage.getItem(SKEY) || "null"); } catch (e) { return null; } }
  function writeSession(s) { try { s ? localStorage.setItem(SKEY, JSON.stringify(s)) : localStorage.removeItem(SKEY); } catch (e) {} }

  var SB = { url: URL, tz: TZ, session: readSession() };

  function SBError(msg, status, code) { var e = new Error(msg); e.status = status; e.code = code; return e; }

  SB.req = async function (path, opt) {
    opt = opt || {};
    var useAuth = opt.auth !== false && SB.session;
    if (useAuth) await SB.refreshIfNeeded();
    var headers = Object.assign({ apikey: KEY, "Content-Type": "application/json" }, opt.headers || {});
    headers.Authorization = "Bearer " + (useAuth && SB.session ? SB.session.access_token : KEY);
    var res = await fetch(URL + path, { method: opt.method || "GET", headers: headers, body: opt.body !== undefined ? JSON.stringify(opt.body) : undefined });
    var text = await res.text();
    var data = null;
    try { data = text ? JSON.parse(text) : null; } catch (e) { data = text; }
    if (!res.ok) {
      var m = (data && (data.message || data.msg || data.error_description || data.error)) || ("HTTP " + res.status);
      throw SBError(m, res.status, data && data.code);
    }
    return data;
  };

  SB.rpc = function (fn, args) { return SB.req("/rest/v1/rpc/" + fn, { method: "POST", body: args || {} }); };
  SB.select = function (table, qs) { return SB.req("/rest/v1/" + table + "?" + (qs || "select=*")); };
  SB.insert = function (table, rows) { return SB.req("/rest/v1/" + table, { method: "POST", body: rows, headers: { Prefer: "return=representation" } }); };
  SB.update = function (table, filter, patch) { return SB.req("/rest/v1/" + table + "?" + filter, { method: "PATCH", body: patch, headers: { Prefer: "return=representation" } }); };
  SB.remove = function (table, filter) { return SB.req("/rest/v1/" + table + "?" + filter, { method: "DELETE" }); };

  function keep(data) {
    if (!data || !data.access_token) return null;
    var s = { access_token: data.access_token, refresh_token: data.refresh_token, expires_at: data.expires_at || Math.floor(Date.now() / 1000) + (data.expires_in || 3600), email: data.user && data.user.email };
    SB.session = s; writeSession(s); return s;
  }
  SB.signIn = async function (email, password) {
    var d = await SB.req("/auth/v1/token?grant_type=password", { method: "POST", auth: false, body: { email: email, password: password } });
    return keep(d);
  };
  /* The invite code travels as user metadata; the database confirms admin e-mails only when it matches. */
  SB.signUp = async function (email, password, invite) {
    var d = await SB.req("/auth/v1/signup", { method: "POST", auth: false, body: { email: email, password: password, data: { invite: invite || "" } } });
    return keep(d) || d;
  };
  SB.refreshIfNeeded = async function () {
    var s = SB.session;
    if (!s || !s.refresh_token) return;
    if (s.expires_at - 60 > Date.now() / 1000) return;
    try {
      var res = await fetch(URL + "/auth/v1/token?grant_type=refresh_token", { method: "POST", headers: { apikey: KEY, "Content-Type": "application/json" }, body: JSON.stringify({ refresh_token: s.refresh_token }) });
      var d = await res.json();
      if (!res.ok) throw new Error("refresh");
      keep(d);
    } catch (e) { SB.session = null; writeSession(null); }
  };
  SB.signOut = async function () {
    try { if (SB.session) await SB.req("/auth/v1/logout", { method: "POST" }); } catch (e) {}
    SB.session = null; writeSession(null);
  };

  /* Dates are business dates in Florida (America/New_York, with daylight saving). */
  SB.today = function () { return new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(new Date()); };
  SB.addDays = function (ds, n) { var d = new Date(ds + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  SB.dow = function (ds) { return new Date(ds + "T12:00:00Z").getUTCDay(); };
  function loc(lang) { return lang === "pt" ? "pt-BR" : "en-US"; }
  SB.fmt = function (ds, lang, opts) { return new Intl.DateTimeFormat(loc(lang), Object.assign({ timeZone: "UTC" }, opts)).format(new Date(ds + "T12:00:00Z")); };
  SB.longDate = function (ds, lang) { return SB.fmt(ds, lang, { weekday: "long", month: "long", day: "numeric", year: "numeric" }); };
  SB.shortDate = function (ds, lang) { return SB.fmt(ds, lang, { weekday: "short", month: "short", day: "numeric" }); };
  SB.stamp = function (iso, lang) { return new Intl.DateTimeFormat(loc(lang), { timeZone: TZ, month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(new Date(iso)); };
  SB.money = function (c) { return c == null ? "" : (c / 100).toLocaleString("en-US", { style: "currency", currency: "USD", minimumFractionDigits: c % 100 ? 2 : 0 }); };
  SB.phoneFmt = function (p) {
    p = String(p || "").replace(/\D/g, "");
    if (p.length === 11 && p[0] === "1") p = p.slice(1);
    if (p.length === 10) return "(" + p.slice(0, 3) + ") " + p.slice(3, 6) + "-" + p.slice(6);
    return p ? "+" + p : "";
  };
  SB.esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  SB.toast = function (msg, err) {
    var t = document.getElementById("toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.toggle("err", !!err); t.classList.add("show");
    clearTimeout(SB._tt); SB._tt = setTimeout(function () { t.classList.remove("show"); }, 4200);
  };

  var ERR = {
    en: {
      DATE_TAKEN: "That date was just taken. Please pick another one.",
      DATE_INVALID: "That date isn't available.",
      WINDOW_INVALID: "Pick morning or afternoon.",
      PHONE_INVALID: "Check your phone number, with area code.",
      NAME_REQUIRED: "Please enter your name.",
      TOO_MANY: "This phone number already has the maximum of upcoming bookings. Cancel one or message us on WhatsApp.",
      TYPE_INVALID: "That service isn't available right now.",
      FORBIDDEN: "You don't have permission to do that.",
      NOT_FOUND: "We couldn't find that booking.",
      CREDS: "Wrong e-mail or password.",
      EXISTS: "This e-mail already has access. Use Sign in.",
      PASS: "The password needs at least 6 characters.",
      NET: "No connection. Please try again.",
      ELSE: "Something went wrong. Please try again."
    },
    pt: {
      DATE_TAKEN: "Essa data acabou de ser reservada. Escolha outra.",
      DATE_INVALID: "Essa data não está disponível.",
      WINDOW_INVALID: "Escolha manhã ou tarde.",
      PHONE_INVALID: "Confira o telefone com DDD.",
      NAME_REQUIRED: "Digite o nome.",
      TOO_MANY: "Esse telefone já atingiu o limite de reservas futuras. Cancele uma ou chame no WhatsApp.",
      TYPE_INVALID: "Esse serviço não está disponível agora.",
      FORBIDDEN: "Você não tem permissão para isso.",
      NOT_FOUND: "Não encontramos essa reserva.",
      CREDS: "E-mail ou senha incorretos.",
      EXISTS: "Esse e-mail já tem acesso. Use Entrar.",
      PASS: "A senha precisa ter pelo menos 6 caracteres.",
      NET: "Sem conexão. Tente de novo.",
      ELSE: "Algo não saiu como esperado. Tente de novo."
    }
  };
  SB.errText = function (e, lang) {
    var L = ERR[lang === "pt" ? "pt" : "en"], m = (e && e.message) || "";
    var codes = ["DATE_TAKEN", "DATE_INVALID", "WINDOW_INVALID", "PHONE_INVALID", "NAME_REQUIRED", "TOO_MANY", "TYPE_INVALID", "FORBIDDEN", "NOT_FOUND"];
    for (var i = 0; i < codes.length; i++) if (m.indexOf(codes[i]) > -1) return L[codes[i]];
    if (/Invalid login credentials/i.test(m)) return L.CREDS;
    if (/already registered/i.test(m)) return L.EXISTS;
    if (/Password should be/i.test(m)) return L.PASS;
    if (/Failed to fetch|NetworkError|Load failed/i.test(m)) return L.NET;
    return L.ELSE;
  };
  window.SB = SB;
})();
