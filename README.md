# pysarg
Python implementation of [ARGs_OAP](https://github.com/biofuture/Ublastx_stageone)

## Installation
+ build from source (*cmake*, *zlib* and *libpthread* are required for building [diamond](https://github.com/bbuchfink/diamond) and [minimap2](https://github.com/lh3/minimap2)): 

```bash
git clone https://github.com/xinehc/pysarg
cd pysarg
python setup.py install
```

+ the source code is also uploaded to [pypi](https://pypi.org/search/?q=pysarg), try:
```bash
## make take a while for building the wheel, as 2 different versions of diamond need to be compiled
## use pip3 if needed
pip install pysarg
```

+ pre-compiled [conda](https://anaconda.org/xinehc/pysarg) packages (`osx-64` or `linux-64`, python 3.6)
```bash
conda install -c xinehc pysarg
```

+ only python=3.6 package has been uploaded, if python!=3.6, create a new conda environment
```bash
conda create -n pysarg python=3.6 -c xinehc pysarg
source activate pysarg
```


## Example
To run the examples, use:
```bash
pysarg stage_one -i pysarg/example/inputdir -o pysarg/example/outputdir
pysarg stage_two -i pysarg/example/outputdir/extracted.fasta -m pysarg/example/outputdir/metadata.txt -o pysarg/example/outputdir 
```
If everything is ok, there should be four files in `outputdir`
+ metadata.txt

|sample  |read_length|read_number|16s_number        |cell_number       |
|--------|-----------|-----------|------------------|------------------|
|STAS    |100        |200000     |9.776536312849162|3.05292019025543  |
|SWHAS104|100        |200000     |9.35754189944134 |3.3635174193105737|

+ output.txt

|sample  |sequence    |gene                            |gene_length|gene_type                          |gene_subtype                                              |covered_length|
|--------|------------|--------------------------------|-----------|-----------------------------------|----------------------------------------------------------|--------------|
|STAS|STAS_30|gi&#124;671541568&#124;ref&#124;WP_031525212.1&#124;|648|macrolide-lincosamide-streptogramin|macrolide-lincosamide-streptogramin__macB|31 |
|STAS|STAS_61|NP_840140                       |273|bacitracin                         |bacitracin__bacA                         |32 |
|STAS|STAS_70|gi&#124;764440891&#124;ref&#124;WP_044366757.1&#124;|439|multidrug |
|...    |...     |...|...        |...                          |...                                           |...            |

+ the above two tables can be merged on column `sample` and then used for normalizing the ARG counts and drawing PCA plots. One example is provided in `notebook/normalize_sarg.ipynb`
+ `extracted.fasta` is the pre-filtered ARG-like sequences in stage-one, `extracted.blast` is the blastx result of `extracted.fasta` in stage-two.