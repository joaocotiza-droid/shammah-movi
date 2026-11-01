"""Truck illustration shared with v2 (scroll-loaded box truck)."""


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- truck art
def box(w, h):
    x = -w / 2
    return (
        f'<rect x="{n(x)}" y="{n(-h)}" width="{n(w)}" height="{n(h)}" rx="3" fill="#c28a52"/>'
        f'<rect x="{n(x)}" y="{n(-h)}" width="{n(w)}" height="{n(h*.2)}" rx="3" fill="#d29c64"/>'
        f'<rect x="{n(-w*.08)}" y="{n(-h)}" width="{n(w*.16)}" height="{n(h*.44)}" fill="#e6cfa6" opacity=".8"/>'
        f'<rect x="{n(x+w*.12)}" y="{n(-h*.44)}" width="{n(w*.34)}" height="{n(h*.22)}" rx="2" fill="#f4ecdd"/>'
        f'<path d="M{n(x+w*.17)} {n(-h*.36)}h{n(w*.22)}M{n(x+w*.17)} {n(-h*.29)}h{n(w*.15)}" stroke="#b7a68c" stroke-width="2"/>'
        f'<path d="M{n(w*.26)} {n(-h*.3)}v{n(-h*.14)}m-4 4l4-4 4 4M{n(w*.38)} {n(-h*.3)}v{n(-h*.14)}m-4 4l4-4 4 4" stroke="#8a5a2c" stroke-width="1.6" fill="none"/>'
        f'<rect x="{n(x)}" y="-4" width="{n(w)}" height="4" fill="#a8743f"/>'
    )


def sofa(w, h):
    x = -w / 2
    return (
        f'<rect x="{n(x+10)}" y="{n(-h)}" width="{n(w-20)}" height="{n(h*.64)}" rx="16" fill="#5e6673"/>'
        f'<rect x="{n(x+26)}" y="{n(-h*.52)}" width="{n(w-52)}" height="{n(h*.32)}" rx="9" fill="#6f7886"/>'
        f'<path d="M0 {n(-h*.52)}v{n(h*.32)}" stroke="#58606c" stroke-width="2"/>'
        f'<rect x="{n(x)}" y="{n(-h*.7)}" width="32" height="{n(h*.6)}" rx="14" fill="#515864"/>'
        f'<rect x="{n(-x-32)}" y="{n(-h*.7)}" width="32" height="{n(h*.6)}" rx="14" fill="#515864"/>'
        f'<rect x="{n(x+4)}" y="{n(-h*.2)}" width="{n(w-8)}" height="{n(h*.12)}" rx="4" fill="#3f454e"/>'
        f'<rect x="{n(x+16)}" y="{n(-h*.08)}" width="7" height="{n(h*.08)}" fill="#8b6a48"/>'
        f'<rect x="{n(-x-23)}" y="{n(-h*.08)}" width="7" height="{n(h*.08)}" fill="#8b6a48"/>'
    )


def fridge(w, h):
    x = -w / 2
    return (
        f'<rect x="{n(x)}" y="{n(-h)}" width="{n(w)}" height="{n(h)}" rx="8" fill="#d9d9dc"/>'
        f'<rect x="{n(x+4)}" y="{n(-h+6)}" width="6" height="{n(h-12)}" rx="3" fill="#efeff1"/>'
        f'<path d="M{n(x)} {n(-h*.64)}h{n(w)}" stroke="#b5b5ba" stroke-width="2"/>'
        f'<rect x="{n(-x-14)}" y="{n(-h*.6)}" width="4" height="46" rx="2" fill="#97979d"/>'
        f'<rect x="{n(-x-14)}" y="{n(-h+16)}" width="4" height="34" rx="2" fill="#97979d"/>'
        f'<path d="M{n(x)} {n(-h*.3)}L{n(-x)} {n(-h*.42)}V{n(-h*.36)}L{n(x)} {n(-h*.24)}z" fill="#fff" opacity=".22"/>'
        f'<path d="M{n(x)} {n(-h*.82)}L{n(-x)} {n(-h*.94)}V{n(-h*.88)}L{n(x)} {n(-h*.76)}z" fill="#fff" opacity=".22"/>'
    )


def mattress(w, h):
    x = -w / 2
    lines = "".join(f"M{n(x+3)} {n(-h+k)}h{n(w-6)}" for k in range(26, int(h), 26))
    return (
        f'<rect x="{n(x)}" y="{n(-h)}" width="{n(w)}" height="{n(h)}" rx="10" fill="#ebe6dc"/>'
        f'<path d="{lines}" stroke="#d3cbbd" stroke-width="1.5"/>'
        f'<rect x="{n(x-1)}" y="{n(-h*.52)}" width="{n(w+2)}" height="8" fill="#ff6b1a"/>'
    )


def lamp(w, h):
    return (
        f'<ellipse cx="0" cy="-4" rx="{n(w*.42)}" ry="4" fill="#3a3a40"/>'
        f'<rect x="-2" y="{n(-h+44)}" width="4" height="{n(h-48)}" fill="#8a8a91"/>'
        f'<path d="M{n(-w*.3)} {n(-h)}H{n(w*.3)}L{n(w*.5)} {n(-h+46)}H{n(-w*.5)}z" fill="#efe2c6"/>'
        f'<path d="M{n(-w*.5)} {n(-h+46)}H{n(w*.5)}" stroke="#d8c7a3" stroke-width="2"/>'
    )


def plant(w, h):
    return (
        f'<path d="M{n(-w*.42)} -32H{n(w*.42)}L{n(w*.32)} 0H{n(-w*.32)}z" fill="#b5683a"/>'
        f'<rect x="{n(-w*.46)}" y="-36" width="{n(w*.92)}" height="7" rx="2" fill="#c57a4a"/>'
        f'<ellipse cx="-8" cy="{n(-h+22)}" rx="9" ry="22" transform="rotate(-24 -8 {n(-h+22)})" fill="#5c8a58"/>'
        f'<ellipse cx="9" cy="{n(-h+18)}" rx="9" ry="22" transform="rotate(22 9 {n(-h+18)})" fill="#4b744a"/>'
        f'<ellipse cx="0" cy="{n(-h+14)}" rx="8" ry="20" fill="#6b9a66"/>'
    )


DRAW = {"box": box, "sofa": sofa, "fridge": fridge, "mattress": mattress, "lamp": lamp, "plant": plant}
# Load order runs from the cab (front) to the doors (back). cx/by = bottom-centre target inside the bay.
ITEMS = [
    ("box", 110, 90, 852, 428), ("fridge", 82, 232, 750, 428), ("box", 96, 76, 852, 338),
    ("box", 78, 60, 850, 262), ("sofa", 226, 96, 588, 428), ("box", 92, 72, 528, 332),
    ("box", 84, 66, 634, 332), ("mattress", 28, 210, 452, 428), ("box", 70, 54, 530, 260),
    ("lamp", 44, 176, 410, 428), ("plant", 46, 78, 368, 428),
]
ITEM_DATA = [{"w": w, "h": h, "cx": cx, "by": by} for (_, w, h, cx, by) in ITEMS]


def wheel(cx):
    spokes = "".join(
        f'<path d="M0 0L0 -21" transform="rotate({a})" stroke="#74747b" stroke-width="5" stroke-linecap="round"/>'
        for a in range(0, 360, 60)
    )
    return (
        f'<circle cx="{cx}" cy="450" r="53" fill="#0a0a0b"/>'
        f'<g transform="translate({cx} 450)"><circle r="42" fill="#121214"/><circle r="38.5" fill="none" stroke="#1f1f22" stroke-width="5" stroke-dasharray="5 4"/>'
        f'<g class="spin"><circle r="25" fill="#2e2e33"/>{spokes}<circle r="8" fill="#b9b9bf"/></g></g>'
    )


def palm(x, s, flip=False):
    k = -1 if flip else 1
    tx, ty = x + k * 20 * s, 492 - 220 * s
    out = f'<path d="M{x} 492Q{n(x + k * 2 * s)} {n(492 - 120 * s)} {n(tx)} {n(ty)}" stroke="#151518" stroke-width="{n(8 * s)}" fill="none" stroke-linecap="round"/>'
    for a in (-170, -140, -105, -70, -35, -8):
        a = a if not flip else -180 - a
        out += (f'<path d="M0 0q{n(40 * s)} {n(-24 * s)} {n(88 * s)} {n(16 * s)}q{n(-46 * s)} {n(-13 * s)} {n(-88 * s)} {n(-6 * s)}z" '
                f'transform="translate({n(tx)} {n(ty)}) rotate({a})" fill="#151518"/>')
    return out


def truck_svg():
    slats = "".join(f"M346 {y}H914" for y in range(179, 428, 13))
    ribs = "".join(f"M{x} 166V428" for x in range(402, 914, 56))
    items = "".join(
        f'<g class="it" transform="translate({cx} {by})">{DRAW[k](w, h)}</g>' for (k, w, h, cx, by) in ITEMS
    )
    return f'''<svg class="rig" id="rig" viewBox="0 150 1280 380" preserveAspectRatio="xMidYMax meet" role="img" aria-label="A Shammah Moving truck being loaded at a home">
<defs>
<linearGradient id="gBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2c31"/><stop offset="1" stop-color="#151517"/></linearGradient>
<linearGradient id="gCab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6f5f2"/><stop offset="1" stop-color="#d4d2cd"/></linearGradient>
<linearGradient id="gDoor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#232327"/><stop offset="1" stop-color="#17171a"/></linearGradient>
<linearGradient id="gBay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d2c1f"/><stop offset="1" stop-color="#16110d"/></linearGradient>
<linearGradient id="gGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a5562"/><stop offset="1" stop-color="#0e1217"/></linearGradient>
<linearGradient id="gGround" x1="0" x2="1"><stop offset="0" stop-color="#3a2a20" stop-opacity="0"/><stop offset=".25" stop-color="#4a3222"/><stop offset=".75" stop-color="#4a3222"/><stop offset="1" stop-color="#3a2a20" stop-opacity="0"/></linearGradient>
<radialGradient id="gSun" cx=".55" cy="1" r=".75"><stop offset="0" stop-color="#ff7a26" stop-opacity=".30"/><stop offset=".45" stop-color="#ff6b1a" stop-opacity=".08"/><stop offset="1" stop-color="#ff6b1a" stop-opacity="0"/></radialGradient>
<radialGradient id="gLamp" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#ffc58a" stop-opacity=".42"/><stop offset="1" stop-color="#ffc58a" stop-opacity="0"/></radialGradient>
<radialGradient id="gGlow" cx=".5" cy="1" r=".9"><stop offset="0" stop-color="#ff6b1a" stop-opacity=".55"/><stop offset="1" stop-color="#ff6b1a" stop-opacity="0"/></radialGradient>
<clipPath id="cBay"><rect x="346" y="166" width="568" height="262"/></clipPath>
</defs>
<rect x="-200" y="150" width="1680" height="345" fill="url(#gSun)"/>
<g class="palms">{palm(1236, 1.0)}{palm(1180, .72, True)}{palm(232, .82, True)}</g>
<rect x="-200" y="493" width="1680" height="40" fill="#0e0e10"/>
<rect x="0" y="491" width="1280" height="2" fill="url(#gGround)"/>
<path d="M-200 515H1480" stroke="#232327" stroke-width="3" stroke-dasharray="38 30"/>
<g class="house" fill="none" stroke="#4a4a52" stroke-width="2" stroke-linejoin="round">
<path d="M6 304L95 236l89 68M22 292V492M168 292V492" fill="#0d0d0f"/>
<rect x="38" y="322" width="34" height="38" fill="#2a1c12" stroke="#7a4a26"/><rect x="118" y="322" width="34" height="38" fill="#2a1c12" stroke="#7a4a26"/>
<path d="M55 322v38M38 341h34M135 322v38M118 341h34" stroke="#7a4a26"/>
<ellipse cx="95" cy="492" rx="70" ry="38" fill="url(#gGlow)" stroke="none"/>
<rect x="74" y="402" width="42" height="90" fill="#2b1a0e" stroke="#ff6b1a" stroke-opacity=".7"/>
</g>
<g id="ramp"><path d="M196 489L328 430h8l-130 63z" fill="#7a7a82"/><path d="M220 482l8-4M244 471l8-4M268 461l8-4M292 450l8-4M316 440l8-4" stroke="#9c9ca3" stroke-width="2"/></g>
<g id="truck">
<ellipse cx="760" cy="494" rx="470" ry="7" fill="#000" opacity=".8"/>
<rect x="330" y="436" width="864" height="22" rx="4" fill="#1f1f22"/>
<rect x="975" y="446" width="72" height="22" rx="6" fill="#38383d"/>
<rect x="346" y="166" width="568" height="262" fill="url(#gBay)"/>
<path d="{ribs}" stroke="#4a3626" stroke-width="2" opacity=".55"/>
<path d="M346 300H914" stroke="#5a4130" stroke-width="3" opacity=".6"/>
<rect x="346" y="420" width="568" height="8" fill="#2f2318"/>
<rect x="346" y="166" width="568" height="262" fill="url(#gLamp)" clip-path="url(#cBay)"/>
<rect x="600" y="167" width="60" height="5" rx="2" fill="#ffe2bd"/>
<g id="items">{items}</g>
<path d="M338 150H922a8 8 0 0 1 8 8V432a8 8 0 0 1-8 8H338a8 8 0 0 1-8-8V158a8 8 0 0 1 8-8zM346 166V428H914V166z" fill="url(#gBody)" fill-rule="evenodd"/>
<path d="M338 151H922" stroke="#fff" stroke-opacity=".22" stroke-width="1.5"/>
<rect x="330" y="429" width="600" height="7" fill="#ff6b1a"/>
<rect class="marker" x="336" y="155" width="10" height="5" rx="2" fill="#ffb347"/>
<rect class="marker" x="914" y="155" width="10" height="5" rx="2" fill="#ffb347"/>
<g clip-path="url(#cBay)"><g id="shutter" transform="translate(0 -262)">
<rect x="346" y="166" width="568" height="262" fill="url(#gDoor)"/>
<path d="{slats}" stroke="#2d2d32" stroke-width="1.5"/>
<image href="assets/logo-160.png" x="382" y="216" width="150" height="150"/>
<text x="560" y="302" class="t-disp" font-size="98" fill="#f4f4f2">SHAMMAH</text>
<text x="566" y="336" class="t-wide" font-size="22" fill="#ff6b1a">MOVING</text>
<path d="M562 352C656 342 760 339 886 340c-2 2-3 4-3 6C780 345 668 348 564 358z" fill="#ff6b1a"/>
<text x="566" y="384" class="t-mono" font-size="14" fill="#9a9aa1">@shammahmoving</text>
<text x="386" y="410" class="t-mono" font-size="10.5" fill="#c9c9cd" letter-spacing="2.4">LOCAL · LONG DISTANCE · INTERNATIONAL · PACKING</text>
<rect x="346" y="420" width="568" height="8" fill="#3a3a40"/>
</g></g>
<path d="M930 236H1062q16 0 26 14l58 80q6 8 20 10l12 2q12 2 12 16V440H930z" fill="url(#gCab)"/>
<path d="M952 254H1056q10 0 16 8l46 68H952z" fill="url(#gGlass)"/>
<path d="M984 254h30l-46 76h-16v-28z" fill="#fff" opacity=".08"/>
<path d="M944 246V430M1108 344V430" stroke="#c3c1bb" stroke-width="2"/>
<rect x="960" y="352" width="26" height="6" rx="3" fill="#9a9aa0"/>
<text x="958" y="398" class="t-mono" font-size="11" fill="#6f6f76">USDOT 1547896</text>
<path d="M1124 298v40" stroke="#222225" stroke-width="8" stroke-linecap="round"/>
<rect x="1172" y="360" width="16" height="22" rx="4" fill="#fff6e0"/>
<rect x="1176" y="388" width="10" height="6" rx="2" fill="#ffb347"/>
<path d="M1180 404v22M1186 404v22" stroke="#bdbbb5" stroke-width="2"/>
<rect x="930" y="429" width="222" height="7" fill="#ff6b1a"/>
<rect x="1150" y="430" width="46" height="26" rx="6" fill="#222225"/>
{wheel(500)}{wheel(1066)}
</g>
</svg>'''


