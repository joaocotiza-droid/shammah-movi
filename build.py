"""Builds index.html for the Shammah Moving site from one bilingual content source.

Run:  python3 build.py
English is written into the HTML (what search engines and link previews read);
the same dictionary is embedded for the EN/PT switch.
"""
import html
import json
from pathlib import Path

WA = "14074856775"
IG = "https://www.instagram.com/shammahmoving/"
PHONE = "+14074856775"
PHONE_LABEL = "(407) 485-6775"
EMAIL = "contact@shammahmoving.com"
# Public address of the site; used for link previews (WhatsApp, Instagram, Facebook) and Google.
SITE_URL = "https://shammah-moving.vercel.app"

T = {
    "en": {
        "metaTitle": "Shammah Moving | Movers in Windermere & Orlando, FL",
        "metaDesc": "Local, interstate and international moving out of Windermere, Florida. Packing, freight, storage and piano moves. We speak English and Portuguese. Get a quote on WhatsApp.",
        "navQuote": "Get a quote", "navServices": "Services", "navHow": "How it works", "navFaq": "FAQ",
        "langAria": "Language",
        "heroKicker": "Hey, Windermere. We're here.",
        "heroA": "Moving?", "heroB": "Just call Shammah.",
        "heroSub": "Local, interstate and international moves out of Windermere, Florida. Tell us what you're moving on WhatsApp and we'll come back with a plan and a quote.",
        "ctaWa": "WhatsApp us", "ctaQuote": "Get a quote",
        "heroAlt": "Shammah truck parked at a home in Windermere, Florida",
        "f1a": "Since 2008", "f1b": "Moving families and businesses in Central Florida.",
        "f2a": "USDOT 1547896", "f2b": "Registered with the U.S. Department of Transportation.",
        "f3a": "In · Out", "f3b": "Local, interstate and international.",
        "f4a": "EN · PT", "f4b": "We speak English and Portuguese.",
        "qTitle": "Get a quote",
        "qSub": "Pick your type of move, fill in what you know and send it. It goes straight to our WhatsApp.",
        "qGroup": "Type of move", "qDetails": "Your details",
        "lFrom": "Moving from", "lTo": "Moving to", "lDate": "Moving date", "lDetails": "Size or items",
        "phFrom": "City or ZIP", "phTo": "City, ZIP or country",
        "sendWa": "Send on WhatsApp",
        "sendNote": "WhatsApp opens with your message ready. Nothing is sent until you tap send.",
        "msgHi": "Hi Shammah! I'd like a quote.", "msgType": "Move", "msgFrom": "From", "msgTo": "To",
        "msgDate": "Date", "msgDet": "Details",
        "waGeneral": "Hi Shammah! I'd like a quote for my move.",
        "svcTitle": "Our services",
        "svcSub": "Local, interstate, international, packing, freight and storage. One crew from start to finish.",
        "svcAlso": "Also: pianos, furniture assembly, loading and unloading.",
        "howTitle": "How it works",
        "h1t": "Message us", "h1d": "Tell us where you're moving from, where to and when. Photos of the big pieces help a lot.",
        "h2t": "Get your quote", "h2d": "We size the crew and the truck for your move and send you a written estimate.",
        "h3t": "Moving day", "h3d": "We show up on time, protect your floors and furniture, and put everything where you want it.",
        "igTitle": "See us in action",
        "igSub": "Real moves, behind the scenes and what our clients say. It's all on our Instagram.",
        "igCta": "Follow @shammahmoving",
        "ig1": "Services", "ig2": "In action", "ig3": "Packing", "ig4": "Reviews",
        "langTitle": "Fala português?\nA gente também.",
        "langSub": "Coming from Brazil or moving across town, you can talk to us in Portuguese from the first message to the last box. Switch the site to PT at the top.",
        "langCta": "Chamar no WhatsApp",
        "faqTitle": "FAQ",
        "endA": "Need to move?", "endB": "Just call Shammah.",
        "endSub": "Send us your move today. We'll take it from there.",
        "call": "Call",
        "fabAria": "Message Shammah Moving on WhatsApp",
        "footRights": "© 2026 Shammah Moving · Windermere, FL · USDOT 1547896",
    },
    "pt": {
        "metaTitle": "Shammah Moving | Mudanças em Windermere e Orlando, FL",
        "metaDesc": "Mudanças locais, interestaduais e internacionais saindo de Windermere, Flórida. Embalagem, fretes, armazenagem e pianos. Atendimento em português. Orçamento pelo WhatsApp.",
        "navQuote": "Orçamento", "navServices": "Serviços", "navHow": "Como funciona", "navFaq": "Dúvidas",
        "langAria": "Idioma",
        "heroKicker": "Hey, Windermere. Chegamos.",
        "heroA": "Vai se mudar?", "heroB": "É só Shammah.",
        "heroSub": "Mudanças locais, interestaduais e internacionais saindo de Windermere, na Flórida. Conte no WhatsApp o que você vai mudar e a gente volta com um plano e o orçamento.",
        "ctaWa": "Chamar no WhatsApp", "ctaQuote": "Pedir orçamento",
        "heroAlt": "Caminhão da Shammah em uma casa em Windermere, Flórida",
        "f1a": "Desde 2008", "f1b": "Mudando famílias e empresas na Flórida Central.",
        "f2a": "USDOT 1547896", "f2b": "Registrada no Departamento de Transportes dos EUA.",
        "f3a": "In · Out", "f3b": "Local, interestadual e internacional.",
        "f4a": "EN · PT", "f4b": "Atendemos em português e inglês.",
        "qTitle": "Peça seu orçamento",
        "qSub": "Escolha o tipo de mudança, preencha o que você já sabe e envie. Cai direto no nosso WhatsApp.",
        "qGroup": "Tipo de mudança", "qDetails": "Seus dados",
        "lFrom": "Saindo de", "lTo": "Indo para", "lDate": "Data da mudança", "lDetails": "Tamanho ou itens",
        "phFrom": "Cidade ou ZIP", "phTo": "Cidade, ZIP ou país",
        "sendWa": "Enviar no WhatsApp",
        "sendNote": "O WhatsApp abre com a mensagem pronta. Nada é enviado até você tocar em enviar.",
        "msgHi": "Olá, Shammah! Gostaria de um orçamento.", "msgType": "Mudança", "msgFrom": "Saindo de",
        "msgTo": "Indo para", "msgDate": "Data", "msgDet": "Detalhes",
        "waGeneral": "Olá, Shammah! Gostaria de um orçamento para a minha mudança.",
        "svcTitle": "Nossos serviços",
        "svcSub": "Local, interestadual, internacional, embalagem, fretes e armazenagem. Uma equipe só, do começo ao fim.",
        "svcAlso": "Também: pianos, montagem de móveis, carga e descarga.",
        "howTitle": "Como funciona",
        "h1t": "Chame a gente", "h1d": "Conte de onde sai, para onde vai e quando. Fotos dos móveis grandes ajudam muito.",
        "h2t": "Receba o orçamento", "h2d": "Definimos a equipe e o caminhão certos para a sua mudança e mandamos o orçamento por escrito.",
        "h3t": "Dia da mudança", "h3d": "Chegamos no horário, protegemos piso e móveis e deixamos tudo onde você quiser.",
        "igTitle": "Veja a gente em ação",
        "igSub": "Mudanças de verdade, bastidores e o que os clientes falam. Tá tudo no nosso Instagram.",
        "igCta": "Seguir @shammahmoving",
        "ig1": "Serviços", "ig2": "Em ação", "ig3": "Embalagem", "ig4": "Depoimentos",
        "langTitle": "Brasileiro\natendendo brasileiro.",
        "langSub": "Chegando do Brasil ou mudando dentro da cidade, você fala com a gente em português da primeira mensagem até a última caixa.",
        "langCta": "Chamar no WhatsApp",
        "faqTitle": "Dúvidas frequentes",
        "endA": "Precisou?", "endB": "É só Shammah.",
        "endSub": "Mande sua mudança hoje mesmo. A gente cuida do resto.",
        "call": "Ligar",
        "fabAria": "Falar com a Shammah Moving no WhatsApp",
        "footRights": "© 2026 Shammah Moving · Windermere, FL · USDOT 1547896",
    },
}

SVC = {
    "en": {
        "local": ("Local moving", "Homes and apartments across Windermere, Orlando and Central Florida.",
                  ["Safe transport", "Careful handling", "On time", "Stress-free"]),
        "interstate": ("Interstate moving", "State to state with full planning, from Florida to Atlanta and beyond.",
                       ["Cross-state moves", "Safe transport", "Full planning & support", "On-time delivery"]),
        "intl": ("International moving", "From Florida to the world and back, door to door.",
                 ["Door to door", "Secure packing", "Sea & air freight", "Customs support"]),
        "packing": ("Professional packing", "Your things boxed, protected and labeled before the truck arrives.",
                    ["High-quality materials", "Careful handling", "Fragile items protected", "Organized & labeled"]),
        "freight": ("Deliveries & freight", "Furniture, appliances and loads of every size, local or long distance.",
                    ["Safe transport", "On-time delivery", "All sizes & types", "Local & long distance"]),
        "storage": ("Storage", "Short or long term, for the gap between homes or a renovation that ran long.",
                    ["Short & long term", "Pickup & delivery", "Wrapped before storage"]),
    },
    "pt": {
        "local": ("Mudança local", "Casas e apartamentos em Windermere, Orlando e na Flórida Central.",
                  ["Transporte seguro", "Manuseio com cuidado", "No prazo combinado", "Sem estresse"]),
        "interstate": ("Mudança interestadual", "De um estado para outro com planejamento completo, da Flórida para Atlanta e além.",
                       ["Mudanças entre estados", "Transporte seguro", "Planejamento e suporte", "Entrega no prazo"]),
        "intl": ("Mudança internacional", "Da Flórida para o mundo e de volta, porta a porta.",
                 ["Porta a porta", "Embalagem segura", "Marítimo e aéreo", "Suporte alfandegário"]),
        "packing": ("Embalagem profissional", "Suas coisas embaladas, protegidas e etiquetadas antes do caminhão chegar.",
                    ["Materiais de qualidade", "Manuseio com cuidado", "Itens frágeis protegidos", "Tudo etiquetado"]),
        "freight": ("Fretes e entregas", "Móveis, eletrodomésticos e cargas de todos os tamanhos, local ou longa distância.",
                    ["Transporte seguro", "Entrega no prazo", "Todos os tamanhos", "Local e longa distância"]),
        "storage": ("Armazenagem", "Curto ou longo prazo, entre uma casa e outra ou durante uma reforma.",
                    ["Curto e longo prazo", "Coleta e entrega", "Embalado antes de guardar"]),
    },
}

FAQ = {
    "en": [
        ("How far ahead should I book?", "As soon as you have a date. Weekends and the end of the month fill up first. Moving sooner? Message us and we'll tell you honestly what's possible."),
        ("Do you bring boxes and packing supplies?", "Yes. We bring sturdy boxes, bubble wrap and moving blankets so your things are protected on the way."),
        ("Do you do international moves?", "Yes, in and out of the US, by sea or air, door to door. Tell us the origin, the destination and roughly what's going and we'll walk you through each step, customs included."),
        ("Do you move pianos?", "Yes, uprights and grands. Tell us the type, the floor and any stairs and we'll plan the right crew and equipment."),
        ("Can you just load or unload my truck?", "Yes. If you rented a U-Haul, a POD or a container, we can load or unload it for you."),
        ("What areas do you cover?", "We're based in Windermere and work all over Orlando and Central Florida, plus moves to other states and other countries."),
    ],
    "pt": [
        ("Com quanta antecedência devo agendar?", "Assim que tiver a data. Fim de semana e final de mês lotam primeiro. Precisa antes? Chama a gente que a gente fala com sinceridade o que dá para fazer."),
        ("Vocês levam caixas e material de embalagem?", "Sim. Levamos caixas resistentes, plástico bolha e mantas para proteger suas coisas no caminho."),
        ("Fazem mudança internacional?", "Sim, para dentro e para fora dos EUA, por via marítima ou aérea, porta a porta. Conte a origem, o destino e mais ou menos o que vai, e explicamos cada etapa, alfândega incluída."),
        ("Vocês mudam piano?", "Sim, de armário e de cauda. Diga o tipo, o andar e se tem escada, e planejamos a equipe e o equipamento certos."),
        ("Vocês podem só carregar ou descarregar meu caminhão?", "Sim. Se você alugou um U-Haul, um POD ou um contêiner, carregamos ou descarregamos para você."),
        ("Quais regiões vocês atendem?", "Estamos em Windermere e atendemos toda Orlando e a Flórida Central, além de mudanças para outros estados e outros países."),
    ],
}

MOVES = {
    "en": [
        {"id": "house", "label": "House", "title": "House move", "line": "From a starter home to five bedrooms, we plan the crew, the truck and the timing around your home.", "inc": ["Furniture wrapped in pads and stretch wrap", "Beds and tables taken apart and put back together", "Floors and door frames protected"], "ph": "e.g. 4 bedrooms, 2 floors"},
        {"id": "apt", "label": "Apartment / condo", "title": "Apartment or condo", "line": "Elevators, stairs, tight hallways and building rules. We work around the building's schedule.", "inc": ["Elevator and loading dock booked ahead", "Right-sized crew for tight spaces", "Quick in and out for reserved slots"], "ph": "e.g. 2 bed, 3rd floor, elevator"},
        {"id": "office", "label": "Office", "title": "Office or business", "line": "Desks, equipment and files moved on your schedule, after hours if your team can't stop.", "inc": ["Room-by-room labeled plan", "Workstations taken down and set up", "Evenings and weekends available"], "ph": "e.g. 15 workstations"},
        {"id": "interstate", "label": "Interstate", "title": "Interstate move", "line": "Leaving Florida or coming in? One crew and one plan, door to door.", "inc": ["Door to door, state to state", "Inventory so nothing goes missing", "Written estimate before we load"], "ph": "e.g. Orlando to Atlanta, 3 bedrooms"},
        {"id": "intl", "label": "International", "title": "International move", "line": "From Florida to the world, or the world to Florida. We plan the route and walk you through every step.", "inc": ["Door to door, in and out of the US", "Sea and air freight", "Customs support"], "ph": "e.g. Orlando to São Paulo, 2-bed apartment"},
        {"id": "freight", "label": "Freight & delivery", "title": "Freight and delivery", "line": "A new sofa, a store pickup or a full load across the state. Any size, on time.", "inc": ["Furniture, appliances and boxes", "All sizes and types of load", "Local and long distance"], "ph": "e.g. sofa and fridge from Kissimmee"},
        {"id": "packing", "label": "Packing", "title": "Packing", "line": "Full or partial. We pack a whole kitchen in an afternoon so you don't spend a week on it.", "inc": ["Boxes, bubble wrap and paper included", "Fragile items packed by hand", "Every box labeled by room"], "ph": "e.g. kitchen and living room only"},
        {"id": "piano", "label": "Piano", "title": "Piano move", "line": "Uprights and grands need technique, the right equipment and people who've done it many times.", "inc": ["Padded, strapped and secured", "Stairs and tight turns planned ahead", "Upright, baby grand and grand"], "ph": "e.g. upright, ground floor, no stairs"},
        {"id": "storage", "label": "Storage", "title": "Storage", "line": "Between homes, renovating or short on space? We keep your things safe until you need them.", "inc": ["Short and long term", "Pickup and delivery", "Everything wrapped before storage"], "ph": "e.g. one bedroom of furniture, 2 months"},
        {"id": "labor", "label": "Load / unload", "title": "Loading and unloading", "line": "Rented a U-Haul, a POD or a container? We bring the muscle and load it right.", "inc": ["Truck, POD and container loading", "Weight balanced so nothing shifts", "Hourly crews"], "ph": "e.g. 26 ft truck, 2-bed home"},
        {"id": "assembly", "label": "Assembly", "title": "Furniture assembly", "line": "New furniture, a move, or the wardrobe that never got finished. We build it, level it and take the boxes away.", "inc": ["Beds, wardrobes, desks and shelving", "Wall anchoring when needed", "Packaging taken away"], "ph": "e.g. 1 bed frame, 2 dressers"},
    ],
    "pt": [
        {"id": "house", "label": "Casa", "title": "Mudança de casa", "line": "Da primeira casa a uma de cinco quartos, planejamos equipe, caminhão e horário em volta da sua casa.", "inc": ["Móveis envolvidos em manta e filme", "Camas e mesas desmontadas e montadas", "Piso e batentes protegidos"], "ph": "ex.: 4 quartos, 2 andares"},
        {"id": "apt", "label": "Apartamento", "title": "Apartamento ou condomínio", "line": "Elevador, escada, corredor estreito e regras do prédio. A gente se encaixa no horário do condomínio.", "inc": ["Elevador e doca reservados antes", "Equipe do tamanho certo para espaço apertado", "Rapidez em horário reservado"], "ph": "ex.: 2 quartos, 3º andar, elevador"},
        {"id": "office", "label": "Escritório", "title": "Escritório ou empresa", "line": "Mesas, equipamentos e arquivos no seu horário, fora do expediente se a equipe não pode parar.", "inc": ["Plano etiquetado sala por sala", "Estações desmontadas e montadas", "Noites e fins de semana"], "ph": "ex.: 15 estações de trabalho"},
        {"id": "interstate", "label": "Interestadual", "title": "Mudança interestadual", "line": "Saindo da Flórida ou chegando? Uma equipe e um plano, de porta a porta.", "inc": ["Porta a porta, entre estados", "Inventário para nada se perder", "Orçamento por escrito antes de carregar"], "ph": "ex.: Orlando para Atlanta, 3 quartos"},
        {"id": "intl", "label": "Internacional", "title": "Mudança internacional", "line": "Da Flórida para o mundo, ou do mundo para a Flórida. Planejamos a rota e acompanhamos cada etapa.", "inc": ["Porta a porta, para dentro e fora dos EUA", "Transporte marítimo e aéreo", "Suporte alfandegário"], "ph": "ex.: Orlando para São Paulo, apto de 2 quartos"},
        {"id": "freight", "label": "Frete e entrega", "title": "Frete e entrega", "line": "Um sofá novo, uma retirada na loja ou uma carga inteira pelo estado. Qualquer tamanho, no prazo.", "inc": ["Móveis, eletrodomésticos e caixas", "Cargas de todos os tamanhos e tipos", "Local e longa distância"], "ph": "ex.: sofá e geladeira de Kissimmee"},
        {"id": "packing", "label": "Embalagem", "title": "Embalagem", "line": "Completa ou parcial. Embalamos uma cozinha inteira em uma tarde para você não perder a semana nisso.", "inc": ["Caixas, plástico bolha e papel inclusos", "Itens frágeis embalados à mão", "Cada caixa etiquetada por cômodo"], "ph": "ex.: só cozinha e sala"},
        {"id": "piano", "label": "Piano", "title": "Mudança de piano", "line": "Piano de armário ou de cauda pede técnica, equipamento certo e gente que já fez isso muitas vezes.", "inc": ["Protegido, amarrado e travado", "Escadas e curvas planejadas antes", "Armário, meia cauda e cauda"], "ph": "ex.: de armário, térreo, sem escada"},
        {"id": "storage", "label": "Armazenagem", "title": "Armazenagem", "line": "Entre uma casa e outra, em reforma ou sem espaço? Guardamos suas coisas com segurança até você precisar.", "inc": ["Curto e longo prazo", "Coleta e entrega", "Tudo embalado antes de guardar"], "ph": "ex.: móveis de 1 quarto, 2 meses"},
        {"id": "labor", "label": "Carga e descarga", "title": "Carga e descarga", "line": "Alugou U-Haul, POD ou contêiner? A gente leva a força e carrega do jeito certo.", "inc": ["Carga de caminhão, POD e contêiner", "Peso distribuído para nada se mexer", "Equipe por hora"], "ph": "ex.: caminhão de 26 pés, casa de 2 quartos"},
        {"id": "assembly", "label": "Montagem", "title": "Montagem de móveis", "line": "Móvel novo, mudança ou aquele guarda-roupa que nunca ficou pronto. Montamos, nivelamos e levamos as caixas.", "inc": ["Camas, guarda-roupas, mesas e estantes", "Fixação na parede quando precisa", "Embalagens retiradas"], "ph": "ex.: 1 cama, 2 cômodas"},
    ],
}

# Flatten services and FAQ into the dictionary so one [data-i18n] pass swaps everything.
for lang in ("en", "pt"):
    for key, (title, desc, tags) in SVC[lang].items():
        T[lang][f"svc_{key}_t"] = title
        T[lang][f"svc_{key}_d"] = desc
        for i, tag in enumerate(tags):
            T[lang][f"svc_{key}_g{i}"] = tag
    for i, (q, a) in enumerate(FAQ[lang]):
        T[lang][f"faq{i}q"] = q
        T[lang][f"faq{i}a"] = a

assert set(T["en"]) == set(T["pt"]), set(T["en"]) ^ set(T["pt"])

EN = T["en"]


def e(key):
    return html.escape(EN[key], quote=True)


ICON_WA = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 9.5c.3 2.4 2.7 4.8 5.2 5.3l1.2-1.2 1.8.8c-.2 1.3-1.2 2-2.4 1.9-3.4-.3-6.4-3.3-6.7-6.7-.1-1.2.6-2.2 1.9-2.4l.8 1.8z"/></svg>'
ICON_IG = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.8" fill="currentColor" stroke="none"/></svg>'
ICON_PIN = '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
CHECK = '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="#ff6b1a"/><path d="M6 10.2l2.6 2.6L14 7.4" fill="none" stroke="#0b0b0c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def service_card(key, img, w=1100, h=728):
    tags = "".join(f'<li data-i18n="svc_{key}_g{i}">{e(f"svc_{key}_g{i}")}</li>' for i in range(len(SVC["en"][key][2])))
    return f'''<article class="svc reveal">
<img src="/assets/{img}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">
<div class="svc-body">
<h3 data-i18n="svc_{key}_t">{e(f"svc_{key}_t")}</h3>
<p data-i18n="svc_{key}_d">{e(f"svc_{key}_d")}</p>
<ul class="tags">{tags}</ul>
</div>
</article>'''


def move_buttons():
    out = []
    for i, m in enumerate(MOVES["en"]):
        out.append(f'<button type="button" class="chip" data-move="{m["id"]}" aria-pressed="{"true" if i == 0 else "false"}">{html.escape(m["label"])}</button>')
    return "\n".join(out)


first = MOVES["en"][0]
first_inc = "".join(f"<li>{CHECK}<span>{html.escape(x)}</span></li>" for x in first["inc"])
faq_html = "\n".join(
    f'<details class="faq-item"><summary data-i18n="faq{i}q">{e(f"faq{i}q")}</summary><p data-i18n="faq{i}a">{e(f"faq{i}a")}</p></details>'
    for i in range(len(FAQ["en"]))
)
storage_tags = "".join(f'<li data-i18n="svc_storage_g{i}">{e(f"svc_storage_g{i}")}</li>' for i in range(3))

schema = {
    "@context": "https://schema.org",
    "@type": "MovingCompany",
    "name": "Shammah Moving",
    "url": SITE_URL,
    "image": SITE_URL + "/assets/og-image.jpg",
    "logo": SITE_URL + "/assets/logo.png",
    "telephone": PHONE,
    "email": EMAIL,
    "foundingDate": "2008",
    "address": {"@type": "PostalAddress", "addressLocality": "Windermere", "addressRegion": "FL", "postalCode": "34786", "addressCountry": "US"},
    "areaServed": ["Windermere, FL", "Orlando, FL", "Central Florida"],
    "knowsLanguage": ["en", "pt-BR"],
    "sameAs": [IG],
}

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e("metaTitle")}</title>
<meta name="description" content="{e("metaDesc")}">
<meta name="theme-color" content="#0b0b0c">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="canonical" href="{SITE_URL}/">
<link rel="alternate" hreflang="en" href="{SITE_URL}/">
<link rel="alternate" hreflang="pt-BR" href="{SITE_URL}/?lang=pt">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Shammah Moving">
<meta property="og:title" content="Shammah Moving · Precisou? É só Shammah.">
<meta property="og:description" content="{e("metaDesc")}">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/barlow-condensed-latin-900-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<style>
@font-face{{font-family:"Barlow Condensed";font-style:italic;font-weight:800;font-display:swap;src:url(/assets/fonts/barlow-condensed-latin-800-italic.woff2) format("woff2")}}
@font-face{{font-family:"Barlow Condensed";font-style:italic;font-weight:900;font-display:swap;src:url(/assets/fonts/barlow-condensed-latin-900-italic.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-style:normal;font-weight:400;font-display:swap;src:url(/assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-style:normal;font-weight:600;font-display:swap;src:url(/assets/fonts/inter-latin-600-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-style:normal;font-weight:700;font-display:swap;src:url(/assets/fonts/inter-latin-700-normal.woff2) format("woff2")}}
:root{{--black:#0b0b0c;--card:#17171a;--line-d:#2a2a2e;--ink:#1d1d1f;--gray:#6e6e73;--gray-d:#a1a1a6;--line:#d2d2d7;--light:#f5f5f7;--orange:#ff6b1a;--orange-ink:#b4531a;--disp:"Barlow Condensed","Arial Narrow",Impact,sans-serif;--sans:Inter,-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;--wrap:1160px}}
*,*::before,*::after{{box-sizing:border-box}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--black);color:#f5f5f7;font-family:var(--sans);font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
img{{max-width:100%;height:auto;display:block}}
a{{color:inherit}}
button{{font:inherit}}
:focus-visible{{outline:2px solid var(--orange);outline-offset:3px;border-radius:6px}}
.wrap{{max-width:var(--wrap);margin:0 auto;padding:0 20px}}
.skip{{position:absolute;left:-9999px;top:8px;z-index:50;background:#fff;color:#000;padding:10px 16px;border-radius:8px}}
.skip:focus{{left:12px}}
.disp{{font-family:var(--disp);font-style:italic;font-weight:900;text-transform:uppercase;letter-spacing:-.005em;line-height:.88;margin:0}}
.h2{{font-size:clamp(48px,7.4vw,100px);white-space:pre-line}}
.lede{{font-size:clamp(17px,1.8vw,20px);line-height:1.5;max-width:600px;margin:22px 0 0}}
.sec{{padding:clamp(88px,11vw,136px) 0}}
.light{{background:#fff;color:var(--ink)}}
.light .lede{{color:var(--gray)}}
.dark .lede{{color:var(--gray-d)}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:54px;padding:0 28px;border-radius:999px;font-size:17px;font-weight:700;text-decoration:none;border:1px solid transparent;transition:transform .15s ease,background-color .2s ease,border-color .2s ease}}
.btn:active{{transform:scale(.98)}}
.btn-o{{background:var(--orange);color:var(--black)}}
.btn-o:hover{{background:#ff8238}}
.btn-ghost{{border-color:rgba(255,255,255,.32);color:#fff;font-weight:600}}
.btn-ghost:hover{{border-color:#fff}}
.btn-ink{{background:var(--black);color:#fff}}
.btn-ink:hover{{background:#262628}}
/* nav */
.nav{{position:sticky;top:0;z-index:20;background:rgba(11,11,12,.82);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(255,255,255,.08)}}
.nav .wrap{{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px}}
.brand{{display:flex;align-items:center;gap:12px;text-decoration:none;color:#fff}}
.brand img{{width:40px;height:40px;border-radius:50%}}
.brand-name{{display:flex;flex-direction:column;line-height:1}}
.brand-name b{{font-family:var(--disp);font-style:italic;font-weight:800;font-size:22px;letter-spacing:.04em}}
.brand-name small{{font-size:9px;font-weight:600;letter-spacing:.42em;color:var(--orange);margin-top:3px}}
.links{{display:flex;gap:26px}}
.links a{{font-size:14px;color:#d2d2d7;text-decoration:none}}
.links a:hover{{color:#fff}}
.nav-r{{display:flex;align-items:center;gap:10px}}
.lang{{display:flex;padding:3px;border-radius:999px;background:rgba(255,255,255,.12)}}
.lang button{{min-height:32px;min-width:42px;padding:0 12px;border:0;border-radius:999px;background:transparent;color:#d2d2d7;font-size:12px;font-weight:700;cursor:pointer}}
.lang button[aria-pressed="true"]{{background:#fff;color:var(--black)}}
.nav .btn{{min-height:38px;padding:0 16px;font-size:14px}}
@media (max-width:900px){{.links{{display:none}}}}
@media (max-width:420px){{.nav .btn-o{{display:none}}}}
/* hero */
.hero{{padding:clamp(72px,9vw,104px) 0 0;text-align:center;overflow:hidden}}
.kicker{{display:inline-flex;align-items:center;gap:8px;margin:0 0 22px;color:var(--orange);font-size:14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}}
.hero h1{{font-size:clamp(60px,8.6vw,124px);color:#fff}}
.hero h1 span{{display:block}}
.hero h1 .o{{color:var(--orange)}}
.swoosh{{display:block;width:min(560px,70vw);height:auto;margin:10px auto 0}}
.hero .lede{{margin:26px auto 0;color:var(--gray-d);max-width:640px}}
.ctas{{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-top:34px}}
.hero-photo{{position:relative;max-width:1040px;margin:64px auto 0;border-radius:32px 32px 0 0;overflow:hidden;background:var(--card)}}
.hero-photo img{{width:100%;aspect-ratio:16/9;object-fit:cover;object-position:62% 55%}}
@media (max-width:640px){{.hero-photo{{border-radius:24px 24px 0 0}}.hero-photo img{{aspect-ratio:4/3}}}}
.hero-chip{{position:absolute;left:20px;bottom:20px;display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;background:rgba(11,11,12,.78);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#fff;font-size:14px;font-weight:600}}
.hero-chip svg{{color:var(--orange)}}
/* facts */
.facts{{background:#151517;border-top:1px solid rgba(255,255,255,.06);padding:56px 0}}
.facts .wrap{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:32px}}
.fact b{{display:block;font-family:var(--disp);font-style:italic;font-weight:800;font-size:40px;line-height:1;text-transform:uppercase;color:var(--orange)}}
.fact span{{display:block;margin-top:8px;font-size:15px;color:var(--gray-d)}}
/* quote */
.chips{{display:flex;flex-wrap:wrap;gap:10px;margin-top:44px}}
.chip{{min-height:46px;padding:0 20px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink);font-size:15px;font-weight:500;cursor:pointer;transition:background-color .15s,border-color .15s}}
.chip:hover{{border-color:var(--ink)}}
.chip[aria-pressed="true"]{{background:var(--orange);border-color:var(--orange);color:var(--black);font-weight:700}}
.quote{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:20px;margin-top:28px}}
.mv{{border-radius:28px;background:var(--black);color:#f5f5f7;padding:clamp(28px,4vw,44px);display:flex;flex-direction:column;gap:18px}}
.mv h3{{font-family:var(--disp);font-style:italic;font-weight:800;text-transform:uppercase;font-size:clamp(38px,4.4vw,54px);line-height:.95;margin:0;color:#fff}}
.mv p{{margin:0;font-size:18px;color:#c7c7cc}}
.mv ul{{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:14px}}
.mv li{{display:flex;gap:12px;align-items:flex-start;font-size:16px}}
.mv li svg{{flex:none;margin-top:2px}}
.form{{border-radius:28px;background:var(--light);padding:clamp(28px,4vw,44px);display:flex;flex-direction:column;gap:16px}}
.form h3{{margin:0 0 4px;font-size:15px;font-weight:700;color:var(--gray)}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}}
.form label{{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:#424245}}
.form input{{min-height:50px;padding:0 14px;border-radius:12px;border:1px solid var(--line);background:#fff;color:var(--ink);font:400 16px var(--sans);width:100%}}
.form input:focus{{border-color:var(--ink);outline:none}}
.form input::placeholder{{color:#8e8e93}}
.form .btn{{margin-top:6px;border-radius:14px;min-height:58px}}
.note{{margin:0;font-size:13px;color:var(--gray)}}
/* services */
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:20px;margin-top:56px}}
.svc{{border-radius:28px;background:var(--card);border:1px solid var(--line-d);overflow:hidden;display:flex;flex-direction:column}}
.svc img{{width:100%;aspect-ratio:3/2;object-fit:cover}}
.svc-body{{padding:28px 30px 32px;display:flex;flex-direction:column;gap:12px}}
.svc h3,.svc-o h3{{font-family:var(--disp);font-style:italic;font-weight:800;text-transform:uppercase;font-size:36px;line-height:1;margin:0}}
.svc h3{{color:#fff}}
.svc p{{margin:0;font-size:16px;color:var(--gray-d)}}
.tags{{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}}
.tags li{{padding:6px 12px;border-radius:999px;background:rgba(255,107,26,.13);color:#ff9a5c;font-size:13px;font-weight:600}}
.svc-o{{border-radius:28px;background:var(--orange);color:var(--black);padding:40px 30px 32px;display:flex;flex-direction:column;justify-content:space-between;gap:32px}}
.svc-o p{{margin:0;font-size:16px;color:#1d1d1f}}
.svc-o .tags li{{background:rgba(11,11,12,.12);color:var(--black)}}
.svc-o .also{{margin-top:16px;padding-top:16px;border-top:1px solid rgba(11,11,12,.22);font-size:14px;font-weight:600}}
/* how */
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:48px;margin-top:64px}}
.step{{border-top:3px solid var(--black);padding-top:24px}}
.step b{{display:block;font-family:var(--disp);font-style:italic;font-weight:900;font-size:60px;line-height:1;color:var(--orange-ink)}}
.step h3{{margin:12px 0 8px;font-size:24px;letter-spacing:-.02em}}
.step p{{margin:0;color:var(--gray)}}
/* instagram */
.ig{{border-top:1px solid #ececf0}}
.ig .wrap{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:48px}}
.ig-text{{flex:1 1 420px}}
.rings{{flex:1 1 420px;display:flex;flex-wrap:wrap;justify-content:center;gap:28px}}
.ring{{display:flex;flex-direction:column;align-items:center;gap:12px;text-decoration:none;color:var(--ink);font-size:15px;font-weight:600}}
.ring span:first-child{{width:112px;height:112px;border-radius:50%;padding:4px;background:conic-gradient(from 200deg,#ff6b1a,#ffb347,#ff6b1a);transition:transform .2s ease}}
.ring:hover span:first-child{{transform:scale(1.05)}}
.ring img,.ring i{{width:100%;height:100%;border-radius:50%;border:3px solid #fff;object-fit:cover;background:var(--black)}}
.ring i{{display:flex;align-items:center;justify-content:center}}
.ig .btn{{margin-top:30px;border-color:var(--black);color:var(--black);font-weight:600}}
.ig .btn:hover{{background:var(--black);color:#fff}}
/* language band */
.band{{background:var(--orange);color:var(--black);padding:clamp(88px,10vw,120px) 0}}
.band .wrap{{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:40px}}
.band .h2{{font-size:clamp(52px,8vw,116px)}}
.band .lede{{color:#1d1d1f}}
/* faq */
.faq{{max-width:860px}}
.faq-list{{margin-top:48px;border-bottom:1px solid var(--line)}}
.faq-item{{border-top:1px solid var(--line)}}
.faq-item summary{{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:24px;padding:26px 0;font-size:20px;font-weight:600;letter-spacing:-.015em}}
.faq-item summary::-webkit-details-marker{{display:none}}
.faq-item summary::after{{content:"";flex:none;width:12px;height:12px;border-right:2px solid var(--ink);border-bottom:2px solid var(--ink);transform:rotate(45deg) translateY(-3px);transition:transform .2s ease}}
.faq-item[open] summary::after{{transform:rotate(-135deg) translateY(-3px)}}
.faq-item p{{margin:-6px 0 26px;color:var(--gray);max-width:720px}}
/* end */
.end{{text-align:center}}
.end img{{width:112px;height:112px;border-radius:50%;margin:0 auto 32px}}
.end h2{{font-size:clamp(62px,10.5vw,150px);color:#fff}}
.end h2 span{{display:block}}
.end h2 .o{{color:var(--orange)}}
.end .lede{{margin:26px auto 0;color:var(--gray-d)}}
footer{{padding:0 0 calc(40px + env(safe-area-inset-bottom))}}
footer .wrap{{border-top:1px solid var(--line-d);padding-top:24px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;font-size:13px;color:var(--gray-d)}}
footer nav{{display:flex;flex-wrap:wrap;gap:18px}}
footer a{{color:#d2d2d7;text-decoration:none}}
footer a:hover{{color:#fff}}
/* floating WhatsApp */
.fab{{position:fixed;right:18px;bottom:calc(18px + env(safe-area-inset-bottom));z-index:30;width:60px;height:60px;border-radius:50%;background:var(--orange);color:var(--black);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.35);opacity:0;transform:translateY(16px) scale(.9);pointer-events:none;transition:opacity .25s ease,transform .25s ease}}
.fab.show{{opacity:1;transform:none;pointer-events:auto}}
.fab svg{{width:28px;height:28px}}
/* reveal */
.js .reveal{{opacity:0;transform:translateY(28px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)}}
.js .reveal.in{{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}.js .reveal{{opacity:1;transform:none;transition:none}}.fab{{transition:none}}}}
</style>
<script>document.documentElement.classList.add("js")</script>
</head>
<body>
<a class="skip" href="#quote">Skip to quote</a>

<header class="nav">
<div class="wrap">
<a class="brand" href="#top" aria-label="Shammah Moving">
<img src="/assets/logo-160.png" alt="" width="40" height="40">
<span class="brand-name"><b>SHAMMAH</b><small>MOVING</small></span>
</a>
<nav class="links" aria-label="Main">
<a href="#quote" data-i18n="navQuote">{e("navQuote")}</a>
<a href="#services" data-i18n="navServices">{e("navServices")}</a>
<a href="#how" data-i18n="navHow">{e("navHow")}</a>
<a href="#faq" data-i18n="navFaq">{e("navFaq")}</a>
</nav>
<div class="nav-r">
<div class="lang" role="group" aria-label="{e("langAria")}" data-i18n-aria="langAria">
<button type="button" data-lang="en" aria-pressed="true">EN</button>
<button type="button" data-lang="pt" aria-pressed="false">PT</button>
</div>
<a class="btn btn-o js-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a>
</div>
</div>
</header>

<main id="top">
<section class="hero" id="hero">
<div class="wrap">
<p class="kicker">{ICON_PIN}<span data-i18n="heroKicker">{e("heroKicker")}</span></p>
<h1 class="disp"><span data-i18n="heroA">{e("heroA")}</span><span class="o" data-i18n="heroB">{e("heroB")}</span></h1>
<svg class="swoosh" viewBox="0 0 600 34" aria-hidden="true"><path d="M6 28C140 10 330 4 594 6c-3 2-4 4-5 6C360 12 170 18 10 34z" fill="#ff6b1a"/></svg>
<p class="lede" data-i18n="heroSub">{e("heroSub")}</p>
<div class="ctas">
<a class="btn btn-o js-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}<span data-i18n="ctaWa">{e("ctaWa")}</span></a>
<a class="btn btn-ghost" href="#quote" data-i18n="ctaQuote">{e("ctaQuote")}</a>
</div>
<figure class="hero-photo">
<img src="/assets/windermere.webp" width="1600" height="1145" alt="{e("heroAlt")}" data-i18n-alt="heroAlt" fetchpriority="high" decoding="async">
<figcaption class="hero-chip">{ICON_PIN}Windermere, FL</figcaption>
</figure>
</div>
</section>

<section class="facts" aria-label="Shammah Moving">
<div class="wrap">
<div class="fact"><b data-i18n="f1a">{e("f1a")}</b><span data-i18n="f1b">{e("f1b")}</span></div>
<div class="fact"><b data-i18n="f2a">{e("f2a")}</b><span data-i18n="f2b">{e("f2b")}</span></div>
<div class="fact"><b data-i18n="f3a">{e("f3a")}</b><span data-i18n="f3b">{e("f3b")}</span></div>
<div class="fact"><b data-i18n="f4a">{e("f4a")}</b><span data-i18n="f4b">{e("f4b")}</span></div>
</div>
</section>

<section class="sec light" id="quote">
<div class="wrap">
<h2 class="disp h2 reveal" data-i18n="qTitle">{e("qTitle")}</h2>
<p class="lede" data-i18n="qSub">{e("qSub")}</p>
<div class="chips" id="moves" role="group" aria-label="{e("qGroup")}" data-i18n-aria="qGroup">
{move_buttons()}
</div>
<div class="quote">
<div class="mv" aria-live="polite">
<h3 id="mvTitle">{html.escape(first["title"])}</h3>
<p id="mvLine">{html.escape(first["line"])}</p>
<ul id="mvInc">{first_inc}</ul>
</div>
<form class="form" id="qform" novalidate>
<h3 data-i18n="qDetails">{e("qDetails")}</h3>
<div class="row">
<label><span data-i18n="lFrom">{e("lFrom")}</span><input type="text" name="from" autocomplete="address-level2" placeholder="{e("phFrom")}" data-i18n-ph="phFrom"></label>
<label><span data-i18n="lTo">{e("lTo")}</span><input type="text" name="to" placeholder="{e("phTo")}" data-i18n-ph="phTo"></label>
</div>
<label><span data-i18n="lDate">{e("lDate")}</span><input type="date" name="date"></label>
<label><span data-i18n="lDetails">{e("lDetails")}</span><input type="text" name="details" id="fDetails" placeholder="{html.escape(first["ph"], quote=True)}"></label>
<a class="btn btn-ink" id="waMove" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}<span data-i18n="sendWa">{e("sendWa")}</span></a>
<p class="note" data-i18n="sendNote">{e("sendNote")}</p>
</form>
</div>
</div>
</section>

<section class="sec dark" id="services">
<div class="wrap">
<h2 class="disp h2 reveal" data-i18n="svcTitle">{e("svcTitle")}</h2>
<p class="lede" data-i18n="svcSub">{e("svcSub")}</p>
<div class="grid">
{service_card("local", "local.webp")}
{service_card("interstate", "interstate.webp")}
{service_card("intl", "intl.webp")}
{service_card("packing", "packing.webp")}
{service_card("freight", "freight.webp")}
<article class="svc-o reveal">
<svg width="56" height="56" viewBox="0 0 40 40" aria-hidden="true" fill="none" stroke="#0b0b0c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 16L20 7l15 9v18H5z"/><path d="M11 34V20h18v14M11 25h18M11 30h18"/></svg>
<div>
<h3 data-i18n="svc_storage_t">{e("svc_storage_t")}</h3>
<p style="margin-top:12px" data-i18n="svc_storage_d">{e("svc_storage_d")}</p>
<ul class="tags" style="margin-top:14px">{storage_tags}</ul>
<p class="also" data-i18n="svcAlso">{e("svcAlso")}</p>
</div>
</article>
</div>
</div>
</section>

<section class="sec light" id="how">
<div class="wrap">
<h2 class="disp h2 reveal" data-i18n="howTitle">{e("howTitle")}</h2>
<div class="steps">
<div class="step reveal"><b>01</b><h3 data-i18n="h1t">{e("h1t")}</h3><p data-i18n="h1d">{e("h1d")}</p></div>
<div class="step reveal"><b>02</b><h3 data-i18n="h2t">{e("h2t")}</h3><p data-i18n="h2d">{e("h2d")}</p></div>
<div class="step reveal"><b>03</b><h3 data-i18n="h3t">{e("h3t")}</h3><p data-i18n="h3d">{e("h3d")}</p></div>
</div>
</div>
</section>

<section class="sec light ig" id="instagram">
<div class="wrap">
<div class="ig-text">
<h2 class="disp h2 reveal" data-i18n="igTitle">{e("igTitle")}</h2>
<p class="lede" data-i18n="igSub">{e("igSub")}</p>
<a class="btn" href="{IG}" target="_blank" rel="noopener">{ICON_IG}<span data-i18n="igCta">{e("igCta")}</span></a>
</div>
<div class="rings">
<a class="ring" href="{IG}" target="_blank" rel="noopener"><span><img src="/assets/local.webp" alt="" width="104" height="104" loading="lazy"></span><span data-i18n="ig1">{e("ig1")}</span></a>
<a class="ring" href="{IG}" target="_blank" rel="noopener"><span><img src="/assets/freight.webp" alt="" width="104" height="104" loading="lazy"></span><span data-i18n="ig2">{e("ig2")}</span></a>
<a class="ring" href="{IG}" target="_blank" rel="noopener"><span><img src="/assets/packing.webp" alt="" width="104" height="104" loading="lazy"></span><span data-i18n="ig3">{e("ig3")}</span></a>
<a class="ring" href="{IG}" target="_blank" rel="noopener"><span><i><svg width="40" height="40" viewBox="0 0 36 28" aria-hidden="true"><path d="M0 28V16C0 7 5 1.5 14 0l1.5 4C10 5.6 7.6 9 7.5 13H14v15zm20 0V16c0-9 5-14.5 14-16l1.5 4c-5.5 1.6-7.9 5-8 9H34v15z" fill="#ff6b1a"/></svg></i></span><span data-i18n="ig4">{e("ig4")}</span></a>
</div>
</div>
</section>

<section class="band" aria-labelledby="langTitle">
<div class="wrap">
<div style="flex:999 1 520px;min-width:0">
<h2 class="disp h2" id="langTitle" data-i18n="langTitle">{e("langTitle")}</h2>
<p class="lede" data-i18n="langSub">{e("langSub")}</p>
</div>
<a class="btn btn-ink js-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-i18n="langCta">{e("langCta")}</a>
</div>
</section>

<section class="sec light" id="faq">
<div class="wrap faq">
<h2 class="disp h2 reveal" data-i18n="faqTitle">{e("faqTitle")}</h2>
<div class="faq-list">
{faq_html}
</div>
</div>
</section>

<section class="sec dark end">
<div class="wrap">
<img src="/assets/logo.png" alt="Shammah Moving" width="112" height="112" loading="lazy">
<h2 class="disp reveal"><span data-i18n="endA">{e("endA")}</span><span class="o" data-i18n="endB">{e("endB")}</span></h2>
<p class="lede" data-i18n="endSub">{e("endSub")}</p>
<div class="ctas">
<a class="btn btn-o js-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}WhatsApp</a>
<a class="btn btn-ghost" href="tel:{PHONE}"><span data-i18n="call">{e("call")}</span>&nbsp;{PHONE_LABEL}</a>
<a class="btn btn-ghost" href="{IG}" target="_blank" rel="noopener">{ICON_IG}@shammahmoving</a>
</div>
</div>
</section>
</main>

<footer>
<div class="wrap">
<span data-i18n="footRights">{e("footRights")}</span>
<nav aria-label="Contact">
<a href="mailto:{EMAIL}">{EMAIL}</a>
<a href="tel:{PHONE}">{PHONE_LABEL}</a>
<a href="{IG}" target="_blank" rel="noopener">Instagram</a>
<a class="js-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a>
</nav>
</div>
</footer>

<a class="fab js-wa" id="fab" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="{e("fabAria")}" data-i18n-aria="fabAria">{ICON_WA}</a>

<script>
(function () {{
  var WA = "{WA}";
  var T = {json.dumps(T, ensure_ascii=False)};
  var MOVES = {json.dumps(MOVES, ensure_ascii=False)};
  var CHECK = {json.dumps(CHECK)};
  var $ = function (s, r) {{ return (r || document).querySelector(s); }};
  var $$ = function (s, r) {{ return Array.prototype.slice.call((r || document).querySelectorAll(s)); }};
  var state = {{ lang: "en", move: "house" }};
  var form = $("#qform");

  function wa(text) {{ return "https://wa.me/" + WA + "?text=" + encodeURIComponent(text); }}
  function esc(s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}}[c]; }}); }}
  function cur() {{
    var list = MOVES[state.lang];
    for (var i = 0; i < list.length; i++) if (list[i].id === state.move) return list[i];
    return list[0];
  }}
  function fmtDate(v) {{
    var p = v.split("-");
    if (p.length !== 3) return v;
    return state.lang === "pt" ? p[2] + "/" + p[1] + "/" + p[0] : p[1] + "/" + p[2] + "/" + p[0];
  }}

  function renderMove() {{
    var m = cur(), t = T[state.lang];
    $$("#moves .chip").forEach(function (b) {{
      var mm = MOVES[state.lang].filter(function (x) {{ return x.id === b.dataset.move; }})[0];
      b.textContent = mm.label;
      b.setAttribute("aria-pressed", b.dataset.move === state.move ? "true" : "false");
    }});
    $("#mvTitle").textContent = m.title;
    $("#mvLine").textContent = m.line;
    $("#mvInc").innerHTML = m.inc.map(function (x) {{ return "<li>" + CHECK + "<span>" + esc(x) + "</span></li>"; }}).join("");
    $("#fDetails").placeholder = m.ph;
    updateQuote();
  }}

  function updateQuote() {{
    var t = T[state.lang], m = cur(), f = form.elements;
    var lines = [t.msgHi, t.msgType + ": " + m.title];
    if (f.from.value.trim()) lines.push(t.msgFrom + ": " + f.from.value.trim());
    if (f.to.value.trim()) lines.push(t.msgTo + ": " + f.to.value.trim());
    if (f.date.value) lines.push(t.msgDate + ": " + fmtDate(f.date.value));
    if (f.details.value.trim()) lines.push(t.msgDet + ": " + f.details.value.trim());
    $("#waMove").href = wa(lines.join("\\n"));
  }}

  function setLang(l) {{
    state.lang = l === "pt" ? "pt" : "en";
    var t = T[state.lang];
    document.documentElement.lang = state.lang === "pt" ? "pt-BR" : "en";
    document.title = t.metaTitle;
    var md = $('meta[name="description"]'); if (md) md.setAttribute("content", t.metaDesc);
    $$("[data-i18n]").forEach(function (el) {{ var v = t[el.dataset.i18n]; if (v != null) el.textContent = v; }});
    $$("[data-i18n-ph]").forEach(function (el) {{ el.placeholder = t[el.dataset.i18nPh]; }});
    $$("[data-i18n-alt]").forEach(function (el) {{ el.alt = t[el.dataset.i18nAlt]; }});
    $$("[data-i18n-aria]").forEach(function (el) {{ el.setAttribute("aria-label", t[el.dataset.i18nAria]); }});
    $$(".lang button").forEach(function (b) {{ b.setAttribute("aria-pressed", b.dataset.lang === state.lang ? "true" : "false"); }});
    $$(".js-wa").forEach(function (a) {{ a.href = wa(t.waGeneral); }});
    renderMove();
    try {{ localStorage.setItem("shammah-lang", state.lang); }} catch (e) {{}}
  }}

  $$(".lang button").forEach(function (b) {{ b.addEventListener("click", function () {{ setLang(b.dataset.lang); }}); }});
  $$("#moves .chip").forEach(function (b) {{
    b.addEventListener("click", function () {{ state.move = b.dataset.move; renderMove(); }});
  }});
  form.addEventListener("input", updateQuote);
  form.addEventListener("submit", function (e) {{ e.preventDefault(); }});

  var initial = "en";
  try {{
    var q = new URLSearchParams(location.search).get("lang");
    if (q === "pt" || q === "en") initial = q;
    else if (localStorage.getItem("shammah-lang")) initial = localStorage.getItem("shammah-lang");
  }} catch (e) {{}}
  setLang(initial);

  var fab = $("#fab");
  if ("IntersectionObserver" in window) {{
    new IntersectionObserver(function (en) {{ fab.classList.toggle("show", !en[0].isIntersecting); }}, {{ threshold: 0.15 }}).observe($("#hero"));
    var io = new IntersectionObserver(function (en) {{
      en.forEach(function (x) {{ if (x.isIntersecting) {{ x.target.classList.add("in"); io.unobserve(x.target); }} }});
    }}, {{ rootMargin: "0px 0px -8% 0px" }});
    $$(".reveal").forEach(function (el) {{ io.observe(el); }});
  }} else {{
    fab.classList.add("show");
    $$(".reveal").forEach(function (el) {{ el.classList.add("in"); }});
  }}
}})();
</script>
</body>
</html>
'''

out = Path(__file__).with_name("index.html")
out.write_text(page, encoding="utf-8")
print("wrote", out, len(page), "bytes")
