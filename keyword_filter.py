#!/usr/bin/env python3
"""
keyword_filter.py
讀取爬蟲產出的 jsonl,只保留 title 或 summary 含關鍵字的論文,原地寫回。
用法: python3 keyword_filter.py data/2026-07-09.jsonl
"""

import sys
import json

# ============================================================
# 關鍵字清單(全部小寫,腳本自動忽略大小寫)。
# 標題或摘要「包含」任一關鍵字就保留。
# 已含常見縮寫、連字號變體、單複數。依需要增刪。
# ============================================================
KEYWORDS = [
    # --- 核心:SLAM / 定位建圖 (命中幾乎都相關) ---
    "slam",
    "visual odometry",
    "localization",
    "localisation",
    "pose estimation",
    "mapping",
    "structure-from-motion",
    "structure from motion",
    "sfm",
    "bundle adjustment",
    "loop closure",

    # --- 核心:特徵 / 描述子 / 匹配 (你的主力題目) ---
    "descriptor",
    "keypoint",
    "key-point",
    "feature matching",
    "feature extraction",
    "local feature",
    "data association",
    "correspondence",
    "image matching",

    # --- 自駕車 / 移動機器人 ---
    "autonomous driving",
    "self-driving",
    "autonomous vehicle",
    "mobile robot",
    "robot perception",
    "robotic perception",
    "navigation",
    "embodied",

    # --- 深度 / 幾何 / 感測 (機器人視覺常見) ---
    "depth estimation",
    "stereo",
    "lidar",
    "point cloud",
    "3d reconstruction",
    "visual-inertial",
    "visual inertial"

    # 在這裡繼續加你的關鍵字...
]
# ============================================================

def matches(paper, keywords):
    text = (paper.get("title", "") + " " + paper.get("summary", "")).lower()
    return any(kw in text for kw in keywords)

def main():
    if len(sys.argv) != 2:
        print("用法: python3 keyword_filter.py <jsonl檔路徑>")
        sys.exit(1)

    path = sys.argv[1]
    kws = [k.lower() for k in KEYWORDS]

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln for ln in f if ln.strip()]

    kept = []
    for ln in lines:
        try:
            paper = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if matches(paper, kws):
            kept.append(ln.rstrip("\n"))

    with open(path, "w", encoding="utf-8") as f:
        for ln in kept:
            f.write(ln + "\n")

    print(f"關鍵字過濾: {len(lines)} 篇 -> 保留 {len(kept)} 篇 "
          f"(砍掉 {len(lines) - len(kept)} 篇無關論文)")

if __name__ == "__main__":
    main()