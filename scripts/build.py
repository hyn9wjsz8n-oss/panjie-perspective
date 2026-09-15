#!/usr/bin/env python3
"""Build both public packages and a standalone prompt from one source of truth."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

sys.dont_write_bytecode = True
from install import RUNTIME_FILES

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
META = json.loads((ROOT / 'release.json').read_text(encoding='utf-8'))
NAME = META['name']
REPO_FILES = (
    '.gitignore', 'README.md', 'LICENSE', 'SKILL.md', 'release.json',
    'agents/openai.yaml', 'references/work-style.md', 'references/workflow.md',
    'references/voice.md', 'references/customer-context.md',
    'docs/platforms.md', 'docs/design.md', 'docs/validation.md',
    'scripts/install.py', 'scripts/build.py',
    'dist/panjie-perspective.zip', 'dist/panjie-perspective-workbuddy.zip',
    'dist/panjie-perspective-prompt.md', 'dist/checksums.json',
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def header(fields):
    # JSON string literals are valid YAML scalars.
    return '---\n' + ''.join(f'{k}: {json.dumps(v, ensure_ascii=False)}\n' for k, v in fields.items()) + '---'


def make_zip(path, content):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, data in sorted(content.items()):
            info = zipfile.ZipInfo(f'{NAME}/{relative}', (2026, 9, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def check_links(base, paths):
    count = 0
    for path in paths:
        if path.suffix != '.md':
            continue
        for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^\n)]+)\)', path.read_text(encoding='utf-8')):
            target = unquote(target.strip('<>'))
            if target.startswith(('https://', 'http://')):
                continue
            file_part, _, fragment = target.partition('#')
            resolved = (path.parent / file_part).resolve() if file_part else path.resolve()
            if not resolved.is_relative_to(base.resolve()) or not resolved.is_file():
                raise ValueError(f'Invalid local reference: {path.name}: {target}')
            if fragment:
                raise ValueError('Unexpected fragment; maintain explicit file links: ' + target)
            count += 1
    return count


def check_public_text(label, data):
    text = unquote(data.decode('utf-8'))
    patterns = [
        r'/Users/|/private/|[A-Za-z]:\\Users\\',
        r'https?://[^\s<>]*?(?:feishu|larksuite)\.',
        r'(?<!\d)1[3-9]\d{9}(?!\d)',
        r'(?i)(?:access_token|refresh_token|app_secret|api_key)\s*[:=]\s*["\x27]?[A-Za-z0-9_-]{12,}',
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            raise ValueError('Public-content check failed: ' + label)


def main():
    DIST.mkdir(exist_ok=True)
    skill_text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    parts = skill_text.split('---', 2)
    if len(parts) != 3 or parts[0]:
        raise ValueError('Invalid skill frontmatter')
    main_header, body = parts[1], parts[2]
    fields = dict(line.split(':', 1) for line in main_header.strip().splitlines())
    if fields['name'].strip() != NAME or not fields['description'].strip():
        raise ValueError('Missing skill identity')
    standard = {p: (ROOT / p).read_bytes() for p in RUNTIME_FILES}
    workbuddy = {p: data for p, data in standard.items() if not p.startswith('agents/')}
    wb_fields = {
        'name': NAME, 'display_name': META['display_name'],
        'display_name_en': "Panjie's Work Perspective",
        'description': fields['description'].strip(),
        'description_zh': META['description_zh'], 'description_en': META['description_en'],
        'version': META['version'], 'author': META['author'], 'category': META['category'],
    }
    wb_suffix = '\n## WorkBuddy 参考文件入口\n\n' + '\n'.join(
        '- @' + p for p in RUNTIME_FILES if p.startswith('references/')
    ) + '\n'
    workbuddy['SKILL.md'] = (header(wb_fields) + body + wb_suffix).encode('utf-8')
    for p in standard.keys() & workbuddy.keys():
        if p != 'SKILL.md' and standard[p] != workbuddy[p]:
            raise ValueError('Platform content diverged: ' + p)
    if workbuddy['SKILL.md'].decode().split('---', 2)[2].removesuffix(wb_suffix) != body:
        raise ValueError('Platform changed the core instructions')
    make_zip(DIST / f'{NAME}.zip', standard)
    make_zip(DIST / f'{NAME}-workbuddy.zip', workbuddy)

    # Inline every runtime reference for hosts that accept text but cannot read folders.
    prompt = '# 盼姐工作判断与表达 · 单文件提示词\n\n'
    prompt += '请将下方内容作为本次任务的风格与工作方法指令；这是模拟，不是本人实时发言。所有工作资料已合并在本文中，无需读取外部文件。\n\n'
    prompt += re.sub(r'\[([^\]]+)\]\(references/[^)]+\)', r'\1（见本文附录）', body)
    for p in RUNTIME_FILES:
        if p.startswith('references/'):
            prompt += '\n\n---\n\n' + (ROOT / p).read_text(encoding='utf-8')
    (DIST / f'{NAME}-prompt.md').write_text(prompt, encoding='utf-8')

    archive_checks = 0
    with tempfile.TemporaryDirectory(prefix='panjie release 中文 ') as temporary:
        temporary = Path(temporary)
        for label, expected in [('standard', standard), ('workbuddy', workbuddy)]:
            suffix = '-workbuddy' if label == 'workbuddy' else ''
            with zipfile.ZipFile(DIST / f'{NAME}{suffix}.zip') as archive:
                if archive.testzip() is not None:
                    raise ValueError('Corrupt archive')
                names = archive.namelist()
                if set(names) != {f'{NAME}/{p}' for p in expected}:
                    raise ValueError('Unexpected archive member')
                if any(PurePosixPath(n).is_absolute() or '..' in PurePosixPath(n).parts for n in names):
                    raise ValueError('Unsafe archive member')
                archive.extractall(temporary / label)
            root = temporary / label / NAME
            for relative, data in expected.items():
                if (root / relative).read_bytes() != data:
                    raise ValueError('Extracted content differs')
                check_public_text(relative, data)
            archive_checks += check_links(root, [root / p for p in expected])
        installed = temporary / 'install with spaces' / NAME
        command = [sys.executable, str(ROOT / 'scripts/install.py'), '--target', 'codex', '--destination', str(installed)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        for p, data in standard.items():
            if (installed / p).read_bytes() != data:
                raise ValueError('Installed content differs')
        second = subprocess.run(command, capture_output=True, text=True)
        if second.returncode != 1:
            raise ValueError('Installer must refuse an existing destination')
        for p, data in standard.items():
            if (installed / p).read_bytes() != data:
                raise ValueError('Installer changed an existing installation')

    release_assets = [DIST / f'{NAME}.zip', DIST / f'{NAME}-workbuddy.zip', DIST / f'{NAME}-prompt.md']
    (DIST / 'checksums.json').write_text(json.dumps({
        'version': META['version'], 'algorithm': 'SHA256',
        'files': [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())} for p in release_assets],
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    validation = f'''# 验证说明

版本 {META['version']}。以下检查针对公开仓库文件与生成包，不代表模型回答效果的评分。

## 已完成

- 标准 SKILL.md 的名称和描述检查。
- WorkBuddy 必需元数据、中英文简介、版本、作者与资源入口检查。
- 标准包与 WorkBuddy 包的人物正文、应用正文和参考资料一致性检查。
- 两种 ZIP 的目录结构、解压完整性与相对引用检查；压缩包内共核对 {archive_checks} 处相对链接。
- 在含中文和空格的新目录解压，验证不依赖维护者的原工作目录。
- 本地安装脚本安装结果与源文件逐字节一致；再次安装拒绝覆盖，已安装文件保持原样。
- 公开资料的本机路径、飞书私有链接、明显联系方式和密钥赋值形式扫描。
- 单文件提示词已合并全部随包参考资料。

## 实际限制

没有在 WorkBuddy 或 Claude Code 客户端完成实机导入和对话验收，不能称为这些客户端的端到端测试。平台配置依据官方文档；行为效果仍取决于模型和用户提供的任务材料。

文本扫描不能替代全面隐私审计。发布采用精选文件清单，原始私人访谈、公司内部问答、客户名单和源知识库不在此仓库。

维护者可运行 `python3 scripts/build.py` 重建发布包并重复上述检查。技能使用者无需运行构建脚本。
'''
    (ROOT / 'docs/validation.md').write_text(validation, encoding='utf-8')
    paths = [ROOT / p for p in REPO_FILES]
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise ValueError('Missing or linked release file: ' + path.name)
        if path.suffix not in ('.zip', '.py'):
            check_public_text(path.name, path.read_bytes())
    relative_links = check_links(ROOT, paths)
    manifest = {
        'version': META['version'], 'repository': META['repository'],
        'scope': 'Selected public files only. This manifest excludes itself.',
        'files': [{'path': p, 'bytes': (ROOT / p).stat().st_size, 'sha256': digest((ROOT / p).read_bytes())} for p in REPO_FILES],
    }
    (ROOT / 'publication-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'public_files': len(REPO_FILES) + 1, 'relative_links': relative_links,
                      'archive_links': archive_checks, 'archives': [p.name for p in release_assets],
                      'result': 'passed'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
