#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pretty-charts 仓库自检与示例索引生成。

用法：
    python scripts/check_refs.py                  # 校验，有问题则退出码 1
    python scripts/check_refs.py --write-index    # 重新生成 examples/INDEX.md

三项校验（都是"必然漂移"的那几类问题，靠人眼盯不住）：
  A. 文档里提到的 references/** 与 examples/** 路径必须真实存在
  B. references/{data,diagram,spec} 下每个 .md 都必须被入口文件按名引用（杜绝"孤儿方法论"）
  C. examples 下每个 .py 都必须被 references/**.md 按名引用（杜绝"孤儿示例"）
  D. 示例脚本里不得出现硬编码颜色（hex 或 white/black/gray），必须从 palette JSON 取色
"""
from __future__ import annotations

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(REPO, "skills", "pretty-charts")
REFS = os.path.join(SKILL, "references")
EXAMPLES = os.path.join(SKILL, "examples")
ENTRY_FILES = ["SKILL.md", "routing.md", "selection.md", "checklist.md"]
IMG_EXT = (".png", ".pdf", ".svg")

EXT = "md|py|json|mplstyle|tex|png|pdf|svg|geojson"
PATH_RE = re.compile(
    r"(?:\.\./)*(?:skills/pretty-charts/)?(?:references|examples)/[A-Za-z0-9_./\-]+\.(?:" + EXT + r")")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def walk(root, suffix):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in sorted(files):
            if name.endswith(suffix):
                yield os.path.join(dirpath, name)


def resolve(md_path, raw):
    if raw.startswith("skills/pretty-charts/"):
        return os.path.normpath(os.path.join(REPO, raw))
    if raw.startswith("."):
        return os.path.normpath(os.path.join(os.path.dirname(md_path), raw))
    return os.path.normpath(os.path.join(SKILL, raw))


def check_paths(problems):
    for md in walk(REPO, ".md"):
        for lineno, line in enumerate(read(md).splitlines(), 1):
            # 行内逃生舱：路径基准不是本 .md（例如 LaTeX 片段相对 .tex 文件）时标 `check-refs: skip`
            if "check-refs: skip" in line:
                continue
            for m in PATH_RE.finditer(line):
                raw = m.group(0)
                if not os.path.exists(resolve(md, raw)):
                    problems.append("悬空路径  %s:%d  ->  %s"
                                    % (os.path.relpath(md, REPO), lineno, raw))


def check_reachable_docs(problems):
    entry_text = "\n".join(read(os.path.join(REFS, f)) for f in ENTRY_FILES
                           if os.path.exists(os.path.join(REFS, f)))
    entry_text += read(os.path.join(SKILL, "SKILL.md"))
    for folder in ("data", "diagram", "spec"):
        for md in walk(os.path.join(REFS, folder), ".md"):
            name = os.path.basename(md)
            if name not in entry_text:
                problems.append("孤儿方法论  references/%s/%s 未被路由文件按名引用"
                                % (folder, name))


def check_reachable_examples(problems):
    refs_text = "\n".join(read(md) for md in walk(REFS, ".md"))
    for py in walk(EXAMPLES, ".py"):
        name = os.path.basename(py)
        if name not in refs_text:
            problems.append("孤儿示例  %s 未被 references 下任何文档引用"
                            % os.path.relpath(py, REPO))


OUT_NAME_RE = re.compile(r"[\"']([A-Za-z0-9_\-]+\.(?:png|pdf|svg))[\"']")
WITH_SUFFIX_RE = re.compile(r"with_suffix\(\s*[\"']\.(png|pdf|svg)[\"']\s*\)")


def declared_outputs(py):
    """脚本显式声明的成图名：字面量文件名 + Path(__file__).with_suffix(ext)。"""
    text = read(py)
    names = set(OUT_NAME_RE.findall(text))
    stem = os.path.splitext(os.path.basename(py))[0]
    names.update("%s.%s" % (stem, ext) for ext in WITH_SUFFIX_RE.findall(text))
    return names


def script_outputs(py):
    base = os.path.dirname(py)
    subs = [""] + [d for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d))]
    found = []
    for name in sorted(declared_outputs(py)):
        for sub in subs:
            if os.path.isfile(os.path.join(base, sub, name)):
                found.append(("%s/%s" % (sub, name)) if sub else name)
                break
    if not found:
        # 文件名由变量拼出、无法静态归属时，退回列本目录与一层子目录里的成图
        for sub in subs:
            for f in sorted(os.listdir(os.path.join(base, sub))):
                if f.endswith(IMG_EXT) and f != "INDEX.md":
                    found.append(("%s/%s" % (sub, f)) if sub else f)
    return found


def build_index():
    lines = [
        "# 示例索引（examples/INDEX）",
        "",
        "> 由 `scripts/check_refs.py --write-index` 生成，**不要手工编辑**。",
        "> 脚本 ↔ 成图 ↔ 方法论文件的映射以本表为准；新增示例后重跑即可。",
        "",
    ]
    groups = {}
    for py in walk(EXAMPLES, ".py"):
        rel = os.path.relpath(py, EXAMPLES).replace(os.sep, "/")
        parts = rel.split("/")
        group = parts[0] + ("/" + parts[1] if len(parts) > 2 else "")
        groups.setdefault(group, []).append((parts[-1], script_outputs(py)))

    for group in sorted(groups):
        lines += ["## %s" % group, "", "| 生成脚本 | 成图 |", "|---|---|"]
        for script, outputs in sorted(groups[group]):
            imgs = "、".join("`%s`" % o for o in outputs) if outputs else "—"
            lines.append("| `%s` | %s |" % (script, imgs))
        lines.append("")
    return "\n".join(lines) + "\n"


HEX_OR_NAMED = re.compile(r"""["'](?:#[0-9A-Fa-f]{6}|white|black|gray|grey)["']""")


def check_no_hardcoded_colors(problems):
    """示例脚本里的颜色必须来自 palette JSON（spec/color.md §1：禁止硬编码色值）。"""
    for py in walk(EXAMPLES, ".py"):
        for lineno, line in enumerate(read(py).splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for m in HEX_OR_NAMED.finditer(line):
                problems.append(
                    "硬编码颜色  %s:%d  ->  %s（改为从 palette JSON 取色，见 spec/color.md §1）"
                    % (os.path.relpath(py, REPO), lineno, m.group(0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-index", action="store_true")
    args = ap.parse_args()

    if args.write_index:
        target = os.path.join(EXAMPLES, "INDEX.md")
        with open(target, "w", encoding="utf-8", newline="") as fh:
            fh.write(build_index())
        print("已生成 %s" % os.path.relpath(target, REPO))

    problems = []
    check_paths(problems)
    check_no_hardcoded_colors(problems)
    check_reachable_docs(problems)
    check_reachable_examples(problems)

    if problems:
        print("发现 %d 个问题：" % len(problems))
        for p in problems:
            print("  -", p)
        return 1
    print("自检通过：引用完整、无孤儿方法论、无孤儿示例。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
