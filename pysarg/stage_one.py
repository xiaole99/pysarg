import sys
import subprocess
import os
import re
import gzip

from collections import defaultdict
from . import settings

def read_files(files, sample):
    def gz_open(file):
        if file.split('.')[-1] == 'gz':
            return(gzip.open(file, 'rt'))
        else:
            return(open(file, 'rt'))

    ## init 
    sampleinfo = defaultdict(lambda: 0)
    for file in files:
        print('reading the sample information:', file)
        with gz_open(file) as f:
            marker = False
            for line in f:
                if line[0] in {'@', '>'}:
                    sampleinfo['read'] += 1
                    marker = True
                elif marker:
                    sampleinfo['base'] += len(line.rstrip())
                    marker = False
    return(sampleinfo['read'], int(sampleinfo['base']/sampleinfo['read']))

def count_16s(sam_file):
    '''
    count the number of proper pairs of a sam file, equivalent to: samtools view -f2 -c sam_file 
    '''
    count = 0
    with open(sam_file) as f:
        for line in f:
            if not line.startswith('@'):
                ## https://www.samformat.info/sam-format-flag
                if line.rstrip().split('\t')[1] in {'99', '147', '83', '163'}:
                    count+=1
    return(count)

def count_uscmg(uscmg_file, ko30, ko30cov):
    with open(uscmg_file) as f:
        for line in f:
            temp = line.strip().split('\t')
            ko30cov[ko30.get(temp[1])['ko30']] += int(temp[3])/int(ko30.get(temp[1])['length'])
    return(ko30cov)

def stage_one(options):

    _extracted = os.path.join(options.outdir, 'extracted.fasta')
    _metadata = os.path.join(options.outdir, 'metadata.txt')

    ## init 
    if os.path.isfile(_extracted): os.remove(_extracted)
    with open(_metadata, 'w') as f:
        f.write('\t'.join(['sample','read_length','read_number','16s_number','cell_number']) + '\n')

    ko30 = defaultdict(dict)
    with open(settings._ko30_list) as f:
        for line in f:
            temp = line.strip().split('\t')
            ko30[temp[0]]['ko30'] = temp[1]
            ko30[temp[0]]['length'] = temp[2]

    samplefile = defaultdict(list)
    for file in sorted([x for x in os.listdir(options.indir) if x[0]!='.']): # .DS_Store
        path = os.path.join(options.indir, file) 
        name = re.sub('_[12].*', '', file)
        samplefile[name].append(path)

    ## save the extracted sequences and metadata
    for sample in samplefile:
        files = samplefile[sample]

        ## get the number and mean length of reads
        read_number, read_length = read_files(files, sample)

        ## align to gg85
        _sam = os.path.join(options.outdir, sample+'.sam')
        with open(_sam, 'w') as f:
            subprocess.call(
                [settings._minimap2, '-ax', 'sr', settings._gg85,
                files[0], 
                files[1], 
                '--sam-hit-only'], stdout=f)
        pair_number = count_16s(_sam) * read_length / 1432

        ## align to sarg and ko30
        count = 0 # remove later
        ko30cov = defaultdict(lambda: 0)
        for file in files:
            prefix = os.path.join(options.outdir, ''.join(os.path.split(file)[-1].split('.')[:-1]))

            if settings._diamond2_version!='v0.9.24':
                subprocess.call(
                    [settings._diamond2, 'blastx',
                    '-d',settings._sarg,
                    '-q',file,
                    '-o',prefix + '.sarg',
                    '-e','10','-k','1','--id', '60', '--query-cover', '15', '-f6', 'full_qseq'])

                ## save the extracted fasta
                with open(_extracted, 'a') as f:
                    with open(prefix + '.sarg') as g:
                        for line in g:
                            f.write('>' + sample + '_' + str(count) + '\n')
                            f.write(line)
                            count += 1
            else: # remove later
                subprocess.call(
                    [settings._diamond2, 'blastx',
                    '-d',settings._sarg,
                    '-q',file,
                    '-o',prefix + '.sarg',
                    '-e','10','-k','1','--id', '60', '--query-cover', '15'])

                def extract_fasta(file, _sarg, _extracted, sample, count): # remove later
                    def gz_open(file):
                        if file.split('.')[-1] == 'gz':
                            return(gzip.open(file, 'rt'))
                        else:
                            return(open(file, 'rt'))

                    sarg = set()
                    with open(_sarg) as f:
                        for line in f:
                            temp = line.strip().split('\t')
                            sarg.add(temp[0])

                    s = False
                    with open(_extracted, 'a') as g:
                        with gz_open(file) as f:
                            for line in f:
                                if line[0] in {'@', '>'} and line[1:].strip() in sarg:
                                    count += 1
                                    g.write('>' + sample + '_' + str(count) + '\n')
                                    s = True
                                elif s:
                                    g.write(line)
                                    s = False
                    return(count)
                count = extract_fasta(file, prefix + '.sarg', _extracted, sample, count)

            subprocess.call(
                [settings._diamond, 'blastx',
                '-d',settings._ko30,
                '-q',file,
                '-o',prefix + '.uscmg',
                '-e',str(options.e_cutoff),'-k','1','--id', str(options.id_cutoff)])
            ko30cov = count_uscmg(prefix + '.uscmg', ko30, ko30cov)

        cell_number = sum(ko30cov.values())/len(ko30cov) if len(ko30cov)!=0 else 0
        metadata = [sample, read_length, read_number, pair_number, cell_number]

        ## save the metadata for later usage
        with open(_metadata, 'a') as f:
            f.write('\t'.join([str(x) for x in metadata]) + '\n')

    ## make the output folder cleaner
    [os.remove(os.path.join(options.outdir, x)) for x in os.listdir(options.outdir) if re.search('.(sarg|uscmg|sam)$',x)]