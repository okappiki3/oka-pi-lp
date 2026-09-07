#!/usr/bin/env python3
"""連載記事 OGP 生成 (1200x630)
使い方:
  python3 gen_ogp_series.py --kai 3 \
    --title "「AIの回答、毎回ファクトチェックが|必要？」使い道で、|確認の重さが変わります" \
    --out assets/img/insights/genai-security/03/ogp.png

  # ハブ用（回番号なし）
  python3 gen_ogp_series.py \
    --title "支援先に聞かれたらどう答える？|生成AI×セキュリティ" \
    --out assets/img/insights/genai-security/ogp.png

タイトル改行は「|」で区切る。--wrap で1行あたりの推奨字数を調整可。
"""
import argparse, math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (10, 88, 132)
NAVY_DEEP = (6, 42, 64)
DARK = (16, 42, 67)
LIGHT_BLUE = (173, 203, 227)
PALE = (236, 244, 250)
GOLD = (201, 168, 76)

SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SANS_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def jp_font(path, size):
    for idx in range(8):
        try:
            f = ImageFont.truetype(path, size, index=idx)
            name = " ".join(f.getname())
            if "JP" in name:
                return f
        except Exception:
            break
    return ImageFont.truetype(path, size, index=0)


def draw_network(draw, seed=7):
    rng = random.Random(seed)
    nodes = []
    for _ in range(26):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H - 90)
        nodes.append((x, y))
    for i, (x1, y1) in enumerate(nodes):
        for x2, y2 in nodes[i + 1:]:
            d = math.hypot(x1 - x2, y1 - y2)
            if d < 230:
                draw.line([x1, y1, x2, y2], fill=(*LIGHT_BLUE, 60), width=1)
    for x, y in nodes:
        r = rng.uniform(2, 4)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*LIGHT_BLUE, 110))


def wrap_title(title, wrap):
    """タイトルを '|' 区切り優先、無ければ wrap 字数で折り返す"""
    if "|" in title:
        return [s for s in title.split("|") if s]
    lines, cur = [], ""
    for ch in title:
        cur += ch
        if len(cur) >= wrap:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kai", type=int, default=None, help="連載の回番号（省略時はハブ）")
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--wrap", type=int, default=20)
    ap.add_argument("--series",
                    default="支援先に聞かれたらどう答える？　生成AI×セキュリティ")
    args = ap.parse_args()

    lines = wrap_title(args.title, args.wrap)
    if len(lines) > 3:
        print(f"[warn] title wraps to {len(lines)} lines. Consider a wider --wrap.")

    # 背景（対角グラデ）
    img = Image.new("RGB", (W, H), "white")
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        gd.line([(0, y), (W, y)], fill=int(40 * (y / H)))
    blue_layer = Image.new("RGB", (W, H), PALE)
    img = Image.composite(blue_layer, img, grad)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_network(ImageDraw.Draw(overlay))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    # 左上: ブランド
    f_brand = jp_font(SANS_BOLD, 28)
    f_brand_en = jp_font(SANS_REG, 18)
    draw.text((70, 52), "オカピー・パートナーズ", font=f_brand, fill=NAVY)
    draw.text((70, 90), "OKA-pi PARTNERS", font=f_brand_en, fill=(90, 130, 160))

    # 右上: 連載バッジ
    badge_txt = f"連載　第{args.kai}回" if args.kai else "連載"
    f_badge = jp_font(SANS_BOLD, 22)
    bw = draw.textlength(badge_txt, font=f_badge)
    bx2 = W - 70
    bx1 = bx2 - bw - 44
    draw.rounded_rectangle([bx1, 52, bx2, 100], radius=24,
                           fill=NAVY)
    draw.text((bx1 + 22, 62), badge_txt, font=f_badge, fill="white")

    # 連載名（見出し上）
    f_series = jp_font(SANS_BOLD, 24)
    draw.text((70, 156), args.series, font=f_series, fill=NAVY)
    draw.rectangle([70, 194, 70 + 90, 200], fill=GOLD)

    # メインタイトル（Bold）
    n = len(lines)
    if n <= 2:
        size = 54
    elif n == 3:
        size = 44
    else:
        size = 36
    f_h = jp_font(SANS_BOLD, size)
    line_h = int(size * 1.45)
    y0 = 240 if n <= 2 else 224
    for i, line in enumerate(lines):
        draw.text((70, y0 + i * line_h), line, font=f_h, fill=DARK)

    # 下部バー
    bar_h = 76
    draw.rectangle([0, H - bar_h, W, H], fill=NAVY_DEEP)
    f_bar = jp_font(SANS_BOLD, 24)
    f_bar_s = jp_font(SANS_REG, 22)
    draw.text((70, H - bar_h + 24),
              "中小企業診断士　岡 実 ／ 支援機関・業界団体の職員研修",
              font=f_bar, fill="white")
    url = "oka-pi.com"
    uw = draw.textlength(url, font=f_bar_s)
    draw.text((W - 70 - uw, H - bar_h + 26), url, font=f_bar_s,
              fill=(200, 225, 245))

    img.convert("RGB").save(args.out, "PNG")
    print(f"saved: {args.out}  ({n} lines, size {size})")


if __name__ == "__main__":
    main()
