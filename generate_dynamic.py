import datetime as dt
import html
import json
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

"""Configuration and daily content for the generated profile assets."""

CITY = "Delhi, India"
LATITUDE = 28.613939
LONGITUDE = 77.209021
TIMEZONE = "Asia/Kolkata"


def make_theme(name, primary, primary_dim, bg_card, bg_accent, border,
         wave_start, wave_mid, bg_grad_end, label, updated, focus, focus2):
  return {
    "name": name, "primary": primary, "primary_dim": primary_dim,
    "bg_card": bg_card, "bg_accent": bg_accent, "border": border,
    "wave_start": wave_start, "wave_mid": wave_mid,
    "bg_grad_end": bg_grad_end, "label": label, "updated": updated,
    "focus": focus, "focus2": focus2,
  }


# One theme per weekday keeps the generated profile visually varied and makes
# the weekday mapping explicit.
THEMES = {
    0: make_theme("Violet", "#c084fc", "#a855f7", "#1e1b2e", "#2d1b4e", "#3b0764", "3b0764", "6b21a8", "#1a0533", "#7c3aed", "#4b3b6b", "RAG · Agentic AI · MCP · AI Governance Platform", "Model Security · Edge Optimization · Encrypted AI"),
    1: make_theme("Lavender", "#d8b4fe", "#a855f7", "#241b35", "#38205c", "#581c87", "581c87", "7e22ce", "#210b3b", "#9333ea", "#62447e", "Multimodal AI · Evaluation · Responsible Systems", "Applied Research · Product Thinking · Reliable Delivery"),
    2: make_theme("Amethyst", "#c4b5fd", "#8b5cf6", "#211c38", "#30205e", "#4c1d95", "4c1d95", "6d28d9", "#1e1044", "#7c3aed", "#57467c", "Machine Learning · Data Products · Model Observability", "Feature Engineering · Experimentation · Clear Metrics"),
    3: make_theme("Orchid", "#e9d5ff", "#c026d3", "#2b1935", "#4a1d52", "#701a75", "701a75", "a21caf", "#310d3b", "#c026d3", "#754b7e", "Open Source · Developer Tools · Practical Automation", "Python · APIs · Documentation · Sustainable Engineering"),
    4: make_theme("Indigo", "#a5b4fc", "#6366f1", "#1c1d3a", "#27265d", "#3730a3", "3730a3", "4f46e5", "#111342", "#6366f1", "#4c4d80", "AI Infrastructure · Cloud Systems · Edge Intelligence", "Fast APIs · Deployment Discipline · Systems That Scale"),
    5: make_theme("Plum", "#f0abfc", "#d946ef", "#321a38", "#511c5c", "#86198f", "86198f", "a21caf", "#350b3d", "#c026d3", "#78477d", "Security · Privacy · Trustworthy AI", "Threat Modeling · Secure Defaults · Human-Centered Design"),
    6: make_theme("Wisteria", "#ddd6fe", "#7c3aed", "#211b36", "#35205a", "#5b21b6", "5b21b6", "7c3aed", "#1e0d3d", "#8b5cf6", "#5b477b", "Learning · Reflection · New Technical Horizons", "Books · Side Projects · Questions Worth Pursuing"),
}

QUOTES = [
    "Artificial intelligence can process data, but it cannot experience faith.",
    "The human brain still performs tasks no machine fully understands.",
    "Technology is created by humans; humans are shaped by deeper purpose.",
    "AI can recognize patterns, but meaning is something humans must find.",
    "Every line of code reflects the mind that wrote it.",
    "Machines follow algorithms; humans follow values.",
    "The universe operates with mathematical precision that scientists continue to study.",
    "Data creates knowledge, but wisdom requires reflection.",
    "Technology expands what we can do, not why we exist.",
    "AI can simulate conversation, but it does not possess consciousness.",
    "Human curiosity built machines that now help us explore creation.",
    "Even the most powerful computer still depends on human direction.",
    "Science explains how systems work; philosophy and faith explore why.",
    "Algorithms can optimize decisions, but morality guides them.",
    "The tools we build often reflect the beliefs we hold.",
    "Innovation grows where curiosity and purpose meet.",
    "Computers solve problems, but humans define which problems matter.",
    "Technology evolves quickly, but fundamental human questions remain.",
    "Knowledge increases with data, but wisdom grows with understanding.",
    "Every discovery in technology raises deeper questions about existence.",
]

WMO_CODES = {
    0:  ("Clear Sky", "☀️"),  1: ("Mainly Clear", "🌤️"),
    2:  ("Partly Cloudy", "⛅"), 3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"), 48: ("Icy Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"), 53: ("Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌧️"), 61: ("Light Rain", "🌧️"),
    63: ("Rain", "🌧️"), 65: ("Heavy Rain", "🌧️"),
    71: ("Light Snow", "🌨️"), 73: ("Snow", "❄️"),
    75: ("Heavy Snow", "❄️"), 80: ("Rain Showers", "🌦️"),
    81: ("Rain Showers", "🌧️"), 82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"), 99: ("Thunderstorm", "⛈️"),
}

DAY_GREETINGS = {
    0: "Moody Monday",   1: "Tame Tuesday",
    2: "Witty Wednesday", 3: "Thirsty Thursday",
    4: "Friyay Friday",  5: "Slack Saturday",
    6: "Slow Sunday",
}

def fetch_weather():
    params = urlencode({
      "latitude": LATITUDE,
      "longitude": LONGITUDE,
      "current": "temperature_2m,weather_code",
      "temperature_unit": "celsius",
      "timezone": TIMEZONE,
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    try:
      with urlopen(url, timeout=10) as response:
        data = json.loads(response.read())
      current = data["current"]
      temp = round(current["temperature_2m"])
      code = current.get("weather_code", current.get("weathercode"))
      desc, emoji = WMO_CODES.get(code, ("Unknown", "🌡️"))
      return temp, desc, emoji
    except Exception as error:
      print(f"Weather fetch failed: {error}", file=sys.stderr)
      return None, "Unknown", "🌡️"

def get_quote(day_of_year):
    return QUOTES[day_of_year % len(QUOTES)]

def wrap_text(text, max_chars):
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line) + len(word) + 1 <= max_chars:
            line = f"{line} {word}".strip()
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def escape_svg(text):
    return html.escape(str(text), quote=False)

# ── Generate dynamic.svg ──────────────────────────────────────────────────────
def generate_dynamic_svg(greeting, city, temp, weather_desc, weather_emoji, quote, updated_str, t):
    quote_lines = wrap_text(f'"{escape_svg(quote)}"', 36)
    quote_svg = ""
    total_height = len(quote_lines) * 24
    start_y = 152 - total_height // 2 + 16
    for i, l in enumerate(quote_lines):
        quote_svg += f'<text class="quote" x="465" y="{start_y + i * 24}">{l}</text>\n    '
    temp_str = f"{escape_svg(temp)}°C" if temp is not None else "N/A"
    greeting = escape_svg(greeting)
    city = escape_svg(city)
    weather_desc = escape_svg(weather_desc)
    weather_emoji = escape_svg(weather_emoji)
    updated_str = escape_svg(updated_str)
    p = t["primary"]; b = t["border"]; bc = t["bg_card"]
    bg2 = t["bg_grad_end"]; la = t["label"]; up = t["updated"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="620" height="320" viewBox="0 0 620 320">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:{bg2}"/>
    </linearGradient>
    <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bc}"/>
      <stop offset="100%" style="stop-color:{t['bg_accent']}"/>
    </linearGradient>
    <style>
      .greeting {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 26px; font-weight: 700; fill: #ffffff; }}
      .label    {{ font-family: 'Courier New', monospace; font-size: 11px; fill: {la}; letter-spacing: 2px; text-transform: uppercase; }}
      .value    {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 15px; fill: #e9d5ff; font-weight: 500; }}
      .weather-big  {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 42px; }}
      .weather-desc {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 13px; fill: {t['primary_dim']}; }}
      .quote    {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 13px; fill: {p}; font-style: italic; text-anchor: middle; }}
      .divider  {{ stroke: {b}; stroke-width: 1; }}
      .updated  {{ font-family: 'Courier New', monospace; font-size: 10px; fill: {up}; }}
      .dot      {{ fill: {la}; animation: pulse 2s ease-in-out infinite; }}
      @keyframes pulse {{ 0%, 100% {{ opacity: 1; r: 4px; }} 50% {{ opacity: 0.4; r: 3px; }} }}
    </style>
  </defs>
  <rect width="620" height="320" fill="url(#bg)" rx="16"/>
  <rect width="618" height="318" x="1" y="1" rx="15" fill="none" stroke="{b}" stroke-width="1"/>
  <rect x="20" y="20" width="260" height="280" rx="12" fill="url(#card)" opacity="0.6"/>
  <text class="greeting" x="40" y="65">{greeting}</text>
  <line x1="40" y1="115" x2="260" y2="115" class="divider"/>
  <text class="label" x="40" y="140">Weather · {city}</text>
  <text class="weather-big" x="40" y="195">{weather_emoji}</text>
  <text class="value" x="95" y="178">{temp_str}</text>
  <text class="weather-desc" x="95" y="198">{weather_desc}</text>
  <line x1="40" y1="215" x2="260" y2="215" class="divider"/>
  <circle class="dot" cx="48" cy="240" r="4"/>
  <text class="label" x="62" y="244">Live · Updates Daily</text>
  <text class="updated" x="40" y="272">Last updated: {updated_str}</text>
  <text class="updated" x="40" y="286">github.com/NinjaOfNeurons</text>
  <line x1="300" y1="20" x2="300" y2="300" class="divider"/>
  <text class="label" x="465" y="55" text-anchor="middle">Today's Thought</text>
  <line x1="320" y1="68" x2="610" y2="68" class="divider"/>
  <line x1="320" y1="285" x2="610" y2="285" class="divider"/>
  {quote_svg}
  <rect x="20" y="292" width="580" height="1" fill="{b}"/>
  <text class="label" x="310" y="310" text-anchor="middle">Trust me, I read the docs.</text>
</svg>"""

# ── Generate chat.svg ─────────────────────────────────────────────────────────
def generate_chat_svg(t):
    p = t["primary"]; bc = t["bg_card"]; ba = t["bg_accent"]
    # Timing (all in seconds, total cycle = 36s)
    # typing shows for 3s before each bubble
    # t1=0  b1=3   t2=7   b2=10  t3=15  b3=18  t4=23  b4=26  all fade=33 reset=36
    # SMIL keyTimes = time/36
    def kt(s): return f"{s/36:.3f}"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="620" height="400" viewBox="0 0 620 400">
  <defs>
    <style>
      .text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 15px; fill: #e9d5ff; }}
      .hi   {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 22px; font-weight: 700; fill: #ffffff; }}
      .dot-a {{ animation: bounce 0.8s ease infinite; }}
      .dot-b {{ animation: bounce 0.8s ease infinite; animation-delay: 0.2s; }}
      .dot-c {{ animation: bounce 0.8s ease infinite; animation-delay: 0.4s; }}
      @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-3px); }} }}
    </style>
  </defs>

  <rect width="620" height="400" fill="#0d1117" rx="16"/>
  <text class="hi" x="28" y="44">Hi there.</text>

  <!-- ── TYPING 1 (0s → 3s) ── -->
  <g>
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{kt(0)};{kt(3)};{kt(3.3)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="58" width="72" height="34" rx="17" fill="{bc}"/>
    <circle class="dot-a" cx="46" cy="75" r="4" fill="{p}"/>
    <circle class="dot-b" cx="60" cy="75" r="4" fill="{p}"/>
    <circle class="dot-c" cx="74" cy="75" r="4" fill="{p}"/>
  </g>
  <!-- BUBBLE 1: I'm Karanpreet Singh (3s → 33s) -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(3)};{kt(4.2)};{kt(33)};{kt(34)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="58" width="240" height="38" rx="18" fill="{bc}"/>
    <text class="text" x="48" y="82">I'm Karanpreet Singh.</text>
  </g>

  <!-- ── TYPING 2 (7s → 10s) ── -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(7)};{kt(7)};{kt(10)};{kt(10.3)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="108" width="72" height="34" rx="17" fill="{bc}"/>
    <circle class="dot-a" cx="46" cy="125" r="4" fill="{p}"/>
    <circle class="dot-b" cx="60" cy="125" r="4" fill="{p}"/>
    <circle class="dot-c" cx="74" cy="125" r="4" fill="{p}"/>
  </g>
  <!-- BUBBLE 2: Research background (10s → 33s) -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(10)};{kt(11.2)};{kt(33)};{kt(34)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="108" width="540" height="56" rx="18" fill="{bc}"/>
    <text class="text" x="48" y="131">Ex Research Assistant at SMARTH, University of Delhi</text>
    <text class="text" x="48" y="153">CPS Lab — where curiosity met real systems.</text>
  </g>

  <!-- ── TYPING 3 (15s → 18s) ── -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(15)};{kt(15)};{kt(18)};{kt(18.3)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="176" width="72" height="34" rx="17" fill="{bc}"/>
    <circle class="dot-a" cx="46" cy="193" r="4" fill="{p}"/>
    <circle class="dot-b" cx="60" cy="193" r="4" fill="{p}"/>
    <circle class="dot-c" cx="74" cy="193" r="4" fill="{p}"/>
  </g>
  <!-- BUBBLE 3: Focus areas (18s → 33s) -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(18)};{kt(19.2)};{kt(33)};{kt(34)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="176" width="530" height="56" rx="18" fill="{ba}"/>
    <text class="text" x="48" y="199">{t['focus']}</text>
    <text class="text" x="48" y="221">{t['focus2']}</text>
  </g>

  <!-- ── TYPING 4 (23s → 26s) ── -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(23)};{kt(23)};{kt(26)};{kt(26.3)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="244" width="72" height="34" rx="17" fill="{bc}"/>
    <circle class="dot-a" cx="46" cy="261" r="4" fill="{p}"/>
    <circle class="dot-b" cx="60" cy="261" r="4" fill="{p}"/>
    <circle class="dot-c" cx="74" cy="261" r="4" fill="{p}"/>
  </g>
  <!-- BUBBLE 4: ML Engineer (26s → 33s) -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(26)};{kt(27.2)};{kt(33)};{kt(34)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="244" width="530" height="38" rx="18" fill="{bc}"/>
    <text class="text" x="48" y="268">ML Engineer at VectorEdge — building practical AI that ships.</text>
  </g>

  <!-- BUBBLE 5: Contact — appears last, stays till reset (29s → 33s) -->
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(29)};{kt(30.2)};{kt(33)};{kt(34)};1" dur="36s" repeatCount="indefinite"/>
    <rect x="28" y="294" width="560" height="56" rx="18" fill="{bc}"/>
    <text class="text" x="48" y="318">Let's build something impactful —</text>
    <text class="text" x="48" y="340">reach out at <tspan fill="{p}">dev.karanpreet@gmail.com</tspan></text>
  </g>

</svg>"""

# ── Generate scholar.svg ──────────────────────────────────────────────────────
def generate_scholar_svg(t):
    p = t["primary"]; b = t["border"]; bc = t["bg_card"]
    la = t["label"]
    # Total cycle 28s looping SMIL animation
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 860 370">
  <defs>
    <style>
      .header     {{ font-family: 'Segoe UI', sans-serif; font-size: 20px; font-weight: 700; fill: #ffffff; }}
      .role       {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; fill: #e9d5ff; }}
      .stat-title {{ font-family: 'Segoe UI', sans-serif; font-size: 12px; fill: {p}; }}
      .stat-value {{ font-family: 'Segoe UI', sans-serif; font-size: 16px; fill: #ffffff; font-weight: 600; }}
      .paper      {{ font-family: 'Courier New', monospace; font-size: 13px; fill: #e9d5ff; }}
      .num        {{ fill: {p}; font-weight: 700; }}
      .link       {{ font-family: 'Segoe UI', sans-serif; font-size: 13px; fill: {p}; font-weight: 600; }}
      .dot-a {{ animation: bounce 0.7s ease infinite; }}
      .dot-b {{ animation: bounce 0.7s ease infinite; animation-delay: 0.15s; }}
      .dot-c {{ animation: bounce 0.7s ease infinite; animation-delay: 0.30s; }}
      @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
    </style>
  </defs>
  <rect width="860" height="370" rx="16" fill="#0d1117"/>
  <rect width="858" height="368" x="1" y="1" rx="15" fill="none" stroke="{b}" stroke-width="1"/>
  <text class="header" x="28" y="42">Google Scholar</text>
  <text class="role"   x="28" y="64">Research @ IIC · VectorEdge.io</text>
  <line x1="28" y1="76" x2="832" y2="76" stroke="{b}" stroke-width="1"/>
  <rect x="28"  y="88" width="110" height="44" rx="8" fill="{bc}"/>
  <text class="stat-title" x="40"  y="104">Citations</text>
  <text class="stat-value" x="40"  y="122">33</text>
  <rect x="150" y="88" width="110" height="44" rx="8" fill="{bc}"/>
  <text class="stat-title" x="162" y="104">h-index</text>
  <text class="stat-value" x="162" y="122">2</text>
  <rect x="272" y="88" width="110" height="44" rx="8" fill="{bc}"/>
  <text class="stat-title" x="284" y="104">i10-index</text>
  <text class="stat-value" x="284" y="122">2</text>
  <line x1="28" y1="144" x2="832" y2="144" stroke="{b}" stroke-width="1"/>
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.107;0.107;0.232;0.232;1" dur="28s" repeatCount="indefinite"/>
    <circle class="dot-a" cx="38" cy="168" r="4" fill="{la}"/>
    <circle class="dot-b" cx="52" cy="168" r="4" fill="{la}"/>
    <circle class="dot-c" cx="66" cy="168" r="4" fill="{la}"/>
  </g>
  <rect x="28" y="156" width="3" height="18" rx="1" fill="{p}">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0;0;0" keyTimes="0;0.107;0.125;0.143;0.161;0.179;0.197;0.215;0.232;1" dur="28s" repeatCount="indefinite"/>
  </rect>
  <text class="paper" x="28" y="170">
    <tspan class="num">1.</tspan>  Multimodal hate speech event detection (2023) · 17 citations
    <animate attributeName="opacity" values="0;0;0;1;1;0;0" keyTimes="0;0.214;0.257;0.271;0.893;0.929;1" dur="28s" repeatCount="indefinite"/>
  </text>
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.286;0.286;0.411;0.411;1" dur="28s" repeatCount="indefinite"/>
    <circle class="dot-a" cx="38" cy="198" r="4" fill="{la}"/>
    <circle class="dot-b" cx="52" cy="198" r="4" fill="{la}"/>
    <circle class="dot-c" cx="66" cy="198" r="4" fill="{la}"/>
  </g>
  <rect x="28" y="186" width="3" height="18" rx="1" fill="{p}">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0;0;0" keyTimes="0;0.286;0.304;0.322;0.340;0.358;0.376;0.393;0.411;1" dur="28s" repeatCount="indefinite"/>
  </rect>
  <text class="paper" x="28" y="200">
    <tspan class="num">2.</tspan>  AI-Driven IRM: Insider risk management (2025) · 7 citations
    <animate attributeName="opacity" values="0;0;0;1;1;0;0" keyTimes="0;0.393;0.436;0.450;0.893;0.929;1" dur="28s" repeatCount="indefinite"/>
  </text>
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.464;0.464;0.589;0.589;1" dur="28s" repeatCount="indefinite"/>
    <circle class="dot-a" cx="38" cy="228" r="4" fill="{la}"/>
    <circle class="dot-b" cx="52" cy="228" r="4" fill="{la}"/>
    <circle class="dot-c" cx="66" cy="228" r="4" fill="{la}"/>
  </g>
  <rect x="28" y="216" width="3" height="18" rx="1" fill="{p}">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0;0;0" keyTimes="0;0.464;0.482;0.500;0.518;0.536;0.554;0.571;0.589;1" dur="28s" repeatCount="indefinite"/>
  </rect>
  <text class="paper" x="28" y="230">
    <tspan class="num">3.</tspan>  Decoding Complexity with CHPDA (2025)
    <animate attributeName="opacity" values="0;0;0;1;1;0;0" keyTimes="0;0.571;0.614;0.629;0.893;0.929;1" dur="28s" repeatCount="indefinite"/>
  </text>
  <g>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.643;0.643;0.768;0.768;1" dur="28s" repeatCount="indefinite"/>
    <circle class="dot-a" cx="38" cy="258" r="4" fill="{la}"/>
    <circle class="dot-b" cx="52" cy="258" r="4" fill="{la}"/>
    <circle class="dot-c" cx="66" cy="258" r="4" fill="{la}"/>
  </g>
  <rect x="28" y="246" width="3" height="18" rx="1" fill="{p}">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0;0;0" keyTimes="0;0.643;0.661;0.679;0.696;0.714;0.732;0.750;0.768;1" dur="28s" repeatCount="indefinite"/>
  </rect>
  <text class="paper" x="28" y="260">
    <tspan class="num">4.</tspan>  LT-EDI-2023: Depression Level Detection in Social Media
    <animate attributeName="opacity" values="0;0;0;1;1;0;0" keyTimes="0;0.750;0.793;0.807;0.893;0.929;1" dur="28s" repeatCount="indefinite"/>
  </text>
  <line x1="28" y1="290" x2="832" y2="290" stroke="{b}" stroke-width="1"/>
  <rect x="28" y="304" width="246" height="38" rx="10" fill="{bc}"/>
  <text class="link" x="42" y="328">View Full Google Scholar Profile →</text>
</svg>"""

# ── Generate README.md ───────────────────────────────────────────────────────
def generate_readme(t, v):
    p   = t["primary"].lstrip("#")
    ws  = t["wave_start"]
    wm  = t["wave_mid"]
    pri = t["primary"].lstrip("#")
    dim = t["primary_dim"].lstrip("#")
    brd = t["border"].lstrip("#")
    lbl = t["label"].lstrip("#")

    return f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:{ws},50:{wm},100:{ws}&height=200&section=header&text=Karanpreet%20Singh&fontSize=54&fontColor=ffffff&fontAlignY=38&desc=Machine%20Learning%20Engineer%20%C2%B7%20Product%20Lead%20%C2%B7%20AI%20Explorer&descAlignY=58&descSize=16&descColor=e9d5ff" />

</div>

<br/>

<a href="https://www.linkedin.com/in/karanpreet-5ingh" target="_blank">
  <img src="https://raw.githubusercontent.com/NinjaOfNeurons/NinjaOfNeurons/main/assets/svg/chat.svg?v={v}" />
</a>

<br/>


---

## Currently Building

```
cli-rag-app/          →  Command-line RAG for intelligent retrieval
agentic-ai-lab/       →  Autonomous agents & tool-using AI systems
```

## Upcoming

```
rag-insider-risk/         →  RAG pipeline for insider risk intelligence
model-health-dashboard/   →  AI model drift & reliability monitoring
```

---

## Research & Certifications

<div align="center">

<a href="https://scholar.google.com/citations?user=gmjWDxkAAAAJ&hl=en" target="_blank">
  <img src="https://raw.githubusercontent.com/NinjaOfNeurons/NinjaOfNeurons/main/assets/svg/scholar.svg?sanitize=true&v={v}" alt="Google Scholar" />
</a>

</div>

---

### Certifications

<div align="center">

<table border="0" cellspacing="0" cellpadding="16">
  <tr>
    <td align="center">
      <a href="https://www.credly.com/badges/487b8d6c-4a04-4049-be2f-515f4e570f15" target="_blank">
        <img src="assets/badges/rag-cert.png" width="110" />
      </a>
      <br/><br/>
      <sub><b>Advanced RAG with<br/>Vector Databases</b></sub><br/>
      <sub>Coursera · Credly</sub>
    </td>
    <td width="20"></td>
    <td align="center">
      <a href="https://www.credly.com/badges/ca8d463b-5766-4baf-bf06-1a0d8bf58a12/public_url" target="_blank">
        <img src="assets/badges/ai-agents-cert.png" width="110" />
      </a>
      <br/><br/>
      <sub><b>Fundamentals of<br/>Building AI Agents</b></sub><br/>
      <sub>Coursera · Credly</sub>
    </td>
    <td width="20"></td>
    <td align="center">
      <a href="https://www.credly.com/earner/earned/badge/355ea60a-d44c-4cc2-b4c0-e7639d465e3e" target="_blank">
        <img src="assets/badges/langchain-cert.png" width="110" />
      </a>
      <br/><br/>
      <sub><b>Agentic AI with<br/>LangChain & LangGraph</b></sub><br/>
      <sub>Coursera · Credly</sub>
    </td>
    <td width="20"></td>
    <td align="center">
      <a href="https://www.credly.com/badges/a4b85937-f69b-4066-8023-02c5c87cba4a/public_url" target="_blank">
        <img src="assets/badges/crewai-cert.png" width="110" />
      </a>
      <br/><br/>
      <sub><b>Agentic AI with LangGraph,<br/>CrewAI, AutoGen & BeeAI</b></sub><br/>
      <sub>Coursera · Credly</sub>
    </td>
    <td width="20"></td>
    <td align="center">
      <a href="https://www.credly.com/badges/51431761-8da1-4087-afd6-bdcec6b612b7/public_url" target="_blank">
        <img src="assets/badges/mcp-cert.png" width="110" />
      </a>
      <br/><br/>
      <sub><b>Build AI Agents<br/>Using MCP</b></sub><br/>
      <sub>Coursera · Credly</sub>
    </td>
  </tr>
</table>

<br/>

</div>

---

## Tech Stack

<div align="center">

<br/>

<table>
  <tr>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/python-icon.svg" width="55" height="55" /><br/>Python
    </td>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/cpp-icon.svg" width="55" height="55" /><br/>C++
    </td>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/aws-icon.svg" width="55" height="55" /><br/>AWS
    </td>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/docker-icon.svg" width="55" height="55" /><br/>Docker
    </td>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/kubernetes-icon.svg" width="55" height="55" /><br/>Kubernetes
    </td>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/github-icon.svg" width="55" height="55" /><br/>GitHub
    </td>
    <td align="center" width="90">
      <img src="https://techstack-generator.vercel.app/mysql-icon.svg" width="55" height="55" /><br/>SQL
    </td>
  </tr>
  <tr>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=pytorch" width="48" height="48" /><br/>PyTorch
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=tensorflow" width="48" height="48" /><br/>TensorFlow
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=opencv" width="48" height="48" /><br/>OpenCV
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=fastapi" width="48" height="48" /><br/>FastAPI
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=flask" width="48" height="48" /><br/>Flask
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=django" width="48" height="48" /><br/>Django
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=gcp" width="48" height="48" /><br/>GCP
    </td>
  </tr>
  <tr>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=linux" width="48" height="48" /><br/>Linux
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=git" width="48" height="48" /><br/>Git
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=grafana" width="48" height="48" /><br/>Grafana
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=prometheus" width="48" height="48" /><br/>Prometheus
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=jenkins" width="48" height="48" /><br/>Jenkins
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=arduino" width="48" height="48" /><br/>Arduino
    </td>
    <td align="center" width="90">
      <img src="https://skillicons.dev/icons?i=androidstudio" width="48" height="48" /><br/>Android
    </td>
  </tr>
</table>

<br/>

**RAG & Vector Intelligence**

<table>
  <tr>
    <td align="center" width="90">
      <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/dark/langchain-color.png" width="48" height="48" /><br/>LangChain
    </td>
    <td align="center" width="90">
      <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/dark/langgraph-color.png" width="48" height="48" /><br/>LangGraph
    </td>
    <td align="center" width="90">
      <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/dark/llamaindex-color.png" width="48" height="48" /><br/>LlamaIndex
    </td>
    <td align="center" width="90">
      <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/dark/gradio-color.png" width="48" height="48" /><br/>Gradio
    </td>
    <td align="center" width="90">
      <img src="https://img.shields.io/badge/-Pinecone-black?style=flat-square&logo=pinecone" /><br/>Pinecone
    </td>
    <td align="center" width="90">
      <img src="https://img.shields.io/badge/-ChromaDB-FF6719?style=flat-square&logo=databricks&logoColor=white" /><br/>ChromaDB
    </td>
    <td align="center" width="90">
      <img src="https://img.shields.io/badge/-FAISS-0467DF?style=flat-square&logo=meta&logoColor=white" /><br/>FAISS
    </td>
  </tr>
</table>

</div>

---

## 2026 Vision

```
▸  Engineering   →  Build production-grade AI systems at scale
▸  Research      →  Publish impactful applied AI work
▸  Frontier      →  AI × Security × Edge Intelligence
▸  Web3          →  Deep dive into Bitcoin infra & decentralized systems
```

---

## Activity


<div align="center">
<img src="https://raw.githubusercontent.com/NinjaOfNeurons/NinjaOfNeurons/main/assets/svg/dynamic.svg?sanitize=true&v={v}" alt="Dynamic Profile Card" />
</div>

<br/>

<div align="center">
<img src="https://raw.githubusercontent.com/NinjaOfNeurons/NinjaOfNeurons/output/github-contribution-grid-snake-dark.svg" alt="contribution snake" />
</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:{ws},50:{wm},100:{ws}&height=120&section=footer&text=%22Let%27s+connect+and+explore+the+world+of+AI+together.%22&fontSize=13&fontColor=e9d5ff&fontAlignY=65" width="100%" />
"""

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    now = dt.datetime.now(dt.timezone.utc)
    weekday = now.weekday()
    t       = THEMES[weekday]

    greeting = DAY_GREETINGS[weekday]
    quote    = get_quote(now.timetuple().tm_yday)
    temp, weather_desc, weather_emoji = fetch_weather()
    updated  = now.strftime("%b %d, %Y · %H:%M UTC")

    # Version = day of year so it increments daily busting all caches
    v = now.timetuple().tm_yday

    output_dir = Path(__file__).resolve().parent
    svg_dir = output_dir / "assets" / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)

    # dynamic.svg
    svg_dynamic = generate_dynamic_svg(greeting, CITY, temp, weather_desc, weather_emoji, quote, updated, t)
    with (svg_dir / "dynamic.svg").open("w", encoding="utf-8") as f:
        f.write(svg_dynamic)
    print(f"✓ dynamic.svg  — {greeting} · {t['name']} theme · {temp}°C {weather_emoji}")

    # chat.svg
    svg_chat = generate_chat_svg(t)
    with (svg_dir / "chat.svg").open("w", encoding="utf-8") as f:
        f.write(svg_chat)
    print(f"✓ chat.svg     — {t['name']} theme · focus: {t['focus'][:40]}...")

    # scholar.svg
    svg_scholar = generate_scholar_svg(t)
    with (svg_dir / "scholar.svg").open("w", encoding="utf-8") as f:
        f.write(svg_scholar)
    print(f"✓ scholar.svg  — {t['name']} theme")

    # README.md
    readme = generate_readme(t, v)
    with (output_dir / "README.md").open("w", encoding="utf-8") as f:
        f.write(readme)
    print(f"✓ README.md    — {t['name']} theme · v={v} · waves + stats updated")

if __name__ == "__main__":
    main()
