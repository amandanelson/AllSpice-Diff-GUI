import PyInstaller.__main__

PyInstaller.__main__.run([
    'AllSpice-Diff-GUI.spec',
    '-y',
    '--debug=all',
    '--clean',
    ])