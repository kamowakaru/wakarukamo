#!/usr/bin/env python3
"""Create copy-and-paste social post drafts for every article."""
from pathlib import Path
import json, os, re, urllib.parse

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
            data.setdefault(current, []).append(re.sub(r"^\s+-\s+", "", line).strip().strip("\"'"))
        elif ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            data[current] = value.strip().strip("\"'") if value.strip() else []
    return data

def truth(value, default):
    if value is None: return default
    return str(value).lower() in {"1", "true", "yes", "on"}

def tagged_url(url, source):
    query = urllib.parse.urlencode({"utm_source":source, "utm_medium":"social", "utm_campaign":"article_share"})
    return f"{url}?{query}"

def fit_post(prefix, description, url, hashtags="", limit=280):
    suffix = f"\n\n{url}" + (f"\n{hashtags}" if hashtags else "")
    room = limit - len(prefix) - len(suffix)
    body = description if len(description) <= room else description[:max(0, room-1)] + "…"
    return prefix + body + suffix

def main():
    site = os.environ.get("SITE_URL", "").rstrip("/") or "https://＜公開サイトURL＞"
    articles = {a["slug"]:a for a in json.loads((ROOT/"data/articles.json").read_text(encoding="utf-8"))}
    tag_names = {t["slug"]:t["name"] for t in json.loads((ROOT/"data/tags.json").read_text(encoding="utf-8"))}
    OUT.mkdir(exist_ok=True)
    active = set()
    for path in sorted(CONTENT.glob("*.md")):
        fm, slug = parse_frontmatter(path), path.stem
        active.add(f"{slug}.md")
        title, description = fm["title"], fm["description"]
        tags = fm.get("tags", []) if isinstance(fm.get("tags"), list) else []
        hashtags = " ".join("#" + re.sub(r"\s+", "", tag_names.get(t, t)) for t in tags[:3])
        base_url = f"{site}/articles/{slug}.html"
        haystack = " ".join([title, description, fm.get("category", ""), *tags]).lower()
        is_howto = truth(fm.get("pinterest"), any(w in haystack for w in ["方法","手順","やり方","使い方","設定","解決","直し方","作り方","how-to","howto"]))
        is_work = truth(fm.get("linkedin"), any(w in haystack for w in ["業務","仕事","効率","自動化","gas","スプレッドシート","spreadsheet","automation"]))
        x_url = tagged_url(base_url, "x")
        x_main = fit_post(f"【{title}】\n", description, x_url, hashtags)
        x_question = fit_post(f"「{title}」で困っていませんか？\n", description, x_url, hashtags)
        threads = f"「{title}」で迷うこと、ありませんか？\n\n今回は、{description}\n実際の手順やポイントを初心者向けにまとめました🐤\n\n{tagged_url(base_url, 'threads')}\n\n{hashtags}"
        sections = [f"# {title}｜SNS投稿メモ", "", "> 自動生成ファイルです。必要に応じて文章を整えてから投稿してください。", "", f"- 記事URL: {base_url}", f"- 使用画像: {articles.get(slug, {}).get('thumbnail', '未設定')}", "", "## X案1：要点型", "", "```text", x_main, "```", "", "## X案2：問いかけ型", "", "```text", x_question, "```", "", "## Threads：体験に寄り添う型", "", "```text", threads, "```"]
        if is_howto:
            pin = f"{description}\n\n初心者向けに手順とポイントを分かりやすく解説します。"
            sections += ["", "## Pinterest（How-to記事対象）", "", f"**Pinタイトル:** {title}", "", "**説明文:**", "", "```text", pin, "```", "", f"**リンク:** {tagged_url(base_url, 'pinterest')}"]
        else:
            sections += ["", "## Pinterest", "", "対象外：How-to記事と判定されませんでした。"]
        if is_work:
            linkedin = f"{title}\n\n{description}\n\n業務で活用するときのポイントを、初心者向けに整理しました。\n\n{tagged_url(base_url, 'linkedin')}\n\n{hashtags}"
            sections += ["", "## LinkedIn（仕事・業務効率化記事対象）", "", "```text", linkedin, "```"]
        else:
            sections += ["", "## LinkedIn", "", "対象外：仕事・業務効率化記事と判定されませんでした。"]
        sections += ["", "## 投稿チェック", "", "- [ ] 記事ページを開いて誤字・リンクを確認", "- [ ] サムネイルの表示を確認", "- [ ] Xへ投稿", "- [ ] Threadsへ投稿", "- [ ] 対象ならPinterestへ投稿", "- [ ] 対象ならLinkedInへ投稿", ""]
        (OUT/f"{slug}.md").write_text("\n".join(sections), encoding="utf-8")
    for stale in OUT.glob("*.md"):
        if stale.name not in active and stale.name != "README.md": stale.unlink()
    print(f"Generated {len(active)} social draft files")

if __name__ == "__main__": main()
