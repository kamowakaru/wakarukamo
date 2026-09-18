#!/usr/bin/env python3
"""Create copy-and-paste X and Threads drafts for every published article."""
from pathlib import Path
import json
import os
import re
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content/articles"
OUT = ROOT / "social-drafts"


def parse_frontmatter(path):
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path.name}: front matter がありません")
    data, current = {}, None
    for raw in parts[1].strip().splitlines():
        line = raw.rstrip()
        if re.match(r"^\s+-\s+", line) and current:
            data.setdefault(current, []).append(
                re.sub(r"^\s+-\s+", "", line).strip().strip("\"'")
            )
        elif ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            data[current] = value.strip().strip("\"'") if value.strip() else []
    return data


def truth(value, default=True):
    if value is None:
        return default
    return str(value).lower() in {"1", "true", "yes", "on"}


def tagged_url(url, source):
    query = urllib.parse.urlencode(
        {"utm_source": source, "utm_medium": "social", "utm_campaign": "article_share"}
    )
    return f"{url}?{query}"


def fit_post(prefix, description, url, hashtags="", limit=280):
    suffix = f"\n\n{url}" + (f"\n{hashtags}" if hashtags else "")
    room = limit - len(prefix) - len(suffix)
    body = description if len(description) <= room else description[: max(0, room - 1)] + "…"
    return prefix + body + suffix


def main():
    site = os.environ.get("SITE_URL", "").rstrip("/") or "https://kamowakaru.github.io/wakarukamo"
    tag_names = {
        item["slug"]: item["name"]
        for item in json.loads((ROOT / "data/tags.json").read_text(encoding="utf-8"))
    }
    OUT.mkdir(exist_ok=True)
    active = set()

    for path in sorted(CONTENT.glob("*.md")):
        fm, slug = parse_frontmatter(path), path.stem
        if truth(fm.get("draft"), False) or not truth(fm.get("social"), True):
            continue

        filename = f"{slug}.txt"
        active.add(filename)
        title, description = fm["title"], fm["description"]
        tags = fm.get("tags", []) if isinstance(fm.get("tags"), list) else []
        hashtags = " ".join(
            "#" + re.sub(r"\s+", "", tag_names.get(tag, tag)) for tag in tags[:3]
        )
        base_url = f"{site}/articles/{slug}.html"
        x_main = fit_post(f"【{title}】\n", description, tagged_url(base_url, "x"), hashtags)
        x_question = fit_post(
            f"「{title}」で困っていませんか？\n",
            description,
            tagged_url(base_url, "x"),
            hashtags,
        )
        threads = (
            f"「{title}」で迷うこと、ありませんか？\n\n"
            f"今回は、{description}\n"
            "実際の手順やポイントを初心者向けにまとめました🐤\n\n"
            f"{tagged_url(base_url, 'threads')}\n\n{hashtags}"
        )

        sections = [
            "ワカルカモ｜記事公開時のSNS投稿原稿",
            "",
            f"記事タイトル：{title}",
            f"記事URL：{base_url}",
            "",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            "X案1：要点型",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            x_main,
            "",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            "X案2：問いかけ型",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            x_question,
            "",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            "Threads案：体験に寄り添う型",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            threads,
            "",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            "投稿前チェック",
            "＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝",
            "□ 記事ページを開いて誤字・リンクを確認",
            "□ サムネイルの表示を確認",
            "□ Xへ投稿",
            "□ Threadsへ投稿",
            "",
            "※URLにはSNS別の流入をGA4で確認できるUTMパラメータが付いています。",
            "※文章は記事内容や実体験に合わせて、必要に応じて少し整えてください。",
            "",
        ]
        (OUT / filename).write_text("\n".join(sections), encoding="utf-8-sig")

    for stale in OUT.iterdir():
        if stale.is_file() and stale.name not in active and stale.name != "README.md":
            stale.unlink()
    print(f"Generated {len(active)} social draft files")


if __name__ == "__main__":
    main()
