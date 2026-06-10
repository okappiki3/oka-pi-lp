#!/usr/bin/env python3
"""oka-pi.com OGP画像ジェネレーター (1200x630)
使い方:
  python3 gen_ogp.py                          # 写真なし（プレースホルダー）
  python3 gen_ogp.py --photo images/OKA2024.png --out images/ogp.png
"""
import argparse, math, random
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1200, 630
NAVY = (10, 88, 132)        # #0a5884 ブランドカラー
DARK = (16, 42, 67)         # 見出し用ダークネイビー
LIGHT_BLUE = (173, 203, 227)
PALE = (236, 244, 250)

SANS_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
SANS_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SANS_MED = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"


def jp_font(path, size):
    """ttcからJPフェイスを探して返す"""
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
    """ヒーローセクション風のノードネットワーク装飾"""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", default=None, help="プロフィール写真のパス")
    ap.add_argument("--out", default="ogp.png")
    args = ap.parse_args()

    img = Image.new("RGB", (W, H), "white")

    # 背景: 白→淡い水色の対角グラデーション
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        for_step = int(40 * (y / H))
        gd.line([(0, y), (W, y)], fill=for_step)
    blue_layer = Image.new("RGB", (W, H), PALE)
    img = Image.composite(blue_layer, img, grad)

    # ネットワーク装飾（透過レイヤー）
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_network(ImageDraw.Draw(overlay))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    # 左上: ブランド名
    f_brand = jp_font(SANS_BOLD, 30)
    f_brand_en = jp_font(SANS_MED, 19)
    draw.text((70, 52), "オカピー・パートナーズ", font=f_brand, fill=NAVY)
    draw.text((70, 94), "OKA-pi PARTNERS", font=f_brand_en, fill=(90, 130, 160))

    # 右上: 拠点バッジ（角丸ピル）
    f_badge = jp_font(SANS_MED, 22)
    badge_txt = "滋賀・関西拠点 ／ 全国オンライン対応"
    bw = draw.textlength(badge_txt, font=f_badge)
    bx2 = W - 70
    bx1 = bx2 - bw - 44
    draw.rounded_rectangle([bx1, 52, bx2, 100], radius=24,
                           outline=NAVY, width=2, fill=(255, 255, 255, 230))
    draw.text((bx1 + 22, 62), badge_txt, font=f_badge, fill=NAVY)

    # 中央見出し（2行・Black）
    f_h = jp_font(SANS_BLACK, 62)
    line1 = "ものづくり企業の強みを、"
    line2 = "価値と次の一手につなげる。"
    y0 = 215
    draw.text((70, y0), line1, font=f_h, fill=DARK)
    draw.text((70, y0 + 90), line2, font=f_h, fill=DARK)

    # アクセントライン
    draw.rectangle([70, y0 + 196, 70 + 160, y0 + 204], fill=NAVY)

    # サブコピー
    f_sub = jp_font(SANS_BOLD, 31)
    draw.text((70, y0 + 232),
              "製造業専門コンサルタント｜中小企業診断士",
              font=f_sub, fill=NAVY)

    # 右側: 顔写真（円形） or プレースホルダー
    cx, cy, cr = 1052, 355, 112
    if args.photo:
        photo = Image.open(args.photo).convert("RGB")
        photo = ImageOps.fit(photo, (cr * 2, cr * 2), centering=(0.5, 0.32))
        mask = Image.new("L", (cr * 2, cr * 2), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, cr * 2, cr * 2], fill=255)
        img.paste(photo, (cx - cr, cy - cr), mask)
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                     outline=NAVY, width=6)
    else:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                     fill=PALE, outline=NAVY, width=6)
        f_ph = jp_font(SANS_MED, 26)
        t = "顔写真"
        tw = draw.textlength(t, font=f_ph)
        draw.text((cx - tw / 2, cy - 18), t, font=f_ph, fill=NAVY)

    # 下部バー（ブランドカラー）
    bar_h = 86
    draw.rectangle([0, H - bar_h, W, H], fill=NAVY)
    f_bar = jp_font(SANS_BOLD, 27)
    f_bar_s = jp_font(SANS_MED, 25)
    draw.text((70, H - bar_h + 26),
              "強みの言語化 ・ 価格転嫁 ・ 販路開拓 ・ 生成AI活用",
              font=f_bar, fill="white")
    url = "oka-pi.com"
    uw = draw.textlength(url, font=f_bar_s)
    draw.text((W - 70 - uw, H - bar_h + 27), url, font=f_bar_s,
              fill=(200, 225, 245))

    img.convert("RGB").save(args.out, "PNG")
    print(f"saved: {args.out}")


if __name__ == "__main__":
    main()
