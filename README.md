# 1001GP scripts and analysis

## 1001GP2PanSN-spec.py
Modify fasta files headers to be in [PanSN-spec](https://github.com/pangenome/PanSN-spec)

```
usage: 1001GP2PanSN-spec.py [-h] -i INPUT -o OUT [-s SAMPLE] [-d DELIMITER]
                            [-c CHROMOSOME] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        fasta file
  -o OUT, --out OUT     output file
  -s SAMPLE, --sample SAMPLE
                        If not set, take sample name
  -d DELIMITER, --delimiter DELIMITER
                        delimiter
  -c CHROMOSOME, --chromosome CHROMOSOME
                        Take chromosome name from this index (sep by '_')
  -n, --near            Near perfect (only missing haplotype)

```


## syri_naming_filtering.py
Add additional features to the data frame. Possible filtering steps if wanted.  

**Filtering**:  
- SNPs
- Size
- Alignments 
```
usage: syri_naming_filtering.py [-h] -i INPUT [-o OUT] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        fasta file
  -o OUT, --out OUT     output file
  -s, --snp             remove SNPS
```