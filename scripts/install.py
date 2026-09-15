#!/usr/bin/env python3
"""Install the public standard skill from this checkout, without network access."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = 'panjie-perspective'
RUNTIME_FILES = (
    'SKILL.md', 'LICENSE', 'agents/openai.yaml',
    'references/work-style.md', 'references/workflow.md',
    'references/voice.md', 'references/customer-context.md',
)


def install(destination):
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('目标已存在；请先保留旧版，再选择新的目标目录。')
    for relative in RUNTIME_FILES:
        source = ROOT / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError('源码不完整或包含不支持的符号链接：' + relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()  # Fail if another process created it after the check.
    try:
        for relative in RUNTIME_FILES:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
    except Exception:
        # Only remove the incomplete directory created by this invocation.
        shutil.rmtree(destination)
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description='安装公开版；不覆盖同名技能，不修改账号或模型配置。')
    parser.add_argument('--target', choices=['codex', 'claude-code'], required=True)
    parser.add_argument('--destination', type=Path, help='自定义最终技能目录；用于旧版或特殊安装位置')
    parser.add_argument('--dry-run', action='store_true', help='只显示目标，不写入')
    args = parser.parse_args()
    personal = '.agents' if args.target == 'codex' else '.claude'
    destination = args.destination or Path.home() / personal / 'skills' / NAME
    if args.dry_run:
        print(destination.expanduser().absolute())
        return
    try:
        result = install(destination)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
    print('已安装：' + str(result))
    print('在工具中选择盼姐技能。没有出现时，重新打开客户端。')


if __name__ == '__main__':
    main()
