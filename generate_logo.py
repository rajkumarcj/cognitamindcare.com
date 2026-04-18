#!/usr/bin/env python3
"""
Cognita Mindcare logo — updated color scheme.
Output: 600x200 RGBA transparent PNG.

Layout: brain icon LEFT, text RIGHT, vertically centered.

Brain icon:
  Left hemisphere:  dark teal  #3AABA0
  Right hemisphere: light mint #7BCBC5
  White lotus/leaf petal cutouts inside
  Thin white curved line separating hemispheres

Text:
  "Cognita"  — dusty rose/mauve #C4A8B0, Lora-Bold serif, large
  "MINDCARE" — cool gray #7A7A7A, InstrumentSans-Regular, smaller spaced caps
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = (
    "/Users/veroraj/Library/Application Support/Claude/local-agent-mode-sessions"
    "/skills-plugin/75d333df-60db-4876-9245-0365b95ad812"
    "/dca81173-ddc5-4bbb-99bb-2d75d8cf36d3/skills/canvas-design/canvas-fonts"
)
OUTPUT = "/Users/veroraj/Website/logo.png"

W, H = 600, 200

# ── Palette ──────────────────────────────────────────────────────────────────
BRAIN_LEFT   = ( 58, 171, 160, 255)   # #3AABA0  left hemisphere (darker teal)
BRAIN_RIGHT  = (123, 203, 197, 255)   # #7BCBC5  right hemisphere (lighter mint)
WHITE        = (255, 255, 255, 255)   # white cutout details + divider line
TEXT_ROSE    = (196, 168, 176, 255)   # #C4A8B0  "Cognita" dusty rose/mauve
TEXT_GRAY    = (122, 122, 122, 255)   # #7A7A7A  "MINDCARE" cool gray


# ── Helper: anti-aliased rotated petal ellipse on a temp layer ───────────────
def petal_layer(fan_cx, fan_cy, petal_length, petal_width, angle_deg, fill,
                scale=4):
    """
    Draw one petal (tall ellipse) pointing straight up with base at
    (fan_cx, fan_cy), then rotate by angle_deg around that base point.
    Returns a W×H RGBA layer.
    """
    big_w = int((petal_width + 8) * scale)
    big_h = int((petal_length + 8) * scale)

    big = Image.new("RGBA", (big_w, big_h), (0, 0, 0, 0))
    px = 4 * scale // 2
    ImageDraw.Draw(big).ellipse([px, px, big_w - px, big_h - px], fill=fill)
    big_small = big.resize((big_w // scale, big_h // scale), Image.LANCZOS)
    sw, sh = big_small.size

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ox = fan_cx - sw // 2
    oy = fan_cy - sh
    layer.paste(big_small, (ox, oy), big_small)

    rotated = layer.rotate(-angle_deg, center=(fan_cx, fan_cy),
                           resample=Image.BICUBIC)
    return rotated


# ── Brain silhouette — two hemispheres ───────────────────────────────────────
def draw_brain(img):
    """
    Two side-by-side brain hemispheres, centered vertically on the canvas.

    Brain block occupies roughly x=20–180, y=30–170 (140×140px region).
    Left hemisphere: dark teal, organic bumpy rounded blob, left half.
    Right hemisphere: lighter mint, mirror image, right half.
    White lotus petal cutouts overlaid on top of both hemispheres.
    White thin curved divider line between hemispheres.
    """
    brain_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(brain_layer)

    # ── Left hemisphere (dark teal #3AABA0) ──────────────────────────────────
    # Main body: left half of central ellipse
    bd.ellipse([35, 45, 160, 155], fill=BRAIN_LEFT)

    # Organic bumps on the left outer edge
    bd.ellipse([24, 50,  65,  88], fill=BRAIN_LEFT)   # top-left bump
    bd.ellipse([22, 82,  60, 118], fill=BRAIN_LEFT)   # mid-left bump
    bd.ellipse([26, 110, 62, 146], fill=BRAIN_LEFT)   # lower-left bump

    # Lower temporal lobe (left side)
    bd.ellipse([38, 138, 140, 168], fill=BRAIN_LEFT)

    # ── Right hemisphere (mint #7BCBC5) ──────────────────────────────────────
    # Main body: right half of central ellipse (overlaps slightly to cover seam)
    bd.ellipse([48, 45, 174, 155], fill=BRAIN_RIGHT)

    # Organic bumps on the right outer edge (mirror of left)
    bd.ellipse([148, 50, 189,  88], fill=BRAIN_RIGHT)  # top-right bump
    bd.ellipse([153, 82, 191, 118], fill=BRAIN_RIGHT)  # mid-right bump
    bd.ellipse([151, 110, 187, 146], fill=BRAIN_RIGHT) # lower-right bump

    # Lower temporal lobe (right side)
    bd.ellipse([72, 138, 175, 168], fill=BRAIN_RIGHT)

    img.alpha_composite(brain_layer)


# ── White lotus/leaf petal cutouts ───────────────────────────────────────────
def draw_lotus(img):
    """
    White petal shapes radiating upward from inside the brain,
    creating the lotus/leaf cutout detail effect.
    Fan base centered inside the brain icon.
    """
    fan_cx, fan_cy = 107, 138   # base of the fan (inside brain)

    # (angle_from_vertical_deg, length, width, color)
    petals = [
        (-50, 58, 10, WHITE),   # far left
        (-33, 63, 12, WHITE),   # left
        (-16, 65, 13, WHITE),   # center-left
        (  0, 64, 13, WHITE),   # straight up
        ( 16, 63, 12, WHITE),   # center-right
        ( 33, 60, 11, WHITE),   # right
        ( 50, 55,  9, WHITE),   # far right
    ]

    combined = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for angle, length, width, color in petals:
        lyr = petal_layer(fan_cx, fan_cy, length, width, angle, color)
        combined.alpha_composite(lyr)

    # Small center oval bud
    bud = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bud).ellipse(
        [fan_cx - 7, fan_cy - 10, fan_cx + 7, fan_cy + 3],
        fill=WHITE
    )
    combined.alpha_composite(bud)

    # Composite petals onto brain using destination-out to create cutouts,
    # but since we want white details (not holes), just composite normally
    # at reduced opacity for a subtle inset look
    # Reduce alpha of white petals so they appear as highlights, not full cutouts
    faded = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for px_x in range(W):
        for px_y in range(H):
            r, g, b, a = combined.getpixel((px_x, px_y))
            if a > 0:
                faded.putpixel((px_x, px_y), (r, g, b, int(a * 0.75)))

    img.alpha_composite(faded)


# ── White curved hemisphere divider line ─────────────────────────────────────
def draw_divider(img):
    """
    A thin white curved line separating the two brain hemispheres.
    Runs vertically with a gentle S-curve through the center of the brain.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Draw a gentle S-curve from top to bottom of brain at x≈107
    cx = 107
    y_top    = 45
    y_bottom = 168
    amplitude = 6  # horizontal sway of the S-curve

    points = []
    steps = 80
    for i in range(steps + 1):
        t = i / steps
        y = y_top + t * (y_bottom - y_top)
        # S-curve: sin(π*t) gives a gentle bow; use full sine for S-shape
        x = cx + int(amplitude * math.sin(2 * math.pi * t - math.pi / 2))
        # Fade alpha at top and bottom for smooth endpoints
        edge_fade = math.sin(math.pi * t)
        alpha = int(220 * edge_fade)
        points.append((x, y, alpha))

    for i in range(len(points) - 1):
        x1, y1, a1 = points[i]
        x2, y2, a2 = points[i + 1]
        avg_alpha = (a1 + a2) // 2
        if avg_alpha > 0:
            d.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, avg_alpha), width=2)

    img.alpha_composite(layer)


# ── "Cognita" text ────────────────────────────────────────────────────────────
def draw_cognita(img, draw):
    """
    Dusty rose #C4A8B0, Lora-Bold serif, large elegant font.
    Positioned to the right of the brain icon, vertically upper portion.
    Canvas is 600x200; brain occupies ~x=20–195.
    Text starts at x≈205, vertical center around y=70–110.
    """
    font_path = os.path.join(FONTS_DIR, "Lora-Bold.ttf")
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    # Find a size that fits comfortably in the right panel (width ≤ 370px)
    chosen_size = 58
    for size in range(80, 40, -1):
        font = ImageFont.truetype(font_path, size)
        bb   = dummy_draw.textbbox((0, 0), "Cognita", font=font)
        total_w = bb[2] - bb[0]
        if total_w <= 370:
            chosen_size = size
            break

    font   = ImageFont.truetype(font_path, chosen_size)
    bb     = dummy_draw.textbbox((0, 0), "Cognita", font=font)
    text_x = 205
    # Place so the visual cap top sits at roughly y=38 (top third of 200px canvas)
    text_y = 38 - bb[1]
    draw.text((text_x, text_y), "Cognita", font=font, fill=TEXT_ROSE)
    print(f"Cognita: size={chosen_size}, bbox={bb}, placed at ({text_x},{text_y})")


# ── "MINDCARE" text ───────────────────────────────────────────────────────────
def draw_mindcare(img, draw):
    """
    Cool gray #7A7A7A, InstrumentSans-Regular, smaller spaced caps.
    Positioned below "Cognita", left-aligned with it at x≈205.
    """
    font_path  = os.path.join(FONTS_DIR, "InstrumentSans-Regular.ttf")
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    # Find a comfortable size; target cap height ~15–18px
    chosen_size = 16
    for size in range(26, 10, -1):
        font  = ImageFont.truetype(font_path, size)
        bb_M  = dummy_draw.textbbox((0, 0), "M", font=font)
        cap_h = bb_M[3] - bb_M[1]
        if cap_h <= 16:
            chosen_size = size
            break

    font = ImageFont.truetype(font_path, chosen_size)

    # Measure character widths for manual letter spacing
    char_widths = []
    for ch in "MINDCARE":
        cb = dummy_draw.textbbox((0, 0), ch, font=font)
        char_widths.append(cb[2] - cb[0])

    letter_spacing = 5   # generous spacing for spaced-caps look

    # Vertical position: below Cognita, leaving a comfortable gap
    # Cognita bottom is roughly at y=38 + cap_height + descender ≈ y=120
    # Place MINDCARE at y≈128
    bb_M    = dummy_draw.textbbox((0, 0), "M", font=font)
    top_off = bb_M[1]
    text_y  = 128 - top_off

    cx = 205
    for i, ch in enumerate("MINDCARE"):
        draw.text((cx, text_y), ch, font=font, fill=TEXT_GRAY)
        cx += char_widths[i] + letter_spacing

    print(f"MINDCARE: size={chosen_size}, spacing={letter_spacing}, ends at x={cx}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_brain(img)
    draw_lotus(img)
    draw_divider(img)
    draw_cognita(img, draw)
    draw_mindcare(img, draw)

    img.save(OUTPUT)
    print(f"\nSaved {OUTPUT}  ({W}×{H} RGBA)")


if __name__ == "__main__":
    main()
