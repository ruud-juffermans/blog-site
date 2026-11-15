import json, re, shutil, sys
from pathlib import Path

src = Path(sys.argv[1])   # portfolio client dir
dst = Path(sys.argv[2])   # blog-site dir

CATS = {"data-engineering": "Data Engineering", "ai": "Artificial Intelligence"}
PROJECT_IMG = {
    "open-data-warehouse": "nl-vehicle-warehouse-1-architectuur.svg",
    "ov-streaming-pipeline": "dashboard.png",
    "strafrecht-rag": "ask.png",
    "digital-twin": "digital-twin-1-architectuur.svg",
}
FIX = {"een-digital-twin-die-alleen-zegt-wat-hij-kan-bewijzen":
       "een-digitale-tweeling-die-alleen-zegt-wat-hij-kan-bewijzen"}

def parse(p):
    t = p.read_text()
    _, fm, body = t.split("---\n", 2)
    meta = {}
    for line in fm.splitlines():
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if m and m.group(2):
            v = m.group(2).strip()
            try: v = json.loads(v)
            except Exception: pass
            meta[m.group(1)] = v
    return meta, body.lstrip("\n")

def links(body):
    def blog(m):
        s = FIX.get(m.group(1), m.group(1))
        return f"](/{s}/"
    body = re.sub(r'\]\((?:/en)?/blog/([a-z0-9-]+)/?', blog, body)
    body = re.sub(r'\]\((?:/en)?/projects/([a-z0-9-]+)/?', r'](/projects/\1/', body)
    body = re.sub(r'\]\((?:/en)?/projects/?\)', '](/projects/)', body)
    body = re.sub(r'\]\((?:/en)?/contact/?\)', '](/about/)', body)
    body = re.sub(r'\]\((?:/en)?/blog/?\)', '](/)', body)
    return body

def captions(body):
    return re.sub(r'^!\[([^\]]*)\]\(([^)\s]+)\s+"([^"]*)"\)\s*$', r'![\1](\2)\n_\3_', body, flags=re.M)

def raw(body):
    body = captions(body)
    return "{% raw %}\n" + body.rstrip() + "\n{% endraw %}\n" if re.search(r'\{\{|\{%', body) else body

def y(s): return json.dumps(s, ensure_ascii=False)
def tag(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

for d in ("_posts", "_projects"):
    (dst / d).mkdir(exist_ok=True)
    for f in (dst / d).glob("*.md"): f.unlink()

for p in sorted((src / "content/blog/en").glob("*.mdx")):
    m, body = parse(p)
    body = links(body)
    fm = ["---", f"title: {y(m['title'])}", f"date: {m['date']} 09:00:00 +0200",
          f"description: {y(m['excerpt'])}",
          f"categories: [{y(CATS[m['topic']])}]",
          "tags: [" + ", ".join(tag(t) for t in m["tags"]) + "]"]
    img = re.search(r'!\[([^\]]*)\]\(([^)\s]+)', body)
    if img:
        fm += ["image:", f"  path: {img.group(2)}", f"  alt: {y(img.group(1))}"]
    elif m.get("project") in PROJECT_IMG:
        fm += ["image:", f"  path: /images/projects/{m['project']}/{PROJECT_IMG[m['project']]}",
               f"  alt: {y('From the ' + m['project'] + ' project')}"]
    if re.search(r'\{\{|\{%', body):
        fm.append('excerpt_separator: "<!--more-->"')
    fm.append("---\n")
    (dst / "_posts" / f"{m['date']}-{p.stem}.md").write_text("\n".join(fm) + "\n" + raw(body))

for i, p in enumerate(sorted((src / "content/projects/en").glob("*.mdx"))):
    m, body = parse(p)
    body = links(body)
    fm = ["---", f"title: {y(m['title'])}", f"description: {y(m['summary'])}",
          f"repo: {m['repo']}", "stack: [" + ", ".join(y(t) for t in m["tags"]) + "]",
          f"image: /images/projects/{p.stem}/{PROJECT_IMG[p.stem]}", "---\n"]
    head = f"[<i class=\"fab fa-github fa-fw\"></i> Source on GitHub]({m['repo']})\n\n"
    (dst / "_projects" / f"{p.stem}.md").write_text("\n".join(fm) + "\n" + raw(head + body))

for sub in ("blog", "projects"):
    shutil.copytree(src / "public/images" / sub, dst / "images" / sub, dirs_exist_ok=True)

a = json.loads((src / "messages/en.json").read_text())["about"]
0 and print(json.dumps({k: a[k] for k in ("intro1", "intro2", "intro3", "pullQuote", "experience")}, indent=1, ensure_ascii=False))
