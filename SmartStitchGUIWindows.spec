# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
              ( './gui_theme/light/*', 'gui_theme/light' ),
              ( './gui_theme/light.tcl', 'gui_theme' ),
              ( './gui_theme/modern_theme.tcl', 'gui_theme' ),
              ( './SmartStitchLogo.png', '.' ),
              ( './SmartStitchLogo.ico', '.' ),
              ]

a = Analysis(['SmartStitchGUI.py'],
             pathex=['.'],
             binaries=[],
             datas = added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SmartStitchGUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='SmartStitchLogo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SmartStitchGUI')
