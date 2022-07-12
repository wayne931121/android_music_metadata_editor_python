# -*- mode: python ; coding: utf-8 -*-
# C:\Users\sky66\anaconda3\envs\tmp\share\sdl2\bin\*.dll

from kivy_deps import sdl2, glew

block_cipher = None

source = "./music_metadata_editor/"

a = Analysis(
    [source+'main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["PIL"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
	*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
	Tree(source+"assets", prefix="assets"),
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=source+'assets\ic.ico',
)
