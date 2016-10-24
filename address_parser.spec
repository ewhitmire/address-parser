# -*- mode: python -*-
import os
import usaddress
import openpyxl

block_cipher = None

data_files = [(os.path.join(os.path.dirname(usaddress.__file__), 'usaddr.crfsuite'), 'usaddress' ),
              (os.path.join(os.path.dirname(openpyxl.__file__), '.constants.json'), 'openpyxl') ]

a = Analysis(['address_parser.py'],
             pathex=[os.getcwd()],
             binaries=None,
             datas= data_files,
             hiddenimports=['pycrfsuite._pycrfsuite', 'pycrfsuite._dumpparser', 'pycrfsuite._logparser'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='address_parser',
          debug=False,
          strip=False,
          upx=True,
          console=True )
