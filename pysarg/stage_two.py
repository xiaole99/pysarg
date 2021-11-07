import sys
import subprocess
import os
import re
import ast
from collections import defaultdict


def read_sarg(fasta_file, structure_file):
	sarg = defaultdict(list)
	with open(fasta_file) as f:
	    for line in f:
	        if line.startswith('>'):
	            name = re.sub('\s.*','',line[1:])
	        else:
	        	sarg[name].append(str(len(line)))

	with open(structure_file) as f:
		next(f) # skip header
		for line in f:
			styp, names = line.strip().split('\t')
			typ = re.sub('__.*','',styp)
			for name in ast.literal_eval(names):
				sarg[name].extend([typ, styp])
		
	return(sarg)

def stage_two(options):
	print(options)

	_path = os.path.dirname(os.path.abspath(__file__))
	_bin_diamond = os.path.join(_path, 'bin','diamond')
	_database_sarg = os.path.join(_path, 'database','SARG.dmnd')

	_database_sarg_structure = os.path.join(_path, 'database','structure_20181107.LIST')
	_database_sarg_fasta = os.path.join(_path, 'database','SARG.2.2.fasta')

	sarg = read_sarg(_database_sarg_fasta, _database_sarg_structure)
	
	# filter the 'pre-filtered' arg-like fasta
	subprocess.call(
        [_bin_diamond, 'blastx',
        '-d',_database_sarg,
        '-q',options.infile,
        '-o',os.path.join(options.outdir, 'extracted.sarg'),
        '-k','1', '-f','tab'])

	meta = {}
	with open(options.metafile) as f:
		next(f)
		for line in f:
			temp = line.strip().split('\t')
			meta[temp[0]] = temp[1:]

	## filter by length and identity and e-value
	res = []
	with open(os.path.join(options.outdir, 'extracted.sarg')) as f:
		for line in f:
			temp = line.strip().split()
			if float(temp[2])>=options.id_cutoff and int(temp[3])>=options.len_cutoff and float(temp[-2])<=options.e_cutoff:
				sample = re.sub('_\d+$','',temp[0])
				res.append([sample] + [temp[0], temp[1]] +  sarg.get(temp[1]) +  [temp[3]])

	## save the file
	with open(os.path.join(options.outdir, 'output.txt'), 'w') as f:
	    f.write('\t'.join([
	    	'sample','sequence','gene','gene_length','gene_type','gene_subtype', 'covered_length']) + '\n')
	    for line in res:
	        f.write('\t'.join([str(x) for x in line]) + '\n')
