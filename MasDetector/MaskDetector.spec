# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
from kivy_deps import sdl2, glew, gstreamer

a = Analysis(['C:\\Users\\angel\\Desktop\\mask-detector\\mask\\Main.py'],
             pathex=['C:\\Users\\angel\\Desktop\\mask-detector\\mask', 'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86','C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64'],
             binaries=[],
             datas=[],
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
          name='MaskDetector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='C:\\Users\\angel\\Desktop\\mask-detector\\mask\\icons\\icoagta.ico')
coll = COLLECT(exe,Tree('C:\\Users\\angel\\Desktop\\mask-detector\\mask'),
               a.binaries + [('msvcp120.dll', 'C:\\Windows\\System32\\msvcp120.dll', 'BINARY'),
                ('msvcr120.dll', 'C:\\Windows\\System32\\msvcr120.dll', 'BINARY')],
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='MaskDetector')
