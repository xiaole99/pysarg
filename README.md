# pysarg
Python implementation of [ARGs_OAP](https://github.com/biofuture/Ublastx_stageone)


## Installation
+ build from source (*cmake*, *zlib* and *libpthread* are required for building [diamond](https://github.com/bbuchfink/diamond) and [minimap2](https://github.com/lh3/minimap2)): 

```
git clone https://github.com/xinehc/pysarg
cd pysarg
python setup.py install
```

+ the source code is also uploaded to [pypi](https://pypi.org/search/?q=pysarg), try:
```
## make take a while for building the wheel, as 2 different versions of diamond are used
pip install pysarg
```

<s>
+ pre-build packages (python>=3.7) do not work for all platform -> command `conda convert -all` only works for pure python code, due the dependencies on diamond and minimap2, need to run `conda build` on {osx-64 linux-32 linux-64}
```
conda install -c xinehc pysarg
```
</s>

## Example
To run the examples, use:
```python
pysarg stage_one -i pysarg/example/inputdir -o pysarg/example/outputdir
pysarg stage_two -i pysarg/example/outputdir/extracted.fasta -m pysarg/example/outputdir/metadata.txt -o pysarg/example/outputdir 
```
If everything is ok, there should be four files in `outputdir`
+ metadata.txt

|sample  |read_length|read_number|16s_number        |cell_number       |
|--------|-----------|-----------|------------------|------------------|
|STAS    |100        |200000     |10.893854748603353|3.05292019025543  |
|SWHAS104|100        |200000     |9.636871508379889 |3.3635174193105737|

+ output.txt

|sample  |sequence    |gene                            |gene_length|gene_type                          |gene_subtype                                              |covered_length|
|--------|------------|--------------------------------|-----------|-----------------------------------|----------------------------------------------------------|--------------|
|STAS    |STAS_1      |ABE98197                        |219        |quinolone                          |quinolone__qnrS                                           |32            |
|STAS    |STAS_29     |ABE98197                        |219        |quinolone                          |quinolone__qnrS                                           |32            |
|STAS    |STAS_49     |NP_840140                       |274        |bacitracin                         |bacitracin__bacA                                          |32            |
|...    |...     |...|...        |...                          |...                                           |...            |

+ the above two tables can be merged on column `sample` and then used for normalizing the ARG counts and drawing PCA plots. One example is provided in `notebook/normalize_sarg.ipynb`
+ `extracted.fasta` is the pre-filtered ARG-like sequences in stage-one, `extracted.blast` is the blastx result of `extracted.fasta` in stage-two.