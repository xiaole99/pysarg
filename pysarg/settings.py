import os

_path = os.path.dirname(os.path.abspath(__file__))
_diamond = os.path.join(_path, 'bin','diamond')
_minimap2 = os.path.join(_path, 'bin','minimap2')

_gg85 = os.path.join(_path, 'database','gg85.mmi')
_sarg = os.path.join(_path, 'database','SARG.dmnd')
_ko30 = os.path.join(_path, 'database','KO30_DIAMOND.dmnd')

_sarg_structure = os.path.join(_path, 'database','structure_20181107.LIST')
_sarg_fasta = os.path.join(_path, 'database','SARG.2.2.fasta')