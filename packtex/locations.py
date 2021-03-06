import os
import sys


paths = {
    'afm': ['TEXMF', 'fonts', 'afm', 'PACKAGE'],
    'aux': ['TEXMF', 'discard'],
    'bbx': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'bib': ['TEXMF', 'doc', 'PACKAGE'],
    'bst': ['TEXMF', 'bibtex', 'bst', 'PACKAGE'],
    'cbx': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'cfg': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'cls': ['TEXMF', 'tex', 'latex', 'base'],
    'csf': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'def': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'drv': ['TEXMF', 'install'],
    'dtx': ['TEXMF', 'install'],
    'dvi': ['TEXMF', 'install'],
    'enc': ['TEXMF', 'fonts', 'enc', 'PACKAGE'],
    'etx': ['TEXMF', 'install'],
    'fd':  ['TEXMF', 'tex', 'latex', 'fss'],
    'gen': ['TEXMF', 'fonts', 'source', 'PACKAGE'],
    'ibx': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'idf': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'ins': ['TEXMF', 'install'],
    'ist': ['TEXMF', 'discard'],
    'lbx': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'log': ['TEXMF', 'discard'],
    'lox': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'map': ['TEXMF', 'fonts', 'map', 'PACKAGE'],
    'mf':  ['TEXMF', 'fonts', 'source', 'PACKAGE'],
    'mtx': ['TEXMF', 'install'],
    'otf': ['FONT'],
    'out': ['TEXMF', 'discard'],
    'pdf': ['TEXMF', 'doc', 'PACKAGE'],
    'pfb': ['TEXMF', 'fonts', 'type1', 'PACKAGE'],
    'sty': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'tex': ['TEXMF', 'install'],
    'tfm': ['TEXMF', 'fonts', 'tfm', 'PACKAGE'],
    'tss': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
    'txt': ['TEXMF', 'discard'],
    'ttf': ['TEXMF', 'fonts', 'truetype', 'PACKAGE'],
    'vf':  ['TEXMF', 'fonts', 'vf', 'PACKAGE'],
    'xml': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
}

home_dir = os.path.expanduser('~')

if sys.platform == 'win32':
    font_dir = os.path.join(home_dir, 'Desktop')
    packtex_dir = os.path.join('C:', 'Program Files', 'PackTeX')
    tex_dir = os.path.join(home_dir, 'texmf')
elif sys.platform == 'darwin':
    font_dir = os.path.join(home_dir, 'Library', 'Fonts')
    packtex_dir = os.path.join(home_dir, '.packtex')
    tex_dir = os.path.join(home_dir, 'Library', 'texmf')
else:
    font_dir = os.path.join(home_dir, '.fonts')
    packtex_dir = os.path.join(home_dir, '.packtex')
    tex_dir = os.path.join(home_dir, 'texmf')

discard_dir = os.path.join(tex_dir, 'discard')
install_dir = os.path.join(tex_dir, 'install')

metadata = os.path.join(packtex_dir, '.metadata')

if not os.path.isfile(metadata):
    if not os.path.exists(packtex_dir):
        os.mkdir(packtex_dir)
    open(metadata, 'w').close()


def get_metadata_file():
    return metadata


def get_discard_dir():
    return discard_dir


def get_install_dir():
    return install_dir


def get_path(filetype, package):
    if filetype:
        try:
            path = '/'.join(paths[filetype])
        except KeyError:
            path = 'TEXMF/extras/PACKAGE'
    else:
        path = '/'.join(paths['sty'])
    path = path.replace('FONT', font_dir)
    path = path.replace('TEXMF', tex_dir)
    path = path.replace('PACKAGE', package)
    return path


def get_tex_dir():
    return tex_dir


def get_valid_filetypes():
    return paths.keys()
