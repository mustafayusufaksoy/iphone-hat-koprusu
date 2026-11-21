#!/usr/bin/env python3
"""README animasyonlarını üretir: python3 assets/uret.py assets"""
import sys

DUR = 10  # seconds per loop
W, H = 960, 480
BG = "#0f172a"
FONT = "font-family='-apple-system,Segoe UI,Helvetica,Arial,sans-serif'"


def kt(*secs):
    return ";".join(f"{s / DUR:.4f}" for s in secs)


def phone(x, y, w, h, body, screen, title, sub, inner=""):
    return f"""
  <g>
    <rect x='{x}' y='{y}' width='{w}' height='{h}' rx='16' fill='{body}'/>
    <rect x='{x+7}' y='{y+14}' width='{w-14}' height='{h-28}' rx='9' fill='{screen}'/>
    <rect x='{x+w/2-12}' y='{y+5}' width='24' height='4' rx='2' fill='#ffffff55'/>
    {inner}
    <text x='{x+w/2}' y='{y+h+26}' text-anchor='middle' {FONT} font-size='17' font-weight='700' fill='#f8fafc'>{title}</text>
    <text x='{x+w/2}' y='{y+h+46}' text-anchor='middle' {FONT} font-size='13' fill='#94a3b8'>{sub}</text>
  </g>"""


def cloud(cx, cy):
    return f"""
  <g>
    <path d='M{cx-70},{cy+28} a30,30 0 0 1 4,-58 a40,40 0 0 1 72,-14 a32,32 0 0 1 58,22 a26,26 0 0 1 -6,50 z'
      fill='#1e3a8a' stroke='#60a5fa' stroke-width='2'/>
    <text x='{cx}' y='{cy+5}' text-anchor='middle' {FONT} font-size='15' font-weight='700' fill='#e0f2fe'>sip.linphone.org</text>
    <text x='{cx}' y='{cy+24}' text-anchor='middle' {FONT} font-size='12' fill='#93c5fd'>ücretsiz SIP sunucusu</text>
  </g>"""


def wire(pid, d, color, label, lx, ly):
    return f"""
  <path id='{pid}' d='{d}' fill='none' stroke='{color}' stroke-opacity='0.35' stroke-width='3' stroke-dasharray='6 7'/>
  <text x='{lx}' y='{ly}' text-anchor='middle' {FONT} font-size='13' font-weight='600' fill='{color}'>{label}</text>"""


def packet(pid, color, t0, t1, icon="📞"):
    # visible only while travelling
    return f"""
  <g opacity='0'>
    <animate attributeName='opacity' dur='{DUR}s' repeatCount='indefinite'
      values='0;0;1;1;0;0' keyTimes='{kt(0, t0 - 0.01, t0, t1, t1 + 0.01, DUR)}'/>
    <animateMotion dur='{DUR}s' repeatCount='indefinite' calcMode='linear'
      keyPoints='0;0;1;1' keyTimes='{kt(0, t0, t1, DUR)}'><mpath href='#{pid}'/></animateMotion>
    <circle r='17' fill='{color}'/>
    <circle r='17' fill='none' stroke='{color}' stroke-opacity='0.5' stroke-width='6'>
      <animate attributeName='r' values='17;26;17' dur='0.8s' repeatCount='indefinite'/>
    </circle>
    <text y='6' text-anchor='middle' font-size='16'>{icon}</text>
  </g>"""


def ring(cx, cy, color, t0, t1):
    out = []
    for i in range(3):
        out.append(f"""
  <circle cx='{cx}' cy='{cy}' r='40' fill='none' stroke='{color}' stroke-width='3' opacity='0'>
    <animate attributeName='opacity' dur='{DUR}s' repeatCount='indefinite'
      values='0;0;1;1;0;0' keyTimes='{kt(0, t0, t0 + 0.01, t1, t1 + 0.01, DUR)}'/>
    <animate attributeName='r' values='40;80' dur='1.2s' begin='{i * 0.4}s' repeatCount='indefinite'/>
    <animate attributeName='stroke-opacity' values='0.9;0' dur='1.2s' begin='{i * 0.4}s' repeatCount='indefinite'/>
  </circle>""")
    return "".join(out)


def show(t0, t1, inner):
    return f"""
  <g opacity='0'>
    <animate attributeName='opacity' dur='{DUR}s' repeatCount='indefinite'
      values='0;0;1;1;0;0' keyTimes='{kt(0, t0, t0 + 0.3, t1, t1 + 0.3, DUR)}'/>
    {inner}
  </g>"""


def voice_flow(pids, t0, t1):
    out = []
    for pid, color in pids:
        out.append(f"""
  <use href='#{pid}v' opacity='0'>
    <animate attributeName='opacity' dur='{DUR}s' repeatCount='indefinite'
      values='0;0;1;1;0;0' keyTimes='{kt(0, t0, t0 + 0.3, t1, t1 + 0.3, DUR)}'/>
  </use>""")
    return "".join(out)


def voice_defs(pid, d, color):
    return f"""
    <path id='{pid}v' d='{d}' fill='none' stroke='{color}' stroke-width='5' stroke-linecap='round' stroke-dasharray='2 14'>
      <animate attributeName='stroke-dashoffset' values='0;-32' dur='0.6s' repeatCount='indefinite'/>
    </path>"""


def steps(items, y):
    """Bottom caption strip whose active step follows the timeline."""
    out = []
    n = len(items)
    seg = (W - 80) / n
    for i, (t0, t1, color, text) in enumerate(items):
        x = 40 + i * seg
        out.append(f"""
  <g>
    <rect x='{x+4}' y='{y}' width='{seg-8}' height='34' rx='17' fill='#1e293b'/>
    <rect x='{x+4}' y='{y}' width='{seg-8}' height='34' rx='17' fill='{color}' opacity='0'>
      <animate attributeName='opacity' dur='{DUR}s' repeatCount='indefinite'
        values='0;0;1;1;0;0' keyTimes='{kt(0, t0, t0 + 0.2, t1, t1 + 0.2, DUR)}'/>
    </rect>
    <text x='{x+seg/2}' y='{y+22}' text-anchor='middle' {FONT} font-size='13' font-weight='700' fill='#f8fafc'>{i+1}. {text}</text>
  </g>""")
    return "".join(out)


def frame(title, body, defs=""):
    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}' role="img" aria-label="{title}">
  <defs>{defs}
    <linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'>
      <stop offset='0' stop-color='#0f172a'/><stop offset='1' stop-color='#1e1b4b'/>
    </linearGradient>
  </defs>
  <rect width='{W}' height='{H}' rx='22' fill='url(#bg)'/>
  <text x='40' y='46' {FONT} font-size='22' font-weight='800' fill='#f8fafc'>{title}</text>
{body}
</svg>
"""


# ---------- common geometry ----------
LX, AX, IX = 70, 285, 805      # left phone, android, iphone x
PY, PW, PH = 150, 78, 140
CX, CY = 545, 150              # cloud centre

P_LEFT = f"M{LX+PW+8},{PY+70} L{AX-8},{PY+70}"
P_UP = f"M{AX+PW+8},{PY+50} C{AX+PW+70},{PY+50} {CX-130},{CY+10} {CX-78},{CY+10}"
P_DOWN = f"M{CX+80},{CY+10} C{CX+150},{CY+10} {IX-70},{PY+50} {IX-8},{PY+50}"
P_TG = f"M{AX+PW/2},{PY+PH+58} C{AX+PW/2},{PY+PH+120} {IX+PW/2},{PY+PH+120} {IX+PW/2},{PY+PH+58}"

android_inner = f"""<text x='{AX+PW/2}' y='{PY+60}' text-anchor='middle' font-size='30'>🤖</text>
    <rect x='{AX+12}' y='{PY+80}' width='{PW-24}' height='18' rx='9' fill='#14532d'/>
    <text x='{AX+PW/2}' y='{PY+93}' text-anchor='middle' {FONT} font-size='9' font-weight='700' fill='#bbf7d0'>SIP Agent</text>"""


def incoming():
    defs = voice_defs("a", P_LEFT, "#4ade80") + voice_defs("b", P_UP, "#4ade80") + voice_defs("c", P_DOWN, "#4ade80")
    b = []
    b.append(wire("p1", P_LEFT, "#fb923c", "GSM / VoLTE", (LX + PW + AX) / 2, PY + 58))
    b.append(wire("p2", P_UP, "#60a5fa", "SIP · TLS + SRTP", AX + 150, PY + 82))
    b.append(wire("p3", P_DOWN, "#c084fc", "push + SIP", IX - 95, PY + 82))
    b.append(wire("p4", P_TG, "#22d3ee", "", 0, 0))
    b.append(f"""<rect x='{(AX+IX+PW)/2-120}' y='{PY+PH+80}' width='240' height='32' rx='16' fill='#155e75' stroke='#22d3ee'/>
    <text x='{(AX+IX+PW)/2}' y='{PY+PH+101}' text-anchor='middle' {FONT} font-size='13' font-weight='700' fill='#cffafe'>✈️ SMS → Telegram (isteğe bağlı)</text>""")
    b.append(cloud(CX, CY))
    b.append(phone(LX, PY, PW, PH, "#475569", "#0f172a", "Arayan", "herhangi bir telefon",
                   f"<text x='{LX+PW/2}' y='{PY+80}' text-anchor='middle' font-size='30'>📱</text>"))
    b.append(phone(AX, PY, PW, PH, "#16a34a", "#052e16", "Android", "hat burada · evde", android_inner))
    iphone_inner = f"<text x='{IX+PW/2}' y='{PY+80}' text-anchor='middle' font-size='30'>🍏</text>"
    b.append(f"<g>{phone(IX, PY, PW, PH, '#e2e8f0', '#111827', 'iPhone', 'SIM yok · Linphone', iphone_inner)}"
             f"<animateTransform attributeName='transform' type='rotate' dur='{DUR}s' repeatCount='indefinite' "
             f"values='0 {IX+PW/2} {PY+PH/2};0 {IX+PW/2} {PY+PH/2};-4 {IX+PW/2} {PY+PH/2};4 {IX+PW/2} {PY+PH/2};-4 {IX+PW/2} {PY+PH/2};4 {IX+PW/2} {PY+PH/2};0 {IX+PW/2} {PY+PH/2};0 {IX+PW/2} {PY+PH/2}' "
             f"keyTimes='{kt(0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, DUR)}'/></g>")
    b.append(ring(LX + PW / 2, PY + PH / 2, "#fb923c", 0.2, 1.4))
    b.append(ring(IX + PW / 2, PY + PH / 2, "#c084fc", 5.2, 6.4))
    b.append(packet("p1", "#f97316", 1.2, 2.6))
    b.append(packet("p2", "#3b82f6", 2.6, 4.0))
    b.append(packet("p3", "#a855f7", 4.0, 5.2))
    b.append(packet("p4", "#06b6d4", 1.4, 4.4, "✉️"))
    # incoming call banner on iPhone
    b.append(show(5.2, 6.4, f"""<rect x='{IX-40}' y='{PY-62}' width='158' height='44' rx='14' fill='#a855f7'/>
    <text x='{IX+39}' y='{PY-35}' text-anchor='middle' {FONT} font-size='14' font-weight='800' fill='#fff'>📲 Gelen arama</text>"""))
    b.append(show(6.6, 9.6, f"""<rect x='{IX-40}' y='{PY-62}' width='158' height='44' rx='14' fill='#16a34a'/>
    <text x='{IX+39}' y='{PY-35}' text-anchor='middle' {FONT} font-size='14' font-weight='800' fill='#fff'>🗣️ Konuşuluyor</text>"""))
    b.append(voice_flow([("a", ""), ("b", ""), ("c", "")], 6.6, 9.6))
    b.append(steps([(0.0, 2.6, "#ea580c", "Hat çalar"),
                    (2.6, 5.2, "#2563eb", "Android internete aktarır"),
                    (5.2, 6.6, "#9333ea", "iPhone çalar"),
                    (6.6, 9.6, "#16a34a", "İki yönlü konuşma")], H - 52))
    return frame("📞 Gelen arama: Android'deki hat iPhone'da çalar", "".join(b), defs)


def outgoing():
    # reverse direction: iPhone → cloud → Android → callee (left)
    R_DOWN = f"M{IX-8},{PY+50} C{IX-70},{PY+50} {CX+150},{CY+10} {CX+80},{CY+10}"
    R_UP = f"M{CX-78},{CY+10} C{CX-130},{CY+10} {AX+PW+70},{PY+50} {AX+PW+8},{PY+50}"
    R_LEFT = f"M{AX-8},{PY+70} L{LX+PW+8},{PY+70}"
    defs = voice_defs("a", R_LEFT, "#4ade80") + voice_defs("b", R_UP, "#4ade80") + voice_defs("c", R_DOWN, "#4ade80")
    b = []
    b.append(wire("q3", R_DOWN, "#c084fc", "Linphone araması", IX - 95, PY + 82))
    b.append(wire("q2", R_UP, "#60a5fa", "X-VSA-Dial = 05…", AX + 150, PY + 82))
    b.append(wire("q1", R_LEFT, "#fb923c", "hattan normal arama", (LX + PW + AX) / 2, PY + 58))
    b.append(cloud(CX, CY))
    b.append(phone(LX, PY, PW, PH, "#475569", "#0f172a", "Aranan", "numarayı sen seçersin",
                   f"<text x='{LX+PW/2}' y='{PY+80}' text-anchor='middle' font-size='30'>📱</text>"))
    b.append(phone(AX, PY, PW, PH, "#16a34a", "#052e16", "Android", "kendi hattından arar", android_inner))
    iphone_inner = f"<text x='{IX+PW/2}' y='{PY+80}' text-anchor='middle' font-size='30'>🍏</text>"
    b.append(phone(IX, PY, PW, PH, "#e2e8f0", "#111827", "iPhone", "numarayı yazarsın", iphone_inner))
    b.append(show(0.2, 1.6, f"""<rect x='{IX-150}' y='{PY-62}' width='228' height='44' rx='14' fill='#a855f7'/>
    <text x='{IX-36}' y='{PY-35}' text-anchor='middle' {FONT} font-size='14' font-weight='800' fill='#fff'>⌨️ sip:…?X-VSA-Dial=05…</text>"""))
    b.append(packet("q3", "#a855f7", 1.4, 2.8, "☎️"))
    b.append(packet("q2", "#3b82f6", 2.8, 4.2, "☎️"))
    b.append(packet("q1", "#f97316", 4.2, 5.4, "☎️"))
    b.append(ring(LX + PW / 2, PY + PH / 2, "#fb923c", 5.4, 6.6))
    b.append(show(4.2, 6.6, f"""<rect x='{AX-50}' y='{PY-62}' width='178' height='44' rx='14' fill='#16a34a'/>
    <text x='{AX+39}' y='{PY-35}' text-anchor='middle' {FONT} font-size='14' font-weight='800' fill='#fff'>📶 Hattan aranıyor</text>"""))
    b.append(show(6.8, 9.6, f"""<rect x='{LX-40}' y='{PY-62}' width='158' height='44' rx='14' fill='#16a34a'/>
    <text x='{LX+39}' y='{PY-35}' text-anchor='middle' {FONT} font-size='14' font-weight='800' fill='#fff'>🗣️ Konuşuluyor</text>"""))
    b.append(voice_flow([("a", ""), ("b", ""), ("c", "")], 6.8, 9.6))
    b.append((f"""<rect x='{AX-10}' y='{PY+PH+70}' width='{IX-AX+PW+20}' height='34' rx='12' fill='#7f1d1d' opacity='0.85'/>
    <text x='{(AX+IX+PW)/2}' y='{PY+PH+92}' text-anchor='middle' {FONT} font-size='13' font-weight='600' fill='#fecaca'>🔒 Yalnız izinli numaralar aranır: 05… 02… 03… 04… 0850…</text>"""))
    b.append(steps([(0.0, 2.8, "#9333ea", "iPhone'dan ara"),
                    (2.8, 4.2, "#2563eb", "Numara Android'e gider"),
                    (4.2, 6.8, "#ea580c", "Android hattan arar"),
                    (6.8, 9.6, "#16a34a", "İki yönlü konuşma")], H - 52))
    return frame("📤 Dış arama: iPhone'dan Android'in hattıyla ara", "".join(b), defs)


if __name__ == "__main__":
    out = sys.argv[1]
    open(f"{out}/gelen-arama.svg", "w").write(incoming())
    open(f"{out}/dis-arama.svg", "w").write(outgoing())
    print("ok")
