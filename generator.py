import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_portfolio(name, field, skills, color):
    prompt = f"""
You are a professional copywriter for elite portfolio websites.
Return ONLY a valid JSON object, no markdown, no explanation, no backticks.

Generate portfolio content for:
- Name: {name}
- Field: {field}
- Skills: {skills}

JSON format exactly:
{{
  "tagline": "one ultra-powerful line (max 8 words) that defines them",
  "hero_subtitle": "one sentence describing their unique value",
  "about": "3 compelling sentences, mix of professional achievements and personal drive",
  "skills_list": ["skill1","skill2","skill3","skill4","skill5","skill6","skill7","skill8"],
  "project1_title": "impressive project name",
  "project1_desc": "2 punchy sentences",
  "project1_tag": "one word category",
  "project2_title": "impressive project name",
  "project2_desc": "2 punchy sentences",
  "project2_tag": "one word category",
  "project3_title": "impressive project name",
  "project3_desc": "2 punchy sentences",
  "project3_tag": "one word category",
  "contact_cta": "short exciting call to action (max 6 words)"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.85
    )

    raw = response.choices[0].message.content
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError("فشل في استخراج JSON من الرد")

    data = json.loads(match.group())
    html = build_html(data, name, field, color)
    return html


def build_html(d, name, field, color):
    # توليد ألوان مشتقة من اللون الأساسي
    skills_html = "".join(
        f'<div class="skill-pill" style="animation-delay:{i*0.08}s">'
        f'<span class="skill-dot"></span>{s}</div>'
        for i, s in enumerate(d.get("skills_list", []))
    )

    first_name = name.split()[0] if ' ' in name else name

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — {field}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
/* ===== VARIABLES ===== */
:root {{
  --accent: {color};
  --accent2: {color}99;
  --bg: #05050d;
  --bg2: #0a0a18;
  --card: #0d0d1f;
  --border: rgba(255,255,255,0.06);
  --text: #f0f0ff;
  --muted: #6060a0;
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
}}

* {{ margin:0; padding:0; box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  overflow-x: hidden;
  cursor: none;
}}

/* ===== CUSTOM CURSOR ===== */
.cursor {{
  width: 12px; height: 12px;
  background: var(--accent);
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  transition: transform 0.15s ease;
  mix-blend-mode: difference;
}}
.cursor-ring {{
  width: 36px; height: 36px;
  border: 1px solid var(--accent2);
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 9998;
  transition: all 0.12s ease;
}}

/* ===== NOISE OVERLAY ===== */
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
  opacity: 0.4;
}}

/* ===== CANVAS BG ===== */
#bg-canvas {{
  position: fixed;
  inset: 0;
  z-index: 0;
  opacity: 0.6;
}}

/* ===== NAV ===== */
nav {{
  position: fixed; top: 0; width: 100%;
  padding: 22px 60px;
  display: flex; justify-content: space-between; align-items: center;
  z-index: 100;
  background: linear-gradient(180deg, rgba(5,5,13,0.95) 0%, transparent 100%);
}}

.nav-logo {{
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 1.3rem;
  color: var(--accent);
  letter-spacing: -0.5px;
}}

.nav-links {{
  display: flex; gap: 36px;
}}
.nav-links a {{
  color: var(--muted);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  transition: color 0.3s;
  position: relative;
}}
.nav-links a::after {{
  content:'';
  position:absolute; bottom:-4px; left:0;
  width:0; height:1px;
  background: var(--accent);
  transition: width 0.3s;
}}
.nav-links a:hover {{ color: var(--text); }}
.nav-links a:hover::after {{ width: 100%; }}

/* ===== HERO ===== */
.hero {{
  min-height: 100vh;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 120px 24px 80px;
  position: relative;
  z-index: 2;
}}

.hero-eyebrow {{
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  color: var(--accent);
  padding: 7px 18px;
  border-radius: 100px;
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 32px;
  animation: fadeUp 0.8s ease both;
}}
.hero-eyebrow span {{
  width:6px; height:6px;
  background: var(--accent);
  border-radius:50%;
  animation: blink 2s infinite;
}}

@keyframes blink {{
  0%,100%{{ opacity:1 }} 50%{{ opacity:0.2 }}
}}

.hero-name {{
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(3.5rem, 10vw, 8rem);
  line-height: 0.95;
  letter-spacing: -4px;
  margin-bottom: 8px;
  animation: fadeUp 0.8s 0.1s ease both;
  position: relative;
}}

/* 3D text effect */
.hero-name .outline-text {{
  -webkit-text-stroke: 1px {color}66;
  color: transparent;
  display: block;
}}

.hero-sub {{
  font-size: clamp(1rem, 2.5vw, 1.3rem);
  color: var(--muted);
  max-width: 480px;
  margin: 24px auto 40px;
  line-height: 1.7;
  font-weight: 300;
  animation: fadeUp 0.8s 0.2s ease both;
}}

.hero-btns {{
  display: flex; gap: 14px; justify-content: center;
  animation: fadeUp 0.8s 0.3s ease both;
}}

.btn-glow {{
  background: var(--accent);
  color: #05050d;
  padding: 15px 32px;
  border-radius: 100px;
  font-weight: 700;
  font-size: 0.9rem;
  text-decoration: none;
  letter-spacing: 0.02em;
  transition: all 0.3s;
  box-shadow: 0 0 30px {color}44;
  position: relative;
  overflow: hidden;
}}
.btn-glow::before {{
  content:'';
  position:absolute; inset:0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
  opacity:0;
  transition: opacity 0.3s;
}}
.btn-glow:hover {{ transform: translateY(-3px); box-shadow: 0 0 50px {color}66; }}
.btn-glow:hover::before {{ opacity:1; }}

.btn-ghost {{
  border: 1px solid var(--border);
  color: var(--text);
  padding: 15px 32px;
  border-radius: 100px;
  font-weight: 500;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.3s;
  backdrop-filter: blur(4px);
}}
.btn-ghost:hover {{ border-color: var(--accent2); background: rgba(255,255,255,0.03); transform: translateY(-3px); }}

/* scroll indicator */
.scroll-hint {{
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: var(--muted);
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  animation: fadeUp 1s 0.6s ease both;
}}
.scroll-line {{
  width: 1px; height: 48px;
  background: linear-gradient(180deg, var(--accent), transparent);
  animation: scrollLine 2s infinite;
}}
@keyframes scrollLine {{
  0% {{ transform: scaleY(0); transform-origin: top; }}
  50% {{ transform: scaleY(1); transform-origin: top; }}
  51% {{ transform: scaleY(1); transform-origin: bottom; }}
  100% {{ transform: scaleY(0); transform-origin: bottom; }}
}}

/* ===== SECTIONS ===== */
.section {{
  padding: 120px 24px;
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}}

.section-tag {{
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 14px;
}}

.section-title {{
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 3.2rem);
  font-weight: 800;
  letter-spacing: -1.5px;
  line-height: 1.1;
  margin-bottom: 48px;
}}

/* ===== ABOUT ===== */
.about-layout {{
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 60px;
  align-items: center;
}}

.about-text {{
  font-size: 1.05rem;
  color: var(--muted);
  line-height: 1.9;
  font-weight: 300;
}}

.about-cards {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}}

.about-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px 18px;
  text-align: center;
  transition: all 0.4s;
  position: relative;
  overflow: hidden;
}}

.about-card::before {{
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 0%, {color}15, transparent 60%);
  opacity: 0;
  transition: opacity 0.4s;
}}

.about-card:hover {{ transform: translateY(-6px) rotateX(5deg); border-color: {color}44; }}
.about-card:hover::before {{ opacity: 1; }}

.card-num {{
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
}}
.card-label {{
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* ===== SKILLS ===== */
.skills-cloud {{ display: flex; flex-wrap: wrap; gap: 10px; }}

.skill-pill {{
  display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  padding: 10px 20px;
  border-radius: 100px;
  font-size: 0.88rem;
  font-weight: 400;
  transition: all 0.3s;
  opacity: 0;
  animation: popIn 0.5s ease forwards;
}}

@keyframes popIn {{
  from {{ opacity:0; transform: scale(0.8) translateY(10px); }}
  to   {{ opacity:1; transform: scale(1) translateY(0); }}
}}

.skill-pill:hover {{
  border-color: var(--accent);
  color: var(--accent);
  background: {color}10;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 24px {color}20;
}}

.skill-dot {{
  width: 5px; height: 5px;
  background: var(--accent);
  border-radius: 50%;
}}

/* ===== PROJECTS ===== */
.projects-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}}

.project-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px 28px;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  transform-style: preserve-3d;
}}

/* 3D card shine */
.project-card .shine {{
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at var(--mx,50%) var(--my,50%), rgba(255,255,255,0.06), transparent 60%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}}

.project-card:hover .shine {{ opacity: 1; }}

.project-card::after {{
  content:'';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, {color}88, transparent);
  opacity: 0;
  transition: opacity 0.4s;
}}

.project-card:hover {{
  border-color: {color}33;
  transform: translateY(-10px) rotateX(4deg) rotateY(-2deg);
  box-shadow: 0 30px 60px rgba(0,0,0,0.4), 0 0 40px {color}15;
}}
.project-card:hover::after {{ opacity: 1; }}

.project-number {{
  font-family: var(--font-display);
  font-size: 3.5rem;
  font-weight: 800;
  color: {color}18;
  line-height: 1;
  margin-bottom: 16px;
  transition: color 0.3s;
}}
.project-card:hover .project-number {{ color: {color}44; }}

.project-tag {{
  display: inline-block;
  background: {color}15;
  color: var(--accent);
  border: 1px solid {color}33;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 14px;
}}

.project-title {{
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: -0.3px;
}}

.project-desc {{
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.75;
}}

.project-arrow {{
  position: absolute;
  bottom: 24px; right: 24px;
  width: 36px; height: 36px;
  border: 1px solid var(--border);
  border-radius: 50%;
  display: grid; place-items: center;
  color: var(--muted);
  font-size: 0.9rem;
  transition: all 0.3s;
}}
.project-card:hover .project-arrow {{
  border-color: var(--accent);
  color: var(--accent);
  transform: rotate(45deg);
  background: {color}15;
}}

/* ===== CONTACT ===== */
.contact-wrapper {{
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 120px 24px;
}}

.contact-glow {{
  position: absolute;
  width: 500px; height: 500px;
  background: radial-gradient(circle, {color}18, transparent 70%);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  animation: glowPulse 3s infinite;
}}

@keyframes glowPulse {{
  0%,100% {{ transform: translate(-50%,-50%) scale(1); opacity:0.6; }}
  50%      {{ transform: translate(-50%,-50%) scale(1.3); opacity:1; }}
}}

.contact-big {{
  font-family: var(--font-display);
  font-size: clamp(3rem, 9vw, 7rem);
  font-weight: 800;
  letter-spacing: -3px;
  line-height: 1;
  margin-bottom: 20px;
  position: relative;
}}

.contact-big .stroke {{
  -webkit-text-stroke: 1px {color}55;
  color: transparent;
}}

.contact-sub {{
  color: var(--muted);
  font-size: 1rem;
  max-width: 380px;
  margin: 0 auto 40px;
  line-height: 1.7;
}}

/* ===== FOOTER ===== */
footer {{
  border-top: 1px solid var(--border);
  padding: 28px 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--muted);
  font-size: 0.8rem;
  position: relative;
  z-index: 2;
}}

/* ===== DIVIDER ===== */
.divider {{
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}}

/* ===== FADE IN ===== */
@keyframes fadeUp {{
  from {{ opacity:0; transform:translateY(30px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}

.reveal {{
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.9s cubic-bezier(0.23,1,0.32,1), transform 0.9s cubic-bezier(0.23,1,0.32,1);
}}
.reveal.in-view {{ opacity:1; transform:translateY(0); }}

@media (max-width: 768px) {{
  nav {{ padding: 18px 24px; }}
  .nav-links {{ display: none; }}
  .about-layout {{ grid-template-columns: 1fr; gap: 40px; }}
  footer {{ flex-direction: column; gap: 12px; text-align: center; }}
}}
</style>
</head>
<body>

<!-- CURSOR -->
<div class="cursor" id="cursor"></div>
<div class="cursor-ring" id="cursor-ring"></div>

<!-- CANVAS BACKGROUND -->
<canvas id="bg-canvas"></canvas>

<!-- NAV -->
<nav>
  <div class="nav-logo">{first_name}.</div>
  <div class="nav-links">
    <a href="#about">About</a>
    <a href="#skills">Skills</a>
    <a href="#projects">Projects</a>
    <a href="#contact">Contact</a>
  </div>
</nav>

<!-- HERO -->
<div class="hero">
  <div>
    <div class="hero-eyebrow">
      <span></span>
      {field}
    </div>
    <h1 class="hero-name">
      {first_name}
      <span class="outline-text">{name.split()[-1] if ' ' in name else ''}</span>
    </h1>
    <p class="hero-sub">{d.get('hero_subtitle','')}</p>
    <div class="hero-btns">
      <a href="#projects" class="btn-glow">View My Work</a>
      <a href="#contact" class="btn-ghost">Let's Talk</a>
    </div>
  </div>
  <div class="scroll-hint">
    <div class="scroll-line"></div>
    scroll
  </div>
</div>

<!-- ABOUT -->
<div class="divider"></div>
<section class="section" id="about">
  <div class="section-tag reveal">About Me</div>
  <div class="section-title reveal">{d.get('tagline','Who I Am')}</div>
  <div class="about-layout">
    <p class="about-text reveal">{d.get('about','')}</p>
    <div class="about-cards">
      <div class="about-card reveal"><div class="card-num">5+</div><div class="card-label">Projects</div></div>
      <div class="about-card reveal"><div class="card-num">3+</div><div class="card-label">Years</div></div>
      <div class="about-card reveal"><div class="card-num">10+</div><div class="card-label">Tools</div></div>
      <div class="about-card reveal"><div class="card-num">∞</div><div class="card-label">Passion</div></div>
    </div>
  </div>
</section>

<!-- SKILLS -->
<div class="divider"></div>
<section class="section" id="skills">
  <div class="section-tag reveal">Skills</div>
  <div class="section-title reveal">What I Work With</div>
  <div class="skills-cloud reveal">{skills_html}</div>
</section>

<!-- PROJECTS -->
<div class="divider"></div>
<section class="section" id="projects">
  <div class="section-tag reveal">Projects</div>
  <div class="section-title reveal">Things I've Built</div>
  <div class="projects-grid">

    <div class="project-card reveal">
      <div class="shine"></div>
      <div class="project-number">01</div>
      <div class="project-tag">{d.get('project1_tag','AI')}</div>
      <div class="project-title">{d.get('project1_title','Project One')}</div>
      <p class="project-desc">{d.get('project1_desc','')}</p>
      <div class="project-arrow">↗</div>
    </div>

    <div class="project-card reveal">
      <div class="shine"></div>
      <div class="project-number">02</div>
      <div class="project-tag">{d.get('project2_tag','Web')}</div>
      <div class="project-title">{d.get('project2_title','Project Two')}</div>
      <p class="project-desc">{d.get('project2_desc','')}</p>
      <div class="project-arrow">↗</div>
    </div>

    <div class="project-card reveal">
      <div class="shine"></div>
      <div class="project-number">03</div>
      <div class="project-tag">{d.get('project3_tag','Tool')}</div>
      <div class="project-title">{d.get('project3_title','Project Three')}</div>
      <p class="project-desc">{d.get('project3_desc','')}</p>
      <div class="project-arrow">↗</div>
    </div>

  </div>
</section>

<!-- CONTACT -->
<div class="divider"></div>
<div class="contact-wrapper" id="contact">
  <div class="contact-glow"></div>
  <div class="section-tag reveal">Contact</div>
  <h2 class="contact-big reveal">
    Let's <span class="stroke">Work</span><br>Together.
  </h2>
  <p class="contact-sub reveal">{d.get('contact_cta','Open to new opportunities.')}</p>
  <a href="mailto:hello@example.com" class="btn-glow reveal">Say Hello →</a>
</div>

<!-- FOOTER -->
<footer>
  <span>{name} © 2025</span>
  <span>Built with AI ✦</span>
</footer>

<script>
// ===== CURSOR =====
const cursor = document.getElementById('cursor');
const ring   = document.getElementById('cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => {{
  mx = e.clientX; my = e.clientY;
  cursor.style.left = mx - 6 + 'px';
  cursor.style.top  = my - 6 + 'px';
}});

function animateRing() {{
  rx += (mx - rx) * 0.12;
  ry += (my - ry) * 0.12;
  ring.style.left = rx - 18 + 'px';
  ring.style.top  = ry - 18 + 'px';
  requestAnimationFrame(animateRing);
}}
animateRing();

document.querySelectorAll('a, button, .skill-pill, .project-card').forEach(el => {{
  el.addEventListener('mouseenter', () => {{ cursor.style.transform = 'scale(2.5)'; ring.style.transform = 'scale(1.5)'; }});
  el.addEventListener('mouseleave', () => {{ cursor.style.transform = 'scale(1)';   ring.style.transform = 'scale(1)'; }});
}});

// ===== CANVAS PARTICLES =====
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');
let W, H, particles = [];

function resize() {{
  W = canvas.width  = window.innerWidth;
  H = canvas.height = window.innerHeight;
}}
resize();
window.addEventListener('resize', resize);

// parse accent color to rgb
function hexToRgb(hex) {{
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return {{r,g,b}};
}}
const ac = hexToRgb('{color}');

for (let i = 0; i < 80; i++) {{
  particles.push({{
    x: Math.random() * 1920,
    y: Math.random() * 1080,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    size: Math.random() * 1.5 + 0.3,
    opacity: Math.random() * 0.5 + 0.1,
  }});
}}

function drawParticles() {{
  ctx.clearRect(0, 0, W, H);

  // connections
  particles.forEach((p, i) => {{
    particles.slice(i+1).forEach(q => {{
      const dx = p.x - q.x, dy = p.y - q.y;
      const dist = Math.sqrt(dx*dx+dy*dy);
      if (dist < 150) {{
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(q.x, q.y);
        ctx.strokeStyle = `rgba(${{ac.r}},${{ac.g}},${{ac.b}},${{(1-dist/150)*0.12}})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }}
    }});
  }});

  // dots
  particles.forEach(p => {{
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
    ctx.fillStyle = `rgba(${{ac.r}},${{ac.g}},${{ac.b}},${{p.opacity}})`;
    ctx.fill();
    p.x += p.vx; p.y += p.vy;
    if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
    if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
  }});

  requestAnimationFrame(drawParticles);
}}
drawParticles();

// ===== 3D PROJECT CARDS =====
document.querySelectorAll('.project-card').forEach(card => {{
  card.addEventListener('mousemove', e => {{
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const cx = rect.width  / 2;
    const cy = rect.height / 2;
    const rx2 = (y - cy) / cy * -8;
    const ry2 = (x - cx) / cx *  8;
    card.style.transform = `translateY(-10px) rotateX(${{rx2}}deg) rotateY(${{ry2}}deg)`;
    card.style.setProperty('--mx', (x/rect.width*100)+'%');
    card.style.setProperty('--my', (y/rect.height*100)+'%');
  }});
  card.addEventListener('mouseleave', () => {{
    card.style.transform = '';
  }});
}});

// ===== SCROLL REVEAL =====
const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('in-view'); }});
}}, {{ threshold: 0.12 }});
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>
</body>
</html>"""