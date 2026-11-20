#!/usr/bin/env python3
"""The World Today -- front page of Thursday 19 November 2026.

Draws a one-page newspaper front page (1024x1024 PNG) summing up the
world news of 19 November 2026, using only the Python standard library.
Deterministic: same bytes on every run. No network, no clock, no random.

Stories (all reported on 19 November 2026):
  1. Trump, Xi and Putin hold first three-way summit in Shenzhen (AP, DPA)
  2. UN court (ICJ) rules Myanmar committed genocide vs Rohingya (BBC, UN)
  3. Wall Street slides 2% for a fifth day; Nikkei falls 4.68% (market data)
  4. Anthropic IPO raises about $81 billion at $83 a share (record debut)
  5. Ukraine hits the Crimean Bridge again, third strike in four days
  6. Cyclone Akvan nears the Andhra Pradesh-Odisha coast of India
  7. Voyager 1 reaches one light-day from Earth

Usage: MAKEFUN_OUTPUT_DIR=out python3 main.py
Writes <output dir>/entry.png (default /output/entry.png).
"""

import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GREY = (96, 92, 82)
SKY = (214, 232, 242)
LAND = (122, 148, 110)
WHITE = (255, 255, 255)

# 5x7 bitmap font. '#' = on, '.' = off. Uppercase + digits + punctuation.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.###", "#..##"),
    "&": (".###.", "#...#", "#...#", ".#.#.", "#.#..", "#.#.#", ".##.#"),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
}


def text_width(text, scale):
    return len(text) * 6 * scale


def wrap_text(text, max_w, scale):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            trial = word if not cur else cur + " " + word
            if text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color, t=1):
        for k in range(t):
            self.hline(x + k, y + k, x + w - 1 - k, color)
            self.hline(x + k, y + h - 1 - k, x + w - 1 - k, color)
            self.vline(x + k, y + k, y + h - 1 - k, color)
            self.vline(x + w - 1 - k, y + k, y + h - 1 - k, color)

    def hline(self, x0, y, x1, color, t=1):
        if x1 < x0:
            x0, x1 = x1, x0
        for k in range(t):
            for x in range(x0, x1 + 1):
                self.set(x, y + k, color)

    def vline(self, x, y0, y1, color, t=1):
        if y1 < y0:
            y0, y1 = y1, y0
        for k in range(t):
            for y in range(y0, y1 + 1):
                self.set(x + k, y, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            for k in range(t):
                self.set(x + k, y, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color, t=1, fill=None):
        if fill is not None:
            for yy in range(cy - r, cy + r + 1):
                dx = int((r * r - (yy - cy) ** 2) ** 0.5)
                self.hline(cx - dx, yy, cx + dx, fill)
        x, y, d = 0, r, 3 - 2 * r
        while x <= y:
            for px, py in ((cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y),
                           (cx - x, cy - y), (cx + y, cy + x), (cx - y, cy + x),
                           (cx + y, cy - x), (cx - y, cy - x)):
                for k in range(t):
                    self.set(px + k, py, color)
                    self.set(px, py + k, color)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def ellipse(self, cx, cy, rx, ry, color):
        for yy in range(cy - ry, cy + ry + 1):
            t = (yy - cy) / ry
            dx = int(rx * (1 - t * t) ** 0.5)
            self.hline(cx - dx, yy, cx + dx, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT["?"])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "#":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def text_center(self, y, s, scale, color):
        self.text((self.w - text_width(s, scale)) // 2, y, s, scale, color)


def write_png(path, canvas):
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * canvas.w * 3:(y + 1) * canvas.w * 3]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


# ---- small pictogram icons (drawn inside a ~56x56 box) ----

def icon_scales(c, x, y):
    c.vline(x + 28, y + 4, y + 44, INK, 3)
    c.hline(x + 8, y + 8, x + 48, INK, 3)
    c.hline(x + 20, y + 48, x + 36, INK, 3)
    for cx in (x + 12, x + 44):
        c.vline(cx, y + 11, y + 26, INK, 2)
        c.line(cx - 9, y + 26, cx + 9, y + 26, INK, 2)
        c.line(cx - 9, y + 26, cx, y + 38, INK, 2)
        c.line(cx + 9, y + 26, cx, y + 38, INK, 2)


def icon_chart(c, x, y):
    c.vline(x + 6, y + 4, y + 50, INK, 2)
    c.hline(x + 6, y + 50, x + 52, INK, 2)
    pts = [(10, 12), (20, 20), (28, 16), (38, 32), (48, 44)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(x + ax, y + ay, x + bx, y + by, RED, 3)
    c.line(x + 48, y + 44, x + 42, y + 42, RED, 3)
    c.line(x + 48, y + 44, x + 46, y + 38, RED, 3)


def icon_chip(c, x, y):
    c.rect(x + 16, y + 16, 26, 26, INK, 3)
    c.rect(x + 23, y + 23, 12, 12, RED, 2)
    for k in range(3):
        px = x + 21 + k * 8
        c.vline(px, y + 8, y + 15, INK, 2)
        c.vline(px, y + 43, y + 50, INK, 2)
        c.hline(x + 8, y + 21 + k * 8, x + 15, INK, 2)
        c.hline(x + 43, y + 21 + k * 8, x + 50, INK, 2)


def icon_bridge(c, x, y):
    c.hline(x + 4, y + 44, x + 52, INK, 3)
    c.vline(x + 12, y + 14, y + 44, INK, 3)
    c.vline(x + 42, y + 14, y + 44, INK, 3)
    c.line(x + 12, y + 14, x + 27, y + 40, INK, 2)
    c.line(x + 42, y + 14, x + 27, y + 40, INK, 2)
    c.line(x + 12, y + 30, x + 27, y + 40, INK, 2)
    c.line(x + 42, y + 30, x + 27, y + 40, INK, 2)


def icon_cyclone(c, x, y):
    import math
    for turn in range(3):
        r0 = 6 + turn * 7
        for a in range(0, 270, 6):
            ang = math.radians(a + turn * 40)
            r = r0 + a / 270.0 * 7
            px = int(x + 28 + r * math.cos(ang))
            py = int(y + 28 + r * math.sin(ang))
            c.fill_rect(px, py, 3, 3, BLUE)
    c.circle(x + 28, y + 28, 4, INK, 2, fill=PAPER)


def icon_voyager(c, x, y):
    c.fill_rect(x + 24, y + 22, 10, 12, INK)
    c.fill_rect(x + 8, y + 24, 12, 8, BLUE)
    c.fill_rect(x + 38, y + 24, 12, 8, BLUE)
    c.line(x + 29, y + 22, x + 40, y + 10, INK, 2)
    c.line(x + 40, y + 10, x + 46, y + 16, INK, 2)
    c.line(x + 40, y + 10, x + 34, y + 16, INK, 2)
    for dx, dy in ((12, 44), (44, 44), (28, 12)):
        c.fill_rect(x + dx, y + dy, 3, 3, RED)


# ---- flags for the lead illustration ----

def flag_usa(c, x, y, w, h):
    stripe = max(1, h // 7)
    for i in range(7):
        c.fill_rect(x, y + i * stripe, w, stripe, RED if i % 2 == 0 else WHITE)
    c.fill_rect(x, y, w * 2 // 5, stripe * 4, BLUE)
    for r in range(3):
        for col in range(4):
            c.fill_rect(x + 4 + col * 8, y + 3 + r * 5, 2, 2, WHITE)


def flag_china(c, x, y, w, h):
    c.fill_rect(x, y, w, h, RED)
    for dx, dy in ((10, 8), (26, 6), (32, 12), (26, 18), (12, 16)):
        c.fill_rect(x + dx, y + dy, 4, 4, (255, 222, 0))


def flag_russia(c, x, y, w, h):
    third = h // 3
    c.fill_rect(x, y, w, third, WHITE)
    c.fill_rect(x, y + third, w, third, BLUE)
    c.fill_rect(x, y + 2 * third, w, h - 2 * third, RED)


# ---- layout ----

COLS = [(36, 296), (364, 296), (692, 296)]


def story(c, col, y, kicker, headline, body, icon):
    x, w = COLS[col]
    c.text(x, y, kicker, 2, BLUE)
    icon(c, x + (w - 56) // 2, y + 22)
    hy = y + 86
    lines = wrap_text(headline, w, 3)
    for i, ln in enumerate(lines):
        c.text(x, hy + i * 26, ln, 3, INK)
    by = hy + len(lines) * 26 + 8
    for i, ln in enumerate(wrap_text(body, w, 2)):
        c.text(x, by + i * 17, ln, 2, INK)


def draw():
    c = Canvas(W, H, PAPER)
    c.rect(16, 16, 992, 992, INK, 3)

    # top line
    c.text(36, 34, "VOL. I - NO. 323", 2, GREY)
    right = "ONE PAGE - FREE"
    c.text(988 - text_width(right, 2), 34, right, 2, GREY)
    c.hline(36, 58, 988, INK, 2)

    # masthead
    c.text_center(72, "THE WORLD TODAY", 8, INK)
    c.hline(36, 136, 988, INK, 2)

    # date bar
    c.fill_rect(36, 146, 952, 46, INK)
    c.text_center(158, "THURSDAY, 19 NOVEMBER 2026", 3, WHITE)

    # ---- lead story ----
    c.text(36, 210, "LEAD STORY - SHENZHEN, CHINA", 2, RED)
    hx = 36
    for i, ln in enumerate(wrap_text(
            "TRUMP, XI AND PUTIN HOLD FIRST THREE-WAY SUMMIT", 560, 4)):
        c.text(hx, 238 + i * 36, ln, 4, INK)
    sub = ("LEADERS AGREE TO TALKS ON NUCLEAR RISKS AND ENERGY FLOWS "
           "AT APEC SIDELINES. DECLARATION SILENT ON UKRAINE AND IRAN.")
    for i, ln in enumerate(wrap_text(sub, 560, 2)):
        c.text(hx, 352 + i * 18, ln, 2, GREY)
    c.text(hx, 440, "FIRST MEETING OF THE THREE LEADERS.", 2, INK)
    c.text(hx, 462, "UKRAINE AND EUROPE NOT AT THE TABLE.", 2, INK)

    # globe illustration
    gx, gy, gr = 806, 322, 98
    c.circle(gx, gy, gr, INK, 3, fill=SKY)
    c.circle(gx, gy, gr, INK, 3)
    for dy in (-52, 0, 52):
        half = int((gr * gr - dy * dy) ** 0.5)
        c.hline(gx - half, gy + dy, gx + half, INK, 2)
    for dx in (-46, 46):
        c.vline(gx + dx, gy - 84, gy + 84, INK, 2)
    c.ellipse(gx - 34, gy - 30, 26, 12, LAND)
    c.ellipse(gx + 28, gy + 26, 30, 14, LAND)
    c.ellipse(gx + 40, gy - 44, 16, 9, LAND)

    # three flags under the globe
    fy = 436
    flag_usa(c, 640, fy, 96, 42)
    flag_china(c, 752, fy, 96, 42)
    flag_russia(c, 864, fy, 96, 42)
    c.rect(640, fy, 96, 42, INK, 2)
    c.rect(752, fy, 96, 42, INK, 2)
    c.rect(864, fy, 96, 42, INK, 2)
    for fx, name in ((640, "USA"), (752, "CHINA"), (864, "RUSSIA")):
        c.text(fx + (96 - text_width(name, 2)) // 2, fy + 48, name, 2, INK)

    c.hline(36, 516, 988, INK, 3)

    # ---- second row ----
    story(c, 0, 534, "JUSTICE - THE HAGUE",
          "MYANMAR GUILTY OF GENOCIDE",
          "ICJ RULES 2017 CRACKDOWN ON ROHINGYA WAS GENOCIDE. "
          "FIRST SUCH FINDING VS A STATE.", icon_scales)
    story(c, 1, 534, "MARKETS - NEW YORK",
          "STOCKS SLIDE FOR FIFTH DAY",
          "S&P 500 DOWN 2.02%. NIKKEI FALLS 4.68% AS AI VALUATION "
          "FEARS SPREAD WORLDWIDE.", icon_chart)
    story(c, 2, 534, "TECH - AI",
          "ANTHROPIC IPO RAISES $81BN",
          "RECORD DEBUT AT $83 A SHARE. STOCK CLOSES UP 17% "
          "ON FIRST DAY OF TRADING.", icon_chip)

    c.hline(36, 756, 988, INK, 3)

    # ---- third row ----
    story(c, 0, 774, "WAR - UKRAINE",
          "CRIMEAN BRIDGE HIT AGAIN",
          "THIRD STRIKE IN FOUR DAYS. RAIL HALTED.", icon_bridge)
    story(c, 1, 774, "WEATHER - INDIA",
          "CYCLONE AKVAN NEARS INDIA",
          "LANDFALL FRIDAY. WINDS TO 110 KM/H.", icon_cyclone)
    story(c, 2, 774, "SPACE",
          "VOYAGER 1 ONE LIGHT-DAY OUT",
          "A LIGHT-DAY FROM EARTH. FARTHEST OBJECT EVER.", icon_voyager)

    # footer
    c.hline(36, 968, 988, INK, 2)
    c.text_center(978, "SOURCES: AP, REUTERS, BBC, UN NEWS, DPA", 2, GREY)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    write_png(os.path.join(out_dir, "entry.png"), draw())


if __name__ == "__main__":
    main()
