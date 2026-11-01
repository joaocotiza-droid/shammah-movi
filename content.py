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
