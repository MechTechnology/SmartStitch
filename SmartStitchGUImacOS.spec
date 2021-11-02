# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
added_files = [
          ('SmartStitchLogo.*', '.'),
          ('gui_theme', 'gui_theme')
          ]

a = Analysis(['SmartStitchGUI.py', 'SmartStitchCore.py'],
             pathex=['/Users/abhimaanmayadam/Desktop/AbhiSmartStitch/SmartStitch'],
             binaries=[],
             datas= added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SmartStitchGUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
app = BUNDLE(exe,
             name='SmartStitchGUI.app',
             icon='SmartStitchLogo.icns',
             bundle_identifier=None)
