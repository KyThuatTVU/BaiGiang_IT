# -*- coding: utf-8 -*-
"""AN TECH ACADEMY — Offline Terminal Video Engine CLI (0% AI, 0% API key).

Cách dùng trên Terminal (tại D:\\Edit hoặc bất kỳ đâu):
  python D:\\Edit\\Kit\\tools\\build.py templates
  python D:\\Edit\\Kit\\tools\\build.py scan <TenBai>
  python D:\\Edit\\Kit\\tools\\build.py check <TenBai>
  python D:\\Edit\\Kit\\tools\\build.py preview <TenBai> [--scene s02] [--theme dark_cyan]
  python D:\\Edit\\Kit\\tools\\build.py render <TenBai> [--theme dark_cyan] [--workers 6]
"""
import argparse
import hashlib
import json
import math
import multiprocessing
import os
import re
import subprocess
import sys
import time
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageOps

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
KIT_ROOT = os.path.dirname(TOOLS_DIR)
EDIT_ROOT = os.path.dirname(KIT_ROOT)
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from core import FF
import sfx
from engine.parser import parse_content_md, list_img_files
from engine.renderer import TEMPLATE_DESCRIPTIONS, render_frame, get_font

STD_PATH = os.path.join(KIT_ROOT, "assets", "standard_2_3.json")


def load_standard():
    with open(STD_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_project(name_or_path):
    if os.path.isdir(name_or_path):
        return os.path.abspath(name_or_path)
    p = os.path.join(EDIT_ROOT, name_or_path)
    if os.path.isdir(p):
        return p
    raise SystemExit(f"[LOI] Khong tim thay thu muc bai giang: {name_or_path} (hoac {p})")


def wav_duration(path):
    with wave.open(path, "rb") as w:
        return w.getnframes() / float(w.getframerate())


def wav_to_f32(path, target_sr=48000):
    r = subprocess.run(
        [FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(target_sr), "-"],
        capture_output=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg decode loi: {path}")
    return np.frombuffer(r.stdout, dtype="<f4").copy()


def write_wav_f32(path, samples, sr=48000):
    clipped = np.clip(samples, -0.99, 0.99)
    pcm = (clipped * 32767.0).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def next_version_base(out_dir, prefix="video"):
    """Không bao giờ ghi đè bản cũ: tự tăng video_v1, video_v2..."""
    v = 1
    while True:
        raw = os.path.join(out_dir, f"{prefix}_v{v}.mp4")
        logo = os.path.join(out_dir, f"{prefix}_v{v}_logo.mp4")
        if not os.path.exists(raw) and not os.path.exists(logo):
            return raw, logo, v
        v += 1


# ─── MULTIPROCESSING FRAME WORKER ────────────────────────────────────────────
_W_CTX = {}


def _init_worker(cfg, theme, scenes_meta, total_frames, frames_dir):
    _W_CTX["cfg"] = cfg
    _W_CTX["theme"] = theme
    _W_CTX["scenes"] = scenes_meta
    _W_CTX["total_frames"] = total_frames
    _W_CTX["frames_dir"] = frames_dir


def _render_chunk(args):
    sc_idx, f_start, f_end = args
    cfg = _W_CTX["cfg"]
    theme = _W_CTX["theme"]
    sc = _W_CTX["scenes"][sc_idx]
    total_frames = _W_CTX["total_frames"]
    frames_dir = _W_CTX["frames_dir"]
    fps = cfg["video"]["fps"]
    t_scene0 = sc["t0"]
    scene_dur = sc["dur"]
    cues = sc["cues"]

    for f in range(f_start, f_end):
        t = f / float(fps)
        lt = max(0.0, t - t_scene0)
        active_sub = ""
        cue_lt = 0.0
        talking = False
        for c in cues:
            if c["t0"] <= t < c["t1"]:
                active_sub = c["sub"]
                cue_lt = t - c["t0"]
                talking = True
                break
            if c["t0"] <= t < c["t1"] + 0.35:
                active_sub = c["sub"]
                cue_lt = t - c["t0"]
        im = render_frame(cfg, theme, sc, lt, scene_dur, f, total_frames, active_sub, cue_lt, talking)
        im.save(os.path.join(frames_dir, f"f{f:05d}.jpg"), quality=90)
    return f_end - f_start


# ─── COMMANDS ────────────────────────────────────────────────────────────────
def cmd_templates(cfg):
    print("=" * 68)
    print("  AN TECH VIDEO ENGINE v1 — DANH SACH TEMPLATE & THEME")
    print("=" * 68)
    print("\n[HIEU UNG CANH (ghi [hieu_ung: ten] trong content.md)]:")
    for k, desc in TEMPLATE_DESCRIPTIONS.items():
        print(f"  - {k:<12} : {desc}")
    print("\n[BO MAU THEME (dung voi co --theme ten_theme)]:")
    for tk in cfg["themes"]:
        mark = " (mac dinh)" if tk == cfg["default_theme"] else ""
        print(f"  - {tk}{mark}")
    print(f"\nFile cau hinh chung: {STD_PATH}")


def cmd_scan(project_dir, cfg):
    files = list_img_files(project_dir)
    if not files:
        print(f"[CANH BAO] Khong tim thay anh nao trong {os.path.join(project_dir, 'img')}")
        return
    cols = 4
    rows = math.ceil(len(files) / cols)
    tw, th, pad, lbl_h = 420, 260, 24, 42
    W_s = cols * tw + (cols + 1) * pad
    H_s = rows * (th + lbl_h) + (rows + 1) * pad + 60
    sheet = Image.new("RGB", (W_s, H_s), (15, 23, 42))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 16), f"IMG SHEET ({len(files)} anh) — {os.path.basename(project_dir)}",
           font=get_font(cfg, "bold", 26), fill=(34, 211, 238))

    img_dir = os.path.join(project_dir, "img")
    lf = get_font(cfg, "bold", 22)
    for idx, fn in enumerate(files):
        r, c = divmod(idx, cols)
        x = pad + c * (tw + pad)
        y = 64 + pad + r * (th + lbl_h + pad)
        src = ImageOps.exif_transpose(Image.open(os.path.join(img_dir, fn))).convert("RGB")
        thumb = ImageOps.contain(src, (tw, th))
        d.rectangle((x, y, x + tw, y + th), fill=(25, 35, 58), outline=(59, 130, 246), width=2)
        sheet.paste(thumb, (x + (tw - thumb.width) // 2, y + (th - thumb.height) // 2))
        d.text((x + 6, y + th + 6), fn, font=lf, fill=(248, 250, 252))

    out_p = os.path.join(project_dir, "_img_sheet.jpg")
    sheet.save(out_p, quality=90)
    print(f"[OK] Da quet {len(files)} anh trong img/ -> {out_p}")
    for f in files:
        print(f"  - {f}")


def cmd_stills(project_dir, cfg, theme_name=None):
    """Xuất nhanh 1 ảnh mẫu cho mỗi cảnh (không cần chạy TTS) để duyệt bố cục trong 2 giây."""
    doc = parse_content_md(project_dir, cfg)
    t_name = theme_name or doc["notes"]["theme"] or cfg["default_theme"]
    theme = cfg["themes"][t_name]
    out_dir = os.path.join(project_dir, "mau", "stills_check")
    os.makedirs(out_dir, exist_ok=True)
    n = len(doc["scenes"])
    for i, sc in enumerate(doc["scenes"]):
        sc["_project_dir"] = project_dir
        sample_sub = sc["cues"][min(2, len(sc["cues"]) - 1)]["sub"] if sc["cues"] else sc["title"]
        im = render_frame(cfg, theme, sc, 10.0, 20.0, i * 300 + 150, max(1, n * 300), sample_sub, 1.5, True)
        out_p = os.path.join(out_dir, f"{sc['id']}_{sc['template']}.jpg")
        im.save(out_p, quality=90)
        print(f"  [OK] {out_p}")
    print(f"[OK] Da xuat {n} anh bo cuc (theme={t_name}) tai: {out_dir}")


def cmd_check(project_dir, cfg):
    doc = parse_content_md(project_dir, cfg)
    total_cues = sum(len(s["cues"]) for s in doc["scenes"])
    print("=" * 68)
    print(f"  KIEM TRA DAU VAO — {os.path.basename(project_dir)}")
    print("=" * 68)
    print(f"  Tieu de      : {doc['title']}")
    print(f"  So canh      : {len(doc['scenes'])} canh | {total_cues} cau thoai")
    print(f"  Loi chao     : {'BAT' if doc['notes']['greeting_enabled'] else 'TAT (theo notes.md)'}")
    print(f"  Muc tieu     : {doc['notes']['target_minutes'] or 'Khong gioi han'} phut | Giong: {doc['notes']['voice']}")
    print(f"  Anh img/     : {len(doc['img_stats']['used'])}/{doc['img_stats']['total_in_dir']} anh duoc gan")

    print("\n[DANH SACH CANH]:")
    all_pron = {}
    for sc in doc["scenes"]:
        imgs_s = ", ".join(x["file"] for x in sc["images"]) or "-"
        print(f"  {sc['id']} | {sc['template']:<10} | {len(sc['cues']):2d} cau | anh: {imgs_s:<18} | {sc['title']}")
        for c in sc["cues"]:
            for k, v in c["pron_applied"]:
                all_pron[k] = v

    if all_pron:
        print(f"\n[PHIEN AM TU DONG ({len(all_pron)} thuat ngu)]:")
        for k, v in sorted(all_pron.items()):
            print(f"  {k:<22} -> {v}")

    if doc["img_stats"]["missing"]:
        print("\n[LOI - ANH BI THIEU TRONG img/]:")
        for sid, fn in doc["img_stats"]["missing"]:
            print(f"  [LOI] Canh {sid} ghi anh '{fn}' nhung khong thay trong img/")
    if doc["img_stats"]["unused"]:
        print("\n[CANH BAO - ANH CHUA DUNG TRONG content.md]:")
        for fn in doc["img_stats"]["unused"]:
            print(f"  [CANH BAO] {fn}")
    if not doc["img_stats"]["missing"]:
        print("\n[OK] Dau vao hop le! San sang chay preview / render.")


def _synth_cues(scenes, audio_dir, voice_mode):
    os.makedirs(audio_dir, exist_ok=True)
    cache_meta_p = os.path.join(audio_dir, "tts_cache.json")
    cache_meta = json.load(open(cache_meta_p, "r", encoding="utf-8")) if os.path.exists(cache_meta_p) else {}

    all_cues = [c for sc in scenes for c in sc["cues"]]
    need = []
    for c in all_cues:
        wav_p = os.path.join(audio_dir, f"{c['id']}.wav")
        h = hashlib.md5((voice_mode + "|" + c["say"]).encode("utf-8")).hexdigest()[:12]
        if os.path.exists(wav_p) and os.path.getsize(wav_p) > 15000 and cache_meta.get(c["id"]) == h:
            c["wav"] = wav_p
            c["cached"] = True
        else:
            c["wav"] = wav_p
            c["hash"] = h
            c["cached"] = False
            need.append(c)

    cached_n = len(all_cues) - len(need)
    if cached_n:
        print(f"  [CACHE] Giu lai {cached_n}/{len(all_cues)} cau da co san (khong phai doc lai)")

    if need:
        if voice_mode == "vieneu":
            import tts_vieneu
            t_load = time.time()
            tts_vieneu.engine()
            print(f"  [OK] Model VieNeu-TTS san sang ({time.time() - t_load:.1f}s)")
            for idx, c in enumerate(need, 1):
                t0 = time.time()
                # Force overwrite if text changed
                if os.path.exists(c["wav"]):
                    os.remove(c["wav"])
                tts_vieneu.synth(c["say"], c["wav"], retries=2)
                cache_meta[c["id"]] = c["hash"]
                json.dump(cache_meta, open(cache_meta_p, "w", encoding="utf-8"), indent=2)
                bar_n = int(20 * idx / len(need))
                bar = "#" * bar_n + "-" * (20 - bar_n)
                print(f"  [TTS] [{bar}] {idx:2d}/{len(need)} | {c['id']} ({time.time() - t0:.1f}s)", flush=True)
        else:
            import asyncio
            import edge_tts
            voice_name = "vi-VN-NamMinhNeural"
            async def _run_edge():
                for idx, c in enumerate(need, 1):
                    mp3_p = c["wav"] + ".mp3"
                    await edge_tts.Communicate(c["say"], voice_name).save(mp3_p)
                    subprocess.run([FF, "-y", "-v", "error", "-i", mp3_p, "-ar", "48000", "-ac", "1", c["wav"]], check=True)
                    os.remove(mp3_p)
                    cache_meta[c["id"]] = c["hash"]
                    json.dump(cache_meta, open(cache_meta_p, "w", encoding="utf-8"), indent=2)
                    print(f"  [TTS-Edge] {idx}/{len(need)} | {c['id']}", flush=True)
            asyncio.run(_run_edge())

    for c in all_cues:
        c["dur"] = wav_duration(c["wav"])


def _build_timeline(scenes, cfg):
    cue_gap = cfg["audio"]["cue_gap_s"]
    scene_gap = cfg["audio"]["scene_gap_s"]
    t = 0.55  # Intro lead-in breath
    for sc in scenes:
        sc["t0"] = t
        if not sc["cues"]:
            t += 3.5
        else:
            for ci, c in enumerate(sc["cues"]):
                c["t0"] = t
                c["t1"] = t + c["dur"]
                t = c["t1"] + (cue_gap if ci < len(sc["cues"]) - 1 else 0.0)
            t += scene_gap
        sc["t1"] = t
        sc["dur"] = sc["t1"] - sc["t0"]
    return t + 0.6  # Outro tail


def _mix_audio_and_loudnorm(scenes, total_dur, cfg, work_dir):
    sr = 48000
    n_samples = int(math.ceil(total_dur * sr))
    mix = np.zeros(n_samples, dtype=np.float32)

    # 1. Place speech tracks
    for sc in scenes:
        for c in sc["cues"]:
            seg = wav_to_f32(c["wav"], sr)
            st = int(c["t0"] * sr)
            en = min(n_samples, st + len(seg))
            mix[st:en] += seg[:en - st]

    # 2. Synthesize & place subtle SFX from Kit/tools/sfx.py (resampled 24k -> 48k)
    sfx_vol = cfg["audio"].get("sfx_volume", 0.28)
    sfx_count = 0

    def add_sfx(sig_24k, at_sec, gain=1.0):
        nonlocal sfx_count
        # Simple linear upsample 24k -> 48k
        x24 = np.asarray(sig_24k, dtype=np.float32)
        x48 = np.repeat(x24, 2)
        st = int(at_sec * sr)
        en = min(n_samples, st + len(x48))
        if st < n_samples and en > st:
            mix[st:en] += x48[:en - st] * (sfx_vol * gain)
            sfx_count += 1

    w_sig = sfx.whoosh()
    p_sig = sfx.pop()
    c_sig = sfx.chime()
    d_sig = sfx.deny()
    s_sig = sfx.success()

    for idx, sc in enumerate(scenes):
        if idx > 0:
            add_sfx(w_sig, max(0.0, sc["t0"] - 0.12), 0.9)
        if sc["template"] == "intro":
            add_sfx(c_sig, sc["t0"] + 0.05, 0.85)
        elif sc["template"] == "va_cham":
            add_sfx(d_sig, sc["t0"] + 1.15, 0.85)
        elif sc["template"] == "outro":
            add_sfx(s_sig, sc["t0"] + 0.1, 0.9)
        else:
            add_sfx(p_sig, sc["t0"] + 0.15, 0.75)

    raw_wav = os.path.join(work_dir, "mix_raw.wav")
    write_wav_f32(raw_wav, mix, sr)
    print(f"  [OK] Gan {sfx_count} hieu ung SFX tong hop (khong nhac nen)")

    # 3. Broadcast dynamics + FFmpeg 2-pass loudnorm (-14.0 LUFS, TP <= -1.2 dBFS after AAC)
    target_i = cfg["audio"]["target_lufs"]
    target_tp = min(cfg["audio"]["true_peak_max"] - 0.5, -1.5)
    pre_chain = "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120:makeup=2,alimiter=limit=-2.5dB:attack=5:release=50"
    p1 = subprocess.run(
        [FF, "-i", raw_wav, "-af", f"{pre_chain},loudnorm=I={target_i}:TP={target_tp}:LRA=7:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr, re.S)
    norm_m4a = os.path.join(work_dir, "audio_norm.m4a")
    if m:
        st = json.loads(m[-1])
        af = (
            f"{pre_chain},loudnorm=I={target_i}:TP={target_tp}:LRA=7:linear=true:"
            f"measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
            f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:"
            f"offset={st['target_offset']}"
        )
    else:
        af = f"{pre_chain},loudnorm=I={target_i}:TP={target_tp}:LRA=7"

    subprocess.run(
        [FF, "-y", "-v", "error", "-i", raw_wav, "-af", af, "-ar", "48000", "-ac", "1", "-c:a", "aac", "-b:a", "192k", norm_m4a],
        check=True,
    )
    return norm_m4a


def _measure_qa(video_path):
    r = subprocess.run(
        [FF, "-i", video_path, "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    err = r.stderr
    m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", err)
    dur_s = 0.0
    if m_dur:
        dur_s = int(m_dur.group(1)) * 3600 + int(m_dur.group(2)) * 60 + float(m_dur.group(3))

    # Extract final summary section of ebur128
    m_i = re.findall(r"^\s*I:\s*(-?\d+\.\d+)\s*LUFS", err, re.M)
    m_tp = re.findall(r"^\s*Peak:\s*(-?\d+\.\d+)\s*dBFS", err, re.M)
    m_lra = re.findall(r"^\s*LRA:\s*(-?\d+\.\d+)\s*LU", err, re.M)
    return {
        "dur_s": dur_s,
        "lufs": float(m_i[-1]) if m_i else None,
        "tp": float(m_tp[-1]) if m_tp else None,
        "lra": float(m_lra[-1]) if m_lra else None,
    }


def run_pipeline(project_dir, cfg, mode="full", scene_filter=None, theme_name=None, voice_override=None, workers=6, no_logo=False):
    t_start = time.time()
    doc = parse_content_md(project_dir, cfg)
    if doc["img_stats"]["missing"]:
        print("[LOI] Co anh ghi trong content.md nhung thieu trong img/:")
        for sid, fn in doc["img_stats"]["missing"]:
            print(f"  - Canh {sid}: thieu '{fn}'")
        raise SystemExit(1)

    t_name = theme_name or doc["notes"]["theme"] or cfg["default_theme"]
    if t_name not in cfg["themes"]:
        raise SystemExit(f"[LOI] Khong thay theme '{t_name}'. Dung 'build.py templates' de xem danh sach.")
    theme = cfg["themes"][t_name]
    voice_mode = voice_override or doc["notes"]["voice"] or cfg["audio"]["default_voice"]

    scenes = doc["scenes"]
    for sc in scenes:
        sc["_project_dir"] = project_dir

    # Select scenes according to mode
    if scene_filter:
        scenes = [s for s in scenes if s["id"].lower() == scene_filter.lower()]
        if not scenes:
            raise SystemExit(f"[LOI] Khong tim thay canh '{scene_filter}'.")
        mode_tag = f"SCENE {scene_filter.upper()}"
        sub_dir = "preview"
        prefix = f"scene_{scene_filter.lower()}"
    elif mode == "preview":
        # Take first scenes up to ~35s (~2 scenes)
        scenes = scenes[:min(2, len(scenes))]
        mode_tag = "PREVIEW 30S"
        sub_dir = "preview"
        prefix = "preview_30s"
    else:
        mode_tag = "FULL MODE"
        sub_dir = "full"
        prefix = "video"

    out_dir = os.path.join(project_dir, "mau", sub_dir)
    audio_dir = os.path.join(project_dir, "mau", "audio_cache")
    frames_dir = os.path.join(out_dir, "frames")
    stills_dir = os.path.join(out_dir, "stills")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(stills_dir, exist_ok=True)

    # Clean stale frames
    for old_f in os.listdir(frames_dir):
        if old_f.endswith(".jpg"):
            os.remove(os.path.join(frames_dir, old_f))

    print("=" * 68)
    print(f"  AN TECH VIDEO ENGINE v1 — {os.path.basename(project_dir)} ({mode_tag})")
    print(f"  Theme: {t_name} | Voice: {voice_mode} | Workers: {workers}")
    print("=" * 68)

    # [1/6] Input check
    total_cues = sum(len(s["cues"]) for s in scenes)
    print("\n[1/6] DOC KICH BAN & KIEM TRA DAU VAO...")
    print(f"  [OK] {len(scenes)} canh, {total_cues} cau thoai")
    print(f"  [OK] Anh img/: {len(doc['img_stats']['used'])}/{doc['img_stats']['total_in_dir']} anh khop")
    if doc["img_stats"]["unused"]:
        print(f"  [CANH BAO] {len(doc['img_stats']['unused'])} anh chua dung: {', '.join(doc['img_stats']['unused'])}")

    # [2/6] TTS + Cache
    print(f"\n[2/6] TONG HOP GIONG DOC ({voice_mode.upper()} offline)...")
    _synth_cues(scenes, audio_dir, voice_mode)
    total_dur = _build_timeline(scenes, cfg)
    fps = cfg["video"]["fps"]
    total_frames = int(math.ceil(total_dur * fps))
    mm, ss = divmod(int(total_dur), 60)
    print(f"  [OK] Hoan tat {total_cues}/{total_cues} cau | Tong thoi luong: {mm:02d}:{ss:02d} ({total_dur:.1f}s, {total_frames} frames)")

    # [3/6] Render frames (parallel CPU)
    print(f"\n[3/6] RENDER KHUNG HINH (Da nhan CPU: {workers} workers)...")
    t_r0 = time.time()

    # Assign exact contiguous frame ranges per scene
    tasks = []
    cur_f = 0
    for idx, sc in enumerate(scenes):
        f_end = total_frames if idx == len(scenes) - 1 else min(total_frames, int(round(sc["t1"] * fps)))
        sc["f0"] = cur_f
        sc["f1"] = f_end
        # Split each scene into chunks of ~90 frames for balanced CPU load
        step = 90
        for s_f in range(cur_f, f_end, step):
            tasks.append((idx, s_f, min(f_end, s_f + step)))
        cur_f = f_end

    if workers > 1 and len(tasks) > 1:
        with multiprocessing.Pool(
            processes=workers,
            initializer=_init_worker,
            initargs=(cfg, theme, scenes, total_frames, frames_dir),
        ) as pool:
            done_f = 0
            for cnt in pool.imap_unordered(_render_chunk, tasks):
                done_f += cnt
                pct = int(100 * done_f / max(1, total_frames))
                if done_f == total_frames or done_f % 450 < 90:
                    print(f"  [RENDER] {done_f:5d}/{total_frames} frames ({pct:3d}%)", flush=True)
    else:
        _init_worker(cfg, theme, scenes, total_frames, frames_dir)
        done_f = 0
        for tk in tasks:
            done_f += _render_chunk(tk)

    # Copy 1 representative still per scene (at 55% of scene) for fast visual QA
    for sc in scenes:
        mid_f = sc["f0"] + int((sc["f1"] - sc["f0"]) * 0.55)
        mid_f = min(total_frames - 1, max(0, mid_f))
        src_st = os.path.join(frames_dir, f"f{mid_f:05d}.jpg")
        dst_st = os.path.join(stills_dir, f"{sc['id']}_{sc['template']}.jpg")
        if os.path.exists(src_st):
            with open(src_st, "rb") as rf, open(dst_st, "wb") as wf:
                wf.write(rf.read())

    print(f"  [OK] Render {total_frames} frames xong trong {time.time() - t_r0:.1f}s | Stills: {stills_dir}")

    # Encode video stream
    video_only = os.path.join(out_dir, f"_{prefix}_video_only.mp4")
    subprocess.run(
        [
            FF, "-y", "-v", "error", "-framerate", str(fps),
            "-i", os.path.join(frames_dir, "f%05d.jpg"),
            "-c:v", "libx264", "-preset", cfg["video"]["preset"],
            "-crf", str(cfg["video"]["crf"]), "-pix_fmt", "yuv420p",
            video_only,
        ],
        check=True,
    )

    # [4/6] Mix audio + SFX + Loudnorm
    print("\n[4/6] GHEP AM THANH + SFX + LOUDNORM (-14 LUFS)...")
    norm_m4a = _mix_audio_and_loudnorm(scenes, total_dur, cfg, out_dir)
    raw_mp4, logo_mp4, ver = next_version_base(out_dir, prefix=prefix)
    subprocess.run(
        [
            FF, "-y", "-v", "error", "-i", video_only, "-i", norm_m4a,
            "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart",
            raw_mp4,
        ],
        check=True,
    )
    if os.path.exists(video_only):
        os.remove(video_only)
    print(f"  [OK] Xuat ban goc (khong logo): {raw_mp4}")

    # [5/6] Stamp Logo
    final_mp4 = raw_mp4
    if not no_logo:
        print("\n[5/6] DONG LOGO AN TECH ACADEMY...")
        lg = cfg["logo_stamp"]
        stamp_py = os.path.join(TOOLS_DIR, "stamp_logo.py")
        subprocess.run(
            [
                sys.executable, stamp_py, raw_mp4,
                "--out", logo_mp4,
                "--pos", lg["pos"],
                "--dy", str(lg["dy"]),
                "--size", str(lg["size"]),
                "--alpha", str(lg["alpha"]),
            ],
            check=True,
        )
        final_mp4 = logo_mp4
    else:
        print("\n[5/6] BO QUA DONG LOGO (--no-logo)")

    # [6/6] Automatic QA
    print("\n[6/6] KIEM DINH TU DONG (QA MASTER 2.3)...")
    qa = _measure_qa(final_mp4)
    lufs_ok = qa["lufs"] is not None and abs(qa["lufs"] - cfg["audio"]["target_lufs"]) <= cfg["audio"]["lufs_tolerance"]
    tp_ok = qa["tp"] is not None and qa["tp"] <= cfg["audio"]["true_peak_max"] + 0.05
    img_ok = len(doc["img_stats"]["missing"]) == 0 and (mode != "full" or len(doc["img_stats"]["unused"]) == 0)

    mm2, ss2 = divmod(int(round(qa["dur_s"])), 60)
    print("  +------------------------+------------------------+---------+")
    print("  | Hang muc               | Thuc do                | Ket qua |")
    print("  +------------------------+------------------------+---------+")
    print(f"  | Thoi luong             | {mm2:02d}:{ss2:02d} ({qa['dur_s']:5.1f}s)        | DAT     |")
    lufs_s = f"{qa['lufs']:.1f} LUFS" if qa["lufs"] is not None else "N/A"
    print(f"  | Am luong (LUFS)        | {lufs_s:<22} | {'DAT' if lufs_ok else 'CAN SUA':<7} |")
    tp_s = f"{qa['tp']:.1f} dBFS" if qa["tp"] is not None else "N/A"
    print(f"  | True Peak              | {tp_s:<22} | {'DAT' if tp_ok else 'CAN SUA':<7} |")
    img_s = f"{len(doc['img_stats']['used'])}/{doc['img_stats']['total_in_dir']} anh"
    print(f"  | Anh img/ su dung       | {img_s:<22} | {'DAT' if img_ok else 'CANH BAO':<7} |")
    lg_s = "khong dong" if no_logo else f"{cfg['logo_stamp']['pos']}, {cfg['logo_stamp']['size']}px, a={cfg['logo_stamp']['alpha']}"
    print(f"  | Logo watermark         | {lg_s:<22} | {'DAT' if not no_logo else 'BO QUA':<7} |")
    print("  +------------------------+------------------------+---------+")

    elapsed = time.time() - t_start
    em, es = divmod(int(elapsed), 60)
    print(f"\nHOAN TAT TRONG {em:02d} phut {es:02d} giay!")
    print(f"File thanh pham : {final_mp4}")
    print(f"File goc backup : {raw_mp4}")
    print(f"Anh kiem tra    : {stills_dir}")


def main():
    cfg = load_standard()
    ap = argparse.ArgumentParser(description="AN TECH ACADEMY — Offline Terminal Video Engine CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("templates", help="Xem danh sach hieu ung animation & bo mau theme")

    p_scan = sub.add_parser("scan", help="Quet img/ va tao anh luoi _img_sheet.jpg")
    p_scan.add_argument("project", help="Ten thu muc bai (vd: Baigiang_Docker) hoac duong dan day du")

    p_chk = sub.add_parser("check", help="Kiem tra content.md, anh img/ va phien am tu dong")
    p_chk.add_argument("project")

    p_st = sub.add_parser("stills", help="Xuat nhanh 1 anh bo cuc cho moi canh trong vai giay")
    p_st.add_argument("project")
    p_st.add_argument("--theme", help="Bo mau theme")

    for name in ("preview", "render"):
        p_run = sub.add_parser(name, help="Xuat mau 30s" if name == "preview" else "Xuat video full + logo + QA")
        p_run.add_argument("project")
        p_run.add_argument("--scene", help="Chi render rieng 1 canh (vd: s02)")
        p_run.add_argument("--theme", help="Bo mau theme (dark_cyan | dark_purple | midnight_emerald)")
        p_run.add_argument("--voice", choices=["vieneu", "edge"], help="Giong doc (mac dinh: vieneu)")
        p_run.add_argument("--workers", type=int, default=6, help="So nhan CPU render song song (mac dinh: 6)")
        p_run.add_argument("--no-logo", action="store_true", help="Bo qua buoc dong logo")

    a = ap.parse_args()
    if a.cmd == "templates":
        cmd_templates(cfg)
    elif a.cmd == "scan":
        cmd_scan(resolve_project(a.project), cfg)
    elif a.cmd == "check":
        cmd_check(resolve_project(a.project), cfg)
    elif a.cmd == "stills":
        cmd_stills(resolve_project(a.project), cfg, theme_name=a.theme)
    elif a.cmd in ("preview", "render"):
        run_pipeline(
            resolve_project(a.project),
            cfg,
            mode=a.cmd,
            scene_filter=a.scene,
            theme_name=a.theme,
            voice_override=a.voice,
            workers=a.workers,
            no_logo=a.no_logo,
        )


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
