#!/usr/bin/env python3
"""Generate silent 9:16 MP4 drafts for the most-viewed articles."""
from pathlib import Path
import csv, json, os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "social-videos"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def font(path, size): return ImageFont.truetype(path, size)
def fit_cover(img, size):
    scale = max(size[0] / img.width, size[1] / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)))
    left, top = (resized.width-size[0])//2, (resized.height-size[1])//2
    return resized.crop((left, top, left+size[0], top+size[1]))
def wrapped(text, width=16): return "\n".join(textwrap.wrap(text, width=width, break_long_words=True))

def slide(article, number, total, text, output):
    source = Image.open(ROOT / article["thumbnail"]).convert("RGB")
    bg = fit_cover(source, (1080, 1920)).filter(ImageFilter.GaussianBlur(24))
    bg = ImageEnhance.Brightness(bg).enhance(.42)
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle((70, 90, 1010, 1830), radius=48, fill=(255,255,255,232))
    draw.text((120, 145), "ワカルカモ", font=font(BOLD, 48), fill="#087be8")
    draw.text((890, 155), f"{number}/{total}", font=font(FONT, 32), fill="#61758a")
    if number == 1:
        thumb = fit_cover(source, (840, 525)); bg.paste(thumb, (120, 320))
        draw.multiline_text((120, 930), wrapped(text, 14), font=font(BOLD, 68), fill="#101820", spacing=22)
    else:
        draw.multiline_text((120, 390), wrapped(text, 14), font=font(BOLD, 68), fill="#101820", spacing=26)
    draw.text((120, 1695), "続きはブログで ▶", font=font(BOLD, 46), fill="#087be8")
    bg.save(output)

def main():
    minimum = int(os.environ.get("MIN_POPULAR_VIEWS", "100"))
    articles = json.loads((ROOT/"data/articles.json").read_text(encoding="utf-8"))
    amap = {f"/articles/{a['slug']}.html":a for a in articles}
    ranked = []
    with (ROOT/"data/analytics-pageviews.csv").open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["path"] in amap and int(row.get("views") or 0) >= minimum:
                ranked.append((int(row["views"]), amap[row["path"]]))
    if not ranked:
        print(f"PV {minimum} 以上の記事がないため動画は作りません")
        return
    OUT.mkdir(exist_ok=True)
    for views, article in sorted(ranked, key=lambda item: (item[0], item[1]["slug"]), reverse=True)[:3]:
        work = OUT / article["slug"]; work.mkdir(exist_ok=True)
        texts = [article["title"], article["description"], "詳しい手順とポイントを\nワカルカモでチェック！"]
        frames = []
        for i, label in enumerate(texts, 1):
            frame = work / f"slide-{i}.png"; slide(article, i, len(texts), label, frame); frames.append(frame)
        inputs = sum((["-loop", "1", "-t", "5", "-i", str(frame)] for frame in frames), [])
        filters = ";".join(f"[{i}:v]fps=30,format=yuv420p[v{i}]" for i in range(3)) + ";[v0][v1][v2]concat=n=3:v=1:a=0[v]"
        output = OUT / f"{article['slug']}.mp4"
        subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", filters, "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)], check=True)
        print(f"{output.name}: {views} PVをもとに生成しました")

if __name__ == "__main__": main()
