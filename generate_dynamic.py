import urllib.request
import json
import datetime
import math
import sys

# ── Config ────────────────────────────────────────────────────────────────────
CITY        = "Ohio, USA"  
LATITUDE    = 40.417286   
LONGITUDE   = -82.907120  
TIMEZONE    = "America/Panama"  
# Asia/Calcutta, America/New_York, Europe/London, etc.
# ──────────────────────────────────────────────────────────────────────────────
QUOTES = [
    "Intelligence is the ability to adapt to change.",
    "The best way to predict the future is to invent it.",
    "Data is the new oil. AI is the refinery.",
    "Build systems that think, then think about what you built.",
    "Research without production is just theory.",
    "Security is not a feature. It's a foundation.",
    "Edge computing: bringing intelligence closer to reality.",
    "A model is only as good as the data it learns from.",
    "Encrypt everything. Trust nothing. Verify always.",
    "RAG: giving AI the memory it was never born with.",
    "The best models are the ones that know their limits.",
    "Agentic AI: from answering questions to taking actions.",
]
 
WMO_CODES = {
    0:  ("Clear Sky", "☀️"),
    1:  ("Mainly Clear", "🌤️"),
    2:  ("Partly Cloudy", "⛅"),
    3:  ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Icy Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌧️"),
    61: ("Light Rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Light Snow", "🌨️"),
    73: ("Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Rain Showers", "🌧️"),
    82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    99: ("Thunderstorm", "⛈️"),
}
 
DAY_GREETINGS = {
    0: "Happy Monday",
    1: "Happy Tuesday",
    2: "Happy Wednesday",
    3: "Happy Thursday",
    4: "Happy Friday",
    5: "Happy Saturday",
    6: "Happy Sunday",
}
 
def fetch_weather():
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&current=temperature_2m,weathercode"
        f"&temperature_unit=celsius"
        f"&timezone={TIMEZONE}"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        temp = round(data["current"]["temperature_2m"])
        code = data["current"]["weathercode"]
        desc, emoji = WMO_CODES.get(code, ("Unknown", "🌡️"))
        return temp, desc, emoji
    except Exception as e:
        print(f"Weather fetch failed: {e}", file=sys.stderr)
        return None, "Unknown", "🌡️"
 
def get_quote(day_of_year):
    return QUOTES[day_of_year % len(QUOTES)]
 
def wrap_text(text, max_chars):
    """Wrap text into lines of max_chars."""
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
 
def generate_svg(greeting, city, temp, weather_desc, weather_emoji, quote, updated_str):
    quote_lines = wrap_text(f'"{quote}"', 36)
    quote_svg = ""
    total_height = len(quote_lines) * 24
    start_y = 152 - total_height // 2 + 16
    for i, l in enumerate(quote_lines):
        quote_svg += f'<text class="quote" x="465" y="{start_y + i * 24}">{l}</text>\n    '
 
    temp_str = f"{temp}°C" if temp is not None else "N/A"
 
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="620" height="320" viewBox="0 0 620 320">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#1a0533"/>
    </linearGradient>
    <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e1b2e"/>
      <stop offset="100%" style="stop-color:#2d1b4e"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .greeting {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 26px;
        font-weight: 700;
        fill: #ffffff;
      }}
      .label {{
        font-family: 'Courier New', monospace;
        font-size: 11px;
        fill: #7c3aed;
        letter-spacing: 2px;
        text-transform: uppercase;
      }}
      .value {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 15px;
        fill: #e9d5ff;
        font-weight: 500;
      }}
      .weather-big {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 42px;
      }}
      .weather-desc {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 13px;
        fill: #a78bfa;
      }}
      .quote {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 13px;
        fill: #c084fc;
        font-style: italic;
        text-anchor: middle;
      }}
      .divider {{
        stroke: #3b0764;
        stroke-width: 1;
      }}
      .updated {{
        font-family: 'Courier New', monospace;
        font-size: 10px;
        fill: #4b3b6b;
      }}
      .dot {{
        fill: #7c3aed;
        animation: pulse 2s ease-in-out infinite;
      }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; r: 4px; }}
        50%       {{ opacity: 0.4; r: 3px; }}
      }}
    </style>
  </defs>
 
  <!-- Background -->
  <rect width="620" height="320" fill="url(#bg)" rx="16"/>
  <rect width="618" height="318" x="1" y="1" rx="15" fill="none" stroke="#3b0764" stroke-width="1"/>
 
  <!-- Left panel -->
  <rect x="20" y="20" width="260" height="280" rx="12" fill="url(#card)" opacity="0.6"/>
 
  <!-- Greeting -->
  <text class="greeting" x="40" y="65">{greeting},</text>
  <text class="greeting" x="40" y="95" fill="#c084fc">Karan ✦</text>
 
  <!-- Divider -->
  <line x1="40" y1="115" x2="260" y2="115" class="divider"/>
 
  <!-- Weather block -->
  <text class="label" x="40" y="140">Weather · {city}</text>
  <text class="weather-big" x="40" y="195">{weather_emoji}</text>
  <text class="value" x="95" y="178">{temp_str}</text>
  <text class="weather-desc" x="95" y="198">{weather_desc}</text>
 
  <!-- Divider -->
  <line x1="40" y1="215" x2="260" y2="215" class="divider"/>
 
  <!-- Live dot + updated -->
  <circle class="dot" cx="48" cy="240" r="4"/>
  <text class="label" x="62" y="244">Live · Updates Daily</text>
  <text class="updated" x="40" y="272">Last updated: {updated_str}</text>
  <text class="updated" x="40" y="286">github.com/NinjaOfNeurons</text>
 
  <!-- Vertical divider -->
  <line x1="300" y1="20" x2="300" y2="300" class="divider"/>
 
  <!-- Right panel - Quote -->
  <text class="label" x="465" y="55" text-anchor="middle">Today's Thought</text>
  <line x1="320" y1="68" x2="610" y2="68" class="divider"/>
  <line x1="320" y1="285" x2="610" y2="285" class="divider"/>
 
  {quote_svg}
 
  <!-- Bottom strip -->
  <rect x="20" y="292" width="580" height="1" fill="#3b0764"/>
  <text class="label" x="310" y="310" text-anchor="middle">ML Engineer · RAG · Agentic AI · Edge Intelligence</text>
 
</svg>
"""
 
def main():
    now = datetime.datetime.utcnow()
    # Use day of week for greeting
    greeting = DAY_GREETINGS[now.weekday()]
    quote    = get_quote(now.timetuple().tm_yday)
    temp, weather_desc, weather_emoji = fetch_weather()
    updated  = now.strftime("%b %d, %Y · %H:%M UTC")
 
    svg = generate_svg(greeting, CITY, temp, weather_desc, weather_emoji, quote, updated)
 
    with open("dynamic.svg", "w", encoding="utf-8") as f:
        f.write(svg)
 
    print(f"✓ Generated dynamic.svg — {greeting}, {temp}°C {weather_emoji}, quote #{now.timetuple().tm_yday % len(QUOTES)}")
 
if __name__ == "__main__":
    main()
 