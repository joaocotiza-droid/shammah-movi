"""Shammah Moving, version 3 (light layout, brand orange and black).

Run:  python3 build.py
Writes index.html (the real site, for Vercel).
Text lives in content.py (shared with v1 and v2) plus the v3 additions below.
The loading-truck illustration lives in truck.py (shared with v2).
"""
import base64
import html
import json
import re
from pathlib import Path

from content import T, SVC, FAQ, MOVES, WA, IG, PHONE, PHONE_LABEL, EMAIL, SITE_URL
from truck import truck_svg, ITEM_DATA

HERE = Path(__file__).parent

# Room-by-room item list in the booking form. Set to False to take it off the site;
# nothing else on the page changes (the request is sent without the list).
SHOW_INVENTORY = True
FMCSA = "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=1547896"

ADD = {
    "en": {
        "heroKicker": "Windermere · Orlando · Central Florida",
        "hc1T": "We speak your language", "hc1D": "English and Portuguese, from the first message to the last box.",
        "hc2T": "Since 2008", "hc2D": "Moving families and businesses in Central Florida.",
        "tLocal": "Local", "tInter": "Interstate", "tIntl": "International",
        "aboutEyebrow": "About us",
        "ab1": "A Windermere crew for the move", "ab2": "across town", "ab3": "and the one", "ab4": "across the ocean.",
        "fEst": "Since", "b11": "types of move, from a single sofa to a full house overseas.",
        "bLang": "Talk to us in English or Portuguese, from quote to delivery.",
        "verify": "Verify on FMCSA",
        "loadEyebrow": "On moving day", "loadA": "Every piece", "loadB": "has its place.",
        "packedA": "Packed.", "packedB": "Next stop: your new home.",
        "hudLoading": "Loading", "hudPacked": "Packed", "hudRoad": "On the way",
        "scrollHint": "Keep scrolling",
        "svcLead": "From a single sofa to a whole house overseas, one crew plans it, packs it and moves it.",
        "svc_local_r": "Windermere → Orlando", "svc_interstate_r": "Florida → Georgia",
        "svc_intl_r": "MCO → GRU", "svc_packing_r": "Fragile · This side up",
        "svc_freight_r": "Pickup → Drop-off",
        "alsoTitle": "Also on the truck",
        "prev": "Previous service", "next": "Next service", "quoteThis": "Quote this move",
        "qH3": "Everything starts with a quote.",
        "st1": "Move type", "st2": "Details", "st3": "Send",
        "mvInc": "Included", "mvFoot": "We reply in English or Portuguese.",
        "endC1D": "Message us with what you're moving. Photos help.",
        "endC2D": "Prefer to talk? Give us a call.",
        "endC3D": "Real moves and behind the scenes.",
        "open": "Open", "igLine": "Real moves and behind the scenes on Instagram.",
        "menu": "Menu", "menuClose": "Close menu",
    },
    "pt": {
        "heroKicker": "Windermere · Orlando · Flórida Central",
        "hc1T": "Falamos a sua língua", "hc1D": "Português e inglês, da primeira mensagem à última caixa.",
        "hc2T": "Desde 2008", "hc2D": "Mudando famílias e empresas na Flórida Central.",
        "tLocal": "Local", "tInter": "Interestadual", "tIntl": "Internacional",
        "aboutEyebrow": "Sobre nós",
        "ab1": "Uma equipe de Windermere para a mudança", "ab2": "do outro lado da cidade", "ab3": "e para a", "ab4": "do outro lado do oceano.",
        "fEst": "Desde", "b11": "tipos de mudança, de um sofá a uma casa inteira para outro país.",
        "bLang": "Fale com a gente em português ou inglês, do orçamento à entrega.",
        "verify": "Consultar no FMCSA",
        "loadEyebrow": "No dia da mudança", "loadA": "Cada peça", "loadB": "tem seu lugar.",
        "packedA": "Carregado.", "packedB": "Próxima parada: sua casa nova.",
        "hudLoading": "Carregando", "hudPacked": "Fechado", "hudRoad": "A caminho",
        "scrollHint": "Continue rolando",
        "svcLead": "De um sofá a uma casa inteira para outro país, uma equipe planeja, embala e leva.",
        "svc_local_r": "Windermere → Orlando", "svc_interstate_r": "Flórida → Geórgia",
        "svc_intl_r": "MCO → GRU", "svc_packing_r": "Frágil · Este lado para cima",
        "svc_freight_r": "Coleta → Entrega",
        "alsoTitle": "Também no caminhão",
        "prev": "Serviço anterior", "next": "Próximo serviço", "quoteThis": "Orçar esta mudança",
        "qH3": "Tudo começa com um orçamento.",
        "st1": "Tipo", "st2": "Detalhes", "st3": "Enviar",
        "mvInc": "Incluso", "mvFoot": "Respondemos em português ou inglês.",
        "endC1D": "Mande o que você vai mudar. Fotos ajudam.",
        "endC2D": "Prefere falar? Ligue pra gente.",
        "endC3D": "Mudanças de verdade e bastidores.",
        "open": "Abrir", "igLine": "Mudanças de verdade e bastidores no Instagram.",
        "menu": "Menu", "menuClose": "Fechar menu",
    },
}
# Booking system copy. These keys override the older quote-by-WhatsApp wording from content.py.
BK = {
    "en": {
        "metaTitle": "Shammah Moving | Book Your Move in Windermere & Orlando, FL",
        "metaDesc": "Book your move online with Shammah Moving. Local, interstate and international moving out of Windermere, Florida, plus packing, freight, storage and pianos. We speak English and Portuguese.",
        "navQuote": "Book a move", "ctaQuote": "Book a date",
        "heroSub": "Local, interstate and international moves out of Windermere, Florida. Pick your date, send the details and we reply on WhatsApp with your quote.",
        "qTitle": "Book your move", "qH3": "Pick a date. We confirm on WhatsApp.",
        "qSub": "Choose your type of move, pick the day you prefer and tell us where you're going. Your request goes straight to our WhatsApp and we reply there with the quote.",
        "st1": "Move type", "st2": "Date", "st3": "Details", "st4": "Sent",
        "quoteThis": "Book this move",
        "sendWa": "Ask on WhatsApp first",
        "sendNote": "Not sure about the details yet? Message us what you're moving and we'll come back with a quote.",
        "h1t": "Pick your date", "h1d": "Choose the type of move and the day you prefer. Add the addresses and a rough size.",
        "h2t": "We confirm", "h2d": "We review the details on WhatsApp, size the crew and the truck, and confirm your date with a written estimate.",
        "endSub": "Send your request today. We'll take it from there.",
        "bkDate": "Choose a date", "bkDateHint": "Pick the day you prefer. We confirm it on WhatsApp.",
        "calPrev": "Previous month", "calNext": "Next month",
        "legOpen": "Open", "legLast": "Last spot", "legFull": "Full", "legClosed": "Closed",
        "calLoad": "Loading dates…",
        "calFail": "We couldn't load the calendar. Message us on WhatsApp and we'll book it for you.",
        "aOpen": "available", "aLast": "last spot", "aFull": "full", "aClosed": "closed",
        "winH": "Arrival window", "winM": "Morning", "winA": "Afternoon",
        "winFull": "This is a full-day move. The crew arrives {w}.",
        "lName": "Full name", "phName": "Your name", "lPhone": "Phone or WhatsApp", "phPhone": "(407) 555-0123",
        "lEmail": "E-mail (optional)", "phEmail": "you@email.com",
        "lNotes": "Anything we should know? (optional)", "phNotes": "Stairs, elevator, piano, fragile items…",
        "sumDate": "Date", "sumArrive": "Arrival", "sumPick": "Pick a date",
        "bookBtn": "Send request on WhatsApp", "sending": "Opening WhatsApp…",
        "vDate": "Pick a date for your move.", "vWin": "Pick morning or afternoon.",
        "vName": "Please enter your name.", "vPhone": "Check your phone number, with area code.",
        "okPending": "Your request is ready.",
        "okSubPending": "Send it on WhatsApp so we can review {d} and reply with your quote. If WhatsApp didn't open, tap the button below.",
        "okType": "Move", "okDate": "Date", "okArrive": "Arrival",
        "okWa": "Send on WhatsApp", "okAgain": "Request another move",
        "rqHead": "New move request from the website", "rqMove": "Move", "rqDate": "Preferred date", "rqArrive": "Arrival",
        "rqName": "Name", "rqPhone": "Phone", "rqEmail": "E-mail", "rqFrom": "From", "rqTo": "To", "rqSize": "Size",
        "rqItems": "Items", "rqNotes": "Notes", "rqLang": "Site language", "rqLangV": "English",
    },
    "pt": {
        "metaTitle": "Shammah Moving | Agende sua mudança em Windermere e Orlando, FL",
        "metaDesc": "Agende sua mudança online com a Shammah Moving. Mudanças locais, interestaduais e internacionais saindo de Windermere, Flórida, além de embalagem, fretes, armazenagem e pianos. Atendimento em português.",
        "navQuote": "Agendar", "ctaQuote": "Agendar data",
        "heroSub": "Mudanças locais, interestaduais e internacionais saindo de Windermere, na Flórida. Escolha a data, envie os detalhes e a gente responde no WhatsApp com o orçamento.",
        "qTitle": "Agende sua mudança", "qH3": "Escolha a data. A gente confirma no WhatsApp.",
        "qSub": "Escolha o tipo de mudança, o dia de sua preferência e conte para onde você vai. O pedido cai direto no nosso WhatsApp e a gente responde por lá com o orçamento.",
        "st1": "Tipo", "st2": "Data", "st3": "Dados", "st4": "Enviado",
        "quoteThis": "Agendar esta mudança",
        "sendWa": "Perguntar no WhatsApp antes",
        "sendNote": "Ainda não tem todos os detalhes? Mande no WhatsApp o que você vai mudar e a gente volta com o orçamento.",
        "h1t": "Escolha a data", "h1d": "Escolha o tipo de mudança e o dia de sua preferência. Coloque os endereços e um tamanho aproximado.",
        "h2t": "A gente confirma", "h2d": "Vemos os detalhes pelo WhatsApp, definimos equipe e caminhão e confirmamos sua data com um orçamento por escrito.",
        "endSub": "Envie seu pedido hoje mesmo. A gente cuida do resto.",
        "bkDate": "Escolha a data", "bkDateHint": "Escolha o dia de sua preferência. Confirmamos pelo WhatsApp.",
        "calPrev": "Mês anterior", "calNext": "Próximo mês",
        "legOpen": "Livre", "legLast": "Última vaga", "legFull": "Lotado", "legClosed": "Fechado",
        "calLoad": "Carregando datas…",
        "calFail": "Não conseguimos carregar o calendário. Chame no WhatsApp que a gente agenda para você.",
        "aOpen": "disponível", "aLast": "última vaga", "aFull": "lotado", "aClosed": "fechado",
        "winH": "Janela de chegada", "winM": "Manhã", "winA": "Tarde",
        "winFull": "Mudança de dia inteiro. A equipe chega {w}.",
        "lName": "Nome completo", "phName": "Seu nome", "lPhone": "Telefone ou WhatsApp", "phPhone": "(407) 555-0123",
        "lEmail": "E-mail (opcional)", "phEmail": "voce@email.com",
        "lNotes": "Algo que a gente deva saber? (opcional)", "phNotes": "Escada, elevador, piano, itens frágeis…",
        "sumDate": "Data", "sumArrive": "Chegada", "sumPick": "Escolha uma data",
        "bookBtn": "Enviar pedido no WhatsApp", "sending": "Abrindo o WhatsApp…",
        "vDate": "Escolha a data da mudança.", "vWin": "Escolha manhã ou tarde.",
        "vName": "Digite seu nome.", "vPhone": "Confira o telefone, com DDD.",
        "okPending": "Seu pedido está pronto.",
        "okSubPending": "Envie pelo WhatsApp para a gente analisar {d} e responder com o orçamento. Se o WhatsApp não abriu, toque no botão abaixo.",
        "okType": "Mudança", "okDate": "Data", "okArrive": "Chegada",
        "okWa": "Enviar no WhatsApp", "okAgain": "Pedir outra mudança",
        "rqHead": "Novo pedido de mudança pelo site", "rqMove": "Mudança", "rqDate": "Data desejada", "rqArrive": "Chegada",
        "rqName": "Nome", "rqPhone": "Telefone", "rqEmail": "E-mail", "rqFrom": "Saída", "rqTo": "Destino", "rqSize": "Tamanho",
        "rqItems": "Itens", "rqNotes": "Observações", "rqLang": "Idioma do site", "rqLangV": "Português",
    },
}
for lang in ("en", "pt"):
    T[lang].update(ADD[lang])
    T[lang].update(BK[lang])
    for m in MOVES[lang]:
        if m["id"] in ("piano", "assembly", "labor"):
            T[lang][f"also_{m['id']}_t"] = m["title"]
            T[lang][f"also_{m['id']}_d"] = m["line"]
assert set(T["en"]) == set(T["pt"]), set(T["en"]) ^ set(T["pt"])
EN = T["en"]


def e(key):
    return html.escape(EN[key], quote=True)


def fill(tpl):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: e(m.group(1)), tpl)


CHECK = '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="#ff6b1a"/><path d="M6 10.2l2.6 2.6L14 7.4" fill="none" stroke="#121214" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_WA = '<svg class="wa" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 9.5c.3 2.4 2.7 4.8 5.2 5.3l1.2-1.2 1.8.8c-.2 1.3-1.2 2-2.4 1.9-3.4-.3-6.4-3.3-6.7-6.7-.1-1.2.6-2.2 1.9-2.4l.8 1.8z"/></svg>'
ICON_IG = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.8" fill="currentColor" stroke="none"/></svg>'
ICON_PHONE = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
ICON_TRUCK = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 6h11v10H2zM13 9h4l3 3.5V16h-7z"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/></svg>'
ICON_PLANE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 13.5L3 11l1.5-1.5 8 1 4.5-4.5a2 2 0 0 1 3 3L15.5 13.5l1 8L15 23l-2.5-7.5L9 19v2.5L7.5 23l-1-3.5L3 18.5 4.5 17H7l3.5-3.5z"/></svg>'
ARR = '<svg class="arr" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 8h11M9 3.5L13.5 8 9 12.5"/></svg>'
ARR_UP = '<svg class="arr" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 11.5l7-7M5.5 4.5h6v6"/></svg>'
ARR_L = '<svg width="18" height="18" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13.5 8h-11M7 3.5L2.5 8 7 12.5"/></svg>'
ARR_R = '<svg width="18" height="18" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 8h11M9 3.5L13.5 8 9 12.5"/></svg>'

# Default length of each type of move; the database (move_types.span) overrides these at runtime.
DEFAULT_SPAN = {"house": "full", "apt": "full", "office": "full", "interstate": "full", "intl": "full",
                "freight": "half", "packing": "half", "piano": "half", "storage": "half", "labor": "half", "assembly": "half"}

SVC_ORDER = [("local", "house"), ("interstate", "interstate"), ("intl", "intl"), ("packing", "packing"), ("freight", "freight")]


def svc_cards():
    out = []
    for k, mv in SVC_ORDER:
        out.append(
            f'<article class="card"><img src="assets/{k}.webp" width="1100" height="728" alt="" loading="lazy" decoding="async">'
            f'<span class="pill-g" data-i18n="svc_{k}_r">{e(f"svc_{k}_r")}</span>'
            f'<div class="card-in"><h3 data-i18n="svc_{k}_t">{e(f"svc_{k}_t")}</h3><p data-i18n="svc_{k}_d">{e(f"svc_{k}_d")}</p></div>'
            f'<a class="card-go" href="#quote" data-pick="{mv}" aria-label="{e("quoteThis")}" data-i18n-aria="quoteThis">{ARR_UP}</a></article>'
        )
    return "\n".join(out)


def also():
    rows = [("svc_storage_t", "svc_storage_d")] + [(f"also_{k}_t", f"also_{k}_d") for k in ("piano", "assembly", "labor")]
    return "\n".join(f'<div class="also-i"><h4 data-i18n="{t}">{e(t)}</h4><p data-i18n="{d}">{e(d)}</p></div>' for t, d in rows)


def marquee():
    keys = ["svc_local_t", "svc_interstate_t", "svc_intl_t", "svc_packing_t", "svc_freight_t", "svc_storage_t", "also_piano_t", "also_assembly_t", "also_labor_t"]
    one = "".join(f'<li><span data-i18n="{k}">{e(k)}</span></li>' for k in keys)
    return f'<ul class="mq-list">{one}</ul><ul class="mq-list" aria-hidden="true">{one}</ul>'


def move_buttons():
    return "\n".join(
        f'<button type="button" class="chip" data-move="{m["id"]}" aria-pressed="{"true" if i == 0 else "false"}">{html.escape(m["label"])}</button>'
        for i, m in enumerate(MOVES["en"])
    )


first = MOVES["en"][0]
first_inc = "".join(f"<li>{CHECK}<span>{html.escape(x)}</span></li>" for x in first["inc"])
faq_html = "\n".join(
    f'<details class="faq-item"><summary data-i18n="faq{i}q">{e(f"faq{i}q")}</summary><p data-i18n="faq{i}a">{e(f"faq{i}a")}</p></details>'
    for i in range(len(FAQ["en"]))
)
mini_moves = "".join(f'<li>{html.escape(m["label"])}</li>' for m in MOVES["en"][:6])

CSS = r'''
/* Layout: light page of framed, rounded "windows" (photo hero, dark truck stage, photo CTA) with bento cards between. One accent: brand orange. */
:root{
  --bg:#ffffff;--surface:#f3f3f1;--surface-2:#e9e9e5;--ink:#121214;--mute:#66666d;--line:#e3e3df;
  --orange:#ff6b1a;--orange-hi:#ff8540;--orange-ink:#bf4c0b;--night:#0d0d0f;--night-2:#18181b;
  --sans:Geist,-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;
  --mono:"Geist Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  --disp:"Barlow Condensed","Arial Narrow",Impact,sans-serif;
  --wrap:1280px;--r-frame:30px;--r-card:24px;--r-ctl:14px;--ease:cubic-bezier(.2,.7,.2,1);
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-padding-top:96px}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:40;background:var(--bg)}
img{max-width:100%;height:auto;display:block}
p{text-wrap:pretty}
a{color:inherit}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--orange);outline-offset:3px;border-radius:8px}
.wrap{width:100%;max-width:var(--wrap);margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.edge{padding-left:max(12px,env(safe-area-inset-left,0px));padding-right:max(12px,env(safe-area-inset-right,0px))}
.skip{position:absolute;left:-9999px;top:8px;z-index:60;background:#fff;color:#000;padding:10px 16px;border-radius:8px}
.skip:focus{left:12px}
h1,h2,h3,h4{text-wrap:balance}
.eyebrow{display:inline-flex;align-items:center;gap:8px;margin:0 0 18px;font:500 12px/1.2 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.eyebrow::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--orange)}
.h2{margin:0;font-weight:500;font-size:clamp(40px,5vw,72px);line-height:1;letter-spacing:-.045em}
.h2 .m{color:#a3a3a8}
.lede{font-size:clamp(17px,1.4vw,19px);line-height:1.55;max-width:34em;margin:0;color:var(--mute)}
.mono{font-family:var(--mono)}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:12px;min-height:52px;padding:0 8px 0 22px;border-radius:999px;font-size:15px;font-weight:600;text-decoration:none;border:1px solid transparent;cursor:pointer;white-space:nowrap;transition:transform .2s var(--ease),background-color .25s,border-color .25s,color .25s,box-shadow .3s}
.btn:active{transform:scale(.97)}
.btn .dot{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;transition:transform .4s var(--ease)}
.btn:hover .dot{transform:rotate(-45deg)}
.btn .wa{transition:transform .35s var(--ease)}
.btn:hover .wa{transform:rotate(-10deg)}
.btn-o{background:var(--orange);color:var(--ink)}
.btn-o .dot{background:var(--ink);color:#fff}
.btn-o:hover{background:var(--orange-hi);box-shadow:0 12px 30px -10px rgba(255,107,26,.6)}
.btn-ink{background:var(--ink);color:#fff}
.btn-ink .dot{background:var(--orange);color:var(--ink)}
.btn-ink:hover{background:#2a2a2e}
.btn-glass{background:rgba(255,255,255,.14);color:#fff;border-color:rgba(255,255,255,.28);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);padding:0 22px}
.btn-glass:hover{background:rgba(255,255,255,.24)}
.btn-line{border-color:var(--line);color:var(--ink);padding:0 22px;background:#fff}
.btn-line:hover{border-color:var(--ink)}
.ctas{display:flex;flex-wrap:wrap;gap:10px}

/* nav: floating pill */
.nav{position:fixed;z-index:30;top:calc(18px + env(safe-area-inset-top,0px));left:0;right:0;pointer-events:none}
.nav-in{pointer-events:auto;max-width:1180px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:7px 7px 7px 16px;border-radius:999px;background:rgba(255,255,255,.86);-webkit-backdrop-filter:saturate(180%) blur(18px);backdrop-filter:saturate(180%) blur(18px);box-shadow:0 1px 0 rgba(0,0,0,.04),0 10px 30px -14px rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.7)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none}
.brand img{width:34px;height:34px;border-radius:50%}
.brand b{font-family:var(--disp);font-style:italic;font-weight:900;font-size:21px;letter-spacing:.03em;line-height:1}
.links{display:flex;gap:2px}
.links a{padding:9px 14px;border-radius:999px;font:500 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:#3c3c41;transition:background-color .2s,color .2s}
.links a:hover{background:var(--surface);color:var(--ink)}
.nav-r{display:flex;align-items:center;gap:8px}
.lang{display:flex;padding:3px;border-radius:999px;background:var(--surface)}
.lang button{min-height:30px;min-width:38px;padding:0 10px;border:0;border-radius:999px;background:transparent;color:#55555b;font:600 12px var(--mono);letter-spacing:.06em;cursor:pointer;transition:background-color .2s,color .2s}
.lang button[aria-pressed="true"]{background:var(--ink);color:#fff}
.nav .btn{min-height:42px;font-size:14px;padding-left:18px;padding-right:5px}
.nav .btn .dot{width:32px;height:32px}
.menu-btn{display:none;width:42px;height:42px;border:0;border-radius:50%;background:var(--ink);cursor:pointer;position:relative}
.menu-btn span{position:absolute;left:13px;right:13px;height:1.6px;background:#fff;border-radius:2px;transition:transform .35s var(--ease),top .35s var(--ease)}
.menu-btn span:first-child{top:17px}.menu-btn span:last-child{top:23px}
.menu-btn[aria-expanded="true"] span:first-child{top:20px;transform:rotate(45deg)}
.menu-btn[aria-expanded="true"] span:last-child{top:20px;transform:rotate(-45deg)}
.menu{position:fixed;z-index:29;inset:0;background:rgba(255,255,255,.97);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);padding-block:calc(100px + env(safe-area-inset-top,0px)) calc(28px + env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;justify-content:space-between;opacity:0;transform:translateY(-10px);transition:opacity .3s ease,transform .4s var(--ease)}
.menu[hidden]{display:none}
.menu.open{opacity:1;transform:none}
.menu nav{display:flex;flex-direction:column}
.menu nav a{font-weight:500;font-size:clamp(38px,11vw,56px);letter-spacing:-.04em;line-height:1.1;text-decoration:none;padding-block:10px;border-bottom:1px solid var(--line)}
.menu .btn{align-self:stretch;justify-content:space-between}
@media (max-width:980px){.links{display:none}.menu-btn{display:block}}
@media (max-width:520px){.nav .btn-o{display:none}.brand b{font-size:19px}}

/* hero */
.hero{padding-top:12px}
.frame{position:relative;border-radius:var(--r-frame);overflow:hidden;isolation:isolate}
.hero .frame{min-height:clamp(640px,92svh,900px);display:flex;flex-direction:column;justify-content:flex-end;background:#1b1b1d;color:#fff}
.hero .frame>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 52%;z-index:-2;transform:scale(1.04);animation:settle 2.4s var(--ease) forwards}
@keyframes settle{to{transform:scale(1)}}
.hero .frame::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(13,13,15,.72) 0%,rgba(13,13,15,.35) 42%,rgba(13,13,15,0) 70%),linear-gradient(180deg,rgba(13,13,15,.5) 0%,rgba(13,13,15,0) 26%,rgba(13,13,15,.1) 48%,rgba(13,13,15,.86) 100%)}
.hero-body{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:28px 56px;align-items:end;padding:clamp(24px,4vw,56px)}
.hero .eyebrow{color:rgba(255,255,255,.8)}
.hero h1{margin:0;font-weight:500;font-size:clamp(52px,7.4vw,118px);line-height:.95;letter-spacing:-.055em}
.hero h1 span{display:block}
.hero h1 .o{color:var(--orange)}
.hero .lede{color:rgba(255,255,255,.82);margin-top:22px;max-width:30em}
.hero .ctas{margin-top:28px}
.hero-tags{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px;padding:0;list-style:none}
.hero-tags li{padding:7px 13px;border-radius:999px;background:rgba(255,255,255,.14);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.22);font:500 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.floats{display:flex;flex-direction:column;gap:12px;align-items:flex-end}
.fcard{width:min(320px,100%);padding:18px 20px;border-radius:20px;background:rgba(255,255,255,.94);color:var(--ink);box-shadow:0 24px 50px -24px rgba(0,0,0,.55);display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 14px;align-items:center;animation:bob 6s ease-in-out infinite}
.fcard:nth-child(2){animation-delay:-3s;margin-right:36px}
.fcard .ic{grid-row:span 2;display:grid;place-items:center;width:44px;height:44px;border-radius:14px;background:var(--orange);color:var(--ink);font:600 13px var(--mono)}
.fcard .ic.dk{background:var(--ink);color:var(--orange)}
.fcard b{font-size:16px;font-weight:600;letter-spacing:-.01em}
.fcard span{font-size:14px;color:var(--mute);line-height:1.4}
@keyframes bob{50%{transform:translateY(-8px)}}
.hero-pin{position:absolute;top:calc(92px + env(safe-area-inset-top,0px));left:clamp(24px,4vw,56px);padding:8px 13px;border-radius:999px;background:rgba(13,13,15,.5);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);font:500 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:#fff}
.hero-social{position:absolute;top:calc(92px + env(safe-area-inset-top,0px));right:clamp(24px,4vw,56px);display:flex;gap:16px;font-size:13px}
.hero-social a{text-decoration:none;color:rgba(255,255,255,.88);display:inline-flex;align-items:center;gap:4px}
.hero-social a:hover{color:#fff}
@media (max-width:900px){
  .hero-body{grid-template-columns:minmax(0,1fr)}
  .floats{flex-direction:row;align-items:stretch;overflow-x:auto;scrollbar-width:none;margin-inline:calc(-1 * clamp(24px,4vw,56px));padding-inline:clamp(24px,4vw,56px);padding-block:4px 10px}
  .floats::-webkit-scrollbar{display:none}
  .fcard{flex:0 0 min(290px,78%);animation:none}
  .fcard:nth-child(2){margin-right:0}
  .hero-social,.hero-pin{display:none}
}

/* marquee */
.mq{overflow:hidden;padding-block:26px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.mq-track{display:flex;width:max-content;animation:slide 48s linear infinite}
.mq:hover .mq-track{animation-play-state:paused}
.mq-list{display:flex;margin:0;padding:0;list-style:none}
.mq-list li{display:flex;align-items:center;gap:28px;padding-right:28px;font-weight:500;font-size:clamp(18px,1.8vw,24px);letter-spacing:-.02em;color:#8d8d93;white-space:nowrap}
.mq-list li::after{content:"";width:8px;height:8px;border-radius:50%;background:var(--orange)}
@keyframes slide{to{transform:translateX(-50%)}}

/* about + bento */
.about{padding-block:clamp(80px,10vw,140px) clamp(40px,6vw,80px);text-align:center}
.statement{margin:0 auto;max-width:17em;font-weight:500;font-size:clamp(32px,4.4vw,62px);line-height:1.12;letter-spacing:-.045em}
.statement .m{color:#a3a3a8}
.ipill{display:inline-grid;place-items:center;vertical-align:-.12em;width:1.5em;height:.95em;border-radius:999px;background:var(--orange);color:var(--ink);margin-inline:.08em}
.ipill.dk{background:var(--ink);color:var(--orange)}
.ipill svg{width:.55em;height:.55em}
.bento{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));grid-auto-rows:minmax(220px,auto);gap:14px;padding-bottom:clamp(80px,10vw,140px)}
.b{position:relative;border-radius:var(--r-card);padding:26px;overflow:hidden;min-width:0;display:flex;flex-direction:column;gap:12px;background:var(--surface)}
.b .big{font-weight:500;font-size:clamp(64px,6.4vw,104px);line-height:.9;letter-spacing:-.06em}
.b p{margin:0;font-size:15px;color:var(--mute)}
.b .lbl{font:500 12px/1.2 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.b-photo{grid-column:span 4;grid-row:span 2;padding:14px;justify-content:space-between;background:#222}
.b-photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease)}
.b-photo:hover img{transform:scale(1.05)}
.b-photo .tag{position:relative;align-self:flex-start;padding:8px 12px;border-radius:999px;background:rgba(13,13,15,.55);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#fff;font:500 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.b-photo .inner{position:relative;background:#fff;border-radius:18px;padding:20px 22px;display:flex;flex-direction:column;gap:8px}
.b-moves{grid-column:span 4;grid-row:span 2;justify-content:space-between}
.mini{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.mini li{padding:7px 12px;border-radius:999px;background:#fff;border:1px solid var(--line);font-size:13px}
.b-lang{grid-column:span 4;background:var(--orange);justify-content:space-between}
.b-lang .lbl,.b-lang p{color:#3b1806}
.b-lang .big{font-size:clamp(52px,5vw,80px)}
.b-dot{grid-column:span 4;background:var(--ink);color:#fff;flex-direction:row;align-items:flex-end;justify-content:space-between;flex-wrap:wrap}
.b-dot .lbl{color:#9a9aa1}
.b-dot .num{font:500 clamp(30px,3vw,44px)/1 var(--mono);letter-spacing:-.03em}
.b-dot a{display:inline-flex;align-items:center;gap:6px;font-size:14px;color:#fff;text-underline-offset:3px}
.b-dot a .arr{transition:transform .35s var(--ease)}
.b-dot a:hover .arr{transform:translateX(4px)}
@media (max-width:980px){.b-photo,.b-moves{grid-column:span 6}.b-lang,.b-dot{grid-column:span 6}}
@media (max-width:640px){.bento{grid-auto-rows:auto}.b-photo,.b-moves,.b-lang,.b-dot{grid-column:span 12;grid-row:auto}.b-photo{min-height:440px}.b-moves{gap:28px}}

/* load: dark stage inside a frame */
.load{position:relative;height:330vh}
.load-stage{position:sticky;top:0;height:100vh;height:100svh;padding-block:calc(84px + env(safe-area-inset-top,0px)) 12px}
.load .frame{height:100%;background:radial-gradient(120% 80% at 55% 100%,#2a1708 0%,var(--night) 60%);color:#f4f4f2;display:flex;flex-direction:column}
.load-head{position:relative;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;padding:clamp(22px,3.4vw,44px) clamp(22px,3.4vw,44px) 0}
.load-head .eyebrow{color:#9a9aa1}
.load-copy{transition:none}
.load-copy h2{margin:0;font-weight:500;font-size:clamp(36px,4.6vw,68px);line-height:1;letter-spacing:-.045em}
.load-copy h2 span{display:block}
.load-copy h2 .o{color:var(--orange)}
.load-copy.alt{position:absolute;left:clamp(22px,3.4vw,44px);right:clamp(22px,3.4vw,44px);bottom:0;opacity:0}
.rig-wrap{flex:1;min-height:0;display:flex;align-items:flex-end;justify-content:center;padding:16px 0 0}
.rig{display:block;width:100%;height:100%;max-height:560px;overflow:visible}
.t-disp{font-family:var(--disp);font-style:italic;font-weight:900}
.t-wide{font-family:var(--mono);font-weight:500;letter-spacing:12px}
.t-mono{font-family:var(--mono);font-weight:500}
.marker{animation:blink 1.6s steps(1) infinite}
@keyframes blink{50%{opacity:.25}}
.hud{display:flex;align-items:center;gap:18px;padding:14px clamp(22px,3.4vw,44px) 22px;font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:#9a9aa1;font-variant-numeric:tabular-nums}
.hud b{color:#fff;font-weight:500;min-width:7ch}
.hud-bar{flex:1;height:2px;background:#2a2a2e;position:relative;overflow:hidden;border-radius:2px}
.hud-bar i{position:absolute;inset:0;background:var(--orange);transform-origin:left;transform:scaleX(0)}
@media (max-width:760px){
  .load{height:280vh}
  .load-head{grid-template-columns:minmax(0,1fr)}
  .rig-wrap{align-items:center}
  .rig{height:auto;max-height:none}
}

/* services */
.svc{padding-block:clamp(90px,11vw,150px) clamp(60px,8vw,110px)}
.svc-grid{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:40px}
.svc-side{display:flex;flex-direction:column;justify-content:space-between;gap:28px;min-width:0}
.svc-side .h2{font-size:clamp(34px,3.4vw,50px)}
.svc-side .lede{margin-top:20px}
.arrows{display:flex;gap:8px}
.arrows button{width:46px;height:46px;border-radius:50%;border:1px solid var(--line);background:#fff;display:grid;place-items:center;cursor:pointer;transition:background-color .2s,border-color .2s,transform .2s var(--ease)}
.arrows button:hover{border-color:var(--ink)}
.arrows button:active{transform:scale(.94)}
.arrows button:disabled{opacity:.35;cursor:default}
.rail{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:4px;min-width:0;scroll-behavior:smooth}
.rail::-webkit-scrollbar{display:none}
.card{position:relative;flex:0 0 min(360px,80%);aspect-ratio:4/5;border-radius:var(--r-card);overflow:hidden;scroll-snap-align:start;color:#fff;background:#222;display:flex;flex-direction:column;justify-content:flex-end}
.card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.card:hover img{transform:scale(1.05)}
.card::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 40%,rgba(0,0,0,.78))}
.pill-g{position:absolute;z-index:2;top:16px;left:16px;padding:7px 12px;border-radius:999px;background:rgba(255,255,255,.18);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.25);font:500 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.card-in{position:relative;z-index:2;padding:22px 74px 22px 22px}
.card h3{margin:0;font-weight:500;font-size:26px;line-height:1.05;letter-spacing:-.03em}
.card p{margin:8px 0 0;font-size:14px;color:rgba(255,255,255,.8)}
.card-go{position:absolute;z-index:3;right:16px;bottom:18px;width:44px;height:44px;border-radius:50%;background:#fff;color:var(--ink);display:grid;place-items:center;transition:transform .4s var(--ease),background-color .2s}
.card-go:hover{background:var(--orange);transform:rotate(45deg)}
.also{display:grid;grid-template-columns:auto repeat(4,minmax(0,1fr));gap:20px 28px;margin-top:56px;padding-top:28px;border-top:1px solid var(--line);align-items:start}
.also h3{margin:0;font:500 12px/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);min-width:120px}
.also-i h4{margin:0;font-weight:600;font-size:17px;letter-spacing:-.01em}
.also-i p{margin:6px 0 0;font-size:14px;color:var(--mute)}
@media (max-width:980px){.svc-grid{grid-template-columns:minmax(0,1fr)}.svc-side{flex-direction:row;align-items:flex-end;flex-wrap:wrap}.also{grid-template-columns:repeat(2,minmax(0,1fr))}.also h3{grid-column:1/-1}}
@media (max-width:520px){.also{grid-template-columns:minmax(0,1fr)}.rail{margin-inline:calc(-1 * max(20px,env(safe-area-inset-left,0px)));padding-inline:max(20px,env(safe-area-inset-left,0px));scroll-padding-inline:max(20px,env(safe-area-inset-left,0px))}}

/* quote */
.quote-sec{padding-bottom:clamp(80px,10vw,140px)}
.panel{border-radius:var(--r-frame);background:var(--surface);padding:clamp(24px,4.4vw,64px)}
.q-head{text-align:center;max-width:760px;margin:0 auto}
.q-head .lede{margin:18px auto 0}
.qsteps{list-style:none;display:flex;justify-content:center;flex-wrap:wrap;gap:8px 28px;margin:36px 0 0;padding:0;font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.qsteps li{display:flex;align-items:center;gap:10px;transition:color .3s}
.qsteps li b{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;border:1px solid #cfcfca;font-weight:500;transition:background-color .3s,border-color .3s,color .3s}
.qsteps li.done{color:var(--ink)}
.qsteps li.done b{background:var(--orange);border-color:var(--orange);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:22px}
.chip{min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink);font-size:15px;font-weight:500;cursor:pointer;white-space:nowrap;transition:background-color .2s,border-color .2s,color .2s,transform .2s var(--ease)}
.chip:hover{border-color:var(--ink)}
.chip:active{transform:scale(.96)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}
@media (max-width:760px){
  .chips{justify-content:flex-start;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin-inline:calc(-1 * clamp(24px,4.4vw,64px));padding:2px clamp(24px,4.4vw,64px) 6px}
  .chips::-webkit-scrollbar{display:none}
}
.quote{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:14px;margin-top:28px}
@media (max-width:860px){.quote{grid-template-columns:minmax(0,1fr)}}
.mv{border-radius:var(--r-card);background:var(--ink);color:#f4f4f2;padding:clamp(26px,3vw,40px);display:flex;flex-direction:column;gap:16px;min-width:0}
.mv h3{margin:0;font-weight:500;font-size:clamp(30px,3vw,42px);line-height:1.02;letter-spacing:-.04em}
.mv p{margin:0;color:#bdbdc2}
.mv .lbl{margin-top:10px;font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:#8f8f96}
.mv ul{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.mv li{display:flex;gap:12px;align-items:flex-start;font-size:16px}
.mv li svg{flex:none;margin-top:2px}
.mv .mv-foot{margin-top:auto;padding-top:18px;border-top:1px solid #2a2a2e;font:500 12px/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:#8f8f96}
.mv.swap #mvTitle,.mv.swap #mvLine,.mv.swap #mvInc{animation:swap .45s var(--ease)}
@keyframes swap{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.form{border-radius:var(--r-card);background:#fff;padding:clamp(26px,3vw,40px);display:flex;flex-direction:column;gap:18px;min-width:0}
.form .lbl{margin:0;font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:14px}
.form label{display:flex;flex-direction:column;gap:7px;font-size:13px;font-weight:600;color:#3d3d42}
.form input{min-height:54px;padding:0 16px;border-radius:var(--r-ctl);border:1px solid var(--line);background:var(--surface);color:var(--ink);font:400 16px var(--sans);width:100%;transition:border-color .2s,background-color .2s,box-shadow .2s}
.form input:hover{border-color:#cfcfca}
.form input:focus{border-color:var(--ink);background:#fff;outline:none;box-shadow:0 0 0 4px rgba(255,107,26,.18)}
.form input::placeholder{color:#8e8e93}
.form .btn{justify-content:space-between;min-height:60px;margin-top:4px}
.note{margin:0;font-size:13px;color:var(--mute)}

/* booking: calendar, arrival window, summary, confirmation */
[hidden]{display:none!important}
.quote{align-items:start}
@media (min-width:861px){.mv{position:sticky;top:96px}}
.mv .sum{margin:auto 0 0;padding-top:18px;border-top:1px solid #2a2a2e;display:grid;gap:12px}
.mv .sum div{display:flex;justify-content:space-between;align-items:baseline;gap:16px}
.mv .sum dt{font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:#8f8f96}
.mv .sum dd{margin:0;font-weight:500;text-align:right;color:#8f8f96}
.mv .sum dd.set{color:#fff}
.mv .sum + .mv-foot{margin-top:18px}
.form .blk{display:flex;flex-direction:column;gap:16px}
.form .blk + .blk{padding-top:24px;border-top:1px solid var(--line)}
.form textarea{padding:14px 16px;border-radius:var(--r-ctl);border:1px solid var(--line);background:var(--surface);color:var(--ink);font:400 16px/1.45 var(--sans);width:100%;resize:vertical;min-height:84px;transition:border-color .2s,background-color .2s,box-shadow .2s}
.form textarea:hover{border-color:#cfcfca}
.form textarea:focus{border-color:var(--ink);background:#fff;outline:none;box-shadow:0 0 0 4px rgba(255,107,26,.18)}
.form textarea::placeholder{color:#8e8e93}
.hp{position:absolute!important;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none}
.verr{margin:0;padding:12px 16px;border-radius:var(--r-ctl);background:#fff1ec;color:#9a2f0a;border:1px solid #ffd2c0;font-size:14px;font-weight:500}
.btn[disabled]{opacity:.65;cursor:progress}
.form .btn.btn-line.wide{justify-content:center;gap:10px;min-height:54px;margin-top:0}
.cal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.cal-head b{font-weight:600;font-size:19px;letter-spacing:-.02em}
.cal-nav{display:flex;gap:6px}
.cal-nav button{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:#fff;display:grid;place-items:center;cursor:pointer;transition:border-color .2s,transform .2s var(--ease)}
.cal-nav button:hover:not(:disabled){border-color:var(--ink)}
.cal-nav button:active:not(:disabled){transform:scale(.94)}
.cal-nav button:disabled{opacity:.3;cursor:default}
.cal-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px}
.cal-wd{padding:6px 0;text-align:center;font:500 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.day{position:relative;height:46px;min-width:0;padding:0;border-radius:12px;border:1px solid transparent;background:var(--surface);color:var(--ink);font:500 15px var(--sans);cursor:pointer;display:grid;place-items:center;transition:background-color .2s,border-color .2s,color .2s,transform .2s var(--ease)}
.day:hover:not(:disabled){border-color:var(--ink)}
.day:active:not(:disabled){transform:scale(.94)}
.day:disabled{cursor:default}
.day.blank{background:none;border:0;pointer-events:none}
.day.off{background:none;color:#c9c9ce}
.day.closed{background:none;color:#b6b6bc}
.day.full{background:none;color:#a3a3a8;text-decoration:line-through;text-decoration-thickness:1.5px}
.day.last::after,.leg .k.last::after{content:"";position:absolute;top:5px;right:5px;width:6px;height:6px;border-radius:50%;background:var(--orange)}
.day.sel{background:var(--ink);border-color:var(--ink);color:#fff}
.cal-msg{margin:0;padding:38px 8px;text-align:center;color:var(--mute);font-size:15px}
.cal-msg.err{color:#9a2f0a}
.leg{display:flex;flex-wrap:wrap;gap:8px 18px;margin:14px 0 0;padding:0;list-style:none;font:500 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.leg li{display:flex;align-items:center;gap:7px}
.leg .k{position:relative;display:inline-block;width:16px;height:16px;border-radius:5px;background:var(--surface)}
.leg .k.last::after{top:2px;right:2px;width:5px;height:5px}
.leg .k.full{background:none;border:1px solid var(--line)}
.leg .k.full::before{content:"";position:absolute;left:1px;right:1px;top:50%;height:1.5px;background:#a3a3a8}
.leg .k.closed{background:none;border:1px dashed #d6d6d1}
.win{display:flex;flex-direction:column;gap:10px;margin-top:20px}
.win-opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.win-opts button{min-height:64px;padding:10px 16px;border-radius:var(--r-ctl);border:1px solid var(--line);background:#fff;text-align:left;cursor:pointer;display:flex;flex-direction:column;justify-content:center;gap:4px;transition:background-color .2s,border-color .2s,color .2s}
.win-opts button b{font-weight:600;font-size:15px}
.win-opts button span{font:500 12px/1 var(--mono);letter-spacing:.04em;color:var(--mute)}
.win-opts button:hover:not(:disabled){border-color:var(--ink)}
.win-opts button[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}
.win-opts button[aria-pressed="true"] span{color:#b5b5ba}
.win-opts button:disabled{opacity:.4;cursor:default;text-decoration:line-through}
.win-note{margin:0;font-size:14px;color:var(--mute)}
.win-note b{color:var(--ink);font-weight:600}
.okc{border-radius:var(--r-card);background:#fff;padding:clamp(26px,3vw,44px);display:flex;flex-direction:column;gap:18px;min-width:0}
.okc .tick{display:grid;place-items:center;width:56px;height:56px;border-radius:50%;background:var(--orange)}
.okc h3{margin:0;font-weight:500;font-size:clamp(36px,4vw,54px);line-height:1;letter-spacing:-.045em}
.okc p{margin:0;color:var(--mute);max-width:34em}
.okc dl{margin:6px 0 0;padding:4px 20px;border-radius:18px;background:var(--surface)}
.okc dl div{display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px dashed #cfcfca}
.okc dl div:last-child{border-bottom:0}
.okc dt{font:500 12px/1.5 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.okc dd{margin:0;font-weight:500;text-align:right}
.okc dd.code{font-family:var(--mono);letter-spacing:.06em}
.okc .acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.okc .btn-line{min-height:52px}
@media (max-width:520px){
  .panel{padding:16px}
  .form,.mv,.okc{padding:20px}
  .chips{margin-inline:-16px;padding-inline:16px}
  .cal-grid{gap:4px}
  .day{height:44px}
  .win-opts{grid-template-columns:minmax(0,1fr)}
  .okc dl{padding:2px 16px}
}

/* how */
.how{padding-bottom:clamp(80px,10vw,140px)}
.how-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px 56px;align-items:end}
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:48px}
.step{border-radius:var(--r-card);background:var(--surface);padding:28px;display:flex;flex-direction:column;gap:10px;min-height:250px}
.step .n{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:#fff;font:500 14px var(--mono);margin-bottom:auto}
.step:nth-child(2) .n{background:var(--orange)}
.step:nth-child(3){background:var(--ink);color:#fff}
.step:nth-child(3) .n{background:var(--orange);color:var(--ink)}
.step:nth-child(3) p{color:#b5b5ba}
.step h3{margin:28px 0 0;font-weight:500;font-size:28px;letter-spacing:-.03em;line-height:1.05}
.step p{margin:0;color:var(--mute);font-size:15px}
@media (max-width:860px){.how-head{grid-template-columns:minmax(0,1fr)}.steps{grid-template-columns:minmax(0,1fr)}.step{min-height:0}}

/* faq */
.faq{padding-bottom:clamp(80px,10vw,140px)}
.faq-wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:40px 64px;align-items:start}
@media (max-width:860px){.faq-wrap{grid-template-columns:minmax(0,1fr)}}
.faq-list{display:flex;flex-direction:column;gap:8px}
.faq-item{border-radius:18px;background:var(--surface);padding:0 22px;transition:background-color .25s}
.faq-item[open]{background:#fff;box-shadow:inset 0 0 0 1px var(--line)}
.faq-item summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:20px 0;font-size:17px;font-weight:600;letter-spacing:-.01em}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:"";flex:none;width:30px;height:30px;border-radius:50%;background:#fff linear-gradient(currentColor,currentColor) center/11px 1.6px no-repeat;box-shadow:inset 0 0 0 1px var(--line);transition:transform .35s var(--ease)}
.faq-item:not([open]) summary::after{background:linear-gradient(currentColor,currentColor) center/11px 1.6px no-repeat,linear-gradient(currentColor,currentColor) center/1.6px 11px no-repeat,#fff}
.faq-item[open] summary::after{background-color:var(--orange);box-shadow:none;transform:rotate(180deg)}
.faq-item p{margin:-4px 0 22px;color:var(--mute);max-width:62ch}
.faq-item[open] p{animation:drop .4s var(--ease)}
@keyframes drop{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}

/* end CTA */
.end .frame{min-height:clamp(560px,80svh,780px);display:flex;flex-direction:column;justify-content:flex-end;color:#fff;background:#222}
.end .frame>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 35%;z-index:-2}
.end .frame::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(13,13,15,.45),rgba(13,13,15,.68) 45%,rgba(13,13,15,.88))}
.end-in{padding:clamp(28px,4vw,56px);display:flex;flex-direction:column;gap:32px}
.end h2{margin:0 auto;text-align:center;font-weight:500;font-size:clamp(44px,6.4vw,100px);line-height:.98;letter-spacing:-.055em}
.end h2 span{display:block}
.end h2 .o{color:var(--orange)}
.end .lede{margin:0 auto;text-align:center;color:rgba(255,255,255,.82)}
.ecards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;max-width:980px;width:100%;margin:0 auto}
.ecard{background:#fff;color:var(--ink);border-radius:22px;padding:22px;display:flex;flex-direction:column;gap:10px;text-decoration:none;transition:transform .4s var(--ease),box-shadow .3s}
.ecard:hover{transform:translateY(-4px);box-shadow:0 20px 40px -20px rgba(0,0,0,.6)}
.ecard .ic{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;background:var(--orange);color:var(--ink)}
.ecard b{font-size:19px;font-weight:600;letter-spacing:-.02em;margin-top:8px}
.ecard span{font-size:14px;color:var(--mute)}
.ecard .go{margin-top:auto;padding-top:8px;display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:600}
.ecard .go .arr{transition:transform .35s var(--ease)}
.ecard:hover .go .arr{transform:translateX(4px)}
@media (max-width:860px){.ecards{grid-template-columns:minmax(0,1fr)}}
footer{padding-block:28px calc(36px + env(safe-area-inset-bottom,0px))}
.foot{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px;font-size:14px;color:var(--mute)}
.foot nav{display:flex;flex-wrap:wrap;gap:18px}
.foot a{color:var(--ink);text-decoration:none}
.foot a:hover{color:var(--orange-ink)}

/* floating WhatsApp */
.fab{position:fixed;right:calc(18px + env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:30;width:58px;height:58px;border-radius:50%;background:var(--orange);color:var(--ink);display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px -8px rgba(0,0,0,.45);opacity:0;transform:translateY(16px) scale(.9);pointer-events:none;transition:opacity .25s ease,transform .25s ease}
.fab.show{opacity:1;transform:none;pointer-events:auto}
.fab svg{width:27px;height:27px;transition:transform .35s var(--ease)}
.fab:hover svg{transform:rotate(-10deg)}

/* scroll reveal: the resting state is visible; only position animates */
.js .rv{transform:translateY(36px);transition:transform 1s var(--ease)}
.js .rv.in{transform:none}

@media (prefers-reduced-motion:reduce){
  .hero .frame>img,.fcard,.mq-track,.marker,.faq-item[open] p,.mv.swap #mvTitle,.mv.swap #mvLine,.mv.swap #mvInc{animation:none}
  .hero .frame>img{transform:none}
  .load{height:auto}.load-stage{position:relative;height:auto}.load .frame{min-height:620px}
  .btn,.btn .dot,.card img,.b-photo img,.menu,.fab,.ecard{transition:none}
  .js .rv{transform:none}
  .rail{scroll-behavior:auto}
}
'''

BODY = r'''
<a class="skip" href="#quote">Skip to quote</a>
<header class="nav edge">
<div class="nav-in">
<a class="brand" href="#top" aria-label="Shammah Moving"><img src="assets/logo-160.png" alt="" width="34" height="34"><b>SHAMMAH</b></a>
<nav class="links" aria-label="Main">
<a href="#about" data-i18n="aboutEyebrow">{{aboutEyebrow}}</a>
<a href="#services" data-i18n="navServices">{{navServices}}</a>
<a href="#how" data-i18n="navHow">{{navHow}}</a>
<a href="#faq" data-i18n="navFaq">{{navFaq}}</a>
</nav>
<div class="nav-r">
<div class="lang" role="group" aria-label="{{langAria}}" data-i18n-aria="langAria">
<button type="button" data-lang="en" aria-pressed="true">EN</button>
<button type="button" data-lang="pt" aria-pressed="false">PT</button>
</div>
<a class="btn btn-o" href="#quote"><span data-i18n="navQuote">{{navQuote}}</span><span class="dot">%%ARR%%</span></a>
<button type="button" class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menu" aria-label="{{menu}}"><span></span><span></span></button>
</div>
</div>
</header>
<div class="menu wrap" id="menu" hidden>
<nav aria-label="Mobile">
<a href="#about" data-i18n="aboutEyebrow">{{aboutEyebrow}}</a>
<a href="#services" data-i18n="navServices">{{navServices}}</a>
<a href="#quote" data-i18n="navQuote">{{navQuote}}</a>
<a href="#how" data-i18n="navHow">{{navHow}}</a>
<a href="#faq" data-i18n="navFaq">{{navFaq}}</a>
</nav>
<a class="btn btn-o js-wa" href="https://wa.me/%%WA%%" target="_blank" rel="noopener"><span data-i18n="ctaWa">{{ctaWa}}</span><span class="dot">%%ICON_WA%%</span></a>
</div>

<main id="top">
<section class="hero edge" aria-label="Shammah Moving">
<div class="frame">
<img src="assets/windermere.webp" width="1600" height="1145" alt="{{heroAlt}}" data-i18n-alt="heroAlt" fetchpriority="high" decoding="async">
<span class="hero-pin">Windermere, FL</span>
<div class="hero-social"><a href="%%IG%%" target="_blank" rel="noopener">Instagram %%ARR_UP%%</a><a class="js-wa" href="https://wa.me/%%WA%%" target="_blank" rel="noopener">WhatsApp %%ARR_UP%%</a></div>
<div class="hero-body">
<div>
<ul class="hero-tags"><li data-i18n="tLocal">{{tLocal}}</li><li data-i18n="tInter">{{tInter}}</li><li data-i18n="tIntl">{{tIntl}}</li></ul>
<h1><span data-i18n="heroA">{{heroA}}</span><span class="o" data-i18n="heroB">{{heroB}}</span></h1>
<p class="lede" data-i18n="heroSub">{{heroSub}}</p>
<div class="ctas">
<a class="btn btn-o js-wa" href="https://wa.me/%%WA%%" target="_blank" rel="noopener"><span data-i18n="ctaWa">{{ctaWa}}</span><span class="dot">%%ICON_WA%%</span></a>
<a class="btn btn-glass" href="#quote" data-i18n="ctaQuote">{{ctaQuote}}</a>
</div>
</div>
<div class="floats">
<div class="fcard"><span class="ic">EN·PT</span><b data-i18n="hc1T">{{hc1T}}</b><span data-i18n="hc1D">{{hc1D}}</span></div>
<div class="fcard"><span class="ic dk">%%ICON_TRUCK_SM%%</span><b data-i18n="hc2T">{{hc2T}}</b><span data-i18n="hc2D">{{hc2D}}</span></div>
</div>
</div>
</div>
</section>

<div class="mq" aria-label="{{navServices}}" data-i18n-aria="navServices"><div class="mq-track">%%MARQUEE%%</div></div>

<section class="about wrap" id="about">
<p class="eyebrow" data-i18n="aboutEyebrow">{{aboutEyebrow}}</p>
<h2 class="statement"><span data-i18n="ab1">{{ab1}}</span> <span class="ipill">%%ICON_TRUCK%%</span> <span data-i18n="ab2">{{ab2}}</span> <span class="m" data-i18n="ab3">{{ab3}}</span> <span class="ipill dk">%%ICON_PLANE%%</span> <span class="m" data-i18n="ab4">{{ab4}}</span></h2>
</section>
<div class="bento wrap">
<article class="b b-photo rv">
<img src="assets/packing.webp" width="1100" height="728" alt="" loading="lazy" decoding="async">
<span class="tag">Windermere, FL</span>
<div class="inner"><span class="lbl" data-i18n="fEst">{{fEst}}</span><span class="big">2008</span><p data-i18n="f1b">{{f1b}}</p></div>
</article>
<article class="b b-moves rv">
<div><span class="lbl" data-i18n="qGroup">{{qGroup}}</span><div class="big" style="margin-top:14px">11</div><p style="margin-top:10px" data-i18n="b11">{{b11}}</p></div>
<ul class="mini" id="miniMoves">%%MINI%%</ul>
</article>
<article class="b b-lang rv">
<span class="lbl" data-i18n="langAria">{{langAria}}</span>
<span class="big">EN · PT</span>
<p data-i18n="bLang">{{bLang}}</p>
</article>
<article class="b b-dot rv">
<div><span class="lbl">USDOT</span><div class="num" style="margin-top:12px">1547896</div><p style="margin-top:10px;color:#b5b5ba" data-i18n="f2b">{{f2b}}</p></div>
<a href="%%FMCSA%%" target="_blank" rel="noopener"><span data-i18n="verify">{{verify}}</span>%%ARR%%</a>
</article>
</div>

<section class="load edge" id="load" aria-labelledby="loadH">
<div class="load-stage">
<div class="frame">
<div class="load-head">
<div class="load-copy" id="copyA"><p class="eyebrow" data-i18n="loadEyebrow">{{loadEyebrow}}</p><h2 id="loadH"><span data-i18n="loadA">{{loadA}}</span><span class="o" data-i18n="loadB">{{loadB}}</span></h2></div>
<div class="load-copy alt" id="copyB" aria-hidden="true"><h2><span data-i18n="packedA">{{packedA}}</span><span class="o" data-i18n="packedB">{{packedB}}</span></h2></div>
</div>
<div class="rig-wrap">%%TRUCK%%</div>
<div class="hud" aria-hidden="true"><b id="hudLabel">{{hudLoading}}</b><span id="hudCount">00/11</span><span class="hud-bar"><i id="hudBar"></i></span></div>
</div>
</div>
</section>

<section class="svc wrap" id="services" aria-labelledby="svcH">
<div class="svc-grid">
<div class="svc-side">
<div><p class="eyebrow" data-i18n="navServices">{{navServices}}</p><h2 class="h2" id="svcH" data-i18n="svcTitle">{{svcTitle}}</h2><p class="lede" data-i18n="svcLead">{{svcLead}}</p></div>
<div class="arrows"><button type="button" id="prev" aria-label="{{prev}}" data-i18n-aria="prev">%%ARR_L%%</button><button type="button" id="next" aria-label="{{next}}" data-i18n-aria="next">%%ARR_R%%</button></div>
</div>
<div class="rail" id="rail">
%%CARDS%%
</div>
</div>
<div class="also">
<h3 data-i18n="alsoTitle">{{alsoTitle}}</h3>
%%ALSO%%
</div>
</section>

<section class="quote-sec edge" id="quote">
<div class="panel">
<div class="q-head">
<p class="eyebrow" data-i18n="qTitle">{{qTitle}}</p>
<h2 class="h2" data-i18n="qH3">{{qH3}}</h2>
<p class="lede" data-i18n="qSub">{{qSub}}</p>
</div>
<ol class="qsteps" aria-hidden="true">
<li class="done" id="qs1"><b>1</b><span data-i18n="st1">{{st1}}</span></li>
<li id="qs2"><b>2</b><span data-i18n="st2">{{st2}}</span></li>
<li id="qs3"><b>3</b><span data-i18n="st3">{{st3}}</span></li>
<li id="qs4"><b>4</b><span data-i18n="st4">{{st4}}</span></li>
</ol>
<div class="chips" id="moves" role="group" aria-label="{{qGroup}}" data-i18n-aria="qGroup">
%%MOVES%%
</div>
<div class="quote">
<div class="mv" id="mv" aria-live="polite">
<h3 id="mvTitle">%%MV_TITLE%%</h3>
<p id="mvLine">%%MV_LINE%%</p>
<p class="lbl" data-i18n="mvInc">{{mvInc}}</p>
<ul id="mvInc">%%MV_INC%%</ul>
<dl class="sum" aria-live="polite">
<div><dt data-i18n="sumDate">{{sumDate}}</dt><dd id="sumDate">—</dd></div>
<div><dt data-i18n="sumArrive">{{sumArrive}}</dt><dd id="sumArr">—</dd></div>
</dl>
<p class="mv-foot" data-i18n="mvFoot">{{mvFoot}}</p>
</div>
<form class="form" id="qform" novalidate>
<div class="blk">
<p class="lbl" data-i18n="bkDate">{{bkDate}}</p>
<div class="cal" id="cal"><p class="cal-msg" data-i18n="calLoad">{{calLoad}}</p></div>
<div class="win" id="win" hidden></div>
</div>
<div class="blk">
<p class="lbl" data-i18n="qDetails">{{qDetails}}</p>
<div class="row">
<label for="fName"><span data-i18n="lName">{{lName}}</span><input type="text" id="fName" name="name" autocomplete="name" maxlength="120" placeholder="{{phName}}" data-i18n-ph="phName"></label>
<label for="fPhone"><span data-i18n="lPhone">{{lPhone}}</span><input type="tel" id="fPhone" name="phone" autocomplete="tel" inputmode="tel" maxlength="30" placeholder="{{phPhone}}" data-i18n-ph="phPhone"></label>
</div>
<label for="fEmail"><span data-i18n="lEmail">{{lEmail}}</span><input type="email" id="fEmail" name="email" autocomplete="email" maxlength="160" placeholder="{{phEmail}}" data-i18n-ph="phEmail"></label>
<div class="row">
<label for="fFrom"><span data-i18n="lFrom">{{lFrom}}</span><input type="text" id="fFrom" name="from" autocomplete="address-level2" maxlength="300" placeholder="{{phFrom}}" data-i18n-ph="phFrom"></label>
<label for="fTo"><span data-i18n="lTo">{{lTo}}</span><input type="text" id="fTo" name="to" maxlength="300" placeholder="{{phTo}}" data-i18n-ph="phTo"></label>
</div>
<!--INV-->
<div class="inv" id="inv" aria-labelledby="invH"><p class="lbl" id="invH">O que vai na mudança · What's going</p><p class="inv-hint" id="invHint">Quantidades aproximadas. Pode pular o que não souber.</p><div id="invList"></div></div>
<style>
.inv{margin:6px 0 4px;padding:18px;border-radius:20px;background:var(--surface)}
.inv .lbl{margin:0 0 4px}
.inv-hint{margin:0 0 14px;color:var(--mute);font-size:14px}
.inv-grp{padding:12px 0;border-top:1px solid var(--line)}
.inv-grp:first-of-type{border-top:0;padding-top:0}
.inv-grp h4{margin:0 0 6px;font:500 11px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.inv-row{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;font-size:15px}
.inv-row span{min-width:0;overflow-wrap:anywhere}
.inv-step{display:inline-flex;align-items:center;gap:0;flex:none;border-radius:999px;background:#fff;border:1px solid var(--line)}
.inv-step button{width:40px;height:40px;border:0;background:transparent;font-size:18px;cursor:pointer;color:var(--ink);border-radius:999px}
.inv-step button:hover{background:var(--surface)}
.inv-step button:disabled{opacity:.35;cursor:default}
.inv-step output{min-width:28px;text-align:center;font:500 15px var(--mono)}
</style>
<!--/INV-->
<label for="fDetails"><span data-i18n="lDetails">{{lDetails}}</span><input type="text" name="details" id="fDetails" maxlength="500" placeholder="%%MV_PH%%"></label>
<label for="fNotes"><span data-i18n="lNotes">{{lNotes}}</span><textarea name="notes" id="fNotes" rows="2" maxlength="1000" placeholder="{{phNotes}}" data-i18n-ph="phNotes"></textarea></label>
<input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
</div>
<p class="verr" id="formErr" role="alert" hidden></p>
<button type="submit" class="btn btn-ink" id="bookBtn"><span id="bookTxt" data-i18n="bookBtn">{{bookBtn}}</span><span class="dot">%%ARR%%</span></button>
<a class="btn btn-line wide" id="waMove" href="https://wa.me/%%WA%%" target="_blank" rel="noopener"><span data-i18n="sendWa">{{sendWa}}</span>%%ICON_WA%%</a>
<p class="note" data-i18n="sendNote">{{sendNote}}</p>
</form>
<div class="okc" id="done" hidden aria-live="polite"></div>
</div>
</div>
</section>

<section class="how wrap" id="how">
<div class="how-head">
<div><p class="eyebrow" data-i18n="navHow">{{navHow}}</p><h2 class="h2" data-i18n="howTitle">{{howTitle}}</h2></div>
</div>
<div class="steps">
<div class="step rv"><span class="n">01</span><h3 data-i18n="h1t">{{h1t}}</h3><p data-i18n="h1d">{{h1d}}</p></div>
<div class="step rv"><span class="n">02</span><h3 data-i18n="h2t">{{h2t}}</h3><p data-i18n="h2d">{{h2d}}</p></div>
<div class="step rv"><span class="n">03</span><h3 data-i18n="h3t">{{h3t}}</h3><p data-i18n="h3d">{{h3d}}</p></div>
</div>
</section>

<section class="faq wrap" id="faq">
<div class="faq-wrap">
<div><p class="eyebrow" data-i18n="navFaq">{{navFaq}}</p><h2 class="h2" data-i18n="faqTitle">{{faqTitle}}</h2></div>
<div class="faq-list">
%%FAQ%%
</div>
</div>
</section>

<section class="end edge" aria-labelledby="endH">
<div class="frame">
<img src="assets/freight.webp" width="1100" height="728" alt="" loading="lazy" decoding="async">
<div class="end-in">
<h2 id="endH"><span data-i18n="endA">{{endA}}</span><span class="o" data-i18n="endB">{{endB}}</span></h2>
<p class="lede" data-i18n="endSub">{{endSub}}</p>
<div class="ecards">
<a class="ecard js-wa" href="https://wa.me/%%WA%%" target="_blank" rel="noopener"><span class="ic">%%ICON_WA%%</span><b>WhatsApp</b><span data-i18n="endC1D">{{endC1D}}</span><span class="go"><span data-i18n="open">{{open}}</span>%%ARR%%</span></a>
<a class="ecard" href="tel:%%PHONE%%"><span class="ic">%%ICON_PHONE%%</span><b>%%PHONE_LABEL%%</b><span data-i18n="endC2D">{{endC2D}}</span><span class="go"><span data-i18n="call">{{call}}</span>%%ARR%%</span></a>
<a class="ecard" href="%%IG%%" target="_blank" rel="noopener"><span class="ic">%%ICON_IG%%</span><b>@shammahmoving</b><span data-i18n="endC3D">{{endC3D}}</span><span class="go"><span data-i18n="open">{{open}}</span>%%ARR%%</span></a>
</div>
</div>
</div>
</section>
</main>

<footer class="wrap">
<div class="foot">
<span data-i18n="footRights">{{footRights}}</span>
<nav aria-label="Contact">
<a href="mailto:%%EMAIL%%">%%EMAIL%%</a>
<a href="tel:%%PHONE%%">%%PHONE_LABEL%%</a>
<a href="%%IG%%" target="_blank" rel="noopener">Instagram</a>
<a class="js-wa" href="https://wa.me/%%WA%%" target="_blank" rel="noopener">WhatsApp</a>
</nav>
</div>
</footer>

<a class="fab js-wa" id="fab" href="https://wa.me/%%WA%%" target="_blank" rel="noopener" aria-label="{{fabAria}}" data-i18n-aria="fabAria">%%ICON_WA%%</a>
'''

JS = r'''
(function () {
  document.documentElement.classList.add("js");
  var WA = "%%WA%%";
  var T = %%T%%;
  var MOVES = %%MOVES_JSON%%;
  var CHECK = %%CHECK%%;
  var ITEMS = %%ITEMS%%;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  var state = { lang: "en", move: "house", date: null, win: null, month: null, inv: {} };
  var INV = [
    { room: "bed", en: "Bedrooms", pt: "Quartos", items: [["bed_double", "Double bed set (bed, nightstands, dresser)", "Cama de casal (cama, criados, cômoda)"], ["bed_single", "Single bed set", "Cama de solteiro"], ["bed_wardrobe", "Wardrobe", "Guarda-roupa"], ["bed_kid", "Kids' room set (bed or crib, dresser)", "Quarto infantil (cama ou berço, cômoda)"]] },
    { room: "kitchen", en: "Kitchen", pt: "Cozinha", items: [["k_fridge", "Refrigerator", "Geladeira"], ["k_stove", "Stove / oven", "Fogão / forno"], ["k_dish", "Dishwasher", "Lava-louças"], ["k_table4", "Dining table (4 seats)", "Mesa de jantar (4 lugares)"], ["k_table6", "Dining table (6+ seats)", "Mesa de jantar (6+ lugares)"], ["k_boxes", "Kitchen boxes (approx.)", "Caixas de cozinha (aprox.)"]] },
    { room: "living", en: "Living room", pt: "Sala", items: [["l_sofa", "Sofa (2–3 seats)", "Sofá (2–3 lugares)"], ["l_sofa_big", "Large sofa (4+ seats)", "Sofá grande (4+ lugares)"], ["l_armchair", "Armchair", "Poltrona"], ["l_tv", "TV and stand", "TV e rack"], ["l_coffee", "Coffee table", "Mesa de centro"], ["l_shelf", "Bookshelf / cabinet", "Estante / armário"]] },
    { room: "other", en: "Other", pt: "Outros", items: [["o_laundry", "Washer / dryer", "Lavadora / secadora"], ["o_office", "Office desk and chair", "Mesa e cadeira de escritório"], ["o_piano", "Piano", "Piano"], ["o_boxes", "Extra boxes (approx.)", "Caixas extras (aprox.)"]] }
  ];
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function sm(x) { x = cl(x); return x * x * (3 - 2 * x); }
  function eio(x) { x = cl(x); return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
  function pad(v) { return (v < 10 ? "0" : "") + v; }

  /* ---------- language + booking ---------- */
  var form = $("#qform"), mv = $("#mv"), menuBtn = $("#menuBtn"), menu = $("#menu"), doneEl = $("#done");
  var hudText = "";
  var SPAN = %%SPAN%%;
  var ARR = %%JARR%%, ARR_L = %%JARR_L%%, ARR_R = %%JARR_R%%, ICON_WA = %%JICON_WA%%;
  var TICK = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#121214" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  /* dates are business dates in Florida (America/New_York) */
  var TZ = "America/New_York";
  var DT = {
    today: function () { return new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(new Date()); },
    addDays: function (ds, n) { var d = new Date(ds + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); },
    dow: function (ds) { return new Date(ds + "T12:00:00Z").getUTCDay(); },
    fmt: function (ds, lang, o) { return new Intl.DateTimeFormat(lang === "pt" ? "pt-BR" : "en-US", Object.assign({ timeZone: "UTC" }, o)).format(new Date(ds + "T12:00:00Z")); },
    longDate: function (ds, lang) { return DT.fmt(ds, lang, { weekday: "long", month: "long", day: "numeric", year: "numeric" }); }
  };
  var cfg = { wa: WA, morning: "8–10 AM", afternoon: "1–3 PM" };
  var avail = {}, loading = true, failed = false, booked = null, focusAfter = null;
  function wa(text) { return "https://wa.me/" + cfg.wa + "?text=" + encodeURIComponent(text); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function tpl(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function pad2(v) { return (v < 10 ? "0" : "") + v; }
  function up(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function mvOf(id) { var l = MOVES[state.lang]; for (var i = 0; i < l.length; i++) if (l[i].id === id) return l[i]; return l[0]; }
  function cur() { return mvOf(state.move); }
  function isHalf(id) { return SPAN[id] === "half"; }
  function winLabel(w) { return w === "afternoon" ? cfg.afternoon : cfg.morning; }
  function A() { return avail[state.move]; }
  function fmtDate(v) { var p = v.split("-"); if (p.length !== 3) return v; return state.lang === "pt" ? p[2] + "/" + p[1] + "/" + p[0] : p[1] + "/" + p[2] + "/" + p[0]; }

  function renderMove(animate) {
    var m = cur();
    $$("#moves .chip").forEach(function (b) {
      b.textContent = mvOf(b.dataset.move).label;
      b.setAttribute("aria-pressed", b.dataset.move === state.move ? "true" : "false");
    });
    $("#mvTitle").textContent = m.title;
    $("#mvLine").textContent = m.line;
    $("#mvInc").innerHTML = m.inc.map(function (x) { return "<li>" + CHECK + "<span>" + esc(x) + "</span></li>"; }).join("");
    $("#fDetails").placeholder = m.ph;
    if (animate && !reduce) { mv.classList.remove("swap"); void mv.offsetWidth; mv.classList.add("swap"); }
    updateQuote();
  }
  function updateQuote() {
    var t = T[state.lang], m = cur(), f = form.elements;
    var lines = [t.msgHi, t.msgType + ": " + m.title];
    if (f.from.value.trim()) lines.push(t.msgFrom + ": " + f.from.value.trim());
    if (f.to.value.trim()) lines.push(t.msgTo + ": " + f.to.value.trim());
    if (state.date) lines.push(t.msgDate + ": " + fmtDate(state.date));
    if (f.details.value.trim()) lines.push(t.msgDet + ": " + f.details.value.trim());
    $("#waMove").href = wa(lines.join("\n"));
  }
  function updateSteps() {
    var f = form.elements, ok = state.date && (!isHalf(state.move) || state.win);
    $("#qs2").classList.toggle("done", !!ok);
    $("#qs3").classList.toggle("done", !!(f.name.value.trim() && f.phone.value.replace(/\D/g, "").length >= 10));
    $("#qs4").classList.toggle("done", !!booked);
  }
  function showErr(msg) { var el = $("#formErr"); el.textContent = msg || ""; el.hidden = !msg; }

  /* the date is a preference: every day from tomorrow on, morning or afternoon. The team confirms availability on WhatsApp. */
  function loadAvail() {
    var id = state.move;
    if (avail[id]) { loading = false; failed = false; afterAvail(); return; }
    var first = DT.addDays(DT.today(), 1), last = DT.addDays(first, 179), map = {}, d = first;
    while (d <= last) { map[d] = { d: d, s: "open", w: ["morning", "afternoon"], lo: false }; d = DT.addDays(d, 1); }
    avail[id] = { map: map, first: first, firstDay: first, lastDay: last };
    loading = false; failed = false; afterAvail();
  }
  function afterAvail() {
    var a = A();
    if (a && a.firstDay && !state.month) state.month = (a.first || a.firstDay).slice(0, 7);
    renderCal(); renderWin(); renderSum(); updateSteps();
  }
  function renderCal() {
    var box = $("#cal"), t = T[state.lang], a = A();
    if (loading) { box.innerHTML = '<p class="cal-msg">' + esc(t.calLoad) + "</p>"; return; }
    if (failed || !a || !a.firstDay || !state.month) { box.innerHTML = '<p class="cal-msg err">' + esc(t.calFail) + "</p>"; return; }
    var ym = state.month, y = +ym.slice(0, 4), mo = +ym.slice(5, 7);
    var lead = DT.dow(ym + "-01"), days = new Date(Date.UTC(y, mo, 0)).getUTCDate();
    var minM = a.firstDay.slice(0, 7), maxM = a.lastDay.slice(0, 7), i, d;
    var h = '<div class="cal-head"><b>' + esc(up(DT.fmt(ym + "-01", state.lang, { month: "long", year: "numeric" }))) + '</b><div class="cal-nav">' +
      '<button type="button" data-nav="-1" aria-label="' + esc(t.calPrev) + '"' + (ym <= minM ? " disabled" : "") + ">" + ARR_L + "</button>" +
      '<button type="button" data-nav="1" aria-label="' + esc(t.calNext) + '"' + (ym >= maxM ? " disabled" : "") + ">" + ARR_R + "</button></div></div>" +
      '<div class="cal-grid">';
    for (i = 0; i < 7; i++) h += '<span class="cal-wd" aria-hidden="true">' + esc(DT.fmt("2026-11-0" + (1 + i), state.lang, { weekday: "short" }).replace(".", "").slice(0, 3)) + "</span>";
    for (i = 0; i < lead; i++) h += '<span class="day blank"></span>';
    for (d = 1; d <= days; d++) {
      var ds = ym + "-" + pad2(d), r = a.map[ds], cls = "day", dis = true, word = t.aClosed;
      if (!r) cls += " off";
      else if (r.s === "closed") cls += " closed";
      else if (r.s === "full") { cls += " full"; word = t.aFull; }
      else { dis = false; word = r.lo ? t.aLast : t.aOpen; if (r.lo) cls += " last"; }
      if (ds === state.date) cls += " sel";
      h += '<button type="button" class="' + cls + '" data-d="' + ds + '"' + (dis ? " disabled" : "") + (ds === state.date ? ' aria-pressed="true"' : "") +
        ' aria-label="' + esc(DT.longDate(ds, state.lang) + ", " + word) + '">' + d + "</button>";
    }
    box.innerHTML = h + "</div>";
    if (focusAfter) {
      var el = box.querySelector(focusAfter);
      if (el && !el.disabled) el.focus();
      focusAfter = null;
    }
  }
  function renderWin() {
    var el = $("#win"), t = T[state.lang], a = A(), r = a && state.date ? a.map[state.date] : null;
    if (!r) { el.hidden = true; el.innerHTML = ""; return; }
    el.hidden = false;
    if (!isHalf(state.move)) {
      el.innerHTML = '<p class="win-note">' + tpl(esc(t.winFull), { w: "<b>" + esc(cfg.morning) + "</b>" }) + "</p>";
      return;
    }
    var h = '<p class="lbl">' + esc(t.winH) + '</p><div class="win-opts">';
    [["morning", t.winM], ["afternoon", t.winA]].forEach(function (p) {
      var ok = r.w.indexOf(p[0]) > -1;
      h += '<button type="button" data-w="' + p[0] + '"' + (ok ? "" : " disabled") + ' aria-pressed="' + (state.win === p[0] ? "true" : "false") + '"><b>' + esc(p[1]) + "</b><span>" + esc(winLabel(p[0])) + "</span></button>";
    });
    el.innerHTML = h + "</div>";
  }
  function renderSum() {
    var t = T[state.lang], d = $("#sumDate"), ar = $("#sumArr");
    if (state.date) { d.textContent = DT.fmt(state.date, state.lang, { weekday: "short", month: "short", day: "numeric", year: "numeric" }); d.className = "set"; }
    else { d.textContent = t.sumPick; d.className = ""; }
    var ok = state.date && (!isHalf(state.move) || state.win);
    if (ok) { ar.textContent = winLabel(isHalf(state.move) ? state.win : "morning"); ar.className = "set"; }
    else { ar.textContent = "—"; ar.className = ""; }
  }
  function pickDate(ds) {
    var a = A(), r = a && a.map[ds];
    if (!r || r.s !== "open") return;
    state.date = ds;
    if (!isHalf(state.move)) state.win = "morning";
    else if (r.w.length === 1) state.win = r.w[0];
    else if (r.w.indexOf(state.win) < 0) state.win = null;
    focusAfter = '.day[data-d="' + ds + '"]';
    renderCal(); renderWin(); renderSum(); updateSteps(); updateQuote(); showErr("");
  }
  function selectMove(id) {
    state.move = id; state.date = null; state.win = null; state.month = null;
    renderMove(true); renderWin(); renderSum(); updateSteps();
    loadAvail();
  }

  $("#cal").addEventListener("click", function (ev) {
    var n = ev.target.closest("[data-nav]"), b = ev.target.closest("button.day[data-d]");
    if (n && !n.disabled) {
      var ym = state.month, y = +ym.slice(0, 4), mo = +ym.slice(5, 7) + (+n.dataset.nav);
      if (mo < 1) { mo = 12; y--; } else if (mo > 12) { mo = 1; y++; }
      state.month = y + "-" + pad2(mo);
      focusAfter = '[data-nav="' + n.dataset.nav + '"]';
      renderCal();
    } else if (b && !b.disabled) pickDate(b.dataset.d);
  });
  $("#win").addEventListener("click", function (ev) {
    var b = ev.target.closest("button[data-w]");
    if (!b || b.disabled) return;
    state.win = b.dataset.w;
    renderWin(); renderSum(); updateSteps(); showErr("");
  });

  /* the whole request becomes one WhatsApp message for the Shammah team */
  function buildRequest() {
    var t = T[state.lang], f = form.elements, m = cur(), inv = invPayload(), pt = state.lang === "pt";
    var arr = winLabel(isHalf(state.move) ? state.win : "morning");
    var L = ["*" + t.rqHead + "*", "",
      t.rqMove + ": " + m.title,
      t.rqDate + ": " + DT.fmt(state.date, state.lang, { weekday: "short", month: "short", day: "numeric", year: "numeric" }),
      t.rqArrive + ": " + (isHalf(state.move) ? (state.win === "afternoon" ? T[state.lang].winA : T[state.lang].winM) + " (" + arr + ")" : arr), "",
      t.rqName + ": " + f.name.value.trim(), t.rqPhone + ": " + f.phone.value.trim()];
    if (f.email.value.trim()) L.push(t.rqEmail + ": " + f.email.value.trim());
    L.push("");
    if (f.from.value.trim()) L.push(t.rqFrom + ": " + f.from.value.trim());
    if (f.to.value.trim()) L.push(t.rqTo + ": " + f.to.value.trim());
    if (f.details.value.trim()) L.push(t.rqSize + ": " + f.details.value.trim());
    if (inv.length) L.push(t.rqItems + ": " + inv.map(function (it) { return it.qty + "x " + (pt ? it.item_pt : it.item); }).join("; "));
    if (f.notes.value.trim()) L.push(t.rqNotes + ": " + f.notes.value.trim());
    L.push("", t.rqLang + ": " + t.rqLangV);
    return L.join("\n");
  }
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var t = T[state.lang], f = form.elements, err = "", focusEl = null;
    if (f.website.value) return;
    if (!state.date) { err = t.vDate; focusEl = $("#cal .day:not(:disabled)"); }
    else if (isHalf(state.move) && !state.win) { err = t.vWin; focusEl = $("#win button:not(:disabled)"); }
    else if (!f.name.value.trim()) { err = t.vName; focusEl = f.name; }
    else if (f.phone.value.replace(/\D/g, "").length < 10) { err = t.vPhone; focusEl = f.phone; }
    if (err) { showErr(err); if (focusEl) focusEl.focus(); return; }
    showErr("");
    booked = { type: state.move, date: state.date, win: state.win || "morning", url: wa(buildRequest()) };
    try { window.open(booked.url, "_blank"); } catch (e) {}
    showDone();
  });
  form.addEventListener("input", function () { updateQuote(); updateSteps(); });

  function renderDone() {
    if (!booked) return;
    var t = T[state.lang], m = mvOf(booked.type), dl = DT.longDate(booked.date, state.lang);
    var arr = winLabel(isHalf(booked.type) ? booked.win : "morning");
    var url = wa(buildRequest());
    function row(k, v) { return "<div><dt>" + esc(k) + "</dt><dd>" + esc(v) + "</dd></div>"; }
    doneEl.innerHTML = '<span class="tick">' + TICK + '</span><h3 id="doneH" tabindex="-1">' + esc(t.okPending) + "</h3><p>" +
      esc(tpl(t.okSubPending, { d: dl })) + "</p><dl>" +
      row(t.okType, m.title) + row(t.okDate, dl) + row(t.okArrive, arr) + "</dl>" +
      '<div class="acts"><a class="btn btn-ink" href="' + esc(url) + '" target="_blank" rel="noopener"><span>' + esc(t.okWa) + '</span><span class="dot">' + ICON_WA + "</span></a>" +
      '<button type="button" class="btn btn-line" id="again">' + esc(t.okAgain) + "</button></div>";
  }
  function showDone() {
    form.hidden = true; doneEl.hidden = false;
    renderDone(); updateSteps();
    var h = $("#doneH"); if (h) h.focus({ preventScroll: true });
    $("#quote").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  }
  doneEl.addEventListener("click", function (ev) {
    if (!ev.target.closest("#again")) return;
    booked = null; form.reset(); state.date = null; state.win = null; state.month = null; state.inv = {};
    doneEl.hidden = true; doneEl.innerHTML = ""; form.hidden = false;
    renderMove(false); renderWin(); renderSum(); updateSteps(); showErr(""); renderInv();
    loadAvail();
    $("#quote").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  });

  function invCount(id) { return state.inv[id] || 0; }
  function renderInv() {
    if (!$("#invList")) return;
    var lg = state.lang, pt = lg === "pt";
    $("#invH").textContent = pt ? "O que vai na mudança" : "What's going";
    $("#invHint").textContent = pt ? "Quantidades aproximadas. Pode pular o que não souber." : "Rough counts are fine. Skip anything you're not sure about.";
    $("#invList").innerHTML = INV.map(function (g) {
      return '<div class="inv-grp"><h4>' + esc(pt ? g.pt : g.en) + "</h4>" + g.items.map(function (it) {
        var n = invCount(it[0]);
        return '<div class="inv-row"><span>' + esc(pt ? it[2] : it[1]) + '</span><div class="inv-step">' +
          '<button type="button" data-inv="' + it[0] + '" data-d="-1" aria-label="' + (pt ? "Diminuir" : "Less") + '"' + (n ? "" : " disabled") + ">&minus;</button>" +
          '<output aria-live="polite">' + n + '</output><button type="button" data-inv="' + it[0] + '" data-d="1" aria-label="' + (pt ? "Aumentar" : "More") + '"' + (n >= 9 ? " disabled" : "") + ">+</button></div></div>";
      }).join("") + "</div>";
    }).join("");
  }
  function invPayload() {
    var out = [];
    INV.forEach(function (g) {
      g.items.forEach(function (it) {
        var q = invCount(it[0]);
        if (q > 0) out.push({ room: g.room, item: it[1], item_pt: it[2], qty: q });
      });
    });
    return out;
  }
  if ($("#invList")) $("#invList").addEventListener("click", function (ev) {
    var b = ev.target.closest("button[data-inv]");
    if (!b || b.disabled) return;
    var id = b.dataset.inv, n = invCount(id) + Number(b.dataset.d);
    state.inv[id] = Math.max(0, Math.min(9, n));
    renderInv();
  });

  function setLang(l) {
    state.lang = l === "pt" ? "pt" : "en";
    var t = T[state.lang];
    document.documentElement.lang = state.lang === "pt" ? "pt-BR" : "en";
    document.title = t.metaTitle;
    var md = $('meta[name="description"]'); if (md) md.setAttribute("content", t.metaDesc);
    $$("[data-i18n]").forEach(function (el) { var v = t[el.dataset.i18n]; if (v != null) el.textContent = v; });
    $$("[data-i18n-ph]").forEach(function (el) { el.placeholder = t[el.dataset.i18nPh]; });
    $$("[data-i18n-alt]").forEach(function (el) { el.alt = t[el.dataset.i18nAlt]; });
    $$("[data-i18n-aria]").forEach(function (el) { el.setAttribute("aria-label", t[el.dataset.i18nAria]); });
    $$(".lang button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.lang === state.lang ? "true" : "false"); });
    $$(".js-wa").forEach(function (a) { a.href = wa(t.waGeneral); });
    $("#miniMoves").innerHTML = MOVES[state.lang].slice(0, 6).map(function (m) { return "<li>" + esc(m.label) + "</li>"; }).join("");
    menuBtn.setAttribute("aria-label", menuBtn.getAttribute("aria-expanded") === "true" ? t.menuClose : t.menu);
    renderMove(false); renderCal(); renderWin(); renderSum(); renderInv(); renderDone();
    hudText = "";
    queue();
    try { localStorage.setItem("shammah-lang", state.lang); } catch (e) {}
  }

  /* ---------- mobile menu ---------- */
  function setMenu(open) {
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", T[state.lang][open ? "menuClose" : "menu"]);
    if (open) {
      menu.hidden = false;
      requestAnimationFrame(function () { requestAnimationFrame(function () { menu.classList.add("open"); }); });
      document.body.style.overflow = "hidden";
    } else {
      menu.classList.remove("open");
      document.body.style.overflow = "";
      setTimeout(function () { if (!menu.classList.contains("open")) menu.hidden = true; }, reduce ? 0 : 320);
    }
  }
  menuBtn.addEventListener("click", function () { setMenu(menuBtn.getAttribute("aria-expanded") !== "true"); });
  $$("#menu a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && !menu.hidden) { setMenu(false); menuBtn.focus(); } });
  window.addEventListener("resize", function () { if (window.innerWidth > 980 && !menu.hidden) setMenu(false); });

  /* ---------- the loading truck ---------- */
  var load = $("#load"), truck = $("#truck"), ramp = $("#ramp"), shutter = $("#shutter");
  var its = $$("#items .it"), spins = $$("#truck .spin"), copyA = $("#copyA"), copyB = $("#copyB");
  var rig = $("#rig"), narrow = null, hudLabel = $("#hudLabel"), hudCount = $("#hudCount"), hudBar = $("#hudBar");
  var N = ITEMS.length, SP = .55, DUR = 1.5, LMAX = SP * (N - 1) + DUR;
  function groundY(x) { return x <= 200 ? 492 : x >= 330 ? 430 : 492 - (x - 200) * 62 / 130; }
  function pose(d, u) {
    var x2 = 338 + d.w / 2, x, y, r = 0;
    if (u < .5) {
      x = 95 + (x2 - 95) * eio(u / .5);
      y = groundY(x) - Math.abs(Math.sin(u * Math.PI * 6)) * 3;
      r = -25.5 * sm((x - 200) / 14) * (1 - sm((x - 318) / 12));
    } else {
      var b = eio((u - .5) / .5), lift = Math.max(0, Math.min(36, d.by - d.h - 172));
      x = x2 + (d.cx - x2) * b;
      y = 430 + (d.by - 430) * b - lift * Math.sin(Math.PI * b);
    }
    return [x, y, r];
  }
  function progress(el) {
    var r = el.getBoundingClientRect(), tot = r.height - window.innerHeight;
    return tot > 0 ? cl(-r.top / tot) : (r.top < 0 ? 1 : 0);
  }
  function renderLoad() {
    var nw = window.innerWidth < 761;
    if (nw !== narrow) { narrow = nw; rig.setAttribute("viewBox", nw ? "300 150 900 380" : "0 150 1280 380"); }
    var p = reduce ? 0 : progress(load);
    var L = reduce ? LMAX : LMAX * cl((p - .02) / .53), done = 0;
    for (var i = 0; i < N; i++) {
      var u = cl((L - i * SP) / DUR), g = its[i];
      if (u <= 0) { g.style.opacity = 0; continue; }
      if (u >= 1) done++;
      var q = pose(ITEMS[i], u);
      g.style.opacity = cl(u / .06);
      g.setAttribute("transform", "translate(" + q[0].toFixed(1) + " " + q[1].toFixed(1) + ") rotate(" + q[2].toFixed(2) + ")");
    }
    var rOut = sm((p - .56) / .06), c = sm((p - .6) / .14), d = cl((p - .8) / .2);
    var dx = 1500 * Math.pow(d, 2.1);
    ramp.style.opacity = 1 - rOut;
    ramp.setAttribute("transform", "translate(" + (rOut * 130).toFixed(1) + " 0)");
    shutter.setAttribute("transform", "translate(0 " + (-262 * (1 - c)).toFixed(1) + ")");
    truck.setAttribute("transform", "translate(" + dx.toFixed(1) + " 0)");
    var ang = (dx / 42) * 57.2958;
    spins.forEach(function (s) { s.setAttribute("transform", "rotate(" + ang.toFixed(1) + ")"); });
    var a = 1 - sm((p - .64) / .08), b = sm((p - .76) / .08);
    copyA.style.opacity = a; copyA.style.transform = "translateY(" + ((1 - a) * -20).toFixed(1) + "px)";
    copyB.style.opacity = b; copyB.style.transform = "translateY(" + ((1 - b) * 20).toFixed(1) + "px)";
    copyB.setAttribute("aria-hidden", b > .5 ? "false" : "true");
    var t = T[state.lang], label = d > 0 ? t.hudRoad : (c > .98 ? t.hudPacked : t.hudLoading), txt = label + "|" + done;
    if (txt !== hudText) { hudText = txt; hudLabel.textContent = label; hudCount.textContent = pad(done) + "/" + N; }
    hudBar.style.transform = "scaleX(" + (reduce ? 1 : p).toFixed(4) + ")";
  }

  /* ---------- services rail ---------- */
  var rail = $("#rail"), prev = $("#prev"), next = $("#next");
  function step() { var c = rail.querySelector(".card"); return c ? c.getBoundingClientRect().width + 14 : 300; }
  function arrows() {
    prev.disabled = rail.scrollLeft < 8;
    next.disabled = rail.scrollLeft + rail.clientWidth > rail.scrollWidth - 8;
  }
  prev.addEventListener("click", function () { rail.scrollBy({ left: -step(), behavior: reduce ? "auto" : "smooth" }); });
  next.addEventListener("click", function () { rail.scrollBy({ left: step(), behavior: reduce ? "auto" : "smooth" }); });
  rail.addEventListener("scroll", arrows, { passive: true });
  $$("[data-pick]").forEach(function (a) { a.addEventListener("click", function () { selectMove(a.dataset.pick); }); });

  /* ---------- reveal ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } });
    }, { rootMargin: "0px 0px -6% 0px" });
    $$(".rv").forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + "ms"; io.observe(el); });
  } else {
    $$(".rv").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- loop ---------- */
  var fab = $("#fab"), ticking = false;
  function frame() {
    ticking = false;
    renderLoad();
    fab.classList.toggle("show", window.scrollY > window.innerHeight * .8);
  }
  function queue() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", function () { queue(); arrows(); });

  $$(".lang button").forEach(function (b) { b.addEventListener("click", function () { setLang(b.dataset.lang); }); });
  $$("#moves .chip").forEach(function (b) { b.addEventListener("click", function () { selectMove(b.dataset.move); }); });

  var initial = "en";
  try {
    var qs = new URLSearchParams(location.search).get("lang");
    if (qs === "pt" || qs === "en") initial = qs;
    else if (localStorage.getItem("shammah-lang")) initial = localStorage.getItem("shammah-lang");
  } catch (e) {}
  setLang(initial);
  arrows();
  loadAvail();
})();
'''


def font_faces(inline):
    faces = [
        ("Barlow Condensed", "italic", 800, "barlow-condensed-latin-800-italic"),
        ("Barlow Condensed", "italic", 900, "barlow-condensed-latin-900-italic"),
        ("Geist", "normal", 400, "geist-latin-400-normal"),
        ("Geist", "normal", 500, "geist-latin-500-normal"),
        ("Geist", "normal", 600, "geist-latin-600-normal"),
        ("Geist Mono", "normal", 500, "geist-mono-latin-500-normal"),
    ]
    out = []
    for fam, style, w, f in faces:
        if inline:
            b64 = base64.b64encode((HERE / "assets/fonts" / f"{f}.woff2").read_bytes()).decode()
            src = f"url(data:font/woff2;base64,{b64}) format(\"woff2\")"
        else:
            src = f"url(/assets/fonts/{f}.woff2) format(\"woff2\")"
        out.append(f'@font-face{{font-family:"{fam}";font-style:{style};font-weight:{w};font-display:swap;src:{src}}}')
    return "\n".join(out)


body = fill(BODY)
repl = {
    "%%TRUCK%%": truck_svg(),
    "%%CARDS%%": svc_cards(),
    "%%ALSO%%": also(),
    "%%MARQUEE%%": marquee(),
    "%%MINI%%": mini_moves,
    "%%MOVES%%": move_buttons(),
    "%%MV_TITLE%%": html.escape(first["title"]),
    "%%MV_LINE%%": html.escape(first["line"]),
    "%%MV_INC%%": first_inc,
    "%%MV_PH%%": html.escape(first["ph"], quote=True),
    "%%FAQ%%": faq_html,
    "%%ICON_TRUCK_SM%%": ICON_TRUCK.replace("<svg ", '<svg width="22" height="22" '),
    "%%ICON_TRUCK%%": ICON_TRUCK, "%%ICON_PLANE%%": ICON_PLANE,
    "%%ICON_WA%%": ICON_WA, "%%ICON_IG%%": ICON_IG, "%%ICON_PHONE%%": ICON_PHONE,
    "%%ARR_UP%%": ARR_UP, "%%ARR_L%%": ARR_L, "%%ARR_R%%": ARR_R, "%%ARR%%": ARR,
    "%%FMCSA%%": html.escape(FMCSA, quote=True),
    "%%WA%%": WA, "%%PHONE%%": PHONE, "%%PHONE_LABEL%%": PHONE_LABEL, "%%EMAIL%%": EMAIL, "%%IG%%": IG,
}
for k, v in repl.items():
    body = body.replace(k, v)

js = JS
for k, v in {
    "%%WA%%": WA,
    "%%T%%": json.dumps(T, ensure_ascii=False),
    "%%MOVES_JSON%%": json.dumps(MOVES, ensure_ascii=False),
    "%%CHECK%%": json.dumps(CHECK),
    "%%ITEMS%%": json.dumps(ITEM_DATA),
    "%%SPAN%%": json.dumps(DEFAULT_SPAN),
    "%%JARR%%": json.dumps(ARR), "%%JARR_L%%": json.dumps(ARR_L), "%%JARR_R%%": json.dumps(ARR_R), "%%JICON_WA%%": json.dumps(ICON_WA),
}.items():
    js = js.replace(k, v)
assert "%%" not in body and "%%" not in js and "{{" not in body

schema = {
    "@context": "https://schema.org", "@type": "MovingCompany", "name": "Shammah Moving", "url": SITE_URL,
    "image": SITE_URL + "/assets/og-image.jpg", "logo": SITE_URL + "/assets/logo.png", "telephone": PHONE,
    "email": EMAIL, "foundingDate": "2008",
    "address": {"@type": "PostalAddress", "addressLocality": "Windermere", "addressRegion": "FL", "postalCode": "34786", "addressCountry": "US"},
    "areaServed": ["Windermere, FL", "Orlando, FL", "Central Florida"], "knowsLanguage": ["en", "pt-BR"], "sameAs": [IG],
}

HEAD = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e("metaTitle")}</title>
<meta name="description" content="{e("metaDesc")}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="canonical" href="{SITE_URL}/">
<link rel="alternate" hreflang="en" href="{SITE_URL}/">
<link rel="alternate" hreflang="pt-BR" href="{SITE_URL}/?lang=pt">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Shammah Moving">
<meta property="og:title" content="Shammah Moving · Moving? Just call Shammah.">
<meta property="og:description" content="{e("metaDesc")}">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/geist-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/windermere.webp" as="image">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<script>document.documentElement.classList.add("js")</script>
<style>
{font_faces(False)}
{CSS}
</style>
</head>
<body>'''

if not SHOW_INVENTORY:
    body = re.sub(r"<!--INV-->.*?<!--/INV-->\n", "", body, flags=re.S)

site = HEAD + body + "<script>" + js + "</script>\n</body>\n</html>\n"
(HERE / "index.html").write_text(site, encoding="utf-8")

print("index.html", len(site), "bytes")
