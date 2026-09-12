#!/usr/bin/env python3
"""Post one newly-added article to the appropriate social accounts.

Every platform is isolated: missing credentials or an API error emits a GitHub
Actions warning but never prevents the site itself from being published.
"""
from pathlib import Path
import json, os, re, sys, urllib.error, urllib.parse, urllib.request

ROOT = Path(__file__).resolve().parents[1]

def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("front matter がありません")
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

def truth(value, default=None):
    if value is None:
        return default
    return str(value).lower() in {"1", "true", "yes", "on"}

def warn(platform, message):
    print(f"::warning title={platform}への投稿をスキップ::{message}")

def request_json(url, payload, token=None, form=False, headers=None):
    headers = dict(headers or {})
    if form:
        body = urllib.parse.urlencode(payload).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    else:
        body = json.dumps(payload, ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read() or b"{}")

def safely(platform, fn):
    try:
        fn()
        print(f"{platform}: 投稿しました")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        warn(platform, f"APIエラー {exc.code}: {detail}")
    except Exception as exc:
        warn(platform, str(exc))

def shortened(prefix, description, url, limit):
    suffix = f"\n{url}"
    available = limit - len(prefix) - len(suffix)
    text = description if len(description) <= available else description[:max(0, available - 1)] + "…"
    return prefix + text + suffix

def main():
    article_path = ROOT / os.environ["ARTICLE_FILE"]
    fm = parse_frontmatter(article_path)
    if truth(fm.get("social"), True) is False:
        print(f"{article_path.name}: social: false のため投稿しません")
        return
    site = os.environ.get("SITE_URL", "").rstrip("/")
    if not site:
        warn("SNS", "GitHub Secret の SITE_URL が未設定です")
        return
    slug, title = article_path.stem, fm["title"]
    description = fm.get("description", "")
    tags = fm.get("tags", []) if isinstance(fm.get("tags"), list) else []
    url = f"{site}/articles/{slug}.html"
    articles = json.loads((ROOT / "data/articles.json").read_text(encoding="utf-8"))
    article = next((a for a in articles if a["slug"] == slug), None)
    image_url = f"{site}/{article['thumbnail']}" if article else ""
    haystack = " ".join([title, description, fm.get("category", ""), *tags]).lower()

    threads_token, threads_user = os.environ.get("THREADS_ACCESS_TOKEN"), os.environ.get("THREADS_USER_ID")
    if threads_token and threads_user:
        story = shortened(f"「{title}」で迷うこと、ありませんか？\n", f"今回は、{description} 実際の手順をわかりやすくまとめました。", url, 500)
        def post_threads():
            created = request_json(f"https://graph.threads.net/v1.0/{threads_user}/threads", {"media_type":"TEXT", "text":story, "access_token":threads_token}, form=True)
            request_json(f"https://graph.threads.net/v1.0/{threads_user}/threads_publish", {"creation_id":created["id"], "access_token":threads_token}, form=True)
        safely("Threads", post_threads)
    else:
        warn("Threads", "THREADS_USER_ID または THREADS_ACCESS_TOKEN が未設定です")

    howto_words = ["方法", "手順", "やり方", "使い方", "設定", "解決", "直し方", "作り方", "how-to", "howto"]
    is_howto = truth(fm.get("pinterest"), any(word in haystack for word in howto_words))
    if is_howto:
        pin_token, board = os.environ.get("PINTEREST_ACCESS_TOKEN"), os.environ.get("PINTEREST_BOARD_ID")
        if pin_token and board and image_url:
            payload = {"board_id":board, "title":title[:100], "description":description[:500], "link":url, "alt_text":f"{title}の解説画像", "media_source":{"source_type":"image_url", "url":image_url}}
            safely("Pinterest", lambda: request_json("https://api.pinterest.com/v5/pins", payload, pin_token))
        else:
            warn("Pinterest", "PINTEREST_ACCESS_TOKEN、PINTEREST_BOARD_ID または画像URLがありません")
    else:
        print("Pinterest: How-to記事ではないため対象外です")

    work_words = ["業務", "仕事", "効率", "自動化", "gas", "スプレッドシート", "spreadsheet", "automation"]
    is_work = truth(fm.get("linkedin"), any(word in haystack for word in work_words))
    if is_work:
        li_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
        author = os.environ.get("LINKEDIN_AUTHOR_URN")
        version = os.environ.get("LINKEDIN_VERSION")
        if li_token and author and version:
            payload = {"author":author, "commentary":f"{title}\n\n{description}\n\n{url}", "visibility":"PUBLIC", "distribution":{"feedDistribution":"MAIN_FEED", "targetEntities":[], "thirdPartyDistributionChannels":[]}, "content":{"article":{"source":url, "title":title, "description":description}}, "lifecycleState":"PUBLISHED", "isReshareDisabledByAuthor":False}
            headers = {"LinkedIn-Version":version, "X-Restli-Protocol-Version":"2.0.0"}
            safely("LinkedIn", lambda: request_json("https://api.linkedin.com/rest/posts", payload, li_token, headers=headers))
        else:
            warn("LinkedIn", "LINKEDIN_ACCESS_TOKEN、LINKEDIN_AUTHOR_URN または LINKEDIN_VERSION が未設定です")
    else:
        print("LinkedIn: 仕事・業務効率化記事ではないため対象外です")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        warn("SNS", str(exc))
