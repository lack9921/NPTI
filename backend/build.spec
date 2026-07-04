# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import sys
import os

block_cipher = None

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent

a = Analysis(
    ['app.py'],
    pathex=[str(ROOT / 'backend')],
    binaries=[],
    datas=[
        (str(ROOT / 'backend' / 'pools.json'), '.'),
        (str(ROOT / 'backend' / 'reports.json'), '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 包含前端构建产物
static_src = ROOT / 'frontend' / 'dist'
if static_src.exists():
    for f in static_src.rglob('*'):
        if f.is_file():
            rel = f.relative_to(static_src.parent)
            a.datas.append((str(f), str(rel.parent)))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NPFJ',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_tracker=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
