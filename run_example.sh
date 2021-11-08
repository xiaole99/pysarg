python setup.py install
pysarg stage_one -i pysarg/example/inputdir -o pysarg/example/outputdir
pysarg stage_two -i pysarg/example/outputdir/extracted.fasta -m pysarg/example/outputdir/metadata.txt -o pysarg/example/outputdir 