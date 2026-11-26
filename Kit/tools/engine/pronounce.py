# -*- coding: utf-8 -*-
"""Bộ phiên âm tự động từ câu hiển thị (sub) -> câu đọc TTS (say).
Đọc từ điển dùng chung tại Kit/assets/pronunciation.json.
"""
import json
import os
import re

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DICT_PATH = os.path.join(KIT_ROOT, "assets", "pronunciation.json")

_NUM_VI = {
    "0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn",
    "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín",
    "10": "mười", "11": "mười một", "12": "mười hai", "13": "mười ba",
    "14": "mười bốn", "15": "mười lăm", "16": "mười sáu",
}


def load_dictionary(custom_path=None):
    path = custom_path or DICT_PATH
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("exact_phrases", {})


def _replace_filenames(text):
    """Đổi tên file kiểu 1.jpg, 2.png -> 'một chấm j p e g', 'hai chấm pê nờ gờ'."""
    def repl(m):
        num = m.group(1)
        ext = m.group(2).lower()
        num_s = _NUM_VI.get(num, num)
        ext_map = {
            "jpg": "j p e g",
            "jpeg": "j p e g",
            "png": "pê nờ gờ",
            "mp4": "mờ pê bốn",
            "wav": "uây",
            "md": "mờ đê",
            "py": "pai",
            "json": "dây sơn",
        }
        return f"{num_s} chấm {ext_map.get(ext, ext)}"

    return re.sub(r"\b(\d+)\.(jpg|jpeg|png|mp4|wav|md|py|json)\b", repl, text, flags=re.IGNORECASE)


def to_say(sub_text, extra_dict=None):
    """Chuyển chuỗi sub thành chuỗi say chuẩn phát âm + trả về danh sách thuật ngữ đã đổi."""
    d = load_dictionary()
    if extra_dict:
        d.update(extra_dict)

    out = _replace_filenames(sub_text)
    applied = []

    # Thay cụm dài trước để tránh cắt nhầm cụm ngắn
    for key in sorted(d.keys(), key=len, reverse=True):
        val = d[key]
        # Với chuỗi chứa ký tự đặc biệt (. / _ -), khớp trực tiếp; ngược lại dùng ranh giới từ
        if re.search(r"[^A-Za-z0-9\s]", key):
            pat = re.compile(re.escape(key))
        else:
            pat = re.compile(r"(?<![A-Za-zÀ-ỹ0-9_])" + re.escape(key) + r"(?![A-Za-zÀ-ỹ0-9_])")
        if pat.search(out):
            out = pat.sub(val, out)
            applied.append((key, val))

    # Thay các ký hiệu toán/lệnh nếu còn sót trong lời đọc
    out = out.replace("→", " sang ")
    out = out.replace("->", " sang ")
    out = out.replace("≤", " nhỏ hơn hoặc bằng ")
    out = out.replace("≥", " lớn hơn hoặc bằng ")
    out = out.replace("±", " cộng trừ ")
    out = re.sub(r"\s{2,}", " ", out).strip()
    return out, applied
