# -*- coding: utf-8 -*-
"""
示例3：文件批量处理工具（重命名 / 按类型归档 / 批量改后缀）
=========================================================
适用场景（办公自动化里需求量极大、且零依赖、最容易上手的一类）：
  - 客户发来几百个文件，命名乱（空格、中文括号、大小写混用），要统一；
  - 要把一个文件夹里的图片/文档/表格自动归类到子文件夹；
  - 把 .jpeg 统一改成 .jpg。

为什么选它当示例：
  - 只用 Python 标准库（os/shutil），**不装任何第三方包**，双击就能跑；
  - 需求高频：调研里"批量重命名/文件整理"是闲鱼、猪八戒上反复出现的单子；
  - 和示例1（Excel）、示例2（图片）组成"办公自动化三件套"，覆盖最大刚需。

用法：
  # 图形界面（推荐给客户用）
  python 示例3_文件批量处理.py --gui

  # 命令行：按扩展名归档
  python 示例3_文件批量处理.py "D:/杂乱文件" --archive

  # 命令行：空格转下划线 + 加前缀 + 序号
  python 示例3_文件批量处理.py "D:/杂乱文件" --space-to-underscore --prefix 订单_ --serial

  # 命令行：批量改后缀 .jpeg -> .jpg
  python 示例3_文件批量处理.py "D:/杂乱文件" --change-ext jpeg jpg
"""

import argparse
import os
import re
import shutil


def batch_rename(folder, prefix="", space_to_underscore=False, serial=False,
                 change_ext=None, archive=False, dry_run=False):
    """对 folder 下的文件做批量处理。返回处理了多少个。"""
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    count = 0

    for idx, name in enumerate(sorted(files), start=1):
        ext = os.path.splitext(name)[1]
        base = os.path.splitext(name)[0]

        # 1) 批量改后缀
        if change_ext and ext.lower() == ("." + change_ext[0].lstrip(".").lower()):
            new_ext = "." + change_ext[1].lstrip(".")
            ext = new_ext

        # 2) 空格转下划线
        if space_to_underscore:
            base = base.replace(" ", "_")

        # 3) 加前缀 + 序号
        new_base = base
        if prefix:
            new_base = prefix + new_base
        if serial:
            new_base = f"{idx:03d}_{new_base}"

        new_name = new_base + ext

        # 4) 归档：移到 扩展名 子文件夹
        if archive:
            sub = os.path.join(folder, ext.lower().lstrip(".") + "文件")
            if not dry_run:
                os.makedirs(sub, exist_ok=True)
            dst = os.path.join(sub, new_name) if archive else os.path.join(folder, new_name)
        else:
            dst = os.path.join(folder, new_name)

        if dry_run:
            print(f"[预览] {name} -> {os.path.relpath(dst, folder)}")
        else:
            shutil.move(os.path.join(folder, name), dst)
            print(f"✅ {name} -> {os.path.relpath(dst, folder)}")
        count += 1

    print(f"\n共处理 {count} 个文件" + ("（预览模式，未实际改动）" if dry_run else ""))
    return count


def launch_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title("文件批量处理工具")
    root.geometry("560x340")

    folder_var = tk.StringVar()
    prefix_var = tk.StringVar()
    space_var = tk.BooleanVar(value=True)
    serial_var = tk.BooleanVar(value=True)
    archive_var = tk.BooleanVar(value=False)
    ext1_var = tk.StringVar()
    ext2_var = tk.StringVar()

    def pick():
        p = filedialog.askdirectory(title="选择文件所在文件夹")
        if p:
            folder_var.set(p)

    def run():
        if not folder_var.get():
            messagebox.showwarning("提示", "请先选择文件夹")
            return
        ce = [ext1_var.get(), ext2_var.get()] if ext1_var.get() and ext2_var.get() else None
        batch_rename(folder_var.get(), prefix=prefix_var.get(),
                     space_to_underscore=space_var.get(), serial=serial_var.get(),
                     change_ext=ce, archive=archive_var.get())
        messagebox.showinfo("完成", "文件处理完成")

    tk.Label(root, text="① 选择文件夹：").pack(anchor="w", padx=15, pady=(15, 0))
    f = tk.Frame(root); f.pack(fill="x", padx=15)
    tk.Entry(f, textvariable=folder_var, width=45).pack(side="left")
    tk.Button(f, text="浏览", command=pick).pack(side="left", padx=5)

    tk.Label(root, text="② 新文件名前缀（可选）：").pack(anchor="w", padx=15, pady=(10, 0))
    tk.Entry(root, textvariable=prefix_var, width=30).pack(padx=15, anchor="w")

    tk.Checkbutton(root, text="空格转下划线", variable=space_var).pack(anchor="w", padx=15)
    tk.Checkbutton(root, text="加序号(001_)", variable=serial_var).pack(anchor="w", padx=15)
    tk.Checkbutton(root, text="按扩展名自动归档到子文件夹", variable=archive_var).pack(anchor="w", padx=15)

    f2 = tk.Frame(root); f2.pack(fill="x", padx=15, pady=8)
    tk.Label(f2, text="批量改后缀：").pack(side="left")
    tk.Entry(f2, textvariable=ext1_var, width=8).pack(side="left", padx=3)
    tk.Label(f2, text="→").pack(side="left")
    tk.Entry(f2, textvariable=ext2_var, width=8).pack(side="left", padx=3)
    tk.Label(f2, text="（如 jpeg → jpg，留空不改）").pack(side="left")

    tk.Button(root, text="▶ 开始处理", command=run, bg="#4CAF50",
              fg="white", width=18).pack(pady=10)

    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="文件批量处理工具")
    parser.add_argument("folder", nargs="?", help="文件所在文件夹")
    parser.add_argument("--prefix", default="", help="新文件名前缀")
    parser.add_argument("--space-to-underscore", action="store_true", help="空格转下划线")
    parser.add_argument("--serial", action="store_true", help="加序号前缀")
    parser.add_argument("--archive", action="store_true", help="按扩展名归档")
    parser.add_argument("--change-ext", nargs=2, default=None, metavar=("FROM", "TO"),
                        help="批量改后缀，如 jpeg jpg")
    parser.add_argument("--dry-run", action="store_true", help="只预览不改动")
    parser.add_argument("--gui", action="store_true", help="启动图形界面")
    args = parser.parse_args()

    if args.gui or not args.folder:
        launch_gui()
        return

    batch_rename(args.folder, prefix=args.prefix,
                 space_to_underscore=args.space_to_underscore, serial=args.serial,
                 change_ext=args.change_ext, archive=args.archive, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
