# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

additional_files = [('assets/SmartStitchLogo.ico', 'assets/SmartStitchLogo.ico', 'DATA'), ('gui/layout.ui', 'gui/layout.ui', 'DATA')]

a = Analysis(
    ['SmartStitchGUI.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartStitch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/SmartStitchLogo.ico',
)
coll = COLLECT(
    exe,
    a.binaries + additional_files,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SmartStitch',
)
