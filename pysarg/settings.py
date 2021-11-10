import os

_path = os.path.dirname(os.path.realpath(__file__))
_diamond = os.path.join(_path, 'bin','diamond')
_diamond2 = os.path.join(_path, 'bin','diamond2') # remove later
_minimap2 = os.path.join(_path, 'bin','minimap2')

_gg85 = os.path.join(_path, 'database','gg85.mmi')

_sarg = os.path.join(_path, 'database','SARG.dmnd')
_sarg_list = os.path.join(_path, 'database','structure_20181107.LIST')
_sarg_fasta = os.path.join(_path, 'database','SARG.2.2.fasta')

_ko30 = os.path.join(_path, 'database','KO30_DIAMOND.dmnd')
_ko30_list = os.path.join(_path, 'database','all_KO30_name.list')

## if not build form source (conda), need to install
if not os.path.isfile(_diamond) or not os.path.isfile(_diamond2) or not os.path.isfile(_minimap2):
	raise RuntimeError('please make sure diamond/minimap2 are installed')