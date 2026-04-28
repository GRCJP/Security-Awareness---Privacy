import sys

# ==============================================================================
# CONFIG - Edit these for your organization, then re-run this script.
# ==============================================================================
CONFIG = {
    'AGENCY_NAME': 'Your Agency',
    'TRAINING_VERSION': '2026.1',
    'SECURITY_CONTACT': 'security@your-agency.gov',
    'RECERTIFICATION_DAYS': 365,
}

# Replace with your agency's logo as a base64 data URI for production.
# Generic placeholder shield used by default.
LOGO_DATA_URI = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4MCA4MCI+PHBhdGggZD0iTTQwIDQgTDcyIDE2IEw3MiA0OCBRNzIgODAgNDAgOTIgUTggODAgOCA0OCBMOCAxNiBaIiBmaWxsPSIjMUYyNjMwIiBzdHJva2U9IiNDOTk2NkIiIHN0cm9rZS13aWR0aD0iMiIvPjxwYXRoIGQ9Ik0yOCA0OCBMMzYgNTYgTDUyIDM2IiBmaWxsPSJub25lIiBzdHJva2U9IiNDOTk2NkIiIHN0cm9rZS13aWR0aD0iNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+'

# Optional hero photo. Set to '' to use SVG fallback only.
BALTIMORE_SKYLINE_DATA_URI = ''

PHOTOS = {
    'welcome': BALTIMORE_SKYLINE_DATA_URI,
    'pii': 'https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1600&q=80',
    'fti': 'https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=1600&q=80',
    'phi': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=80',
    'ssa': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=1600&q=80',
    'dodont': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1600&q=80',
    'disposal': '',  # SVG-only - photos for this topic tend to be wrong (industrial/destruction)
    'mishandling': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=1600&q=80',
    'reporting': 'https://images.unsplash.com/photo-1573497019418-b400bb3ab074?auto=format&fit=crop&w=1600&q=80',
}

# === SIDE GUTTER LIBRARY (Level C: tan-only outlines, ~40% opacity, fade near content) ===

def fade_def(side, mod=1):
    fid = 'fade-' + side + '-' + str(mod)
    if side == 'left':
        return '<defs><linearGradient id="' + fid + '" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#F5F0EA" stop-opacity="0"/><stop offset="62%" stop-color="#F5F0EA" stop-opacity="0"/><stop offset="100%" stop-color="#F5F0EA" stop-opacity="1"/></linearGradient></defs>'
    return '<defs><linearGradient id="' + fid + '" x1="1" y1="0" x2="0" y2="0"><stop offset="0%" stop-color="#F5F0EA" stop-opacity="0"/><stop offset="62%" stop-color="#F5F0EA" stop-opacity="0"/><stop offset="100%" stop-color="#F5F0EA" stop-opacity="1"/></linearGradient></defs>'

def fade_rect(side, mod=1):
    return '<rect x="0" y="0" width="240" height="900" fill="url(#fade-' + side + '-' + str(mod) + ')"/>'

def gutter_svg(side, mod, body):
    """Wrap inner SVG body with the standard viewBox, fade defs, and fade rect."""
    return ('<svg viewBox="0 0 240 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
            + fade_def(side, mod) + body + fade_rect(side, mod) + '</svg>')

# === GUTTER BODIES (per module, per side) ===
# Each body is the inner content, wrapped in <g opacity="0.4">. Uses tan strokes/fills only.

# Module 1: Foundations - shield, globe, people, monitor with chart
_M1L = '<g opacity="0.4"><g transform="translate(50 60)"><path d="M 36 0 L 70 14 L 70 38 Q 70 64 36 76 Q 0 64 0 38 L 0 14 Z" fill="#C9966B" opacity="0.5"/><path d="M 36 0 L 70 14 L 70 38 Q 70 64 36 76 Q 0 64 0 38 L 0 14 Z" fill="none" stroke="#A87A52" stroke-width="1.6"/><rect x="24" y="32" width="24" height="18" rx="2" fill="#A87A52"/><path d="M 28 32 L 28 24 Q 28 18 36 18 Q 44 18 44 24 L 44 32" fill="none" stroke="#A87A52" stroke-width="2.5"/></g><circle cx="155" cy="80" r="3" fill="#C9966B"/><g transform="translate(165 110)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(60 200)"><circle cx="22" cy="22" r="22" fill="none" stroke="#A87A52" stroke-width="1.6"/><ellipse cx="22" cy="22" rx="22" ry="8" fill="none" stroke="#A87A52" stroke-width="1"/><path d="M 0 22 Q 8 12 22 12 Q 36 12 44 22" fill="none" stroke="#A87A52" stroke-width="1"/><path d="M 0 22 Q 8 32 22 32 Q 36 32 44 22" fill="none" stroke="#A87A52" stroke-width="1"/><line x1="22" y1="0" x2="22" y2="44" stroke="#A87A52" stroke-width="1"/></g><g transform="translate(150 280)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(35 340)"><circle cx="20" cy="14" r="9" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 4 50 Q 4 26 20 26 Q 36 26 36 50 L 36 70 L 4 70 Z" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(95 360)"><circle cx="16" cy="12" r="7" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.2"/><path d="M 2 44 Q 2 22 16 22 Q 30 22 30 44 L 30 60 L 2 60 Z" fill="none" stroke="#A87A52" stroke-width="1.2"/></g><circle cx="170" cy="380" r="3" fill="#C9966B"/><g transform="translate(40 470)"><rect x="0" y="0" width="90" height="60" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="36" y="60" width="18" height="6" fill="#A87A52" opacity="0.7"/><rect x="22" y="66" width="46" height="3" fill="#A87A52" opacity="0.7"/><rect x="8" y="10" width="36" height="6" fill="#C9966B" opacity="0.5"/><line x1="8" y1="22" x2="60" y2="22" stroke="#A87A52" stroke-width="1"/><polyline points="8,46 22,38 36,42 50,30 66,40 80,32" fill="none" stroke="#C9966B" stroke-width="1.5"/></g><g transform="translate(160 540)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><circle cx="135" cy="600" r="2.5" fill="#C9966B"/><g transform="translate(50 640)"><circle cx="22" cy="14" r="9" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 6 50 Q 6 26 22 26 Q 38 26 38 50 L 38 70 L 6 70 Z" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(120 700)"><path d="M 28 0 L 56 12 L 56 32 Q 56 52 28 60 Q 0 52 0 32 L 0 12 Z" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.5"/><path d="M 14 30 L 24 40 L 42 22" fill="none" stroke="#A87A52" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g><g transform="translate(40 800)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g></g>'

_M1R = '<g opacity="0.4" transform="translate(240 0) scale(-1 1)"><g transform="translate(40 80)"><rect x="0" y="0" width="100" height="64" rx="3" fill="none" stroke="#A87A52" stroke-width="1.6"/><rect x="40" y="64" width="20" height="6" fill="#A87A52" opacity="0.7"/><rect x="26" y="70" width="48" height="3" fill="#A87A52" opacity="0.7"/><rect x="38" y="14" width="24" height="20" rx="2" fill="#C9966B" opacity="0.5"/><circle cx="50" cy="22" r="4" fill="none" stroke="#A87A52" stroke-width="1.2"/><path d="M 44 32 Q 44 26 50 26 Q 56 26 56 32 Z" fill="none" stroke="#A87A52" stroke-width="1.2"/><line x1="10" y1="46" x2="80" y2="46" stroke="#A87A52" stroke-width="0.8"/><line x1="10" y1="54" x2="68" y2="54" stroke="#A87A52" stroke-width="0.8"/></g><g transform="translate(165 180)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(60 240)"><circle cx="0" cy="0" r="6" fill="#C9966B" opacity="0.6"/><path d="M -10 24 Q -10 8 0 8 Q 10 8 10 24 L 10 44 L -10 44 Z" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.3"/></g><circle cx="140" cy="320" r="3" fill="#C9966B"/><g transform="translate(45 340)"><path d="M 36 0 L 70 14 L 70 38 Q 70 64 36 76 Q 0 64 0 38 L 0 14 Z" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.6"/><path d="M 18 38 L 30 50 L 56 24" fill="none" stroke="#A87A52" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g><g transform="translate(160 440)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(50 480)"><circle cx="20" cy="20" r="20" fill="none" stroke="#A87A52" stroke-width="1.4"/><line x1="20" y1="0" x2="20" y2="40" stroke="#A87A52" stroke-width="1"/><ellipse cx="20" cy="20" rx="20" ry="8" fill="none" stroke="#A87A52" stroke-width="1"/><path d="M 0 20 Q 8 10 20 10 Q 32 10 40 20" fill="none" stroke="#A87A52" stroke-width="1"/></g><circle cx="155" cy="540" r="2.5" fill="#A87A52"/><g transform="translate(60 580)"><circle cx="20" cy="14" r="9" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 4 50 Q 4 26 20 26 Q 36 26 36 50 L 36 70 L 4 70 Z" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(120 680)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(40 720)"><rect x="0" y="0" width="76" height="100" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="22" y="-6" width="32" height="10" rx="2" fill="#A87A52" opacity="0.7"/><line x1="10" y1="20" x2="60" y2="20" stroke="#A87A52" stroke-width="1"/><line x1="10" y1="32" x2="56" y2="32" stroke="#A87A52" stroke-width="1"/><line x1="10" y1="44" x2="60" y2="44" stroke="#A87A52" stroke-width="1"/></g><circle cx="170" cy="820" r="3" fill="#C9966B"/></g>'

# Module 2: Handling - ID badge on monitor, padlock, magnifier, files, key
_M2L = '<g opacity="0.4"><g transform="translate(30 50)"><rect x="0" y="0" width="100" height="68" rx="3" fill="none" stroke="#A87A52" stroke-width="1.6"/><rect x="40" y="68" width="20" height="6" fill="#A87A52" opacity="0.7"/><rect x="26" y="74" width="48" height="3" fill="#A87A52" opacity="0.7"/><rect x="36" y="14" width="28" height="22" rx="2" fill="#C9966B" opacity="0.5"/><circle cx="50" cy="24" r="4" fill="none" stroke="#A87A52" stroke-width="1.2"/><path d="M 44 34 Q 44 28 50 28 Q 56 28 56 34 Z" fill="none" stroke="#A87A52" stroke-width="1.2"/><line x1="10" y1="46" x2="80" y2="46" stroke="#A87A52" stroke-width="0.8"/><line x1="10" y1="54" x2="70" y2="54" stroke="#A87A52" stroke-width="0.8"/></g><g transform="translate(160 130)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(140 180)"><rect x="0" y="14" width="40" height="32" rx="3" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 6 14 L 6 8 Q 6 -2 20 -2 Q 34 -2 34 8 L 34 14" fill="none" stroke="#A87A52" stroke-width="2.5"/></g><circle cx="140" cy="260" r="3" fill="#C9966B"/><g transform="translate(40 280)"><circle cx="20" cy="20" r="18" fill="none" stroke="#A87A52" stroke-width="2"/><line x1="33" y1="33" x2="50" y2="50" stroke="#A87A52" stroke-width="3" stroke-linecap="round"/><circle cx="20" cy="20" r="14" fill="#C9966B" opacity="0.18"/></g><g transform="translate(155 360)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(40 420)"><rect x="0" y="0" width="64" height="86" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="22" y="-6" width="20" height="6" rx="1" fill="#A87A52" opacity="0.7"/><line x1="10" y1="14" x2="54" y2="14" stroke="#A87A52" stroke-width="1"/><line x1="10" y1="24" x2="48" y2="24" stroke="#A87A52" stroke-width="1"/><line x1="10" y1="34" x2="54" y2="34" stroke="#A87A52" stroke-width="1"/><rect x="10" y="44" width="44" height="20" fill="#C9966B" opacity="0.4"/></g><circle cx="160" cy="500" r="2.5" fill="#A87A52"/><g transform="translate(140 540) rotate(35)"><circle cx="0" cy="0" r="12" fill="none" stroke="#A87A52" stroke-width="2"/><circle cx="0" cy="0" r="5" fill="#C9966B" opacity="0.5"/><rect x="12" y="-3" width="40" height="6" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.3"/><rect x="42" y="3" width="5" height="6" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.2"/></g><g transform="translate(45 640)"><rect x="0" y="0" width="60" height="78" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="6" y="-6" width="22" height="6" rx="1" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1"/></g><g transform="translate(150 720)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(50 770)"><rect x="0" y="14" width="40" height="32" rx="3" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 6 14 L 6 8 Q 6 -2 20 -2 Q 34 -2 34 8 L 34 14" fill="none" stroke="#A87A52" stroke-width="2.5"/></g></g>'

_M2R = '<g opacity="0.4" transform="translate(240 0) scale(-1 1)"><g transform="translate(45 70)"><rect x="0" y="14" width="40" height="32" rx="3" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 6 14 L 6 8 Q 6 -2 20 -2 Q 34 -2 34 8 L 34 14" fill="none" stroke="#A87A52" stroke-width="2.5"/></g><g transform="translate(115 130)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(35 180)"><rect x="0" y="0" width="100" height="68" rx="3" fill="none" stroke="#A87A52" stroke-width="1.6"/><rect x="40" y="68" width="20" height="6" fill="#A87A52" opacity="0.7"/><rect x="36" y="14" width="28" height="22" rx="2" fill="#C9966B" opacity="0.5"/><circle cx="50" cy="24" r="4" fill="none" stroke="#A87A52" stroke-width="1.2"/><line x1="10" y1="46" x2="80" y2="46" stroke="#A87A52" stroke-width="0.8"/></g><circle cx="160" cy="290" r="3" fill="#C9966B"/><g transform="translate(50 320)"><rect x="0" y="0" width="60" height="78" rx="3" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.5"/><rect x="6" y="-6" width="22" height="6" rx="1" fill="#A87A52" opacity="0.7"/></g><g transform="translate(145 420)"><circle cx="20" cy="20" r="18" fill="none" stroke="#A87A52" stroke-width="2"/><line x1="33" y1="33" x2="46" y2="46" stroke="#A87A52" stroke-width="3" stroke-linecap="round"/></g><g transform="translate(40 500) rotate(-30)"><circle cx="0" cy="0" r="12" fill="none" stroke="#A87A52" stroke-width="2"/><circle cx="0" cy="0" r="5" fill="#C9966B" opacity="0.5"/><rect x="12" y="-3" width="40" height="6" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.3"/></g><g transform="translate(150 580)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(50 620)"><rect x="0" y="0" width="64" height="86" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="22" y="-6" width="20" height="6" rx="1" fill="#A87A52" opacity="0.7"/></g><circle cx="160" cy="700" r="2.5" fill="#C9966B"/><g transform="translate(50 770)"><rect x="0" y="14" width="40" height="32" rx="3" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 6 14 L 6 8 Q 6 -2 20 -2 Q 34 -2 34 8 L 34 14" fill="none" stroke="#A87A52" stroke-width="2.5"/></g></g>'

# Module 3: In Practice - person at laptop, gear, charts, envelope, mobile
_M3L = '<g opacity="0.4"><g transform="translate(20 50)"><circle cx="20" cy="14" r="10" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 4 50 Q 4 26 20 26 Q 36 26 36 50 L 30 70 L 10 70 Z" fill="none" stroke="#A87A52" stroke-width="1.4"/><rect x="40" y="48" width="64" height="42" rx="2" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="44" y="52" width="56" height="34" fill="#C9966B" opacity="0.18"/><rect x="48" y="58" width="20" height="4" fill="#C9966B" opacity="0.6"/><line x1="48" y1="68" x2="92" y2="68" stroke="#A87A52" stroke-width="0.8"/><line x1="48" y1="74" x2="80" y2="74" stroke="#A87A52" stroke-width="0.8"/><line x1="40" y1="90" x2="104" y2="90" stroke="#A87A52" stroke-width="2"/></g><g transform="translate(155 170)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(145 200)"><circle cx="20" cy="20" r="18" fill="none" stroke="#A87A52" stroke-width="1.8"/><circle cx="20" cy="20" r="6" fill="#C9966B" opacity="0.5"/><g stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"><line x1="20" y1="0" x2="20" y2="6"/><line x1="20" y1="34" x2="20" y2="40"/><line x1="0" y1="20" x2="6" y2="20"/><line x1="34" y1="20" x2="40" y2="20"/></g></g><circle cx="155" cy="290" r="3" fill="#C9966B"/><g transform="translate(35 320)"><rect x="0" y="0" width="76" height="56" rx="2" fill="none" stroke="#A87A52" stroke-width="1.5"/><line x1="0" y1="14" x2="76" y2="14" stroke="#A87A52" stroke-width="1"/><line x1="6" y1="22" x2="40" y2="22" stroke="#A87A52" stroke-width="0.8"/><rect x="6" y="30" width="14" height="20" fill="#C9966B" opacity="0.7"/><rect x="22" y="34" width="14" height="16" fill="#C9966B" opacity="0.5"/><rect x="38" y="26" width="14" height="24" fill="#C9966B" opacity="0.8"/><rect x="54" y="36" width="14" height="14" fill="#C9966B" opacity="0.5"/></g><g transform="translate(160 410)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(140 470)"><rect x="0" y="0" width="60" height="40" fill="none" stroke="#A87A52" stroke-width="1.5"/><polyline points="0,0 30,24 60,0" fill="none" stroke="#A87A52" stroke-width="1.5"/></g><g transform="translate(40 550)"><rect x="0" y="0" width="48" height="68" rx="6" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="4" y="6" width="40" height="50" fill="#C9966B" opacity="0.18"/><circle cx="24" cy="62" r="2" fill="#A87A52"/></g><circle cx="135" cy="600" r="2.5" fill="#A87A52"/><g transform="translate(115 640)"><circle cx="20" cy="14" r="9" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 4 50 Q 4 26 20 26 Q 36 26 36 50 L 36 70 L 4 70 Z" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(40 740)"><rect x="0" y="0" width="60" height="40" fill="none" stroke="#A87A52" stroke-width="1.5"/><polyline points="0,0 30,24 60,0" fill="none" stroke="#A87A52" stroke-width="1.5"/></g><g transform="translate(160 800)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g></g>'

_M3R = '<g opacity="0.4" transform="translate(240 0) scale(-1 1)"><g transform="translate(40 70)"><rect x="0" y="0" width="80" height="50" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="32" y="50" width="16" height="6" fill="#A87A52" opacity="0.7"/><rect x="20" y="56" width="40" height="3" fill="#A87A52" opacity="0.7"/><rect x="6" y="6" width="68" height="38" fill="#C9966B" opacity="0.18"/><rect x="10" y="12" width="22" height="4" fill="#C9966B" opacity="0.6"/></g><g transform="translate(165 150)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(50 200)"><circle cx="20" cy="20" r="18" fill="none" stroke="#A87A52" stroke-width="1.8"/><circle cx="20" cy="20" r="6" fill="#C9966B" opacity="0.5"/></g><g transform="translate(140 260)"><rect x="0" y="0" width="60" height="40" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.5"/><polyline points="0,0 30,24 60,0" fill="none" stroke="#A87A52" stroke-width="1.5"/></g><circle cx="155" cy="350" r="3" fill="#A87A52"/><g transform="translate(50 380)"><rect x="0" y="0" width="76" height="56" rx="2" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="6" y="20" width="14" height="30" fill="#C9966B" opacity="0.6"/><rect x="24" y="14" width="14" height="36" fill="#C9966B" opacity="0.45"/><rect x="42" y="26" width="14" height="24" fill="#C9966B" opacity="0.7"/><rect x="60" y="32" width="12" height="18" fill="#C9966B" opacity="0.4"/></g><g transform="translate(160 470)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(40 530)"><circle cx="20" cy="14" r="9" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 4 50 Q 4 26 20 26 Q 36 26 36 50 L 36 70 L 4 70 Z" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(140 620)"><rect x="0" y="0" width="48" height="68" rx="6" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="4" y="6" width="40" height="50" fill="#C9966B" opacity="0.18"/></g><circle cx="50" cy="700" r="2.5" fill="#C9966B"/><g transform="translate(40 740)"><rect x="0" y="0" width="80" height="50" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="6" y="6" width="68" height="38" fill="#C9966B" opacity="0.18"/></g><g transform="translate(165 810)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g></g>'

# Module 4: Consequences - phishing hook, broken padlock, alert bell, warning triangle
_M4L = '<g opacity="0.4"><g transform="translate(40 60)"><rect x="0" y="0" width="80" height="56" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="32" y="56" width="16" height="6" fill="#A87A52" opacity="0.7"/><line x1="40" y1="-26" x2="40" y2="14" stroke="#A87A52" stroke-width="1.4"/><path d="M 40 14 Q 38 18 36 18 Q 34 18 34 16 Q 34 12 40 12 Q 46 12 46 16 Q 46 18 44 18" fill="none" stroke="#A87A52" stroke-width="1.4"/><rect x="28" y="22" width="24" height="18" rx="1" fill="#C9966B" opacity="0.5"/><circle cx="40" cy="30" r="3" fill="none" stroke="#A87A52" stroke-width="1"/></g><g transform="translate(160 130)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(140 180)"><rect x="2" y="14" width="40" height="32" rx="3" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 8 14 L 8 8 Q 8 0 22 0 Q 28 0 32 4" fill="none" stroke="#A87A52" stroke-width="2.5"/><path d="M 36 8 Q 36 14 36 14" fill="none" stroke="#A87A52" stroke-width="2.5"/><line x1="0" y1="50" x2="50" y2="0" stroke="#A87A52" stroke-width="2"/></g><circle cx="155" cy="280" r="3" fill="#C9966B"/><g transform="translate(35 310)"><circle cx="22" cy="22" r="22" fill="#C9966B" opacity="0.18"/><path d="M 22 6 L 22 30" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/><circle cx="22" cy="36" r="2.5" fill="#A87A52"/><path d="M 4 22 Q 4 4 22 4 Q 40 4 40 22" fill="none" stroke="#A87A52" stroke-width="1.6"/><line x1="-4" y1="14" x2="2" y2="14" stroke="#A87A52" stroke-width="1.2"/><line x1="42" y1="14" x2="48" y2="14" stroke="#A87A52" stroke-width="1.2"/></g><g transform="translate(160 400)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(40 450)"><polygon points="30,0 60,52 0,52" fill="#C9966B" opacity="0.45"/><polygon points="30,0 60,52 0,52" fill="none" stroke="#A87A52" stroke-width="1.6"/><rect x="28" y="18" width="4" height="20" fill="#A87A52"/><circle cx="30" cy="44" r="2" fill="#A87A52"/></g><circle cx="155" cy="540" r="2.5" fill="#A87A52"/><g transform="translate(50 580)"><rect x="0" y="0" width="80" height="56" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="6" y="6" width="68" height="38" fill="#1F2630" opacity="0.15"/><rect x="14" y="14" width="32" height="3" fill="#A87A52" opacity="0.6"/><rect x="14" y="22" width="40" height="3" fill="#A87A52" opacity="0.4"/><rect x="14" y="30" width="24" height="6" fill="#A94442" opacity="0.4"/></g><g transform="translate(140 680)"><rect x="2" y="14" width="40" height="32" rx="3" fill="none" stroke="#A87A52" stroke-width="1.4"/><line x1="0" y1="50" x2="50" y2="0" stroke="#A87A52" stroke-width="2"/></g><g transform="translate(50 760)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(120 790)"><polygon points="30,0 60,52 0,52" fill="#C9966B" opacity="0.4"/><rect x="28" y="18" width="4" height="20" fill="#A87A52"/></g></g>'

_M4R = '<g opacity="0.4" transform="translate(240 0) scale(-1 1)"><g transform="translate(40 70)"><polygon points="30,0 60,52 0,52" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.6"/><rect x="28" y="18" width="4" height="20" fill="#A87A52"/><circle cx="30" cy="44" r="2" fill="#A87A52"/></g><g transform="translate(155 160)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(50 200)"><circle cx="22" cy="22" r="22" fill="#C9966B" opacity="0.18"/><path d="M 22 6 L 22 30" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/><path d="M 4 22 Q 4 4 22 4 Q 40 4 40 22" fill="none" stroke="#A87A52" stroke-width="1.6"/></g><circle cx="160" cy="290" r="3" fill="#C9966B"/><g transform="translate(40 320)"><rect x="0" y="0" width="80" height="56" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="28" y="22" width="24" height="18" rx="1" fill="#C9966B" opacity="0.5"/><circle cx="40" cy="30" r="3" fill="none" stroke="#A87A52" stroke-width="1"/></g><g transform="translate(155 410)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(50 460)"><rect x="2" y="14" width="40" height="32" rx="3" fill="#C9966B" opacity="0.5" stroke="#A87A52" stroke-width="1.4"/><path d="M 8 14 L 8 8 Q 8 0 22 0 Q 28 0 32 4" fill="none" stroke="#A87A52" stroke-width="2.5"/><line x1="0" y1="50" x2="50" y2="0" stroke="#A87A52" stroke-width="2"/></g><circle cx="160" cy="540" r="2.5" fill="#A87A52"/><g transform="translate(50 580)"><polygon points="40,0 80,68 0,68" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.6"/><rect x="38" y="22" width="4" height="28" fill="#A87A52"/><circle cx="40" cy="60" r="2.5" fill="#A87A52"/></g><g transform="translate(140 690)"><rect x="0" y="0" width="80" height="56" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="14" y="14" width="32" height="3" fill="#A87A52" opacity="0.6"/></g><g transform="translate(50 800)"><circle cx="22" cy="22" r="20" fill="none" stroke="#A87A52" stroke-width="1.6"/><path d="M 22 8 L 22 26" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/></g></g>'

# Module 5: Acknowledgment - clipboard, certificate seal, signed document, checkmark
_M5L = '<g opacity="0.4"><g transform="translate(45 50)"><rect x="0" y="0" width="64" height="86" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="20" y="-6" width="24" height="10" rx="2" fill="#A87A52" opacity="0.6"/><g stroke="#A87A52" stroke-width="0.8" fill="none"><circle cx="14" cy="22" r="3"/><path d="M 11 22 L 13 24 L 17 20" stroke="#4A7C59" stroke-width="1.4"/><line x1="22" y1="22" x2="54" y2="22"/><circle cx="14" cy="38" r="3"/><path d="M 11 38 L 13 40 L 17 36" stroke="#4A7C59" stroke-width="1.4"/><line x1="22" y1="38" x2="50" y2="38"/><circle cx="14" cy="54" r="3"/><line x1="22" y1="54" x2="54" y2="54"/></g></g><g transform="translate(165 130)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(140 200)"><circle cx="24" cy="24" r="22" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.4"/><circle cx="24" cy="24" r="14" fill="none" stroke="#A87A52" stroke-width="1"/><path d="M 16 24 L 22 30 L 32 18" fill="none" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/><path d="M 24 46 L 18 60 L 24 56 L 30 60 Z" fill="#A87A52"/></g><circle cx="50" cy="280" r="3" fill="#C9966B"/><g transform="translate(40 320)"><rect x="0" y="0" width="80" height="60" rx="2" fill="none" stroke="#A87A52" stroke-width="1.5"/><line x1="8" y1="12" x2="60" y2="12" stroke="#A87A52" stroke-width="1"/><line x1="8" y1="22" x2="55" y2="22" stroke="#A87A52" stroke-width="1"/><line x1="8" y1="32" x2="60" y2="32" stroke="#A87A52" stroke-width="1"/><line x1="8" y1="48" x2="60" y2="48" stroke="#A87A52" stroke-width="0.6"/><path d="M 10 44 Q 18 36 26 44 Q 32 50 42 38 Q 50 32 58 44" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(160 410)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(150 460)"><circle cx="20" cy="20" r="20" fill="none" stroke="#A87A52" stroke-width="1.6"/><path d="M 10 20 L 17 27 L 30 14" fill="none" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/></g><g transform="translate(40 540)"><rect x="0" y="0" width="64" height="86" rx="3" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.5"/><rect x="20" y="-6" width="24" height="10" rx="2" fill="#A87A52" opacity="0.6"/></g><circle cx="155" cy="650" r="2.5" fill="#A87A52"/><g transform="translate(135 690)"><circle cx="24" cy="24" r="22" fill="none" stroke="#A87A52" stroke-width="1.5"/><circle cx="24" cy="24" r="14" fill="none" stroke="#A87A52" stroke-width="0.8"/><path d="M 16 24 L 22 30 L 32 18" fill="none" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/></g><g transform="translate(40 780)"><rect x="0" y="0" width="80" height="60" rx="2" fill="none" stroke="#A87A52" stroke-width="1.5"/><path d="M 10 44 Q 18 36 26 44 Q 32 50 42 38 Q 50 32 58 44" fill="none" stroke="#A87A52" stroke-width="1.4"/></g></g>'

_M5R = '<g opacity="0.4" transform="translate(240 0) scale(-1 1)"><g transform="translate(40 60)"><circle cx="24" cy="24" r="22" fill="#C9966B" opacity="0.4" stroke="#A87A52" stroke-width="1.5"/><path d="M 16 24 L 22 30 L 32 18" fill="none" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/></g><g transform="translate(155 130)" stroke="#A87A52" stroke-width="1.2"><line x1="-4" y1="0" x2="4" y2="0"/><line x1="0" y1="-4" x2="0" y2="4"/></g><g transform="translate(120 170)"><rect x="0" y="0" width="64" height="86" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="20" y="-6" width="24" height="10" rx="2" fill="#A87A52" opacity="0.6"/><g stroke="#A87A52" stroke-width="0.8" fill="none"><circle cx="14" cy="22" r="3"/><path d="M 11 22 L 13 24 L 17 20" stroke="#4A7C59" stroke-width="1.4"/><line x1="22" y1="22" x2="54" y2="22"/></g></g><circle cx="50" cy="280" r="3" fill="#A87A52"/><g transform="translate(40 320)"><rect x="0" y="0" width="80" height="60" rx="2" fill="#C9966B" opacity="0.3" stroke="#A87A52" stroke-width="1.5"/><path d="M 10 44 Q 18 36 26 44 Q 32 50 42 38 Q 50 32 58 44" fill="none" stroke="#A87A52" stroke-width="1.4"/></g><g transform="translate(155 420)" stroke="#A87A52" stroke-width="1.2" fill="none"><line x1="-4" y1="-4" x2="4" y2="4"/><line x1="4" y1="-4" x2="-4" y2="4"/></g><g transform="translate(50 470)"><circle cx="24" cy="24" r="22" fill="none" stroke="#A87A52" stroke-width="1.4"/><circle cx="24" cy="24" r="14" fill="none" stroke="#A87A52" stroke-width="0.8"/><path d="M 16 24 L 22 30 L 32 18" fill="none" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/></g><g transform="translate(135 580)"><rect x="0" y="0" width="64" height="86" rx="3" fill="none" stroke="#A87A52" stroke-width="1.5"/><rect x="20" y="-6" width="24" height="10" rx="2" fill="#A87A52" opacity="0.6"/></g><circle cx="50" cy="690" r="2.5" fill="#C9966B"/><g transform="translate(50 730)"><circle cx="20" cy="20" r="20" fill="#C9966B" opacity="0.4"/><path d="M 10 20 L 17 27 L 30 14" fill="none" stroke="#A87A52" stroke-width="2.5" stroke-linecap="round"/></g><g transform="translate(140 800)"><rect x="0" y="0" width="64" height="60" rx="2" fill="none" stroke="#A87A52" stroke-width="1.5"/><path d="M 10 44 Q 18 36 26 44 Q 32 50 42 38" fill="none" stroke="#A87A52" stroke-width="1.4"/></g></g>'

# Assemble the 10 gutter SVGs with proper unique fade IDs
GUTTER_M1_LEFT  = gutter_svg('left',  1, _M1L)
GUTTER_M1_RIGHT = gutter_svg('right', 1, _M1R)
GUTTER_M2_LEFT  = gutter_svg('left',  2, _M2L)
GUTTER_M2_RIGHT = gutter_svg('right', 2, _M2R)
GUTTER_M3_LEFT  = gutter_svg('left',  3, _M3L)
GUTTER_M3_RIGHT = gutter_svg('right', 3, _M3R)
GUTTER_M4_LEFT  = gutter_svg('left',  4, _M4L)
GUTTER_M4_RIGHT = gutter_svg('right', 4, _M4R)
GUTTER_M5_LEFT  = gutter_svg('left',  5, _M5L)
GUTTER_M5_RIGHT = gutter_svg('right', 5, _M5R)


GUTTERS = {
    1: (GUTTER_M1_LEFT, GUTTER_M1_RIGHT),
    2: (GUTTER_M2_LEFT, GUTTER_M2_RIGHT),
    3: (GUTTER_M3_LEFT, GUTTER_M3_RIGHT),
    4: (GUTTER_M4_LEFT, GUTTER_M4_RIGHT),
    5: (GUTTER_M5_LEFT, GUTTER_M5_RIGHT),
}

# === HERO BG SVGs (the fallback layer that shows behind/instead of photo) ===

SVG_BALTIMORE = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g fill="#0F1419"><rect x="20" y="80" width="60" height="120"/><rect x="85" y="60" width="40" height="140"/><rect x="130" y="40" width="55" height="160"/><rect x="190" y="70" width="35" height="130"/><rect x="230" y="50" width="50" height="150"/><rect x="285" y="20" width="45" height="180"/><rect x="335" y="0" width="55" height="200"/><polygon points="362,0 362,-20 372,-30 382,-20 382,0"/><rect x="395" y="30" width="35" height="170"/><rect x="435" y="15" width="60" height="185"/><rect x="500" y="-10" width="50" height="210"/><rect x="555" y="25" width="40" height="175"/><rect x="600" y="10" width="55" height="190"/><rect x="660" y="-5" width="65" height="205"/><rect x="730" y="40" width="40" height="160"/><rect x="775" y="30" width="50" height="170"/><rect x="830" y="60" width="35" height="140"/><rect x="870" y="45" width="50" height="155"/><rect x="925" y="75" width="40" height="125"/><rect x="970" y="55" width="45" height="145"/><rect x="1020" y="80" width="35" height="120"/><rect x="1060" y="65" width="50" height="135"/><rect x="1115" y="90" width="40" height="110"/><rect x="1160" y="75" width="35" height="125"/></g><g fill="#E5C7A3" opacity="0.5"><rect x="35" y="100" width="3" height="4"/><rect x="55" y="120" width="3" height="4"/><rect x="100" y="80" width="3" height="4"/><rect x="155" y="60" width="3" height="4"/><rect x="240" y="65" width="3" height="4"/><rect x="305" y="40" width="3" height="4"/><rect x="350" y="20" width="3" height="4"/><rect x="450" y="35" width="3" height="4"/><rect x="510" y="10" width="3" height="4"/><rect x="615" y="30" width="3" height="4"/><rect x="675" y="15" width="3" height="4"/><rect x="785" y="50" width="3" height="4"/><rect x="885" y="65" width="3" height="4"/><rect x="985" y="75" width="3" height="4"/><rect x="1075" y="85" width="3" height="4"/></g></svg>'''

SVG_DOCS = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g opacity="0.35"><rect x="100" y="40" width="120" height="160" rx="4" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="120" y1="70" x2="200" y2="70" stroke="#C9966B" stroke-width="1.5"/><line x1="120" y1="85" x2="190" y2="85" stroke="#C9966B" stroke-width="1.5"/><line x1="120" y1="100" x2="200" y2="100" stroke="#C9966B" stroke-width="1.5"/><line x1="120" y1="115" x2="180" y2="115" stroke="#C9966B" stroke-width="1.5"/><line x1="120" y1="130" x2="200" y2="130" stroke="#C9966B" stroke-width="1.5"/><rect x="260" y="30" width="120" height="170" rx="4" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="280" y1="60" x2="360" y2="60" stroke="#C9966B" stroke-width="1.5"/><line x1="280" y1="75" x2="350" y2="75" stroke="#C9966B" stroke-width="1.5"/><line x1="280" y1="90" x2="360" y2="90" stroke="#C9966B" stroke-width="1.5"/><line x1="280" y1="105" x2="340" y2="105" stroke="#C9966B" stroke-width="1.5"/><rect x="420" y="50" width="120" height="150" rx="4" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="440" y1="80" x2="520" y2="80" stroke="#C9966B" stroke-width="1.5"/><line x1="440" y1="95" x2="510" y2="95" stroke="#C9966B" stroke-width="1.5"/><line x1="440" y1="110" x2="520" y2="110" stroke="#C9966B" stroke-width="1.5"/></g><g transform="translate(700, 40)"><circle cx="80" cy="80" r="64" fill="#C9966B" opacity="0.18"/><rect x="50" y="74" width="60" height="46" rx="4" fill="#C9966B" opacity="0.85"/><path d="M 60 74 L 60 56 Q 60 40 80 40 Q 100 40 100 56 L 100 74" fill="none" stroke="#C9966B" stroke-width="5"/><circle cx="80" cy="92" r="5" fill="#1F2630"/><rect x="77.5" y="92" width="5" height="14" fill="#1F2630"/></g></svg>'''

SVG_FORMS = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g opacity="0.4"><rect x="80" y="30" width="180" height="160" fill="none" stroke="#C9966B" stroke-width="2"/><text x="100" y="58" fill="#C9966B" font-family="monospace" font-size="14" font-weight="700">FORM 1040</text><line x1="100" y1="74" x2="240" y2="74" stroke="#C9966B" stroke-width="1.2"/><line x1="100" y1="90" x2="230" y2="90" stroke="#C9966B" stroke-width="1.2"/><line x1="100" y1="106" x2="240" y2="106" stroke="#C9966B" stroke-width="1.2"/><line x1="100" y1="122" x2="225" y2="122" stroke="#C9966B" stroke-width="1.2"/><line x1="100" y1="138" x2="240" y2="138" stroke="#C9966B" stroke-width="1.2"/><line x1="100" y1="154" x2="220" y2="154" stroke="#C9966B" stroke-width="1.2"/><rect x="180" y="164" width="60" height="20" fill="#C9966B" opacity="0.5"/></g><g transform="translate(440, 40)" opacity="0.85"><circle cx="70" cy="70" r="62" fill="none" stroke="#C9966B" stroke-width="3"/><circle cx="70" cy="70" r="62" fill="#1F2630" opacity="0.35"/><text x="70" y="60" fill="#E5C7A3" font-family="serif" font-size="16" font-weight="700" text-anchor="middle" letter-spacing="0.1em">IRS</text><line x1="35" y1="72" x2="105" y2="72" stroke="#C9966B" stroke-width="1.5"/><text x="70" y="92" fill="#E5C7A3" font-family="serif" font-size="11" text-anchor="middle">PUB 1075</text><text x="70" y="106" fill="#E5C7A3" font-family="serif" font-size="9" text-anchor="middle" opacity="0.7">SAFEGUARDS</text></g><g transform="translate(680, 60)" opacity="0.55"><rect x="0" y="0" width="100" height="80" fill="none" stroke="#C9966B" stroke-width="2"/><rect x="10" y="10" width="80" height="12" fill="#C9966B" opacity="0.5"/><line x1="10" y1="36" x2="90" y2="36" stroke="#C9966B" stroke-width="1.2"/><line x1="10" y1="48" x2="90" y2="48" stroke="#C9966B" stroke-width="1.2"/><line x1="10" y1="60" x2="90" y2="60" stroke="#C9966B" stroke-width="1.2"/></g><g transform="translate(840, 50)" opacity="0.5"><rect x="0" y="0" width="120" height="100" fill="none" stroke="#C9966B" stroke-width="2"/><text x="20" y="22" fill="#C9966B" font-family="monospace" font-size="9" font-weight="700">W-2</text><line x1="20" y1="36" x2="100" y2="36" stroke="#C9966B" stroke-width="1.2"/><line x1="20" y1="50" x2="90" y2="50" stroke="#C9966B" stroke-width="1.2"/><line x1="20" y1="64" x2="100" y2="64" stroke="#C9966B" stroke-width="1.2"/><line x1="20" y1="78" x2="80" y2="78" stroke="#C9966B" stroke-width="1.2"/></g></svg>'''

SVG_MEDICAL = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g opacity="0.4"><rect x="100" y="30" width="160" height="170" rx="6" fill="none" stroke="#C9966B" stroke-width="2"/><circle cx="180" cy="64" r="14" fill="none" stroke="#C9966B" stroke-width="1.5"/><line x1="180" y1="54" x2="180" y2="74" stroke="#C9966B" stroke-width="2"/><line x1="170" y1="64" x2="190" y2="64" stroke="#C9966B" stroke-width="2"/><line x1="120" y1="100" x2="240" y2="100" stroke="#C9966B" stroke-width="1.2"/><line x1="120" y1="115" x2="220" y2="115" stroke="#C9966B" stroke-width="1.2"/><line x1="120" y1="130" x2="240" y2="130" stroke="#C9966B" stroke-width="1.2"/><line x1="120" y1="145" x2="200" y2="145" stroke="#C9966B" stroke-width="1.2"/><line x1="120" y1="160" x2="240" y2="160" stroke="#C9966B" stroke-width="1.2"/><line x1="120" y1="175" x2="220" y2="175" stroke="#C9966B" stroke-width="1.2"/></g><g transform="translate(380, 50)" opacity="0.7"><polyline points="0,70 30,70 45,40 65,100 80,55 100,75 130,75 145,90 165,55 180,70 220,70" fill="none" stroke="#C9966B" stroke-width="2"/></g><g transform="translate(680, 40)" opacity="0.85"><rect x="40" y="10" width="80" height="120" rx="6" fill="#C9966B" opacity="0.18"/><circle cx="80" cy="50" r="12" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="80" y1="42" x2="80" y2="58" stroke="#C9966B" stroke-width="2.5"/><line x1="72" y1="50" x2="88" y2="50" stroke="#C9966B" stroke-width="2.5"/><text x="80" y="80" fill="#E5C7A3" font-family="serif" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="0.1em">HIPAA</text><line x1="55" y1="90" x2="105" y2="90" stroke="#C9966B" stroke-width="1"/><text x="80" y="106" fill="#E5C7A3" font-family="serif" font-size="7" text-anchor="middle" opacity="0.7">PROTECTED</text></g><g transform="translate(900, 60)" opacity="0.5"><rect x="0" y="0" width="120" height="80" fill="none" stroke="#C9966B" stroke-width="1.5"/><line x1="10" y1="20" x2="50" y2="20" stroke="#C9966B" stroke-width="1"/><line x1="10" y1="32" x2="60" y2="32" stroke="#C9966B" stroke-width="1"/><line x1="60" y1="20" x2="60" y2="80" stroke="#C9966B" stroke-width="1"/><polyline points="65,55 80,55 90,40 100,70 110,55" fill="none" stroke="#C9966B" stroke-width="1.5"/></g></svg>'''

SVG_GOVT = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g transform="translate(400, 0)" opacity="0.55"><polygon points="200,40 60,90 60,200 340,200 340,90" fill="#1F2630"/><polygon points="200,40 50,92 350,92" fill="none" stroke="#C9966B" stroke-width="2"/><rect x="80" y="100" width="240" height="6" fill="#C9966B" opacity="0.7"/><rect x="100" y="115" width="20" height="80" fill="#C9966B" opacity="0.6"/><rect x="140" y="115" width="20" height="80" fill="#C9966B" opacity="0.6"/><rect x="180" y="115" width="20" height="80" fill="#C9966B" opacity="0.6"/><rect x="220" y="115" width="20" height="80" fill="#C9966B" opacity="0.6"/><rect x="260" y="115" width="20" height="80" fill="#C9966B" opacity="0.6"/><polygon points="200,15 195,40 205,40" fill="#C9966B"/><line x1="200" y1="0" x2="200" y2="40" stroke="#C9966B" stroke-width="1"/><rect x="60" y="195" width="280" height="5" fill="#C9966B" opacity="0.6"/></g><g opacity="0.3"><rect x="80" y="120" width="40" height="80" fill="none" stroke="#C9966B" stroke-width="1.5"/><rect x="130" y="100" width="50" height="100" fill="none" stroke="#C9966B" stroke-width="1.5"/><rect x="190" y="130" width="35" height="70" fill="none" stroke="#C9966B" stroke-width="1.5"/><rect x="975" y="115" width="45" height="85" fill="none" stroke="#C9966B" stroke-width="1.5"/><rect x="1030" y="100" width="55" height="100" fill="none" stroke="#C9966B" stroke-width="1.5"/><rect x="1095" y="130" width="35" height="70" fill="none" stroke="#C9966B" stroke-width="1.5"/></g></svg>'''

SVG_WORKSPACE = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g transform="translate(280, 30)" opacity="0.55"><rect x="0" y="0" width="200" height="120" rx="6" fill="none" stroke="#C9966B" stroke-width="2.5"/><rect x="6" y="6" width="188" height="108" rx="3" fill="#1F2630" opacity="0.4"/><line x1="20" y1="24" x2="100" y2="24" stroke="#C9966B" stroke-width="1.2"/><line x1="20" y1="36" x2="120" y2="36" stroke="#C9966B" stroke-width="1.2"/><rect x="20" y="50" width="160" height="18" fill="#C9966B" opacity="0.3"/><line x1="20" y1="80" x2="160" y2="80" stroke="#C9966B" stroke-width="1.2"/><line x1="20" y1="92" x2="140" y2="92" stroke="#C9966B" stroke-width="1.2"/><rect x="60" y="125" width="80" height="6" fill="#C9966B" opacity="0.7"/><rect x="80" y="131" width="40" height="40" fill="#C9966B" opacity="0.5"/></g><g transform="translate(580, 40)" opacity="0.65"><circle cx="50" cy="60" r="38" fill="#4A7C59" opacity="0.3"/><circle cx="50" cy="60" r="38" fill="none" stroke="#4A7C59" stroke-width="2.5"/><path d="M 32 60 L 44 72 L 68 48" fill="none" stroke="#4A7C59" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g><g transform="translate(720, 40)" opacity="0.65"><circle cx="50" cy="60" r="38" fill="#A94442" opacity="0.3"/><circle cx="50" cy="60" r="38" fill="none" stroke="#A94442" stroke-width="2.5"/><line x1="34" y1="44" x2="66" y2="76" stroke="#A94442" stroke-width="4" stroke-linecap="round"/><line x1="66" y1="44" x2="34" y2="76" stroke="#A94442" stroke-width="4" stroke-linecap="round"/></g><g transform="translate(860, 50)" opacity="0.5"><rect x="0" y="20" width="80" height="60" rx="3" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="0" y1="35" x2="80" y2="35" stroke="#C9966B" stroke-width="1.2"/><circle cx="10" cy="27" r="2" fill="#C9966B"/><circle cx="20" cy="27" r="2" fill="#C9966B"/><circle cx="30" cy="27" r="2" fill="#C9966B"/></g></svg>'''

SVG_DISPOSAL = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g transform="translate(420, 0)" opacity="0.55"><rect x="60" y="20" width="240" height="50" fill="#FFFFFF" opacity="0.6"/><rect x="60" y="20" width="240" height="50" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="80" y1="32" x2="280" y2="32" stroke="#C9966B" stroke-width="1.5"/><line x1="80" y1="44" x2="270" y2="44" stroke="#C9966B" stroke-width="1.5"/><line x1="80" y1="56" x2="280" y2="56" stroke="#C9966B" stroke-width="1.5"/><rect x="40" y="70" width="280" height="36" rx="4" fill="#1F2630" opacity="0.85"/><rect x="50" y="80" width="260" height="3" fill="#FFD200" opacity="0.85"/><rect x="50" y="90" width="260" height="2" fill="#C9966B" opacity="0.7"/><circle cx="62" cy="98" r="2.5" fill="#FFD200" opacity="0.85"/><circle cx="78" cy="98" r="2.5" fill="#FFD200" opacity="0.85"/><circle cx="298" cy="98" r="2.5" fill="#FFD200" opacity="0.85"/><circle cx="282" cy="98" r="2.5" fill="#FFD200" opacity="0.85"/></g><g opacity="0.45" stroke="#C9966B" stroke-width="2"><line x1="500" y1="120" x2="500" y2="200"/><line x1="520" y1="120" x2="520" y2="200"/><line x1="540" y1="120" x2="540" y2="200"/><line x1="560" y1="120" x2="560" y2="200"/><line x1="580" y1="120" x2="580" y2="200"/><line x1="600" y1="120" x2="600" y2="200"/><line x1="620" y1="120" x2="620" y2="200"/><line x1="640" y1="120" x2="640" y2="200"/><line x1="660" y1="120" x2="660" y2="200"/><line x1="680" y1="120" x2="680" y2="200"/><line x1="700" y1="120" x2="700" y2="200"/><line x1="720" y1="120" x2="720" y2="200"/><line x1="740" y1="120" x2="740" y2="200"/></g><g opacity="0.55" fill="#FFFFFF"><rect x="498" y="135" width="4" height="14"/><rect x="538" y="155" width="4" height="14"/><rect x="578" y="140" width="4" height="14"/><rect x="618" y="160" width="4" height="14"/><rect x="658" y="148" width="4" height="14"/><rect x="698" y="138" width="4" height="14"/><rect x="738" y="158" width="4" height="14"/></g><g transform="translate(880, 60)" opacity="0.5"><rect x="0" y="0" width="120" height="100" fill="none" stroke="#C9966B" stroke-width="2"/><rect x="0" y="20" width="120" height="20" fill="#C9966B" opacity="0.45"/><rect x="20" y="0" width="80" height="20" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="20" y1="50" x2="100" y2="130" stroke="#C9966B" stroke-width="1.5"/><line x1="100" y1="50" x2="20" y2="130" stroke="#C9966B" stroke-width="1.5"/></g></svg>'''

SVG_WARNING = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g opacity="0.55"><polygon points="600,30 700,170 500,170" fill="#1F2630" opacity="0.7"/><polygon points="600,30 700,170 500,170" fill="none" stroke="#C9966B" stroke-width="3"/><rect x="595" y="80" width="10" height="50" fill="#C9966B"/><circle cx="600" cy="148" r="6" fill="#C9966B"/></g><g transform="translate(160, 40)" opacity="0.4"><rect x="0" y="0" width="180" height="120" rx="4" fill="none" stroke="#C9966B" stroke-width="2"/><line x1="14" y1="22" x2="120" y2="22" stroke="#C9966B" stroke-width="1.2"/><line x1="14" y1="36" x2="100" y2="36" stroke="#C9966B" stroke-width="1.2"/><rect x="14" y="50" width="150" height="20" fill="#A94442" opacity="0.4"/><line x1="14" y1="80" x2="160" y2="80" stroke="#C9966B" stroke-width="1.2"/><line x1="14" y1="94" x2="140" y2="94" stroke="#C9966B" stroke-width="1.2"/><line x1="14" y1="108" x2="160" y2="108" stroke="#C9966B" stroke-width="1.2"/></g><g transform="translate(820, 50)" opacity="0.5"><rect x="0" y="0" width="160" height="100" fill="none" stroke="#C9966B" stroke-width="2"/><polygon points="80,12 105,55 55,55" fill="none" stroke="#A94442" stroke-width="2"/><rect x="78" y="30" width="4" height="18" fill="#A94442"/><circle cx="80" cy="52" r="2" fill="#A94442"/><line x1="14" y1="74" x2="146" y2="74" stroke="#C9966B" stroke-width="1.2"/><line x1="14" y1="86" x2="120" y2="86" stroke="#C9966B" stroke-width="1.2"/></g></svg>'''

SVG_ALERT = '''<svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg"><g opacity="0.18"><circle cx="600" cy="180" r="160" fill="none" stroke="#C9966B" stroke-width="1.5"/><circle cx="600" cy="180" r="120" fill="none" stroke="#C9966B" stroke-width="1.5"/><circle cx="600" cy="180" r="80" fill="none" stroke="#C9966B" stroke-width="1.5"/><circle cx="600" cy="180" r="40" fill="none" stroke="#C9966B" stroke-width="1.5"/></g><g transform="translate(540, 50)" opacity="0.85"><circle cx="60" cy="70" r="48" fill="#C9966B" opacity="0.22"/><path d="M 60 38 L 60 78" stroke="#E5C7A3" stroke-width="5" stroke-linecap="round"/><circle cx="60" cy="92" r="4" fill="#E5C7A3"/><path d="M 26 70 Q 26 36 60 36 Q 94 36 94 70" fill="none" stroke="#C9966B" stroke-width="3" opacity="0.7"/></g><g opacity="0.55"><rect x="180" y="100" width="80" height="60" rx="3" fill="none" stroke="#C9966B" stroke-width="1.8"/><text x="220" y="138" fill="#C9966B" font-family="monospace" font-size="20" font-weight="700" text-anchor="middle">!</text><rect x="940" y="100" width="80" height="60" rx="3" fill="none" stroke="#C9966B" stroke-width="1.8"/><text x="980" y="138" fill="#C9966B" font-family="monospace" font-size="20" font-weight="700" text-anchor="middle">!</text></g></svg>'''

# === BODY ILLUSTRATIONS (small SVGs for concept blocks and cream blocks) ===

# PII concept: lock surrounded by 5 numbered practices
ART_PII_LOCK = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><rect x="84" y="84" width="72" height="48" rx="6" fill="#C9966B"/><path d="M 100 84 L 100 64 Q 100 44 120 44 Q 140 44 140 64 L 140 84" fill="none" stroke="#A87A52" stroke-width="6"/><circle cx="120" cy="106" r="5" fill="#1F2630"/><rect x="117.5" y="106" width="5" height="14" rx="1" fill="#1F2630"/><g stroke="#A87A52" stroke-width="1" fill="none" opacity="0.55" stroke-dasharray="3 2"><circle cx="120" cy="108" r="68"/><circle cx="120" cy="108" r="84"/></g><g font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle"><circle cx="42" cy="48" r="14" fill="#A87A52"/><text x="42" y="52" fill="#FFFFFF">1</text><circle cx="42" cy="168" r="14" fill="#A87A52"/><text x="42" y="172" fill="#FFFFFF">5</text><circle cx="120" cy="20" r="14" fill="#A87A52"/><text x="120" y="24" fill="#FFFFFF">2</text><circle cx="198" cy="48" r="14" fill="#A87A52"/><text x="198" y="52" fill="#FFFFFF">3</text><circle cx="198" cy="168" r="14" fill="#A87A52"/><text x="198" y="172" fill="#FFFFFF">4</text></g></svg>'''

ART_PII_MASKED = '''<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="30" width="160" height="100" rx="6" fill="#FFFFFF" stroke="#A87A52" stroke-width="2"/><rect x="20" y="30" width="160" height="14" fill="#A87A52"/><text x="100" y="68" fill="#1F2630" font-family="monospace" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="0.05em">JOHN DOE</text><text x="100" y="90" fill="#3D4A5B" font-family="monospace" font-size="11" text-anchor="middle">SSN: ***-**-1234</text><text x="100" y="108" fill="#3D4A5B" font-family="monospace" font-size="9" text-anchor="middle">DOB: **/**/****</text><text x="100" y="124" fill="#A87A52" font-family="sans-serif" font-size="8" font-weight="700" text-anchor="middle" letter-spacing="0.15em">MASKED</text></svg>'''

# FTI concept: source test arrow - centered composition
ART_FTI_SOURCE = '''<svg viewBox="0 0 220 160" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="50" width="56" height="74" fill="none" stroke="#A87A52" stroke-width="2"/><text x="48" y="68" fill="#A87A52" font-family="serif" font-size="11" font-weight="700" text-anchor="middle">IRS</text><line x1="26" y1="78" x2="70" y2="78" stroke="#A87A52" stroke-width="1.5"/><line x1="26" y1="88" x2="64" y2="88" stroke="#A87A52" stroke-width="1.5"/><line x1="26" y1="98" x2="70" y2="98" stroke="#A87A52" stroke-width="1.5"/><line x1="26" y1="108" x2="60" y2="108" stroke="#A87A52" stroke-width="1.5"/><line x1="82" y1="86" x2="146" y2="86" stroke="#A87A52" stroke-width="2.5"/><polygon points="146,80 158,86 146,92" fill="#A87A52"/><circle cx="180" cy="86" r="30" fill="#C9966B" opacity="0.25"/><circle cx="180" cy="86" r="30" fill="none" stroke="#A87A52" stroke-width="2"/><text x="180" y="84" fill="#1F2630" font-family="serif" font-size="11" font-weight="700" text-anchor="middle">FTI</text><text x="180" y="98" fill="#3D4A5B" font-family="serif" font-size="7" text-anchor="middle">PUB 1075</text></svg>'''

ART_FTI_NOTES = '''<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg"><rect x="38" y="22" width="124" height="116" rx="3" fill="#FFD200" opacity="0.4" stroke="#A87A52" stroke-width="1.5"/><line x1="46" y1="40" x2="154" y2="40" stroke="#A87A52" stroke-width="1.2"/><line x1="46" y1="54" x2="146" y2="54" stroke="#A87A52" stroke-width="1.2"/><line x1="46" y1="68" x2="138" y2="68" stroke="#A87A52" stroke-width="1.2"/><line x1="46" y1="82" x2="150" y2="82" stroke="#A87A52" stroke-width="1.2"/><line x1="46" y1="96" x2="130" y2="96" stroke="#A87A52" stroke-width="1.2"/><text x="100" y="124" fill="#A94442" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="0.1em">= FTI</text></svg>'''

# PHI concept: minimum necessary
ART_PHI_MIN = '''<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="30" width="80" height="100" rx="4" fill="#FFFFFF" stroke="#A87A52" stroke-width="2"/><rect x="20" y="30" width="80" height="12" fill="#A87A52"/><line x1="28" y1="54" x2="92" y2="54" stroke="#A87A52" stroke-width="1"/><line x1="28" y1="66" x2="84" y2="66" stroke="#A87A52" stroke-width="1"/><line x1="28" y1="78" x2="92" y2="78" stroke="#A87A52" stroke-width="1"/><line x1="28" y1="90" x2="80" y2="90" stroke="#A87A52" stroke-width="1"/><line x1="28" y1="102" x2="92" y2="102" stroke="#A87A52" stroke-width="1"/><line x1="28" y1="114" x2="76" y2="114" stroke="#A87A52" stroke-width="1"/><line x1="110" y1="80" x2="148" y2="80" stroke="#A87A52" stroke-width="2.5"/><polygon points="148,74 160,80 148,86" fill="#A87A52"/><rect x="170" y="60" width="56" height="40" rx="3" fill="#C9966B" opacity="0.3" stroke="#A87A52" stroke-width="2"/><line x1="178" y1="76" x2="218" y2="76" stroke="#A87A52" stroke-width="1.5"/><text x="198" y="94" fill="#A87A52" font-family="sans-serif" font-size="8" font-weight="700" text-anchor="middle">MIN</text></svg>'''

# SSA: data verification flow (more relevant than just an ID badge)
ART_SSA_BADGE = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><rect x="14" y="48" width="62" height="86" rx="3" fill="#1F2630"/><rect x="14" y="48" width="62" height="20" fill="#A87A52"/><text x="45" y="62" fill="#FFFFFF" font-family="serif" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="0.15em">SSA</text><line x1="22" y1="80" x2="68" y2="80" stroke="#E5C7A3" stroke-width="1.5"/><line x1="22" y1="92" x2="62" y2="92" stroke="#E5C7A3" stroke-width="1.5"/><line x1="22" y1="104" x2="68" y2="104" stroke="#E5C7A3" stroke-width="1.5"/><line x1="22" y1="116" x2="58" y2="116" stroke="#E5C7A3" stroke-width="1.5"/><g transform="translate(86, 84)"><line x1="0" y1="0" x2="58" y2="0" stroke="#A87A52" stroke-width="2"/><polygon points="58,-6 70,0 58,6" fill="#A87A52"/><text x="35" y="-12" fill="#A87A52" font-family="sans-serif" font-size="8" font-weight="700" text-anchor="middle">VERIFY</text></g><circle cx="194" cy="92" r="36" fill="#C9966B" opacity="0.25"/><circle cx="194" cy="92" r="36" fill="none" stroke="#A87A52" stroke-width="2"/><path d="M 178 92 L 188 102 L 210 80" fill="none" stroke="#4A7C59" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><text x="194" y="148" fill="#A87A52" font-family="sans-serif" font-size="8" font-weight="700" text-anchor="middle" letter-spacing="0.1em">AUTHORIZED</text></svg>'''

# Disposal: shredder with paper feeding in + irretrievable shreds
ART_DISPOSAL_SHRED = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><rect x="60" y="14" width="120" height="60" fill="#FFFFFF" stroke="#A87A52" stroke-width="2"/><line x1="74" y1="28" x2="166" y2="28" stroke="#A87A52" stroke-width="1.2"/><line x1="74" y1="40" x2="160" y2="40" stroke="#A87A52" stroke-width="1.2"/><line x1="74" y1="52" x2="166" y2="52" stroke="#A87A52" stroke-width="1.2"/><line x1="74" y1="64" x2="150" y2="64" stroke="#A87A52" stroke-width="1.2"/><text x="120" y="44" fill="#A87A52" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle" opacity="0.0">SENSITIVE</text><rect x="40" y="74" width="160" height="22" rx="2" fill="#1F2630"/><rect x="48" y="80" width="144" height="3" fill="#FFD200"/><rect x="48" y="86" width="144" height="2" fill="#A87A52"/><circle cx="56" cy="91" r="1.5" fill="#FFD200"/><circle cx="64" cy="91" r="1.5" fill="#FFD200"/><circle cx="184" cy="91" r="1.5" fill="#FFD200"/><circle cx="176" cy="91" r="1.5" fill="#FFD200"/><line x1="56" y1="100" x2="56" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="74" y1="100" x2="74" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="92" y1="100" x2="92" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="110" y1="100" x2="110" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="128" y1="100" x2="128" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="146" y1="100" x2="146" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="164" y1="100" x2="164" y2="160" stroke="#A87A52" stroke-width="2"/><line x1="182" y1="100" x2="182" y2="160" stroke="#A87A52" stroke-width="2"/><g opacity="0.5"><line x1="56" y1="105" x2="56" y2="115" stroke="#FFFFFF" stroke-width="2"/><line x1="92" y1="118" x2="92" y2="128" stroke="#FFFFFF" stroke-width="2"/><line x1="128" y1="105" x2="128" y2="115" stroke="#FFFFFF" stroke-width="2"/><line x1="164" y1="125" x2="164" y2="135" stroke="#FFFFFF" stroke-width="2"/></g><text x="120" y="174" fill="#A87A52" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="0.1em">IRRETRIEVABLE</text></svg>'''

# Reporting: bell with stronger sound waves
ART_REPORTING_BELL = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><circle cx="120" cy="92" r="74" fill="#C9966B" opacity="0.14"/><circle cx="120" cy="92" r="56" fill="#C9966B" opacity="0.18"/><path d="M 120 38 L 120 116" stroke="#A87A52" stroke-width="7" stroke-linecap="round"/><circle cx="120" cy="138" r="9" fill="#A87A52"/><path d="M 60 92 Q 60 40 120 40 Q 180 40 180 92" fill="none" stroke="#A87A52" stroke-width="5"/><path d="M 60 92 L 180 92" stroke="#A87A52" stroke-width="5"/><line x1="22" y1="56" x2="40" y2="56" stroke="#A87A52" stroke-width="2.5" opacity="0.7"/><line x1="14" y1="74" x2="36" y2="74" stroke="#A87A52" stroke-width="2.5" opacity="0.55"/><line x1="20" y1="92" x2="42" y2="92" stroke="#A87A52" stroke-width="2.5" opacity="0.4"/><line x1="200" y1="56" x2="218" y2="56" stroke="#A87A52" stroke-width="2.5" opacity="0.7"/><line x1="204" y1="74" x2="226" y2="74" stroke="#A87A52" stroke-width="2.5" opacity="0.55"/><line x1="198" y1="92" x2="220" y2="92" stroke="#A87A52" stroke-width="2.5" opacity="0.4"/><circle cx="120" cy="92" r="8" fill="#A87A52" opacity="0.4"/></svg>'''

# Privacy: person silhouette inside a protective boundary - data flowing in stays controlled
ART_PRIVACY_SHIELD = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><circle cx="120" cy="92" r="78" fill="none" stroke="#A87A52" stroke-width="2" stroke-dasharray="6 4" opacity="0.45"/><circle cx="120" cy="92" r="56" fill="#C9966B" opacity="0.18"/><circle cx="120" cy="92" r="56" fill="none" stroke="#A87A52" stroke-width="2"/><circle cx="120" cy="76" r="14" fill="#A87A52"/><path d="M 96 124 Q 96 100 120 100 Q 144 100 144 124 L 144 130 L 96 130 Z" fill="#A87A52"/><g font-family="sans-serif" font-size="9" font-weight="700" fill="#A87A52" opacity="0.65"><text x="34" y="54" text-anchor="middle">NAME</text><text x="206" y="54" text-anchor="middle">SSN</text><text x="34" y="142" text-anchor="middle">DOB</text><text x="206" y="142" text-anchor="middle">PHI</text></g><g stroke="#A87A52" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.5"><line x1="48" y1="58" x2="76" y2="76"/><line x1="192" y1="58" x2="164" y2="76"/><line x1="48" y1="138" x2="76" y2="120"/><line x1="192" y1="138" x2="164" y2="120"/></g></svg>'''

# Protection: vault/safe (avoids redundancy with CIA card grid below)
ART_PROTECTION_PILLARS = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><rect x="40" y="30" width="160" height="120" rx="6" fill="#1F2630"/><rect x="48" y="38" width="144" height="104" rx="3" fill="none" stroke="#E5C7A3" stroke-width="1.5"/><circle cx="120" cy="90" r="38" fill="#A87A52"/><circle cx="120" cy="90" r="32" fill="none" stroke="#E5C7A3" stroke-width="1.5"/><circle cx="120" cy="90" r="20" fill="#1F2630"/><circle cx="120" cy="90" r="6" fill="#E5C7A3"/><g stroke="#E5C7A3" stroke-width="2" stroke-linecap="round"><line x1="120" y1="62" x2="120" y2="68"/><line x1="120" y1="112" x2="120" y2="118"/><line x1="92" y1="90" x2="98" y2="90"/><line x1="142" y1="90" x2="148" y2="90"/><line x1="100" y1="70" x2="104" y2="74"/><line x1="136" y1="106" x2="140" y2="110"/><line x1="140" y1="70" x2="136" y2="74"/><line x1="104" y1="106" x2="100" y2="110"/></g><rect x="56" y="50" width="22" height="18" fill="none" stroke="#E5C7A3" stroke-width="1"/><text x="67" y="62" fill="#E5C7A3" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">C</text><rect x="162" y="50" width="22" height="18" fill="none" stroke="#E5C7A3" stroke-width="1"/><text x="173" y="62" fill="#E5C7A3" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">I</text><rect x="56" y="116" width="22" height="18" fill="none" stroke="#E5C7A3" stroke-width="1"/><text x="67" y="128" fill="#E5C7A3" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">A</text></svg>'''

# Combine: name + ssn + dob = identity theft
ART_COMBINE = '''<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg"><rect x="14" y="20" width="56" height="34" rx="3" fill="#F5F0EA" stroke="#A87A52" stroke-width="1.5"/><text x="42" y="40" fill="#A87A52" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">NAME</text><rect x="14" y="64" width="56" height="34" rx="3" fill="#F5F0EA" stroke="#A87A52" stroke-width="1.5"/><text x="42" y="84" fill="#A87A52" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">SSN</text><rect x="14" y="108" width="56" height="34" rx="3" fill="#F5F0EA" stroke="#A87A52" stroke-width="1.5"/><text x="42" y="128" fill="#A87A52" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">DOB</text><line x1="80" y1="38" x2="120" y2="74" stroke="#A87A52" stroke-width="1.5"/><line x1="80" y1="80" x2="120" y2="80" stroke="#A87A52" stroke-width="1.5"/><line x1="80" y1="124" x2="120" y2="86" stroke="#A87A52" stroke-width="1.5"/><polygon points="118,68 130,80 118,92" fill="#A87A52"/><rect x="140" y="50" width="86" height="60" rx="4" fill="#A94442" opacity="0.85"/><text x="183" y="78" fill="#FFFFFF" font-family="serif" font-size="11" font-weight="700" text-anchor="middle">IDENTITY</text><text x="183" y="94" fill="#FFFFFF" font-family="serif" font-size="11" font-weight="700" text-anchor="middle">THEFT</text></svg>'''

# AI risk
ART_AI_RISK = '''<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg"><rect x="14" y="40" width="80" height="80" rx="6" fill="#FFFFFF" stroke="#A87A52" stroke-width="2"/><circle cx="40" cy="60" r="3" fill="#A87A52"/><circle cx="68" cy="60" r="3" fill="#A87A52"/><path d="M 36 78 Q 54 86 72 78" fill="none" stroke="#A87A52" stroke-width="2" stroke-linecap="round"/><line x1="32" y1="100" x2="76" y2="100" stroke="#A87A52" stroke-width="1.5"/><line x1="38" y1="110" x2="70" y2="110" stroke="#A87A52" stroke-width="1.5"/><line x1="98" y1="80" x2="138" y2="80" stroke="#A94442" stroke-width="2.5"/><polygon points="138,74 150,80 138,86" fill="#A94442"/><line x1="98" y1="80" x2="138" y2="80" stroke="#A94442" stroke-width="2.5" stroke-dasharray="4 3"/><circle cx="184" cy="80" r="44" fill="#C9966B" opacity="0.22"/><circle cx="184" cy="80" r="44" fill="none" stroke="#A87A52" stroke-width="2"/><text x="184" y="76" fill="#1F2630" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">PUBLIC</text><text x="184" y="92" fill="#1F2630" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">AI TOOL</text><polygon points="174,108 184,120 194,108" fill="#A94442" opacity="0.7"/></svg>'''

# Email risk
ART_EMAIL_RISK = '''<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg"><rect x="40" y="34" width="160" height="92" rx="4" fill="#FFFFFF" stroke="#A87A52" stroke-width="2"/><polyline points="40,34 120,90 200,34" fill="none" stroke="#A87A52" stroke-width="2"/><polyline points="40,126 90,84 40,42" fill="none" stroke="#A87A52" stroke-width="0.8" opacity="0.5"/><polyline points="200,126 150,84 200,42" fill="none" stroke="#A87A52" stroke-width="0.8" opacity="0.5"/><circle cx="180" cy="124" r="26" fill="#A94442"/><line x1="170" y1="114" x2="190" y2="134" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/><line x1="190" y1="114" x2="170" y2="134" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/></svg>'''

# Penalties: gavel + cell bars + IRC code reference (more specific than scale)
ART_PENALTIES = '''<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="40" width="68" height="100" fill="#1F2630"/><rect x="28" y="50" width="6" height="80" fill="#E5C7A3"/><rect x="42" y="50" width="6" height="80" fill="#E5C7A3"/><rect x="56" y="50" width="6" height="80" fill="#E5C7A3"/><rect x="70" y="50" width="6" height="80" fill="#E5C7A3"/><rect x="20" y="40" width="68" height="8" fill="#A87A52"/><rect x="20" y="132" width="68" height="8" fill="#A87A52"/><g transform="translate(118, 50) rotate(-25)"><rect x="0" y="20" width="50" height="14" rx="2" fill="#A87A52"/><rect x="-8" y="14" width="14" height="26" rx="3" fill="#1F2630"/><rect x="46" y="34" width="6" height="50" fill="#A87A52"/></g><rect x="116" y="106" width="60" height="36" fill="none" stroke="#A87A52" stroke-width="2"/><text x="146" y="132" fill="#A87A52" font-family="serif" font-size="22" font-weight="700" text-anchor="middle">$$</text><g transform="translate(186, 38)"><rect x="0" y="0" width="44" height="60" rx="3" fill="none" stroke="#A87A52" stroke-width="2"/><text x="22" y="20" fill="#A87A52" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">IRC</text><text x="22" y="34" fill="#A87A52" font-family="monospace" font-size="7" text-anchor="middle">800-53</text><line x1="6" y1="42" x2="38" y2="42" stroke="#A87A52" stroke-width="1"/><text x="22" y="54" fill="#A87A52" font-family="monospace" font-size="7" text-anchor="middle">AT-1..4</text></g><text x="120" y="166" fill="#A94442" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="0.1em">PERSONAL</text></svg>'''

# Build hero photo block
def hero(slug, eyebrow, title, subtitle, svg_bg):
    photo_url = PHOTOS.get(slug, '')
    style = f'background-image: url(\'{photo_url}\');' if photo_url else ''
    return f'''<div class="hero-photo {slug}" style="{style}">
      <div class="hero-svg-bg" aria-hidden="true">{svg_bg}</div>
      <div class="hero-photo-overlay"></div>
      <div class="hero-block-content">
        <div class="section-eyebrow">{eyebrow}</div>
        <h2>{title}</h2>
        <p class="hero-subtitle">{subtitle}</p>
      </div>
    </div>'''

print("Helpers defined OK")

# Build the full Index.html
sections = []

# Header + opening
sections.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{AGENCY_NAME}} Annual Sensitive Data Training</title>
  <?!= include('Stylesheet'); ?>
</head>
<body>

<header class="app-header" role="banner">
  <div class="app-header-inner">
    <div class="app-header-brand">
      <img class="app-header-logo" alt="State of " src="{LOGO_DATA_URI}">
      <div class="app-header-text">
        <div class="agency-tag">{{AGENCY_NAME}}</div>
        <h1>Annual Sensitive Data Training</h1>
      </div>
    </div>
  </div>
</header>

<div class="progress-container" role="progressbar" aria-label="Training progress">
  <div class="progress-inner">
    <div class="progress-modules">
      <div class="progress-module" data-mod="0">Foundations</div>
      <div class="progress-module" data-mod="1">Handling</div>
      <div class="progress-module" data-mod="2">In Practice</div>
      <div class="progress-module" data-mod="3">Consequences</div>
      <div class="progress-module" data-mod="4">Acknowledgment</div>
    </div>
    <div class="progress-label">
      <span id="progress-step-name" class="step-name">Welcome</span>
      <span id="progress-step-pct" class="step-pct">0%</span>
    </div>
    <div style="height:6px;background:var(--beige);border-radius:3px;overflow:hidden;margin-top:8px;">
      <div id="progress-fill" style="height:100%;background:linear-gradient(90deg,var(--tan-light),var(--tan));border-radius:3px;transition:width 0.6s cubic-bezier(0.4,0,0.2,1);width:0%;"></div>
    </div>
  </div>
</div>

<main class="app-container" role="main">
''')

# STEP 0: Welcome
sections.append(f'''
  <section class="step active card" data-step-name="Welcome">
    {hero('welcome', 'Begin Training', 'Welcome', 'Annual training on safeguarding sensitive data &mdash; what it is, how to handle it, and your responsibilities under federal and state law.', SVG_BALTIMORE)}
    <div class="card-body">
      <div class="callout">
        <p><strong>Time required:</strong> approximately 20 minutes. <strong>What happens next:</strong> you'll move through five short modules. At the end, sign your Personal Responsibility Statement and receive your completion certificate by email.</p>
      </div>

      <h3>Confirm your information</h3>
      <p class="body-text">We've captured your email from your Workspace login: <strong><?= userEmail ?></strong></p>

      <? if (alreadyCompleted) {{ ?>
        <div class="already-done-banner">
          <h3>You've already completed this training cycle</h3>
          <p>Records show a completion on <strong><?= lastCompletion.trainingDate ?></strong> for version <?= lastCompletion.version ?>. Next due: <strong><?= lastCompletion.nextDue ?></strong>.</p>
          <p style="margin-bottom:0;"><em>You may complete the training again to refresh, but it's not required until your next due date.</em></p>
        </div>
      <? }} ?>

      <div class="form-group">
        <label for="firstName">First Name <span class="required-mark" aria-hidden="true">*</span></label>
        <input type="text" id="firstName" data-required="true" autocomplete="given-name">
        <div class="field-error" id="firstName-error" role="alert"></div>
      </div>
      <div class="form-group">
        <label for="lastName">Last Name <span class="required-mark" aria-hidden="true">*</span></label>
        <input type="text" id="lastName" data-required="true" autocomplete="family-name">
        <div class="field-error" id="lastName-error" role="alert"></div>
      </div>
      <div class="form-group">
        <label for="role">Role / Title <span class="required-mark" aria-hidden="true">*</span></label>
        <input type="text" id="role" data-required="true" autocomplete="organization-title">
        <div class="help-text">Your current job title at the agency.</div>
        <div class="field-error" id="role-error" role="alert"></div>
      </div>
      <div class="form-group">
        <label for="sensitiveDataAccess">Do you handle PII, PHI, SSA data, or other sensitive information? <span class="required-mark" aria-hidden="true">*</span></label>
        <select id="sensitiveDataAccess" data-required="true">
          <option value="">&mdash; Select &mdash;</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Unsure">Unsure</option>
        </select>
        <div class="help-text">Includes PII, PHI, SSA data, financial/business info. You may have access even if you don't work with it directly &mdash; including system admins, developers, DBAs, QA staff, and anyone with backend access. If unsure, select Unsure and the Information Security Office will follow up.</div>
        <div class="field-error" id="sensitiveDataAccess-error" role="alert"></div>
      </div>
      <div class="form-group">
        <label for="ftiAccess">Do you specifically access Federal Tax Information (FTI)? <span class="required-mark" aria-hidden="true">*</span></label>
        <select id="ftiAccess" data-required="true">
          <option value="">&mdash; Select &mdash;</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Unsure">Unsure</option>
        </select>
        <div class="help-text">FTI is tax data from the IRS or secondary sources. FTI access is governed by additional federal requirements and triggers extra reporting and recertification controls.</div>
        <div class="field-error" id="ftiAccess-error" role="alert"></div>
      </div>
      <div class="form-group">
        <label for="supervisorEmail">Supervisor's Email Address <span class="required-mark" aria-hidden="true">*</span></label>
        <input type="email" id="supervisorEmail" data-required="true" data-validate="email-domain" autocomplete="off">
        <div class="help-text">Your direct supervisor's @your-agency.gov email. Used for compliance escalation if recertification becomes overdue.</div>
        <div class="field-error" id="supervisorEmail-error" role="alert"></div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" disabled>Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Begin Training &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 1: Module 1 intro
sections.append('''
  <section class="step card" data-step-name="Module 1: Foundations">
    <div class="module-intro">
      <div class="module-intro-content">
        <span class="module-number">Module 1 of 5</span>
        <div class="scenario-hook">
          <div class="scenario-hook-label">Picture this</div>
          <p class="scenario-hook-text">You start your first day at the agency. HR hands you credentials for systems containing tax records, medical data, and Social Security numbers for thousands of constituents. <em>What rules govern what you can do with that access?</em></p>
        </div>
        <h2>Foundations</h2>
        <p class="module-subtitle">Start with the fundamentals: what data privacy and protection mean, what counts as sensitive data, and the laws that govern how we handle it.</p>
        <div class="module-sections-list">
          <h4>What you'll cover</h4>
          <ul>
            <li>What data privacy is and why it matters</li>
            <li>The difference between privacy and protection</li>
            <li>Categories of sensitive data {{AGENCY_NAME}} manages</li>
            <li>'s Personal Information Protection Act</li>
          </ul>
        </div>
        <div class="module-intro-buttons">
          <button type="button" class="btn btn-light" data-action="prev">&larr; Previous</button>
          <button type="button" class="btn btn-primary large" data-action="next">Start Module &rarr;</button>
        </div>
      </div>
    </div>
  </section>
''')

# STEP 2: M1 §1 Privacy - with concept block
sections.append(f'''
  <section class="step card" data-step-name="What Is Data Privacy">
    <div class="hero-block cream">
      <div class="hero-block-content">
        <div class="section-eyebrow">Module 1 &middot; Foundations</div>
        <h2>What is data privacy?</h2>
        <p class="hero-subtitle">The guidelines that govern how we collect, use, and share information about people.</p>
      </div>
    </div>
    <div class="card-body">
      <div class="concept-block">
        <div class="concept-block-text">
          <p>Some information can hurt real people if it gets out. Names, SSNs, medical records, tax data, bank accounts &mdash; when these end up where they shouldn't be, individuals get harmed and {{AGENCY_NAME}} faces real legal consequences.</p>
          <p style="margin-bottom: 0;">Data privacy is how we keep that from happening. It's the set of rules that decide who can see what, when, and why &mdash; ensuring the people whose data we hold keep meaningful control over it.</p>
        </div>
        <div class="concept-block-art">{ART_PRIVACY_SHIELD}</div>
      </div>

      <h3>Why it matters at the agency</h3>
      <p class="body-text">Federal and state laws &mdash; the Privacy Act of 1974, applicable state privacy laws, HIPAA, and sector-specific frameworks &mdash; set strict requirements for handling sensitive data. NIST 800-53 controls form the baseline; sector frameworks (tax, healthcare, criminal justice, education, controlled unclassified information) layer additional requirements on top.</p>

      <div class="callout callout-info">
        <p><strong>The bottom line:</strong> as agency employees and contractors, we hold sensitive information about thousands of constituents. Data privacy isn't a checkbox &mdash; it's the foundation of public trust in everything we do.</p>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 3: M1 §2 Protection - cream block
sections.append(f'''
  <section class="step card" data-step-name="What Is Data Protection">
    <div class="card-body">
      <div class="section-eyebrow">Module 1 &middot; Foundations</div>
      <h2>What is data protection?</h2>
      <p class="lead">If privacy is the policy, protection is the practice.</p>

      <div class="cream-block">
        <div class="cream-block-art">{ART_PROTECTION_PILLARS}</div>
        <div class="cream-block-text">
          <div class="cream-block-eyebrow">Three Pillars</div>
          <p style="margin: 0 0 12px;">Privacy says <em>what we should do</em>. Protection is <em>how we actually do it</em>. The three pillars below &mdash; <strong>Confidentiality, Integrity, Availability</strong> &mdash; are the foundation of every data protection control at the agency.</p>
        </div>
      </div>

      <p class="body-text">At the agency, data protection means encryption that secures data in transit and at rest, access controls that ensure only authorized people see sensitive records, backup and recovery procedures that prevent loss, and audit logs that show exactly who did what and when.</p>

      <h3>The three pillars in detail</h3>
      <div class="data-grid data-grid-3">
        <div class="data-card">
          <div class="data-card-icon">C</div>
          <div class="data-card-label">Confidentiality</div>
          <div class="data-card-text">Only authorized people can see the data. Enforced by access controls, encryption, and authentication.</div>
        </div>
        <div class="data-card">
          <div class="data-card-icon">I</div>
          <div class="data-card-label">Integrity</div>
          <div class="data-card-text">Data stays accurate and unaltered. Enforced by audit logs, change controls, and validation.</div>
        </div>
        <div class="data-card">
          <div class="data-card-icon">A</div>
          <div class="data-card-label">Availability</div>
          <div class="data-card-text">Authorized users can access data when needed. Enforced by backups, recovery, and redundancy.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 4: M1 §3 Categories - concept reverse
sections.append(f'''
  <section class="step card" data-step-name="Categories of Sensitive Data">
    <div class="hero-block tan">
      <div class="hero-block-content">
        <div class="section-eyebrow">Module 1 &middot; Foundations</div>
        <h2>What is sensitive data?</h2>
        <p class="hero-subtitle">Information that, if mishandled, can harm individuals, compromise security, or violate the law.</p>
      </div>
    </div>
    <div class="card-body">
      <div class="concept-block reverse">
        <div class="concept-block-text">
          <p>Five categories of data at {{AGENCY_NAME}} get treated as sensitive. Each has its own rules, but the underlying principle is the same: <strong>if mishandled, real people get hurt and real legal consequences follow.</strong></p>
          <p style="margin-bottom: 0;">A single piece of data alone is rarely catastrophic &mdash; but combine elements and the risk multiplies. Name + SSN + DOB creates an identity theft kit; any one alone is far less dangerous.</p>
        </div>
        <div class="concept-block-art">{ART_COMBINE}</div>
      </div>

      <h3>The five categories {{AGENCY_NAME}} manages</h3>
      <div class="data-grid data-grid-2">
        <div class="data-card">
          <div class="data-card-label">Personally Identifiable Info (PII)</div>
          <div class="data-card-text">Information that identifies a person &mdash; names, addresses, SSNs, driver's license numbers, dates of birth.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Federal Tax Information (FTI)</div>
          <div class="data-card-text">Tax data received from the IRS or secondary sources. Governed by a dedicated federal framework with stricter controls than general PII.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Protected Health Info (PHI)</div>
          <div class="data-card-text">Medical records, diagnoses, treatment information, Medicare/Medicaid data &mdash; protected by HIPAA.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Social Security Admin (SSA) Data</div>
          <div class="data-card-text">SSN verifications, benefit records, earnings history, disability claims.</div>
        </div>
        <div class="data-card" style="grid-column: 1 / -1;">
          <div class="data-card-label">Financial &amp; Business Information</div>
          <div class="data-card-text">Bank accounts, credit/debit cards, payment processing records, IT security details, program eligibility data.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 5: M1 §4 applicable state privacy laws
sections.append('''
  <section class="step card" data-step-name="applicable state privacy laws">
    <div class="card-body">
      <div class="section-eyebrow">Module 1 &middot; Foundations</div>
      <h2>'s Personal Information Protection Act</h2>
      <p class="lead">The state law that governs how  agencies handle residents' personal information.</p>

      <p class="body-text">applicable state privacy laws &mdash; <strong>Md. Code Ann. Comm. Law &sect; 14-3504</strong> &mdash; ensures that  consumers' personal identifying information is reasonably protected. If a breach occurs, applicable state privacy laws requires that affected individuals be notified so they can take steps to safeguard themselves.</p>

      <h3>What applicable state privacy laws defines as "personal information"</h3>
      <p class="body-text">Under applicable state privacy laws, personal information means an individual's first and last name in combination with any of:</p>
      <ul class="checked-list">
        <li>Social Security number, ITIN, passport number, or federal ID number</li>
        <li>Driver's license or state ID number</li>
        <li>Account number, credit/debit card with security code or password</li>
        <li>Health information, including mental health</li>
        <li>Health insurance or certificate number with unique identifier</li>
        <li>Biometric data &mdash; fingerprints, voice prints, retina or iris images</li>
        <li>Username or email address with password or security question</li>
      </ul>

      <div class="callout callout-info">
        <p><strong>Important:</strong> state privacy laws cover PII, but {{AGENCY_NAME}} also protects FTI, PHI, and SSA data &mdash; each governed by additional federal frameworks with stricter requirements. When two laws apply, the stricter one wins.</p>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 6: M1 feature spread
sections.append('''
  <section class="step card" data-step-name="Why This Matters">
    <div class="feature-spread">
      <div class="feature-spread-content">
        <div class="feature-spread-eyebrow">Why this matters</div>
        <p class="feature-spread-quote">"Every record in our systems represents a real person. They trusted us with information they wouldn't share on social media &mdash; or even with their neighbors."</p>
        <div class="feature-spread-stats">
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">5</div>
            <div class="feature-spread-stat-label">Categories of sensitive data</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">365</div>
            <div class="feature-spread-stat-label">Days per training cycle</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">100%</div>
            <div class="feature-spread-stat-label">Required for system access</div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue to Module 2 &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 7: Module 2 intro
sections.append('''
  <section class="step card" data-step-name="Module 2: Handling Sensitive Data">
    <div class="module-intro">
      <div class="module-intro-content">
        <span class="module-number">Module 2 of 5</span>
        <div class="scenario-hook">
          <div class="scenario-hook-label">Picture this</div>
          <p class="scenario-hook-text">A coworker stops by your desk on Friday afternoon: "Hey, can you email me a list of client SSNs to my Gmail? I need to finish a report this weekend." She's well-meaning, deadline-stressed, and genuinely trying to help. <em>What's the right call?</em></p>
        </div>
        <h2>Handling Sensitive Data</h2>
        <p class="module-subtitle">Real situations like this come up constantly. This module covers how to handle each type of sensitive data {{AGENCY_NAME}} manages, so you know the right answer before the situation arrives.</p>
        <div class="module-sections-list">
          <h4>What you'll cover</h4>
          <ul>
            <li>Interacting with PII data</li>
            <li>Federal Tax Information (FTI) and the source test</li>
            <li>Privileged FTI access for DBAs, sysadmins, and developers</li>
            <li>Protected Health Information (PHI) under HIPAA</li>
            <li>Social Security Administration data</li>
          </ul>
        </div>
        <div class="module-intro-buttons">
          <button type="button" class="btn btn-light" data-action="prev">&larr; Previous</button>
          <button type="button" class="btn btn-primary large" data-action="next">Start Module &rarr;</button>
        </div>
      </div>
    </div>
  </section>
''')

# STEP 8: M2 §1 PII - hero photo + concept + cream
sections.append(f'''
  <section class="step card" data-step-name="Interacting With PII">
    {hero('pii', 'Module 2 &middot; Section 1 of 5', 'Interacting with PII data', 'Five practices that protect personally identifiable information in everything you do.', SVG_DOCS)}
    <div class="card-body">
      <div class="concept-block">
        <div class="concept-block-text">
          <p>A single data point is rarely sensitive on its own &mdash; but combining elements increases the risk of exposure dramatically. The five practices below protect PII, and they apply equally to FTI, PHI, and SSA data, which carry additional rules on top.</p>
          <p style="margin-bottom: 0;"><strong>The principle:</strong> minimum necessary access, encrypted everywhere, approved channels only, and report anything that looks wrong.</p>
        </div>
        <div class="concept-block-art">{ART_PII_LOCK}</div>
      </div>

      <div class="data-grid data-grid-1">
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">1</div>
          <div class="data-card-label">Access Control</div>
          <div class="data-card-text">Only authorized individuals access sensitive data, following the <strong>need-to-know</strong> principle. Permissions reviewed regularly and removed when no longer needed.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">2</div>
          <div class="data-card-label">Encrypt at Rest &amp; in Transit</div>
          <div class="data-card-text">Always encrypt PII stored in databases or systems, and any data transmitted over networks. Use strong encryption standards approved by the Information Security Office.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">3</div>
          <div class="data-card-label">Avoid Unapproved Storage</div>
          <div class="data-card-text">Never store PII in personal email, unsecured cloud services, or local devices. Never transmit PII through standard your-agency.gov email.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">4</div>
          <div class="data-card-label">Mask &amp; Redact</div>
          <div class="data-card-text">Display only the minimum PII necessary for the task. Mask or redact in logs, reports, and screens.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">5</div>
          <div class="data-card-label">Report Suspected Exposure</div>
          <div class="data-card-text">If you suspect improper handling, unauthorized access, or a potential breach, follow the agency's incident reporting protocol immediately.</div>
        </div>
      </div>

      <div class="cream-block reverse">
        <div class="cream-block-text">
          <div class="cream-block-eyebrow">Minimum necessary in practice</div>
          <p style="margin: 0;">Even within authorized systems, display only what's needed. <strong>Mask SSNs to last 4 digits</strong>, abbreviate addresses to ZIP, use case IDs instead of full names. Access alone doesn't justify full display.</p>
        </div>
        <div class="cream-block-art">{ART_PII_MASKED}</div>
      </div>

      <h3>Try it: real scenarios</h3>
      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">Back to that Friday afternoon coworker asking you to email SSNs to her Gmail. She really does need to finish the report. She really is trying to help.</p>
        <div class="scenario-question">What's the right response?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Decline and report.</strong> This violates multiple rules: PII can't go to personal email, can't leave approved systems, and personal devices aren't cleared for sensitive data. Politely decline, suggest approved remote access tools, and notify the Information Security Office &mdash; even from a well-intentioned coworker, this is a reportable incident.</div>
        </div>
      </div>

      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">You're building a status dashboard and need to show recent applications. The data includes client names, SSNs, and addresses.</p>
        <div class="scenario-question">How should the dashboard display this data?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Show only what the user needs to do their job.</strong> Mask SSNs to last 4 digits (or omit entirely), abbreviate addresses to ZIP, use case IDs instead of full names where possible. The minimum-necessary principle applies even within authorized systems &mdash; access alone doesn't justify full display.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 9: M2 §2 FTI
sections.append(f'''
  <section class="step card" data-step-name="Interacting With FTI">
    {hero('fti', 'Module 2 &middot; Section 2 of 5', 'Interacting with Federal Tax Information', 'FTI carries the strictest handling rules of any data we touch.', SVG_FORMS)}
    <div class="card-body">
      <p class="body-text">Federal Tax Information (FTI) is data received from the IRS or authorized secondary sources. Like PII, FTI must be encrypted, access-controlled, and securely stored &mdash; but FTI carries additional rules under its dedicated federal framework, often the most prescriptive data-handling requirements in an agency's environment.</p>

      <div class="cream-block">
        <div class="cream-block-art">{ART_FTI_SOURCE}</div>
        <div class="cream-block-text">
          <div class="cream-block-eyebrow">The "source test"</div>
          <p style="margin: 0;">The defining characteristic of FTI is its <strong>source</strong>, not its content. A tax return that arrives from the IRS is FTI. The same numbers brought in by a client directly are <strong>not</strong> FTI &mdash; they're PII. <em>Where did this data originate?</em></p>
        </div>
      </div>

      <h3>Key FTI handling rules</h3>
      <div class="data-grid">
        <div class="data-card">
          <div class="data-card-label">No Personal Devices</div>
          <div class="data-card-text">FTI cannot be accessed from personal devices. Always use agency-approved, secured systems with VPN and MFA.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Audit Logging Mandatory</div>
          <div class="data-card-text">All FTI access must be logged, monitored, and reviewed. Every view, edit, and deletion is recorded.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Strict Third-Party Rules</div>
          <div class="data-card-text">Contractors and vendors must meet the same standards and have proper agreements in place before FTI access.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Immediate Reporting</div>
          <div class="data-card-text">Any unauthorized access or exposure must be reported to the Information Security Office and escalated to the appropriate federal regulators per the agency's incident response plan.</div>
        </div>
      </div>

      <div class="concept-block reverse no-divider">
        <div class="concept-block-text">
          <p style="margin: 0;">Anything you create from FTI &mdash; sticky notes, screenshots, spreadsheets, meeting notes &mdash; <strong>becomes FTI itself</strong> and inherits all handling rules. Store in approved systems, log access, and dispose per the applicable sanitization standards (typically NIST 800-88).</p>
        </div>
        <div class="concept-block-art">{ART_FTI_NOTES}</div>
      </div>

      <h3>Try it: scenarios</h3>
      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">A client emails a copy of their own 1040 directly to your work address asking for help with their case.</p>
        <div class="scenario-question">Is this FTI? What rules apply?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Not FTI &mdash; but still PII.</strong> Data sent directly from a taxpayer is PII (still encrypted, still need-to-know, still access-controlled), but it's not FTI because it didn't come from the IRS. The source test is everything: same numbers, different source = different rules.</div>
        </div>
      </div>

      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">A contractor on your project has clearance from a previous federal job. They want to start querying FTI tomorrow.</p>
        <div class="scenario-question">Can they?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Not without agency-specific authorization.</strong> Prior clearance doesn't transfer. Contractors need a current contractual agreement, agency-specific access provisioning, this annual training, and a signed PRS &mdash; all in place <em>before</em> first FTI access.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 10: M2 §2b Privileged FTI Access
sections.append('''
  <section class="step card" data-step-name="Privileged FTI Access">
    <div class="card-body">
      <div class="section-eyebrow">Module 2 &middot; Section 3 of 5</div>
      <h2>If you have privileged access</h2>
      <p class="lead">DBAs, system administrators, developers, and anyone with backend access to systems handling regulated data carry additional responsibilities under <strong>NIST 800-53 AT-3</strong> (role-based training) and applicable sector-specific frameworks.</p>

      <p class="body-text">Even if you don't view FTI content directly, your role lets you reach it. The IRS treats this as elevated access requiring elevated awareness. Roles change &mdash; if you ever move into one of these positions, this section applies to you.</p>

      <div class="callout callout-info">
        <p><strong>Roles this applies to:</strong> Database administrators, system administrators, network engineers, application developers, QA staff with production data access, security analysts, contractors with elevated permissions on FTI-handling systems.</p>
      </div>

      <h3>What's different for privileged users</h3>

      <div class="data-grid data-grid-2">
        <div class="data-card data-card-dark">
          <div class="data-card-icon">1</div>
          <div class="data-card-label">Two-Person Rule</div>
          <div class="data-card-text">Production database changes affecting FTI must be reviewed by a second authorized person before execution. Never deploy direct-to-prod alone for FTI systems.</div>
        </div>
        <div class="data-card data-card-dark">
          <div class="data-card-icon">2</div>
          <div class="data-card-label">No Production Data in Dev/Test</div>
          <div class="data-card-text">FTI cannot be copied to non-production environments &mdash; ever. Use synthetic data or properly sanitized data for development and testing.</div>
        </div>
        <div class="data-card data-card-dark">
          <div class="data-card-icon">3</div>
          <div class="data-card-label">Logs Are Sacred</div>
          <div class="data-card-text">Audit logs documenting FTI access cannot be modified, deleted, or rotated outside of approved retention policy. The logs are how the IRS verifies our controls.</div>
        </div>
        <div class="data-card data-card-dark">
          <div class="data-card-icon">4</div>
          <div class="data-card-label">Change Management Discipline</div>
          <div class="data-card-text">Any infrastructure change touching FTI systems requires a 45-day advance notification to the IRS. Ad-hoc fixes that bypass change management are reportable incidents.</div>
        </div>
      </div>

      <div class="callout callout-warn">
        <p style="font-weight: 600; margin-bottom: 8px;">Privileged access carries elevated personal responsibility.</p>
        <p>A DBA who runs an unauthorized SELECT on regulated data tables &mdash; even out of curiosity &mdash; commits a federal disclosure violation. The query logs are reviewed during framework audits.</p>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 11: M2 §3 PHI
sections.append(f'''
  <section class="step card" data-step-name="Interacting With PHI">
    {hero('phi', 'Module 2 &middot; Section 4 of 5', 'Interacting with Protected Health Information', 'Healthcare data carries some of the strongest legal protections &mdash; and the highest stakes for individuals.', SVG_MEDICAL)}
    <div class="card-body">
      <p class="body-text">PHI is health information that can identify a specific individual. PHI is governed by HIPAA and, where federally administered programs are involved, by additional CMS frameworks like ARC-AMPE. Mishandling PHI can affect insurance, employment, and personal relationships &mdash; and carries substantial civil and criminal penalties.</p>

      <div class="cream-block">
        <div class="cream-block-art">{ART_PHI_MIN}</div>
        <div class="cream-block-text">
          <div class="cream-block-eyebrow">Minimum necessary</div>
          <p style="margin: 0;">Use, disclose, and request only the minimum PHI needed to accomplish the task. <strong>Don't pull a full medical record when a single data point will do.</strong> The principle protects patients and protects you.</p>
        </div>
      </div>

      <div class="data-grid data-grid-2">
        <div class="data-card">
          <div class="data-card-label">Authorization Required</div>
          <div class="data-card-text">PHI generally cannot be shared without written authorization, except for treatment, payment, healthcare operations, or specifically permitted purposes.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Encrypt &amp; Log</div>
          <div class="data-card-text">PHI must be encrypted at rest and in transit. All access must be logged and audited &mdash; same requirements as FTI.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Breach Notification</div>
          <div class="data-card-text">HIPAA requires affected individuals to be notified of breaches. applicable state privacy laws adds state-level breach notification on top.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Conversation Counts Too</div>
          <div class="data-card-text">Casually mentioning a person's diagnosis to another authorized employee is still an unauthorized disclosure if it exceeds minimum necessary.</div>
        </div>
      </div>

      <div class="callout callout-info">
        <p><strong>HIPAA + applicable state privacy laws:</strong> when PHI is involved, both federal HIPAA and applicable state privacy laws may apply simultaneously. The stricter requirement always governs. When an agency administers Medicaid and related health-benefit programs, {{AGENCY_NAME}} and its contractors are bound by HIPAA in their roles as covered entities, business associates, or both.</p>
      </div>

      <h3>Try it: a scenario</h3>
      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">A coworker mentions in casual conversation that they ran into a former classmate while reviewing a Medicaid claim &mdash; "Small world, she's in treatment for X."</p>
        <div class="scenario-question">Is this a HIPAA violation?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Yes &mdash; and a reportable incident.</strong> Sharing a specific person's health condition, even verbally and even with another authorized employee, exceeds the minimum-necessary standard and isn't for treatment, payment, or healthcare operations. It's an unauthorized disclosure under HIPAA. Politely cut the conversation off and report it.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 12: M2 §4 SSA
sections.append(f'''
  <section class="step card" data-step-name="Interacting With SSA Data">
    {hero('ssa', 'Module 2 &middot; Section 5 of 5', 'Interacting with SSA data', 'SSA data drives critical decisions &mdash; accuracy, integrity, and confidentiality all matter equally.', SVG_GOVT)}
    <div class="card-body">
      <div class="concept-block reverse">
        <div class="concept-block-text">
          <p style="margin: 0;">Handling Social Security Administration data requires strict adherence to security protocols. While the safeguards for PII apply, SSA data demands additional protections due to its use in benefits administration and identity verification.</p>
        </div>
        <div class="concept-block-art">{ART_SSA_BADGE}</div>
      </div>

      <div class="data-grid data-grid-2">
        <div class="data-card">
          <div class="data-card-label">Data Accuracy &amp; Integrity</div>
          <div class="data-card-text">Verify, update, and accurately record SSA data to prevent benefit discrepancies. Keep separate from other datasets to prevent commingling.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Approved Systems Only</div>
          <div class="data-card-text">Store only in approved systems with controlled access and strong encryption. Never on personal devices or unapproved cloud locations.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Authorized Sharing Only</div>
          <div class="data-card-text">SSA data can only be shared with approved entities under strict legal guidelines. Never email unencrypted; never store outside authorized systems.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Need-to-Know Access</div>
          <div class="data-card-text">Only authorized individuals access, following need-to-know. Permissions reviewed regularly and removed when responsibilities change.</div>
        </div>
      </div>

      <h3>Try it: a scenario</h3>
      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">You're working from home and accidentally open an SSA report from your work account on a personal device. You realize a few minutes later.</p>
        <div class="scenario-question">What should you do?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Close the file and report it.</strong> Even an accidental view on a personal device counts as exposure on an unauthorized system. Don't try to "fix" it by deleting and moving on &mdash; report what happened to the Information Security Office so they can determine if any further action is needed. The mistake is small; not reporting it makes it bigger.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 13: M2 feature spread
sections.append('''
  <section class="step card" data-step-name="Why This Matters">
    <div class="feature-spread">
      <div class="feature-spread-content">
        <div class="feature-spread-eyebrow">Why this matters</div>
        <p class="feature-spread-quote">"There are only two kinds of FTI mishandling cases: the ones we can defend in an audit, and the ones that end careers. The difference is following the rules above."</p>
        <div class="feature-spread-stats">
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">5</div>
            <div class="feature-spread-stat-label">Sensitive data categories</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">24h</div>
            <div class="feature-spread-stat-label">FTI breach reporting window</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">100%</div>
            <div class="feature-spread-stat-label">Of FTI access logged</div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue to Module 3 &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 14: Module 3 intro
sections.append('''
  <section class="step card" data-step-name="Module 3: In Practice">
    <div class="module-intro">
      <div class="module-intro-content">
        <span class="module-number">Module 3 of 5</span>
        <div class="scenario-hook">
          <div class="scenario-hook-label">Picture this</div>
          <p class="scenario-hook-text">It's 4:50 PM. You're wrapping up. There's a printout sitting on the printer with a few client SSNs at the top &mdash; not yours, but you're standing right there. The printer area's empty. <em>What do you do?</em></p>
        </div>
        <h2>In Practice</h2>
        <p class="module-subtitle">The everyday rules that apply across all sensitive data &mdash; the do's, don'ts, disposal, and the modern risks of email and AI.</p>
        <div class="module-sections-list">
          <h4>What you'll cover</h4>
          <ul>
            <li>What to do &mdash; and what not to do</li>
            <li>Properly disposing of sensitive information</li>
            <li>Email and AI: two modern risks</li>
          </ul>
        </div>
        <div class="module-intro-buttons">
          <button type="button" class="btn btn-light" data-action="prev">&larr; Previous</button>
          <button type="button" class="btn btn-primary large" data-action="next">Start Module &rarr;</button>
        </div>
      </div>
    </div>
  </section>
''')

# STEP 15: M3 §1 Do/Don't
sections.append(f'''
  <section class="step card" data-step-name="Do This - Don't Do That">
    {hero('dodont', 'Module 3 &middot; Section 1 of 3', 'What to do &mdash; and what not to do', "Most security breaches don't come from sophisticated hackers. They come from a saved file in the wrong folder, an email sent to the wrong person, or a sticky note left on a desk.", SVG_WORKSPACE)}
    <div class="card-body">
      <p class="body-text">The rules below cover what causes 95% of real-world incidents &mdash; and how to avoid them. Following them isn't about being paranoid. It's about the small habits that compound into a culture where the data we hold stays where it should.</p>

      <div class="do-dont-grid">
        <div class="do-card">
          <h4>&check; What to do</h4>
          <ul>
            <li>Verify authorization before accessing or sharing sensitive information</li>
            <li>Use approved, secure channels for everything</li>
            <li>If you stumble across sensitive data, report it immediately to your supervisor and the Information Security Office</li>
            <li>Delete temporary files, clear caches, and log out when finished</li>
            <li>Be cautious of phishing emails and social engineering</li>
            <li>Verify requests &mdash; call back through a known number, not one provided in the request</li>
          </ul>
        </div>
        <div class="dont-card">
          <h4>&times; What not to do</h4>
          <ul>
            <li>Never save PII, FTI, PHI, or SSA data in personal cloud accounts</li>
            <li>Never store sensitive data on USB drives or personal laptops</li>
            <li>Never disable MFA, share credentials, or reuse weak passwords</li>
            <li>Never email sensitive data through standard your-agency.gov email</li>
            <li>Never click suspicious links asking you to "verify" your account</li>
            <li>Never assume someone else will report a problem &mdash; silence is not safe</li>
          </ul>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 16: M3 §2 Disposal
sections.append(f'''
  <section class="step card" data-step-name="Disposing of Sensitive Information">
    {hero('disposal', 'Module 3 &middot; Section 2 of 3', 'Disposing of sensitive information', "Data that's no longer needed is still a liability &mdash; until it's properly destroyed.", SVG_DISPOSAL)}
    <div class="card-body">
      <div class="concept-block">
        <div class="concept-block-text">
          <p style="margin: 0;">Sensitive data must be disposed of securely to prevent unauthorized access, identity theft, and breaches. Compliance with NIST 800-88 sanitization standards and applicable sector frameworks (HIPAA, sector-specific data handling rules) requires that sensitive information be made <strong>irretrievable</strong> &mdash; not just deleted from view, but destroyed in a way that prevents recovery.</p>
        </div>
        <div class="concept-block-art">{ART_DISPOSAL_SHRED}</div>
      </div>

      <div class="data-grid data-grid-2">
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">1</div>
          <div class="data-card-label">Classify Before Disposing</div>
          <div class="data-card-text">Identify and classify all sensitive data marked for removal. You can't dispose of something properly if you don't know what it is.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">2</div>
          <div class="data-card-label">Follow {{AGENCY_NAME}} Standards</div>
          <div class="data-card-text">For paper: shred, pulp, burn, or disintegrate. For digital media: NIST 800-88 sanitization (clear, purge, or destroy). Use agency-approved methods only.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">3</div>
          <div class="data-card-label">Use the Change Request Process</div>
          <div class="data-card-text">Use the agency's change request process for system-level disposal. Major data deletion requires authorization.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">4</div>
          <div class="data-card-label">Maintain Disposal Logs</div>
          <div class="data-card-text">Every destruction of FTI must be logged for audit. The log proves data was destroyed when required.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 17: M3 §3 Email & AI
sections.append(f'''
  <section class="step card" data-step-name="Email and AI">
    <div class="card-body">
      <div class="section-eyebrow">Module 3 &middot; Section 3 of 3</div>
      <h2>Email and AI: two modern risks</h2>
      <p class="lead">Two specific places where sensitive data most commonly leaves where it's supposed to stay.</p>

      <div class="cream-block">
        <div class="cream-block-art">{ART_EMAIL_RISK}</div>
        <div class="cream-block-text">
          <div class="cream-block-eyebrow">Email is monitored</div>
          <p style="margin: 0;">Emailing sensitive information through standard channels is prohibited at the agency. PII, FTI, PHI, and SSA data must remain within approved platforms. <strong>The same rule applies to text messages, chat apps, and personal messaging tools</strong> &mdash; never use them for sensitive data. All email and computer activity is monitored for compliance.</p>
        </div>
      </div>

      <div class="cream-block reverse">
        <div class="cream-block-text">
          <div class="cream-block-eyebrow">AI tools = uncontrolled output</div>
          <p style="margin: 0;">Generative AI tools must <strong>not</strong> be used to process, store, or generate PII, FTI, SSA data, PHI, or proprietary source code. Once data goes into a public AI tool, it may be retained, used for training, or otherwise become uncontrolled.</p>
        </div>
        <div class="cream-block-art">{ART_AI_RISK}</div>
      </div>

      <p class="body-text">If you're unsure whether a particular AI use is permitted, contact the Information Security Office <strong>before</strong> using it on anything that might contain sensitive information.</p>

      <h3>Try it: a scenario</h3>
      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">You need to draft a sensitive email to a client. You\'re in a hurry, so you paste your draft into a public AI chatbot and ask it to "make this sound more professional." The draft mentions the client\'s name, address, and case number.</p>
        <div class="scenario-question">Is this a problem?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Yes &mdash; and a reportable incident.</strong> Once the client\'s details are in a public AI tool, the data may be retained, used for training, or otherwise become uncontrolled. This applies even if you\'re only "polishing the wording." Use only agency-approved AI tools, and when in doubt, contact the Information Security Office before pasting anything that could identify a person.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 18: M3 feature spread
sections.append('''
  <section class="step card" data-step-name="Why This Matters">
    <div class="feature-spread">
      <div class="feature-spread-content">
        <div class="feature-spread-eyebrow">Why this matters</div>
        <p class="feature-spread-quote">"The most damaging incidents in government data security don't come from breaches. They come from convenience &mdash; the saved file, the forwarded email, the AI tool used 'just this once.'"</p>
        <div class="feature-spread-stats">
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">95%</div>
            <div class="feature-spread-stat-label">Incidents are human-caused</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">0</div>
            <div class="feature-spread-stat-label">Approved consumer AI tools</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">100%</div>
            <div class="feature-spread-stat-label">Of email is monitored</div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue to Module 4 &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 19: Module 4 intro
sections.append('''
  <section class="step card" data-step-name="Module 4: When Things Go Wrong">
    <div class="module-intro">
      <div class="module-intro-content">
        <span class="module-number">Module 4 of 5</span>
        <div class="scenario-hook">
          <div class="scenario-hook-label">Picture this</div>
          <p class="scenario-hook-text">You walk past a colleague's desk and notice their screen showing FTI data. Their door is open. They've been in another meeting for ten minutes. <em>Is this a problem? Whose problem?</em></p>
        </div>
        <h2>When Things Go Wrong</h2>
        <p class="module-subtitle">The consequences of mishandling sensitive data &mdash; for you, for the agency, and for the people we serve &mdash; and exactly how to report when something seems off.</p>
        <div class="module-sections-list">
          <h4>What you'll cover</h4>
          <ul>
            <li>What happens when sensitive data is mishandled</li>
            <li>Personal liability and federal penalties</li>
            <li>Reporting an incident: who, when, how</li>
          </ul>
        </div>
        <div class="module-intro-buttons">
          <button type="button" class="btn btn-light" data-action="prev">&larr; Previous</button>
          <button type="button" class="btn btn-primary large" data-action="next">Start Module &rarr;</button>
        </div>
      </div>
    </div>
  </section>
''')

# STEP 20: M4 §1 Mishandling
sections.append(f'''
  <section class="step card" data-step-name="Mishandling Consequences">
    {hero('mishandling', 'Module 4 &middot; Section 1 of 3', 'What happens when sensitive data is mishandled', 'The harm extends beyond {{AGENCY_NAME}} &mdash; to individuals, to public trust, and personally to you.', SVG_WARNING)}
    <div class="card-body">
      <p class="body-text">When sensitive data is mishandled, real people get hurt first. A breached SSN can lead to years of identity theft. A leaked health condition can affect insurance, employment, and personal relationships. A mishandled benefits record can interrupt the support someone depends on. Beyond that personal harm, {{AGENCY_NAME}} and  face severe regulatory, financial, and operational consequences.</p>

      <div class="data-grid data-grid-2">
        <div class="data-card data-card-alert">
          <div class="data-card-label">Harm to Individuals</div>
          <div class="data-card-text">Identity theft, fraud, financial loss, exposed health conditions, and lasting personal impact for the people whose data was mishandled.</div>
        </div>
        <div class="data-card data-card-alert">
          <div class="data-card-label">Financial Losses to the agency</div>
          <div class="data-card-text">Direct breach response costs, regulatory fines, civil settlements, and credit monitoring for affected individuals.</div>
        </div>
        <div class="data-card data-card-alert">
          <div class="data-card-label">Reputational Damage</div>
          <div class="data-card-text">Loss of public trust in {{AGENCY_NAME}} and its programs. Diminished confidence in our ability to safeguard the people we serve.</div>
        </div>
        <div class="data-card data-card-alert">
          <div class="data-card-label">Legal Consequences</div>
          <div class="data-card-text">Civil liability under applicable state privacy laws, HIPAA, and the Privacy Act. Criminal liability under federal disclosure statutes for violations involving regulated data.</div>
        </div>
        <div class="data-card data-card-alert">
          <div class="data-card-label">Operational Disruption</div>
          <div class="data-card-text">Suspension or termination of FTI access by the IRS. Required corrective action plans. Increased audit scrutiny going forward.</div>
        </div>
        <div class="data-card data-card-alert">
          <div class="data-card-label">Personal Liability</div>
          <div class="data-card-text">For FTI specifically, federal law assigns personal civil and criminal liability to the individual responsible &mdash; not just to the agency.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 21: M4 §2 Penalties
sections.append(f'''
  <section class="step card" data-step-name="Enforcement and Penalties">
    <div class="card-body">
      <div class="section-eyebrow">Module 4 &middot; Section 2 of 3</div>
      <h2>Enforcement and penalties</h2>
      <p class="lead">Read this carefully: when FTI is mishandled, federal law assigns liability to the individual responsible &mdash; not to the agency.</p>

      <div class="concept-block">
        <div class="concept-block-text">
          <p>Failing to follow secure practices can result in serious consequences for both individuals and the agency. Security violations may lead to loss of system access, disciplinary action up to and including termination, and legal penalties under federal and state law.</p>
          <p style="margin-bottom: 0;"><strong>For FTI specifically:</strong> federal law imposes <strong>personal</strong> criminal and civil liability on the individual who mishandles the data. The agency can support its employees, but it cannot take a federal criminal charge for them.</p>
        </div>
        <div class="concept-block-art">{ART_PENALTIES}</div>
      </div>

      <h3>Federal disclosure penalties for regulated data</h3>

      <div class="penalty-grid">
        <div class="penalty-card">
          <div class="penalty-stat">5<span class="penalty-stat-unit">yr</span></div>
          <div class="penalty-label">Federal Prison</div>
          <div class="penalty-text">Up to 5 years for unauthorized disclosure under federal data-disclosure statutes.</div>
        </div>
        <div class="penalty-card">
          <div class="penalty-stat">$5,000</div>
          <div class="penalty-label">Fine</div>
          <div class="penalty-text">Plus prosecution costs under applicable federal disclosure statutes.</div>
        </div>
        <div class="penalty-card">
          <div class="penalty-stat">$1,000</div>
          <div class="penalty-label">Per Incident</div>
          <div class="penalty-text">Civil damages under applicable federal disclosure statutes, plus punitive if willful.</div>
        </div>
      </div>

      <div class="data-grid data-grid-2">
        <div class="data-card data-card-alert">
          <div class="data-card-label">Disciplinary Action</div>
          <div class="data-card-text">Employees and contractors who fail to comply may face suspension, reassignment, or termination. Prior good performance does not exempt repeat or willful violations.</div>
        </div>
        <div class="data-card data-card-alert">
          <div class="data-card-label">Civil &amp; Criminal Penalties</div>
          <div class="data-card-text">Unauthorized access, misuse, or disclosure can result in heavy fines, criminal charges, and potential imprisonment under the Privacy Act, applicable state privacy laws, HIPAA, and sector-specific federal data-handling frameworks.</div>
        </div>
      </div>

      <div class="callout callout-warn callout-strong">
        <strong>Personal liability is real.</strong> Plus termination of clearance and permanent ineligibility for future government work involving sensitive data.
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 22: M4 §3 Reporting
sections.append(f'''
  <section class="step card" data-step-name="Reporting an Incident">
    {hero('reporting', 'Module 4 &middot; Section 3 of 3', 'Reporting an incident', 'Speed matters. False alarms are fine. Silence is not.', SVG_ALERT)}
    <div class="card-body">
      <div class="concept-block reverse">
        <div class="concept-block-text">
          <p style="margin: 0;">If you suspect a security incident involving sensitive data &mdash; whether it's PII, FTI, PHI, SSA data, or you're not even sure what kind &mdash; report it immediately. Timely reporting ensures compliance and helps mitigate risk through swift response. <strong>You don't need certainty before reporting. Just report.</strong></p>
        </div>
        <div class="concept-block-art">{ART_REPORTING_BELL}</div>
      </div>

      <div class="callout callout-warn callout-strong">
        <strong>The 24-hour rule:</strong> if you suspect a problem, the clock starts now. Report immediately to the Information Security Office. False alarms are fine &mdash; silence is not.
      </div>

      <h3>What counts as a reportable incident</h3>
      <div class="data-grid data-grid-2">
        <div class="data-card">
          <div class="data-card-label">Unauthorized Access or Disclosure</div>
          <div class="data-card-text">Someone accessing sensitive data without need-to-know, or sharing it with someone not entitled to receive it.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Data Breaches</div>
          <div class="data-card-text">Confirmed or suspected exposure to unauthorized parties &mdash; through hacking, theft, accidental email, lost device.</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Mishandling</div>
          <div class="data-card-text">Sensitive data on personal devices, shared via unapproved channels, or left exposed (printouts, screens, sticky notes).</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Improper Sharing</div>
          <div class="data-card-text">Sensitive data sent to the wrong recipient, posted in the wrong system, or commingled inappropriately.</div>
        </div>
      </div>

      <h3>How to report</h3>
      <p class="body-text">Use your agency's incident reporting process. Provide as much detail as you can: what you observed, what data is involved, when you noticed, and any actions taken. <strong>If you're unsure who to contact, email the Information Security Office at security@your-agency.gov</strong> &mdash; getting the report in is more important than getting the channel right.</p>

      <div class="callout callout-info">
        <p><strong>For incidents involving regulated data:</strong> the Information Security Office handles all external escalation to federal regulators within the timelines required by the applicable framework (typically 24-72 hours from confirmation). You don't make those calls yourself &mdash; your job is to report to the Information Security Office promptly.</p>
      </div>

      <h3>Try it: a scenario</h3>
      <div class="scenario-card">
        <span class="scenario-label">Scenario</span>
        <p class="scenario-setup">Back to that colleague's open door and visible FTI screen. They're in a meeting; the conference room door has been open for 10 minutes.</p>
        <div class="scenario-question">Is this reportable? What do you do?</div>
        <button type="button" class="scenario-reveal-btn">Reveal Answer &rarr;</button>
        <div class="scenario-answer">
          <div class="scenario-answer-label">Answer</div>
          <div class="scenario-answer-text"><strong>Yes &mdash; report it.</strong> Even if no one unauthorized actually saw the data, this is a potential exposure of FTI and a violation of the two-barrier rule. Lock the screen yourself if you can, then notify the Information Security Office with what you observed and when. Your job is to report &mdash; the determination of whether it rises to a confirmed incident isn't yours to make.</div>
        </div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 23: M4 feature spread
sections.append('''
  <section class="step card" data-step-name="Why This Matters">
    <div class="feature-spread">
      <div class="feature-spread-content">
        <div class="feature-spread-eyebrow">Why this matters</div>
        <p class="feature-spread-quote">"The cost of reporting a false alarm is a few minutes of your time. The cost of staying silent on a real incident is measured in years and dollars."</p>
        <div class="feature-spread-stats">
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">24h</div>
            <div class="feature-spread-stat-label">Window to report incidents</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">5y</div>
            <div class="feature-spread-stat-label">Maximum prison for FTI disclosure</div>
          </div>
          <div class="feature-spread-stat">
            <div class="feature-spread-stat-number">0</div>
            <div class="feature-spread-stat-label">Penalties for false alarms</div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue to Module 5 &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 24: Module 5 intro
sections.append('''
  <section class="step card" data-step-name="Module 5: Acknowledgment">
    <div class="module-intro">
      <div class="module-intro-content">
        <span class="module-number">Module 5 of 5</span>
        <div class="scenario-hook">
          <div class="scenario-hook-label">Picture this</div>
          <p class="scenario-hook-text">A year from now, an audit team asks for proof that you understood your responsibilities. Your signed Personal Responsibility Statement &mdash; the one you're about to sign &mdash; is the answer.</p>
        </div>
        <h2>Acknowledgment</h2>
        <p class="module-subtitle">A short summary of the key points, then sign your Personal Responsibility Statement to complete the training and receive your certificate.</p>
        <div class="module-sections-list">
          <h4>What's left</h4>
          <ul>
            <li>Five things to remember</li>
            <li>Personal Responsibility Statement</li>
            <li>Receive your completion certificate</li>
          </ul>
        </div>
        <div class="module-intro-buttons">
          <button type="button" class="btn btn-light" data-action="prev">&larr; Previous</button>
          <button type="button" class="btn btn-primary large" data-action="next">Continue &rarr;</button>
        </div>
      </div>
    </div>
  </section>
''')

# STEP 25: Five things
sections.append('''
  <section class="step card" data-step-name="Five Things to Remember">
    <div class="card-body">
      <div class="section-eyebrow">Module 5 &middot; Summary</div>
      <h2>Five things to remember</h2>
      <p class="lead">If you remember nothing else from this training, remember these.</p>

      <div class="data-grid data-grid-1">
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">1</div>
          <div class="data-card-label">All sensitive data deserves protection</div>
          <div class="data-card-text">PII, FTI, PHI, and SSA data each have their own rules &mdash; but all require encryption, access controls, secure storage, and proper disposal.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">2</div>
          <div class="data-card-label">Need-to-know access only</div>
          <div class="data-card-text">Access is based on the job, not the person. Even with clearance, only access data your role actually requires.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">3</div>
          <div class="data-card-label">Approved channels only</div>
          <div class="data-card-text">Standard email, personal devices, public AI tools, and unapproved cloud services are not acceptable for sensitive data.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">4</div>
          <div class="data-card-label">Report fast &mdash; don't wait for certainty</div>
          <div class="data-card-text">Suspected problem? Report to the Information Security Office promptly. False alarms are fine; silence is not.</div>
        </div>
        <div class="data-card data-card-numbered">
          <div class="data-card-icon">5</div>
          <div class="data-card-label">You're personally accountable</div>
          <div class="data-card-text">For FTI especially, federal law assigns liability to the individual responsible &mdash; not just to the agency. Treat the data accordingly.</div>
        </div>
      </div>

      <div class="callout">
        <p><strong>When in doubt &mdash; ask.</strong> Email the Information Security Office at security@your-agency.gov. There's no penalty for asking.</p>
      </div>

      <h3>How would you rate this training?</h3>
      <div class="form-group">
        <label for="qualityRating">Quality rating (optional)</label>
        <select id="qualityRating">
          <option value="">&mdash; Select &mdash;</option>
          <option value="7">7 &mdash; Excellent</option>
          <option value="6">6 &mdash; Very Good</option>
          <option value="5">5 &mdash; Good</option>
          <option value="4">4 &mdash; Acceptable</option>
          <option value="3">3 &mdash; Needs Improvement</option>
          <option value="2">2 &mdash; Poor</option>
          <option value="1">1 &mdash; Very Poor</option>
        </select>
        <div class="help-text">Helps us improve content for future cycles. Anonymous in aggregate reporting.</div>
      </div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" data-action="next">Continue to Acknowledgment &rarr;</button>
      </div>
    </div>
  </section>
''')

# STEP 26: PRS
sections.append('''
  <section class="step card" data-step-name="Personal Responsibility Statement">
    <div class="hero-block navy">
      <div class="hero-block-content">
        <div class="section-eyebrow">Final Step</div>
        <h2>Personal Responsibility Statement</h2>
        <p class="hero-subtitle">Signing this isn't paperwork &mdash; it's a federal requirement.</p>
      </div>
    </div>
    <div class="card-body">
      <p class="body-text">By signing below, I acknowledge each of the following:</p>

      <div class="prs-numbered">
        <? for (var i = 0; i < prsAcknowledgments.length; i++) { ?>
          <div class="prs-item">
            <div class="prs-item-number"><?= (i + 1) ?></div>
            <div class="prs-item-text"><?= prsAcknowledgments[i] ?></div>
          </div>
        <? } ?>
      </div>

      <div class="prs-checkbox">
        <input type="checkbox" id="prs-acknowledged" data-ack-required="true">
        <label for="prs-acknowledged">I have read and agree to all five acknowledgments above.</label>
      </div>
      <div class="field-error" id="prs-acknowledged-error" role="alert">You must acknowledge the PRS to complete training.</div>

      <div class="form-group" style="margin-top: 36px;">
        <label for="signature">Type your full legal name as your signature <span class="required-mark" aria-hidden="true">*</span></label>
        <input type="text" id="signature" data-required="true" autocomplete="off" placeholder="Type your full name">
        <div class="help-text">Your typed name must include both first and last name as entered earlier. This is recorded as your electronic signature.</div>
        <div class="field-error" id="signature-error" role="alert"></div>
      </div>

      <div class="error-banner" id="submit-error" style="display:none;" role="alert"></div>

      <div class="button-row">
        <button type="button" class="btn btn-secondary" data-action="prev">&larr; Previous</button>
        <button type="button" class="btn btn-primary" id="submit-btn">Submit &amp; Generate Certificate</button>
      </div>
    </div>
  </section>
''')

# STEP 27: Submitting
sections.append('''
  <section class="step card" id="submitting-state" data-step-name="Submitting">
    <div class="card-body">
      <div class="submitting">
        <div class="spinner" aria-hidden="true"></div>
        <h2 style="margin-top:0;">Recording your acknowledgment and generating certificate&hellip;</h2>
        <p>Please don't close this window.</p>
      </div>
    </div>
  </section>
''')

# STEP 28: Success
sections.append('''
  <section class="step card" id="success-state" data-step-name="Complete">
    <div class="card-body success-card">
      <div class="success-icon" aria-hidden="true">&check;</div>
      <h2>Training complete</h2>
      <p class="lead">Your acknowledgment has been recorded and your certificate has been generated.</p>
      <dl class="success-details">
        <dt>Completion Date</dt><dd id="success-completion-date"></dd>
        <dt>Next Due</dt><dd id="success-next-due"></dd>
        <dt>Certificate ID</dt><dd id="success-cert-id"></dd>
        <dt>Confirmation Email Sent To</dt><dd id="success-email"></dd>
      </dl>
      <div class="certificate-download">
        <h3>Your completion certificate</h3>
        <p>A copy has been emailed to you and saved to the agency's certificates archive.</p>
        <a id="success-cert-link" href="#" target="_blank" rel="noopener" style="display:none;">Download Certificate (PDF) &rarr;</a>
      </div>
      <p style="margin-top: 32px;">You'll receive recertification reminders 30, 14, 7, and 1 day(s) before your next due date.</p>
      <p style="font-size: 15px; color: var(--gray); margin-top: 28px;">
        Questions or to report a suspected incident: <a href="mailto:security@your-agency.gov" style="color: var(--tan-dark);">security@your-agency.gov</a>
      </p>
    </div>
  </section>
''')

# Footer
sections.append('''
</main>

<?!= include('JavaScript'); ?>

</body>
</html>
''')

INDEX = ''.join(sections)

# Substitute config placeholders. Handle double-braced (from non-f-string sources)
# first, then single-braced (from f-string evaluation).
for ph, val in [
    ('AGENCY_NAME', CONFIG['AGENCY_NAME']),
    ('TRAINING_VERSION', CONFIG['TRAINING_VERSION']),
    ('SECURITY_CONTACT', CONFIG['SECURITY_CONTACT']),
    ('RECERTIFICATION_DAYS', str(CONFIG['RECERTIFICATION_DAYS'])),
]:
    INDEX = INDEX.replace('{{' + ph + '}}', val)
    INDEX = INDEX.replace('{' + ph + '}', val)

with open('Index.html', 'w') as f:
    f.write(INDEX)

step_count = INDEX.count('<section class="step')
print(f"Step count: {step_count}")
print(f"File size: {len(INDEX):,} bytes")
