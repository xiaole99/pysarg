import sys
import subprocess
import os
import re
import pysam
from collections import defaultdict

def prepare_samples(indir):
    files = os.listdir(indir)
    samples = sorted(list({re.sub('_[12].*', '', x) for x in files}))

    # if fq ...
    # if gzip ... 

    return(samples)

def count_reads(files):
    read = 0
    base = 0
    for file in files:
        with open(file) as f:
            for line in f:
                if line.startswith('>'):
                    read += 1
                else:
                    base += len(line)
    return(read, int(base/read))

def count_pairs(file, lread):
    ## read mapped in proper pair -> flag 2
    return(int(pysam.view(file, '-f2', '-c')) * lread / 1432)

def count_uscmg(files, seqs):
    kocov = defaultdict(lambda: 0)

    for file in files:
        with open(file) as f:
            for line in f:
                temp = line.strip().split('\t')
                kocov[seqs.get(temp[1])['ko']] += int(temp[3])/int(seqs.get(temp[1])['length'])

    cellnum = sum(kocov.values())/len(kocov)
    return(cellnum)

def stage_one(options):

    _path = os.path.dirname(os.path.abspath(__file__))
    _bin_diamond = os.path.join(_path, 'bin','diamond')
    _bin_minimap2 = os.path.join(_path, 'bin','minimap2')

    _database_gg85 = os.path.join(_path, 'database','gg85.mmi')
    _database_sarg = os.path.join(_path, 'database','SARG.dmnd')
    _database_ko30 = os.path.join(_path, 'database','KO30_DIAMOND.dmnd')

    _extracted = os.path.join(options.outdir, 'extracted.fa')
    _meta = os.path.join(options.outdir, 'metadata.txt')

    ## reset
    if os.path.exists(_extracted):
        os.remove(_extracted)

    seqs = defaultdict(dict)
    with open(os.path.join(_path, 'database','all_KO30_name.list')) as f:
        for line in f:
            temp = line.strip().split('\t')
            seqs[temp[0]]['ko'] = temp[1]
            seqs[temp[0]]['length'] = temp[2]

    meta = []
    samples = prepare_samples(options.indir)
    for sample in samples:
        for suffix in ['_1', '_2']:
            subprocess.call(
                [_bin_diamond, 'blastx',
                '-d',_database_sarg,
                '-q',os.path.join(options.indir, sample + suffix + '.fa'),
                '-o',os.path.join(options.outdir, sample + suffix + '.sarg'),
                '-e','10','-k','1','--id', '60', '--query-cover', '15'])

            subprocess.call(
                [_bin_diamond, 'blastx',
                '-d',_database_ko30,
                '-q',os.path.join(options.indir, sample + suffix + '.fa'),
                '-o',os.path.join(options.outdir, sample + suffix + '.uscmg'),
                '-e',str(options.e_cutoff),'-k','1','--id', str(options.id_cutoff)])

        with open(os.path.join(options.outdir, sample +'.sam'), 'w') as f:
            subprocess.call(
                [_bin_minimap2, '-ax', 'sr', _database_gg85,
                os.path.join(options.indir, sample + '_1.fa'), 
                os.path.join(options.indir, sample + '_2.fa')], stdout=f)

        _fa = [os.path.join(options.indir, sample + '_' + str(x) + '.fa') for x in range(1,3)]
        _sarg = [os.path.join(options.outdir, sample + '_' + str(x) + '.sarg') for x in range(1,3)]

        ## number of reads, mean length of reads
        nread, lread = count_reads(_fa)

        def extract_fasta(_fa, _sarg, _extracted, sample):
            sarg = set()
            for file in _sarg:
                with open(file) as f:
                    for line in f:
                        temp = line.strip().split('\t')
                        sarg.add(temp[0])

            count = 0
            s = False
            with open(_extracted, 'a') as g:
                for file in _fa:
                    with open(file) as f:
                        for line in f:
                            if line.startswith('>') and line[1:].strip() in sarg:
                                count += 1
                                index = '>' + os.path.split(sample)[-1] + '_' + str(count) +'\n'
                                g.write(index)
                                s = True
                            elif s:
                                g.write(line)
                                s = False

        extract_fasta(_fa, _sarg, _extracted, sample) 

        _sam = os.path.join(options.outdir, sample + '.sam')
        pairnum = count_pairs(_sam, lread)

        _uscmg = [os.path.join(options.outdir, sample + '_' + str(x) + '.uscmg') for x in range(1,3)]

        cellnum = count_uscmg(_uscmg, seqs)
        meta.append([sample, lread, nread, pairnum, cellnum])

    ## save the meta-data for later usage
    with open(_meta,'w') as f:
        f.write('\t'.join(['sample','read_length','number_reads','number_16s_reads','number_cells']) + '\n')
        for line in meta:
            f.write('\t'.join([str(x) for x in line]) + '\n')
