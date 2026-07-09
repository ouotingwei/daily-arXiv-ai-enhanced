#!/usr/bin/env python3
"""
keyword_filter.py
讀取爬蟲產出的 jsonl,只保留 title 或 summary 含關鍵字的論文,原地寫回。
用法: python3 keyword_filter.py data/2026-07-09.jsonl
"""
import sys, json

# ============================================================
# 精確關鍵字清單(全小寫,自動忽略大小寫)。
# 只放「幾乎不可能誤收」的詞:這些詞在 ML 論文出現,
# 幾乎百分百就是視覺SLAM/機器人視覺領域。
# 已刻意排除 localization / mapping / navigation 等一詞多義的廣詞。
# ============================================================
KEYWORDS = [
    # SLAM 系統(極精確)
    "slam",
    "v-slam",
    "visual odometry",
    "orb-slam"

    # 特徵 / 描述子 / 匹配(你的主力,精確)
    "feature matching",
    "image matching",

    # 幾何 / 感測(精確)
    "point cloud",
    "stereo matching",
    "stereo depth",
    "depth estimation",
    "3d reconstruction",
    "lidar",
    "structure-from-motion",
    "structure from motion",

    # 應用(精確,不易誤收)
    "autonomous driving",
    "self-driving",
    "autonomous vehicle",
    "mobile robot",

    # 你論文相關的高效架構(酌情,可註解掉)
    "mamba",
    # 在這裡繼續加你確定要的精確關鍵字...
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
    with open(path, encoding="utf-8") as f:
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
          f"(砍掉 {len(lines) - len(kept)} 篇)")

if __name__ == "__main__":
    main()
