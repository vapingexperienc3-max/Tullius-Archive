import os
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
import unicodedata

ROOT = "."  # Archive 루트
OLD_REPO = "Tullius-ferry"

def nfc(path: str) -> str:
    return unicodedata.normalize("NFC", path)

# Archive 안의 모든 html 파일 수집
html_files = []
for root, _, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(".html"):
            html_files.append(os.path.join(root, f))

# 실제 파일 경로 세트 (매칭용)
real_files = {
    nfc(os.path.relpath(f, ROOT))
    for f in html_files
}

def find_real_path(decoded_path):
    decoded_path = nfc(decoded_path.lstrip("/"))
    for real in real_files:
        if real.endswith(decoded_path):
            return real
    return None

for html_path in html_files:
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    changed = False
    html_dir = os.path.dirname(os.path.relpath(html_path, ROOT))

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if OLD_REPO not in href:
            continue

        parsed = urlparse(href)
        decoded = unquote(parsed.path)

        # Tullius-ferry 이후 경로만 사용
        if OLD_REPO in decoded:
            decoded = decoded.split(OLD_REPO, 1)[1]

        real = find_real_path(decoded)
        if not real:
            continue  # 실제 파일 없으면 건너뜀

        rel = os.path.relpath(real, html_dir if html_dir else ".")
        a["href"] = rel.replace("\\", "/")
        changed = True

    if changed:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"✔ fixed: {html_path}")