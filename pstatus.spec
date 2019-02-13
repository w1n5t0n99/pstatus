# -*- mode: python -*-
import PyInstaller.utils.hooks

hiddenimports = ['pysnmp.smi.exval','pysnmp.cache']
a = Analysis(['pstatus.py'],
             pathex=['C:\\Users\\relam\\Documents\\Projects\\pstatus'],
             binaries=[],
             datas=[],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
			)

x = Tree('C:\\Python35-32\\Lib\\site-packages\\pysnmp\\smi\mibs',prefix='pysnmp\\smi\\mibs',excludes='.py')
			

pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz,
          a.scripts,
          a.binaries + [('pstatus.ico', 'C:\\Users\\relam\\Documents\\Projects\\pstatus\\pstatus.ico', 'DATA')],
          a.zipfiles,
          a.datas,
		  x,
          name='pstatus',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon='C:\\Users\\relam\\Documents\\Projects\\pstatus\\pstatus.ico')
