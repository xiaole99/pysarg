python setup.py install
pysarg stage_one -i pysarg/example/inputdir -o pysarg/example/outputdir
pysarg stage_two -i pysarg/example/outputdir/extracted.fa -o pysarg/example/outputdir -m pysarg/example/outputdir/metadata.txt