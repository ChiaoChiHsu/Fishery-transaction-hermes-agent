#!/usr/bin/env python3
"""
install_seed_content.py

把本 repo 的 tools/ 資料夾內容，安裝到使用者電腦的 Hermes 家目錄（預設 ~/.hermes）。

對應關係：
    tools/SOUL.md                              -> $HERMES_HOME/SOUL.md
    tools/memories/MEMORY.md                   -> $HERMES_HOME/memories/MEMORY.md
    tools/memories/USER.md                     -> $HERMES_HOME/memories/USER.md
    tools/skills/fishery-transaction-analysis/  -> $HERMES_HOME/skills/fishery-transaction-analysis/

用法（本檔案放在 repo 最外層，與 tools/ 資料夾同一層）：
    python3 install_seed_content.py            # 一般安裝（不覆蓋既有檔案）
    python3 install_seed_content.py --force     # 覆蓋既有檔案
    python3 install_seed_content.py --dry-run   # 只列出會做什麼，不實際寫入
    python3 install_seed_content.py --hermes-home /path/to/.hermes  # 指定目標目錄
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

# 本檔案放在 repo 最外層（根目錄），來源資料放在同層的 tools/ 資料夾
REPO_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = REPO_ROOT / "tools"


def get_hermes_home(override: str | None = None) -> Path:
    """依照 hermes-agent 的規則決定 HERMES_HOME 位置。"""
    if override:
        return Path(override).expanduser().resolve()
    env = os.getenv("HERMES_HOME")
    if env:
        return Path(env).expanduser().resolve()
    if os.name == "nt":
        local = os.getenv("LOCALAPPDATA", "").strip()
        if local:
            return Path(local) / "hermes"
    return Path.home() / ".hermes"


def copy_file(src: Path, dst: Path, force: bool, dry_run: bool) -> None:
    if not src.exists():
        print(f"[跳過] 來源不存在：{src}")
        return
    if dst.exists() and not force:
        print(f"[跳過] 已存在（用 --force 覆蓋）：{dst}")
        return
    if dry_run:
        print(f"[將複製] {src}  ->  {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"[已安裝] {dst}")


def copy_dir(src: Path, dst: Path, force: bool, dry_run: bool) -> None:
    if not src.exists():
        print(f"[跳過] 來源資料夾不存在：{src}")
        return
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        copy_file(item, target, force, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="安裝 SOUL/MEMORY/USER/skills 到使用者的 Hermes 家目錄")
    parser.add_argument("--force", action="store_true", help="覆蓋已存在的檔案")
    parser.add_argument("--dry-run", action="store_true", help="只顯示會做的動作，不實際寫入")
    parser.add_argument("--hermes-home", default=None, help="指定 Hermes 家目錄路徑（預設自動偵測）")
    args = parser.parse_args()

    home = get_hermes_home(args.hermes_home)
    print(f"目標 Hermes 家目錄：{home}")
    if args.dry_run:
        print("（dry-run 模式，不會實際寫入任何檔案）")
    print()

    # 1) SOUL.md
    copy_file(SOURCE_DIR / "SOUL.md", home / "SOUL.md", args.force, args.dry_run)

    # 2) memories/MEMORY.md、memories/USER.md
    copy_file(SOURCE_DIR / "memories" / "MEMORY.md", home / "memories" / "MEMORY.md", args.force, args.dry_run)
    copy_file(SOURCE_DIR / "memories" / "USER.md", home / "memories" / "USER.md", args.force, args.dry_run)

    # 3) skills/fishery-transaction-analysis/（整個資料夾，含 SKILL.md 及其他輔助檔案）
    copy_dir(
        SOURCE_DIR / "skills" / "fishery-transaction-analysis",
        home / "skills" / "fishery-transaction-analysis",
        args.force,
        args.dry_run,
    )

    print("\n完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
