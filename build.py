#!/usr/bin/env python3
"""Generate the static Norse Audio mockup. Local only. Safe to re-run."""
from pathlib import Path
import json
import html as htmlmod

ROOT = Path(__file__).resolve().parent

NAV = [
    ("Home", "index.html", "home"),
    ("Products", "products/", "products"),
    ("About Us", "about-us/", "about-us"),
    ("News", "news/", "news"),
    ("Contact", "contact/", "contact"),
    ("Family", "family/", "family"),
]

FB = "https://www.facebook.com/profile.php?id=61580190315646"
IG = "https://www.instagram.com/norse_audio/"
BLADELIUS = "https://bladelius.com"
ABTECH = "https://ab-tech.se"

ICON_FB = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-5 2.2-5 5v2H6v4h3v8h4v-8h3l1-4h-4V9c0-.6.4-1 1-1z"/></svg>'''
ICON_IG = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm10 2H7a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm-5 3.2A3.8 3.8 0 1 1 8.2 12 3.8 3.8 0 0 1 12 8.2zm0 1.6A2.2 2.2 0 1 0 14.2 12 2.2 2.2 0 0 0 12 9.8zM17.2 6.6a.9.9 0 1 1-.9.9.9.9 0 0 1 .9-.9z"/></svg>'''
ICON_MENU = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3V6zm0 5h18v2H3v-2zm0 5h18v2H3v-2z"/></svg>'''

ASSET_V = "1"
SITE = "https://www.norseaudio.se"

DESC_DEFAULT = (
    "Norse Audio, powered by Bladelius. A modular high-fidelity system "
    "designed in Sweden: the X1 power amplifier, X2 pre-amplifier and X5 power supply."
)

NEWS = [
    {
        "slug": "warsaw-audio-video-show-2025",
        "title": "Warsaw Audio Video Show 2025",
        "date": "20 Oct, 2025",
        "date_iso": "2025-10-20",
        "image": "images/news/warsaw.jpg",
        "alt": "Norse Audio component at the Warsaw Audio Video Show 2025",
        "excerpt": "See our products for the first time ever. Visit us in room 401 and 407 in the Sobieski Hotel at this year's audio video show in Warsaw, October 24–26.",
        "body": (
            "<p>See our products for the first time ever.</p>"
            "<p>Visit us in room 401 and 407 in the Sobieski Hotel at this year's "
            "audio video show in Warsaw, October 24–26.</p>"
        ),
    },
    {
        "slug": "norse-by-bladelius",
        "title": "Norse, powered by Bladelius",
        "date": "6 Oct, 2025",
        "date_iso": "2025-10-06",
        "image": "images/news/system.jpg",
        "alt": "Norse Audio component",
        "excerpt": "Read more about the new Norse X1 and X5.",
        "body": (
            "<p>Read more about the new Norse X1 power amplifier and X5 power supply "
            'on the <a href="../products/">products</a> page.</p>'
        ),
        "link_override": None,
    },
]


def prefix(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def href(depth: int, target: str) -> str:
    p = prefix(depth)
    if target == "index.html":
        return p + "index.html" if p else "index.html"
    return p + target


def header(depth: int, current: str) -> str:
    p = prefix(depth)
    items = []
    for label, target, key in NAV:
        url = href(depth, target)
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'          <li><a href="{url}"{cur}>{label}</a></li>')
    nav = "\n".join(items)
    return f'''  <header class="site-header">
    <div class="inner">
      <a class="logo" href="{href(depth, "index.html")}" aria-label="Norse Audio home">
        <img src="{p}images/brand/logo.png?v={ASSET_V}" width="200" height="53" alt="Norse">
      </a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">{ICON_MENU}</button>
      <nav class="site-nav" id="site-nav">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>'''


def footer(depth: int) -> str:
    p = prefix(depth)
    return f'''  <footer class="site-footer">
    <div class="inner">
      <div>Norse Audio, powered by Bladelius</div>
      <div class="footer-social">
        <a href="{FB}" target="_blank" rel="noopener" title="Facebook" aria-label="Facebook">{ICON_FB}</a>
        <a href="{IG}" target="_blank" rel="noopener" title="Instagram" aria-label="Instagram">{ICON_IG}</a>
      </div>
    </div>
  </footer>
  <script src="{p}js/main.js?v={ASSET_V}"></script>'''


def jsonld_tag(data) -> str:
    if not data:
        return ""
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{payload}\n  </script>\n'


def org_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Norse Audio",
        "brand": "Norse Audio",
        "url": f"{SITE}/",
        "logo": f"{SITE}/images/brand/logo.png",
        "parentOrganization": {
            "@type": "Organization",
            "name": "Bladelius",
            "url": BLADELIUS + "/",
        },
        "sameAs": [IG, FB],
    }


def product_jsonld(name: str, description: str, image_file: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": description,
        "brand": {"@type": "Brand", "name": "Norse Audio"},
        "image": f"{SITE}/images/products/{image_file}",
    }


def page(depth: int, current: str, title: str, body: str, extra_head: str = "", description: str = "", json_ld=None) -> str:
    p = prefix(depth)
    desc = description or DESC_DEFAULT
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{htmlmod.escape(title)}</title>
  <meta name="description" content="{htmlmod.escape(desc)}">
  <link rel="icon" href="{p}favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{p}css/style.css?v={ASSET_V}">
{extra_head}{jsonld_tag(json_ld)}</head>
<body>
{header(depth, current)}
{body}
{footer(depth)}
</body>
</html>
'''


def write(rel: str, text: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", rel, path.stat().st_size)


def img_src(path: str, depth: int) -> str:
    return path if depth == 0 else prefix(depth) + path


def family_mini(depth: int) -> str:
    p = prefix(depth)
    return f'''      <section class="product-group sister-mini">
        <h2>The Bladelius family</h2>
        <div class="sister-mini-grid">
          <article class="sister-mini-card">
            <a class="thumb" href="{BLADELIUS}" target="_blank" rel="noopener">
              <img src="{p}images/family/bladelius.jpg" alt="Bladelius amplifier">
            </a>
            <div class="sister-mini-body">
              <h3>Bladelius</h3>
              <p>High-performance audio electronics, designed in Sweden.</p>
              <a class="text-link" href="{BLADELIUS}" target="_blank" rel="noopener">Visit website</a>
            </div>
          </article>
          <article class="sister-mini-card">
            <a class="thumb" href="{ABTECH}" target="_blank" rel="noopener">
              <img src="{p}images/family/abtech.jpg" alt="AB Tech product">
            </a>
            <div class="sister-mini-body">
              <h3>AB Tech</h3>
              <p>High-end audio isolators, cables and power products, made in Sweden.</p>
              <a class="text-link" href="{ABTECH}" target="_blank" rel="noopener">Visit website</a>
            </div>
          </article>
        </div>
        <p class="sister-more"><a class="text-link" href="{href(depth, "family/")}">The Bladelius family</a></p>
      </section>'''


def home():
    slides = []
    for i, post in enumerate(NEWS):
        active = " is-active" if i == 0 else ""
        url = "news/"
        img = post["image"]
        slides.append(
            f'        <article class="slide{active}">\n'
            f'          <a href="{url}">\n'
            f'            <div class="slide-image"><img src="{htmlmod.escape(img)}" alt="{htmlmod.escape(post["alt"])}"></div>\n'
            f'            <div class="slide-body">\n'
            f'              <p class="kicker">News · {htmlmod.escape(post["date"])}</p>\n'
            f'              <h3>{htmlmod.escape(post["title"])}</h3>\n'
            f'              <p>{htmlmod.escape(post["excerpt"])}</p>\n'
            f'            </div>\n'
            f'          </a>\n'
            f'        </article>'
        )

    extra = '  <style>.hero { background-image: url("images/hero/home.jpg"); background-position: 50% 50%; }</style>\n'
    body = (
        '  <main>\n'
        '    <section class="hero" aria-label="Norse Audio"></section>\n'
        '\n'
        '    <section class="home-latest">\n'
        '      <div class="wrap">\n'
        '        <div class="section-head">\n'
        '          <h2>Latest</h2>\n'
        '          <a class="text-link" href="news/">All news</a>\n'
        '        </div>\n'
        '        <div class="slider" data-slider data-interval="7000" aria-label="Latest news">\n'
        '          <div class="slider-viewport">\n'
        + "\n".join(slides) + "\n"
        '          </div>\n'
        '          <div class="slider-controls">\n'
        '            <button type="button" class="slider-prev" aria-label="Previous"></button>\n'
        '            <div class="slider-dots" role="tablist" aria-label="Choose slide"></div>\n'
        '            <button type="button" class="slider-next" aria-label="Next"></button>\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
        '\n'
        '    <section class="home-follow">\n'
        '      <div class="wrap">\n'
        '        <h2>Follow</h2>\n'
        '        <p>Updates from the workshop and the road, on Instagram and Facebook.</p>\n'
        '        <div class="follow-links">\n'
        f'          <a href="{IG}" target="_blank" rel="noopener">Instagram</a>\n'
        f'          <a href="{FB}" target="_blank" rel="noopener">Facebook</a>\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
        '  </main>'
    )
    write("index.html", page(0, "home", "Norse Audio", body, extra_head=extra,
                             description=DESC_DEFAULT, json_ld=org_jsonld()))


def products():
    body = f'''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>Products</h1>
        <p class="lede">The Norse Audio system is a modular high-fidelity setup, powered by Bladelius. The X1 power amplifier, X2 pre-amplifier and X5 power supply are built to work together, so a system can start simple and grow.</p>
      </header>

      <section class="product-group">
        <h2>The Norse system</h2>
        <div class="product-grid">
          <a class="product-card" href="../x1/">
            <div class="thumb"><img src="../images/products/front.jpg" alt="Norse Audio X1 Power Amplifier"></div>
            <div class="label">X1 — Power Amplifier</div>
          </a>
          <a class="product-card" href="../x2/">
            <div class="thumb"><img src="../images/products/detail.jpg" alt="Norse Audio X2 Pre-Amplifier"></div>
            <div class="label">X2 — Pre-Amplifier</div>
          </a>
          <a class="product-card" href="../x5/">
            <div class="thumb"><img src="../images/products/angle.jpg" alt="Norse Audio X5 Power Supply"></div>
            <div class="label">X5 — Power Supply</div>
          </a>
        </div>
      </section>

{family_mini(1)}
    </div>
  </main>'''
    write("products/index.html", page(1, "products", "Norse Audio – Products", body,
                                      description="The Norse Audio system: X1 power amplifier, X2 pre-amplifier and X5 power supply. A modular high-fidelity system powered by Bladelius."))


def x1():
    body = '''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>X1 Power Amplifier</h1>
        <p class="lede">The heart of the Norse system. A fully balanced amplifier that can run as a stereo unit or, with a second X1, as a dual-mono pair.</p>
      </header>

      <div class="product-hero">
        <a href="../images/products/front.jpg" data-lightbox>
          <img src="../images/products/front.jpg" alt="Norse Audio X1 Power Amplifier">
        </a>
      </div>

      <div class="split">
        <div class="prose">
          <p>A rear-panel toggle switch lets you move between stereo and mono modes, so a system can begin with a single stereo amplifier and later become a dual-mono setup.</p>
          <p>The X1 also has an adjustable bias toggle with two modes:</p>
          <ul>
            <li><strong>Normal Bias</strong> — increases Class A operation for a warmer, richer sound with exceptional linearity.</li>
            <li><strong>Low Bias</strong> — prioritises efficiency while keeping high-quality audio, for extended use or less demanding listening.</li>
          </ul>
          <h2>Simpler is better</h2>
          <p>The X1 uses a single voltage amplifier stage for the shortest signal path possible. It is a fully balanced design without a ground reference, paired with a high-performance DC servo that operates outside the signal path.</p>
          <p>The input stage uses hand-matched, current-loaded JFETs in a foldback cascade arrangement, for linear performance at any output level. Combined with current feedback, the X1 is fast, stable and dynamic.</p>
          <p>This power output will drive a wide range of loudspeakers, from compact bookshelf models to demanding floorstanders, with precision and control.</p>
        </div>
        <div class="specs">
          <h2>Specifications</h2>
          <ul>
            <li>Power output, stereo: 50 W per channel at 8 ohms; 100 W per channel at 4 ohms</li>
            <li>Power output, mono: 200 W at 8 ohms; 390 W at 4 ohms</li>
            <li>Rated distortion: less than 0.01%</li>
            <li>Signal-to-noise ratio: more than 125 dB</li>
            <li>Frequency response: 1 Hz to 100 kHz, +0/−3 dB</li>
            <li>Bias modes: Low or Normal, via toggle switch</li>
            <li>Configuration: stereo or mono, via toggle switch</li>
            <li>Dimensions: 240 mm (W) × 67 mm (H) × 248 mm (D)</li>
            <li>Weight: 6 kg</li>
          </ul>
        </div>
      </div>

      <div class="gallery">
        <a href="../images/products/angle.jpg" data-lightbox><img src="../images/products/angle.jpg" alt="Norse Audio component, three-quarter view"></a>
        <a href="../images/products/detail.jpg" data-lightbox><img src="../images/products/detail.jpg" alt="Norse Audio component, close view"></a>
      </div>
    </div>
  </main>'''
    write("x1/index.html", page(
        1, "products", "Norse Audio – X1 Power Amplifier", body,
        description="The Norse Audio X1 power amplifier. Stereo or mono, with adjustable bias, powered by Bladelius.",
        json_ld=product_jsonld(
            "Norse Audio X1 Power Amplifier",
            "A fully balanced power amplifier that can run in stereo or mono, with adjustable bias. Part of the Norse Audio modular system, powered by Bladelius.",
            "front.jpg",
        ),
    ))


def x2():
    body = '''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>X2 Pre-Amplifier</h1>
        <p class="lede">A high-end discrete MOSFET preamplifier, with a fully discrete, DC-coupled signal path and a high-precision relay attenuator.</p>
      </header>

      <div class="product-hero">
        <a href="../images/products/detail.jpg" data-lightbox>
          <img src="../images/products/detail.jpg" alt="Norse Audio X2 Pre-Amplifier">
        </a>
      </div>

      <div class="split">
        <div class="prose">
          <p>The X2 uses a pure single-ended MOSFET gain stage, carefully set up for exceptional linearity, ultra-low noise, and a natural, effortless sound. The signal path is fully discrete and DC-coupled throughout, with a current-loaded output stage for maximum linearity, preserving signal integrity while keeping the warmth and musicality of a well-executed single-ended MOSFET design.</p>
          <p>Volume control is a high-precision relay attenuator that uses premium 0.01% tolerance metal-film resistors in a ladder, or switched-resistor, topology. The result is outstanding accuracy, perfect channel matching and complete transparency, with no loss of quality even at the lowest listening levels.</p>
          <h2>Connectivity</h2>
          <ul>
            <li>4 pairs of balanced XLR inputs</li>
            <li>3 pairs of balanced XLR outputs, for bi-amping or for driving several power amplifiers and subwoofers at once</li>
          </ul>
          <h2>Refinements</h2>
          <ul>
            <li>Ultra-low noise power supply with several stages of regulation and extensive decoupling</li>
            <li>Microprocessor-controlled relay switching for silent input selection and muting</li>
            <li>High-quality input and output relays with gold-plated contacts</li>
            <li>A short, minimalist signal path and premium-grade components</li>
            <li>Remote control</li>
          </ul>
          <p>This architecture is built for a wide dynamic range, strong channel separation, effortless micro-dynamics and precise control. It brings together the musicality of single-ended MOSFET operation with the accuracy, speed and drive of a modern high-end system.</p>
        </div>
        <div class="specs">
          <h2>Specifications</h2>
          <ul>
            <li>Topology: discrete single-ended MOSFET, DC-coupled</li>
            <li>Volume: precision relay attenuator, 0.01% metal-film resistors</li>
            <li>Inputs: 4 × balanced XLR</li>
            <li>Outputs: 3 × balanced XLR</li>
            <li>Remote control</li>
            <li>Powered by the X5 power supply</li>
          </ul>
        </div>
      </div>

      <div class="gallery">
        <a href="../images/products/front.jpg" data-lightbox><img src="../images/products/front.jpg" alt="Norse Audio component, front view"></a>
        <a href="../images/products/angle.jpg" data-lightbox><img src="../images/products/angle.jpg" alt="Norse Audio component, three-quarter view"></a>
      </div>
    </div>
  </main>'''
    write("x2/index.html", page(
        1, "products", "Norse Audio – X2 Pre-Amplifier", body,
        description="The Norse Audio X2 pre-amplifier. A discrete MOSFET, fully balanced preamplifier, powered by Bladelius.",
        json_ld=product_jsonld(
            "Norse Audio X2 Pre-Amplifier",
            "A high-end discrete MOSFET preamplifier with a fully discrete, DC-coupled signal path and a precision relay attenuator. Part of the Norse Audio modular system, powered by Bladelius.",
            "detail.jpg",
        ),
    ))


def x5():
    body = '''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>X5 Power Supply</h1>
        <p class="lede">The backbone of the Norse system. Clean, stable power for up to two X1 power amplifiers and one X2 pre-amplifier.</p>
      </header>

      <div class="product-hero">
        <a href="../images/products/angle.jpg" data-lightbox>
          <img src="../images/products/angle.jpg" alt="Norse Audio X5 Power Supply">
        </a>
      </div>

      <div class="split">
        <div class="prose">
          <p>The X5 feeds the rest of the system. Adjustable power settings let you match the supply to a stereo or mono setup.</p>
          <p>Even at lower power settings the X1 stays authoritative, with clarity and impact for a wide range of speakers and rooms. The X5 has two power outputs for X1 amplifiers and one dedicated output for the X2 pre-amplifier, so a system can grow from a single stereo amplifier to a dual-mono pair without changing the supply.</p>
          <p>The result is quiet operation and clean reproduction across different listening conditions.</p>
        </div>
        <div class="specs">
          <h2>Specifications</h2>
          <ul>
            <li>Power outputs: 2 for X1 power amplifiers; 1 for the X2 pre-amplifier</li>
            <li>Adjustable power, stereo: 25–50 W at 8 ohms; 40–100 W at 4 ohms</li>
            <li>Adjustable power, mono: 100–200 W at 8 ohms; 200–390 W at 4 ohms</li>
            <li>Dimensions: 240 mm (W) × 67 mm (H) × 248 mm (D)</li>
            <li>Weight: 6 kg</li>
          </ul>
        </div>
      </div>

      <div class="gallery">
        <a href="../images/products/front.jpg" data-lightbox><img src="../images/products/front.jpg" alt="Norse Audio component, front view"></a>
        <a href="../images/products/detail.jpg" data-lightbox><img src="../images/products/detail.jpg" alt="Norse Audio component, close view"></a>
      </div>
    </div>
  </main>'''
    write("x5/index.html", page(
        1, "products", "Norse Audio – X5 Power Supply", body,
        description="The Norse Audio X5 power supply. Clean, stable power for the X1 and X2, powered by Bladelius.",
        json_ld=product_jsonld(
            "Norse Audio X5 Power Supply",
            "A dedicated power supply for up to two X1 power amplifiers and one X2 pre-amplifier, with adjustable power settings. Part of the Norse Audio modular system, powered by Bladelius.",
            "angle.jpg",
        ),
    ))


def about():
    body = f'''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>About Us</h1>
        <p class="lede">Norse Audio is a sub-brand of Bladelius. The system is designed in Sweden.</p>
      </header>
      <div class="split">
        <div class="prose">
          <p>The Norse Audio system is a modular high-fidelity setup: the X1 power amplifier, the X2 pre-amplifier and the X5 power supply. Each part is built to work in the same ecosystem, so a system can start with a single stereo amplifier and later become a dual-mono setup, without changing direction.</p>
          <p>Chassis are machined from non-magnetic materials, to reduce electromagnetic interference and the effect of vibration, and to keep the performance stable.</p>
          <p>Powered by Bladelius.</p>
          <p><a class="text-link" href="{href(1, "family/")}">The Bladelius family</a></p>
        </div>
        <div>
          <img src="../images/products/angle.jpg" alt="Norse Audio component">
        </div>
      </div>
    </div>
  </main>'''
    write("about-us/index.html", page(
        1, "about-us", "Norse Audio – About Us", body,
        description="Norse Audio is a sub-brand of Bladelius. A modular high-fidelity system, designed in Sweden.",
    ))


def news():
    items = []
    for post in NEWS:
        img = "../" + post["image"]
        items.append(
            f'        <article class="news-item">\n'
            f'          <a class="thumb" href="{htmlmod.escape(post["slug"])}/">\n'
            f'            <img src="{htmlmod.escape(img)}" alt="{htmlmod.escape(post["alt"])}">\n'
            f'          </a>\n'
            f'          <div>\n'
            f'            <h2><a href="{htmlmod.escape(post["slug"])}/">{htmlmod.escape(post["title"])}</a></h2>\n'
            f'            <time datetime="{post["date_iso"]}">{htmlmod.escape(post["date"])}</time>\n'
            f'            <div class="body"><p>{htmlmod.escape(post["excerpt"])}</p></div>\n'
            f'          </div>\n'
            f'        </article>'
        )
        # individual post pages (depth 2)
        post_body = f'''  <main class="page">
    <div class="wrap">
      <article class="news-item" style="display:block; border-top:0; padding-top:0;">
        <header class="page-header">
          <h1>{htmlmod.escape(post["title"])}</h1>
          <time datetime="{post["date_iso"]}">{htmlmod.escape(post["date"])}</time>
        </header>
        <p><img src="../../{htmlmod.escape(post["image"])}" alt="{htmlmod.escape(post["alt"])}"></p>
        <div class="prose body">
          {post["body"]}
        </div>
        <p style="margin-top:2em"><a class="text-link" href="../">All news</a></p>
      </article>
    </div>
  </main>'''
        # news posts are depth 2: news/slug/
        # Fix product link in second post: from depth 2, products is ../../products/
        post_html = post_body
        if post["slug"] == "norse-by-bladelius":
            post_html = post_html.replace('href="../products/"', 'href="../../products/"')
        write(f'news/{post["slug"]}/index.html', page(
            2, "news", f'Norse Audio – {post["title"]}', post_html,
            description=post["excerpt"],
        ))

    body = f'''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>News</h1>
      </header>
      <div class="news-list">
{chr(10).join(items)}
      </div>
    </div>
  </main>'''
    write("news/index.html", page(1, "news", "Norse Audio – News", body,
                                  description="News from Norse Audio, powered by Bladelius."))


def contact():
    body = f'''  <main class="page">
    <div class="wrap">
      <div class="split reverse">
        <div>
          <img src="../images/products/front.jpg" alt="Norse Audio component">
        </div>
        <div>
          <h1>Contact form</h1>
          <p class="lede">You can contact us by filling out this form.</p>

          <form class="form" data-contact action="https://api.web3forms.com/submit" method="POST">
            <input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
            <input type="hidden" name="from_name" value="Norse Audio website">
            <input type="hidden" name="subject" value="Contact form — norseaudio.se">
            <div class="hp" aria-hidden="true">
              <label>Leave this empty <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label>
            </div>

            <div>
              <label for="name">Name <span class="req">*</span></label>
              <input id="name" name="name" type="text" required autocomplete="name">
            </div>
            <div>
              <label for="email">E-mail <span class="req">*</span></label>
              <input id="email" name="email" type="email" required autocomplete="email">
            </div>
            <div>
              <label for="message">Message <span class="req">*</span></label>
              <textarea id="message" name="message" required></textarea>
            </div>
            <button class="btn" type="submit">Submit</button>
            <div class="form-status" role="status" aria-live="polite"></div>
          </form>
        </div>
      </div>
    </div>
  </main>'''
    write("contact/index.html", page(
        1, "contact", "Norse Audio – Contact", body,
        description="Contact Norse Audio through the form on this page.",
    ))


def family():
    body = f'''  <main class="page">
    <div class="wrap">
      <header class="page-header">
        <h1>The Bladelius family</h1>
        <p class="lede">Norse Audio, Bladelius and AB Tech are part of the Bladelius family of Swedish audio brands.</p>
      </header>

      <div class="sister-grid">
        <article class="sister-card">
          <div class="sister-photo">
            <img src="../images/family/bladelius.jpg" alt="Bladelius amplifier">
          </div>
          <div class="sister-body">
            <img class="sister-wordmark" src="../images/brand/bladelius-wordmark.png" alt="Bladelius">
            <p>Bladelius designs high-performance audio electronics, from amplifiers and preamplifiers to related components, for listeners around the world.</p>
            <a class="btn" href="{BLADELIUS}" target="_blank" rel="noopener">Visit website</a>
          </div>
        </article>

        <article class="sister-card">
          <div class="sister-photo">
            <img src="../images/family/abtech.jpg" alt="AB Tech product">
          </div>
          <div class="sister-body">
            <img class="sister-wordmark abtech" src="../images/brand/abtech-logo.png" alt="AB Tech">
            <p>AB Tech makes high-end audio isolators, cables and power products, designed and made in Sweden.</p>
            <a class="btn" href="{ABTECH}" target="_blank" rel="noopener">Visit website</a>
          </div>
        </article>
      </div>
    </div>
  </main>'''
    write("family/index.html", page(
        1, "family", "Norse Audio – The Bladelius family", body,
        description="The Bladelius family: Norse Audio, Bladelius and AB Tech.",
    ))


def error_404():
    body = '''  <main class="page">
    <div class="wrap">
      <div class="error-page">
        <h1>Page not found</h1>
        <p class="lede">This page does not exist, or the address may have changed.</p>
        <div class="error-links">
          <a class="btn" href="index.html">Home</a>
          <a class="btn btn-ghost" href="products/">Products</a>
          <a class="btn btn-ghost" href="contact/">Contact</a>
        </div>
      </div>
    </div>
  </main>'''
    write("404.html", page(0, "", "Norse Audio – Page not found", body,
                           description="This page could not be found."))


def main():
    home()
    products()
    x1()
    x2()
    x5()
    about()
    news()
    contact()
    family()
    error_404()
    print("done")


if __name__ == "__main__":
    main()
