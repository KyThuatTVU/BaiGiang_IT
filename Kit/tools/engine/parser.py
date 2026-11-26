# -*- coding: utf-8 -*-
"""Parser thuần Python (0% AI) đọc content.md + notes.md + img/ thành cấu trúc bài giảng."""
import os
import re
from engine.pronounce import to_say

TEMPLATE_ALIASES = {
    "intro": "intro",
    "mo_dau": "intro",
    "intro_kinetic": "intro",
    "va_cham": "va_cham",
    "collision": "va_cham",
    "dem_so": "dem_so",
    "counter": "dem_so",
    "counter_stats": "dem_so",
    "so_sanh": "so_sanh",
    "before_after": "so_sanh",
    "code": "code",
    "code_spotlight": "code",
    "quy_trinh": "quy_trinh",
    "steps": "quy_trinh",
    "steps_pipeline": "quy_trinh",
    "anh_dong": "anh_dong",
    "photo_motion": "anh_dong",
    "outro": "outro",
    "ket_bai": "outro",
    "outro_brand": "outro",
}


def _strip_accents_key(s):
    rep = {
        "à": "a", "á": "a", "ả": "a", "ã": "a", "ạ": "a",
        "ă": "a", "ằ": "a", "ắ": "a", "ẳ": "a", "ẵ": "a", "ặ": "a",
        "â": "a", "ầ": "a", "ấ": "a", "ẩ": "a", "ẫ": "a", "ậ": "a",
        "đ": "d",
        "è": "e", "é": "e", "ẻ": "e", "ẽ": "e", "ẹ": "e",
        "ê": "e", "ề": "e", "ế": "e", "ể": "e", "ễ": "e", "ệ": "e",
        "ì": "i", "í": "i", "ỉ": "i", "ĩ": "i", "ị": "i",
        "ò": "o", "ó": "o", "ỏ": "o", "õ": "o", "ọ": "o",
        "ô": "o", "ồ": "o", "ố": "o", "ổ": "o", "ỗ": "o", "ộ": "o",
        "ơ": "o", "ờ": "o", "ớ": "o", "ở": "o", "ỡ": "o", "ợ": "o",
        "ù": "u", "ú": "u", "ủ": "u", "ũ": "u", "ụ": "u",
        "ư": "u", "ừ": "u", "ứ": "u", "ử": "u", "ữ": "u", "ự": "u",
        "ỳ": "y", "ý": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y",
    }
    out = "".join(rep.get(c, c) for c in s.lower().strip())
    return re.sub(r"\s+", "_", out)


def parse_notes(project_dir, standard_cfg):
    """Đọc notes.md hoặc note.md của bài (nếu có)."""
    info = {
        "greeting_enabled": standard_cfg.get("greeting", {}).get("enabled_by_default", True),
        "target_minutes": None,
        "voice": standard_cfg.get("audio", {}).get("default_voice", "vieneu"),
        "theme": standard_cfg.get("default_theme", "dark_cyan"),
        "raw": "",
    }
    for fname in ("notes.md", "note.md"):
        p = os.path.join(project_dir, fname)
        if os.path.exists(p):
            txt = open(p, "r", encoding="utf-8").read()
            info["raw"] = txt.strip()
            low = txt.lower()
            for kw in standard_cfg.get("greeting", {}).get("disable_keywords", []):
                if kw in low:
                    info["greeting_enabled"] = False
            m_min = re.search(r"(\d+(?:\.\d+)?)\s*(?:phút|phut|min)", low)
            if m_min:
                info["target_minutes"] = float(m_min.group(1))
            if "edge" in low and ("giọng" in low or "giong" in low or "voice" in low):
                info["voice"] = "edge"
            m_th = re.search(r"theme\s*:\s*([a-z0-9_]+)", low)
            if m_th:
                info["theme"] = m_th.group(1)
            break
    return info


def list_img_files(project_dir):
    img_dir = os.path.join(project_dir, "img")
    if not os.path.isdir(img_dir):
        return []
    exts = (".jpg", ".jpeg", ".png", ".webp")
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(exts) and not f.startswith("_")]
    # Natural sort (1.jpg, 2.jpg, 10.jpg)
    def nkey(s):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]
    return sorted(files, key=nkey)


def _auto_choose_template(sc, idx, total):
    if idx == 0:
        return "intro"
    if idx == total - 1 and total > 2:
        return "outro"
    if sc["code"]:
        return "code"
    if sc["stats"]:
        return "dem_so"
    if sc["before"] or sc["after"]:
        return "so_sanh"
    if sc["left"] or sc["right"]:
        return "va_cham"
    if sc["steps"]:
        return "quy_trinh"
    if sc["images"]:
        return "anh_dong"
    return "quy_trinh"


def parse_content_md(project_dir, standard_cfg):
    """Đọc content.md và đối chiếu với thư mục img/."""
    md_path = os.path.join(project_dir, "content.md")
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Không tìm thấy {md_path}")

    lines = open(md_path, "r", encoding="utf-8").read().splitlines()
    title = os.path.basename(project_dir)
    subtitle = ""
    scenes = []
    cur = None
    in_code = False
    code_lang = ""
    code_buf = []

    def finish_scene(sc):
        if sc is not None:
            scenes.append(sc)

    for raw in lines:
        line = raw.rstrip()

        # Code block fence
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_lang = line.strip()[3:].strip() or "text"
                code_buf = []
            else:
                in_code = False
                if cur is not None:
                    cur["code"] = "\n".join(code_buf)
                    cur["code_lang"] = code_lang
            continue

        if in_code:
            code_buf.append(line)
            continue

        if not line.strip():
            continue

        # H1 = main title
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            continue

        # Subtitle right under H1 (optional)
        if cur is None and line.startswith("> "):
            subtitle = line[2:].strip()
            continue

        # H2 = new scene
        if line.startswith("## "):
            finish_scene(cur)
            header = line[3:].strip()
            tpl_raw = None
            m_tag = re.search(r"\[\s*(?:hieu_ung|hiệu_ứng|template)\s*:\s*([^\]]+)\]", header, re.IGNORECASE)
            if m_tag:
                tpl_raw = _strip_accents_key(m_tag.group(1))
                header = header[:m_tag.start()].strip()

            # Remove leading "Cảnh X:" if present to get clean title & tag
            sc_num = len(scenes) + 1
            clean_title = re.sub(r"^(?:Cảnh|Canh|Phần|Phan)\s*\d+\s*[:\.\-·]\s*", "", header, flags=re.IGNORECASE).strip()
            cur = {
                "id": f"s{sc_num:02d}",
                "index": sc_num,
                "tag": f"PHẦN {sc_num:02d} · {clean_title.upper()}",
                "title": clean_title,
                "subtitle": "",
                "template": TEMPLATE_ALIASES.get(tpl_raw, None) if tpl_raw else None,
                "left": None,
                "right": None,
                "warning": "",
                "before": [],
                "after": [],
                "stats": [],
                "steps": [],
                "images": [],
                "code": "",
                "code_lang": "",
                "cues": [],
            }
            continue

        if cur is None:
            continue

        # Spoken cue line: "> ..."
        if line.lstrip().startswith("> "):
            sub = line.lstrip()[2:].strip()
            if sub:
                say, applied = to_say(sub)
                cid = f"{cur['id']}_c{len(cur['cues']) + 1:02d}"
                cur["cues"].append({
                    "id": cid,
                    "sub": sub,
                    "say": say,
                    "pron_applied": applied,
                })
            continue

        # Markdown image: ![caption](1.jpg)
        m_img = re.match(r"^\s*!\[([^\]]*)\]\(([^)]+)\)", line)
        if m_img:
            cap = m_img.group(1).strip()
            fname = os.path.basename(m_img.group(2).strip())
            cur["images"].append({"file": fname, "caption": cap})
            continue

        # Bullet items: "- ..."
        if line.lstrip().startswith("- "):
            item = line.lstrip()[2:].strip()

            # Key: value bullets
            m_kv = re.match(r"^([^:]+):\s*(.+)$", item)
            if m_kv:
                k = _strip_accents_key(m_kv.group(1))
                v = m_kv.group(2).strip()
                if k in ("mo_ta", "phu_de", "subtitle"):
                    cur["subtitle"] = v
                    continue
                if k in ("trai", "left"):
                    parts = [p.strip() for p in v.split("|")]
                    cur["left"] = {"name": parts[0], "detail": parts[1] if len(parts) > 1 else ""}
                    continue
                if k in ("phai", "right"):
                    parts = [p.strip() for p in v.split("|")]
                    cur["right"] = {"name": parts[0], "detail": parts[1] if len(parts) > 1 else ""}
                    continue
                if k in ("canh_bao", "ket_qua", "warning"):
                    cur["warning"] = v
                    continue
                if k in ("truoc", "cu", "before"):
                    cur["before"].append(v)
                    continue
                if k in ("sau", "moi", "after"):
                    cur["after"].append(v)
                    continue
                if k in ("anh", "hinh", "img", "image"):
                    # Support: "- ảnh: 1.jpg | Chú thích" OR "- ảnh: 1.jpg, 2.jpg"
                    if "|" in v:
                        parts = [p.strip() for p in v.split("|", 1)]
                        cur["images"].append({"file": os.path.basename(parts[0]), "caption": parts[1]})
                    else:
                        for f in v.split(","):
                            fn = os.path.basename(f.strip())
                            if fn:
                                cur["images"].append({"file": fn, "caption": ""})
                    continue

            # Stat item: "- 1247 | Nhãn" or "- 0đ | Chi phí API" or "- 100% | Offline"
            if "|" in item:
                left_p, right_p = [p.strip() for p in item.split("|", 1)]
                m_num = re.match(r"^([+-]?\d+(?:[.,]\d+)?)\s*([^\d]*)$", left_p)
                if m_num and cur["template"] in (None, "dem_so") and re.match(r"^[+-]?\d", left_p):
                    num_str = m_num.group(1).replace(",", "")
                    suffix = m_num.group(2).strip()
                    try:
                        val = float(num_str) if "." in num_str else int(num_str)
                        cur["stats"].append({"value": val, "suffix": suffix, "label": right_p})
                        continue
                    except ValueError:
                        pass
                cur["steps"].append({"title": left_p, "desc": right_p})
                continue

            # Plain bullet -> step / takeaway
            cur["steps"].append({"title": item, "desc": ""})
            continue

    finish_scene(cur)

    # Auto-attach s01_xxx.jpg naming convention if scene has no explicit images
    all_imgs = list_img_files(project_dir)
    for sc in scenes:
        if not sc["images"]:
            prefix = sc["id"] + "_"
            matched = [f for f in all_imgs if f.lower().startswith(prefix)]
            for f in matched:
                sc["images"].append({"file": f, "caption": ""})

    # Auto-assign templates if omitted
    total = len(scenes)
    for idx, sc in enumerate(scenes):
        if not sc["template"]:
            sc["template"] = _auto_choose_template(sc, idx, total)

    # Validate images
    img_dir = os.path.join(project_dir, "img")
    used_imgs = set()
    missing_imgs = []
    for sc in scenes:
        for im in sc["images"]:
            fn = im["file"]
            used_imgs.add(fn)
            if not os.path.exists(os.path.join(img_dir, fn)):
                missing_imgs.append((sc["id"], fn))
    unused_imgs = [f for f in all_imgs if f not in used_imgs]

    notes = parse_notes(project_dir, standard_cfg)

    return {
        "title": title,
        "subtitle": subtitle,
        "project_dir": project_dir,
        "notes": notes,
        "scenes": scenes,
        "img_stats": {
            "total_in_dir": len(all_imgs),
            "used": sorted(used_imgs),
            "missing": missing_imgs,
            "unused": unused_imgs,
        },
    }
