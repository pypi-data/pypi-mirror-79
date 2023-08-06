# chewBBACA

**chewBBACA** stands for "BSR-Based Allele Calling Algorithm". The "chew" part could be thought of as "Comprehensive and  Highly Efficient Workflow" 
but at this point still it needs a bit of work to make that claim so we just add "chew" to add extra coolness to the software name. BSR stands for 
BLAST Score Ratio as proposed by [Rasko DA et al.](http://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-6-2) 

chewBBACA is a comprehensive pipeline including a set of functions for the creation and validation of whole genome and core genome MultiLocus Sequence 
Typing (wg/cgMLST) schemas, providing an allele calling algorithm based on Blast Score Ratio that can be run in multiprocessor 
settings and a set of functions to visualize and validate allele variation in the loci.

chewBBACA performs the schema creation and allele calls on complete or draft genomes resulting from de novo assemblers.

chewBBACA has been published (version 2.0.5 at the time) in Microbial Genomics under the title:
**chewBBACA: A complete suite for gene-by-gene schema creation and strain identification**  - [Link to paper](http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000166) 

When using chewBBACA please use the following citation:

Silva M, Machado M, Silva D, Rossi M, Moran-Gilad J, Santos S, Ramirez M, Carriço J. 15/03/2018. M Gen 4(3): [doi:10.1099/mgen.0.000166](doi:10.1099/mgen.0.000166)

# IMPORTANT

- As from 25/01/2018, chewBBACA's code has been adapted for **python 3** (tested on >=3.4). The previous python 2 version is no longer supported and can be found at https://github.com/B-UMMI/chewBBACA/tree/chewbbaca_py2.
- chewBBACA includes Prodigal training files for some species. You can consult the list of Prodigal training files that are readily available [here](https://github.com/B-UMMI/chewBBACA/tree/master/CHEWBBACA/prodigal_training_files). We strongly recommend using the same Prodigal training file for schema creation and allele calling to ensure consistent results.

# Latest updates

## 2.5.0 - 2.5.4

We've developed [Chewie-NS](https://chewbbaca.online/), a Nomenclature Server that is based on the [TypOn](https://jbiomedsem.biomedcentral.com/articles/10.1186/2041-1480-5-43) ontology and integrates with chewBBACA to provide access to gene-by-gene typing schemas and to allow a common and global allelic nomenclature to be maintained.

To allow all users to interact with the Chewie-NS, we've implemented the following set of modules:

- `LoadSchema`: enables upload of new schemas to the Chewie-NS.
- `DownloadSchema`: enables download of any schema from the Chewie-NS.
- `SyncSchema`: compares local schemas, previously downloaded from the Chewie-NS, with the remote versions in the Chewie-NS to download and add new alleles to local schemas, submit new alleles to update remote schemas and ensure that a common allele identifier nomenclature is maintained.
- `NSStats`:  retrieves basic information about species and schemas in the Chewie-NS.

The [documentation](https://chewie-ns.readthedocs.io/en/latest/) includes information about the integration with chewBBACA and how to run the new [LoadSchema](https://chewie-ns.readthedocs.io/en/latest/user/upload_api.html), [DownloadSchema](https://chewie-ns.readthedocs.io/en/latest/user/download_api.html), [SyncSchema](https://chewie-ns.readthedocs.io/en/latest/user/synchronize_api.html) and [NSStats](https://chewie-ns.readthedocs.io/en/latest/user/nsstats_api.html) processes.
The Chewie-NS [source code](https://github.com/B-UMMI/Nomenclature_Server_docker_compose) is freely available and deployment of local instances can be easily achieved through Docker Compose.

This version also includes other changes:

- The `AlleleCall` process will detect if a schema was created with previous chewBBACA versions and ask users if they wish to convert the schema to the latest version. The conversion process **will not alter** your schema files, it will simply add configuration files and copy the Prodigal training file to the schema's directory. You can force schema conversion with the `--fc` argument.
- The Prodigal training file used to create the schema will be included in the schema's directory and can be automatically detected by the `AlleleCall` process.
- Schemas created with the `CreateSchema` process or adapted with the `PrepExternalSchema` retain information about parameters values (BLAST Score Ratio, Prodigal training file, genetic code, minimum sequence length and sequence size variation threshold) and users are advised to keep performing allele call with those parameters values to ensure consistent results and provide the possibility of schema upload to the Chewie-NS. The AlleleCall process detects if a user provides parameters values that differ from the original values and requests confirmation before proceeding (you may force execution with the `--fc` argument).
- The AlleleCall process creates a SQLite database in the schema's directory that is used to store the allelic profiles determined with that schema.
- Further optimizations in the `PrepExternalSchema` process.

---------
## Check the [wiki pages](https://github.com/B-UMMI/chewBBACA/wiki)...
...for a much more thorough chewBBACA walkthrough.
Below you can find a list of commands for a quick usage of the software.

## An extensive [tutorial repository](https://github.com/B-UMMI/chewBBACA_tutorial)...
...is available as example on how to run an analysis pipeline using chewBBACA.

## Use [BBACA gitter](https://gitter.im/BBACA/Lobby)...
... if you have any pressing question. Chat can be faster and better than email for troubleshooting purposes.

## A ready to use [docker image](https://hub.docker.com/r/mickaelsilva/chewbbaca_py3/)...
...automatically built from the latest version of chewBBACA in Ubuntu 16.04.

## chewBBACA is available as a Galaxy module.
Many Thanks to Stefano Morabito and Arnold Knijn (https://github.com/aknijn) for EURL VTEC in ISS, Rome! 
https://toolshed.g2.bx.psu.edu/repository?repository_id=88fd7663075eeae9&changeset_revision=093352878303

----------

## Quick Usage

**Important Notes before starting:**

 - **chewBBACA** defines an allele as a complete Coding DNA Sequence, with start and stop codons according 
 to the [NCBI genetic code table 11](http://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi) identified using [Prodigal 2.6.0 ](https://github.com/hyattpd/prodigal/releases/). It will 
 automatically exclude any allele for which the DNA sequence does not contain start or stop codons and for which the length is not multiple of three. 
 - All the referenced lists of files *must contain full path* for the files.
 - Make sure that your fasta files are UNIX format. If they were created in Linux or MacOS systems they should be in the correct format, but if they were created in Windows systems, you should do a a quick conversion using for example [dos2unix](http://linuxcommand.org/man_pages/dos2unix1.html).

## 0. Setting up the analysis

**Installing chewBBACA**

Install using conda:

```
conda install -c bioconda chewbbaca
```

Install using pip:

```
pip3 install chewbbaca
```

chewBBACA has the following dependencies:

Python dependencies (defined in the [requirements](https://github.com/B-UMMI/chewBBACA/blob/master/CHEWBBACA/requirements.txt) file, should be automatically installed):
* numpy>=1.14.0
* scipy>=0.13.3
* biopython>=1.70
* plotly>=1.12.9
* SPARQLWrapper>=1.8.0
* requests>=2.2.1
* pandas>=0.22.0

Main dependencies:
* [BLAST 2.9.0+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/) or above
* [Prodigal 2.6.0 ](https://github.com/hyattpd/prodigal/releases/) or above

Other dependencies (for schema evaluation only):
* [ClustalW2](http://www.clustal.org/download/current/)
* [mafft](https://mafft.cbrc.jp/alignment/software/)

Installation through conda should take care of all dependencies. If you install through pip you will need to ensure that you have BLAST and Prodigal installed and added to the PATH.

----------

## 1. wgMLST schema creation

Create your own wgMLST schema based on a set of genomes fasta files. The command is the following:

```
chewBBACA.py CreateSchema -i ./genomes/ -o OutputFolderName --cpu 4
```

**Parameters**

`-i` Folder containing the genomes from which schema will be created. Alternatively a file 
 containing the path to the list of genomes. One file path (must be full path) 
 to any fasta/multifasta file containing all the complete or draft genomes you want to call alleles for.

`-o` prefix for the output folder for the schema

`--cpu` Number of cpus to use

`--bsr` (Optional) Minimum BSR for defining locus similarity. Default at 0.6. 

`--ptf` (Optional but recommended, contact for new species) path to file of prodigal training file to use.

**Outputs:** 

One fasta file per gene in the `-o` directory that is created. 
The fasta file names are the given according the FASTA annotation for each coding sequence. 

**Optional:** 

Information about each locus is almost non existant at this point, the only information directly given by the schema creation is where are located each identified protein on the 
genome (proteinID_Genome.tsv file). A function was added to fetch information on each locus based on the [uniprot SPARQL endpoint](http://sparql.uniprot.org/sparql).

```
chewBBACA.py UniprotFinder -i schema_seed/ -t proteinID_Genome.tsv --cpu 4
```

**Parameters**

`-i` Folder containing the reference genes of the schema.

`-t` proteinID_Genome.tsv output from the schema creation

`--cpu` Number of cpus to use

**Outputs:** 

A tsv file with the information of each fasta (new_protids.tsv), location on the genome, a name for which the protein sequence was submitted on uniprot and a link to that identified protein. 

----------

## 2.  Allele call using the wgMLST schema 


Then run is the following:

```
chewBBACA.py AlleleCall -i ./genomes/ -g genes/ -o OutPrefix --cpu 3 
```

**Parameters** 

`-i` Folder containing the query genomes. Alternatively a file
 containing the list with the full path of the location of the query genomes.
`-g` Folder containing the reference genes of the schema. Alternatively a file
 containing the list with the full path of the location of the reference genes.  

`-o` prefix for the output directory. ID for the allele call run.

`--cpu` Number of cpus to use 

`-b` (optional)Blastp full path. In case of slurm system BLAST version being outdated it may 
be hard to use a different one, use this option using the full path of the updated blastp executable

`--ptf` (Optional but recommended, contact for new species) path to file of prodigal training file to use.


**Outputs files**:
```
./< outPrefix >_< datestamp>/< outPrefix >/results_statistics.txt
./< outPrefix >_< datestamp>/< outPrefix >/results_contigsInfo.txt
./< outPrefix >_< datestamp>/< outPrefix >/results_Alleles.txt 
./< outPrefix >_< datestamp>/< outPrefix >logging_info.txt 
./< outPrefix >_< datestamp>/< outPrefix >RepeatedLoci.txt
```


----------

## 3. Evaluate wgMLST call quality per genome


Usage:


```
chewBBACA.py TestGenomeQuality -i alleles.tsv -n 12 -t 200 -s 5 -o OutFolder
```
	
`-i` raw output file from an allele calling (i.e. results_Alleles.txt)

`-n` maximum number of iterations. Each iteration removes a set of genomes over the defined threshold (-t) and recalculates all loci presence percentages.

`-t` maximum threshold, will start at 5. This threshold represents the maximum number of missing loci allowed, for each genome independently, before removing it (genome).

`-s` step to add to each threshold (suggested 5)

`-o` Folder for the analysis files

The output consists in a plot with all thresholds and a removedGenomes.txt file where its 
informed of which genomes are removed per threshold when it reaches a stable point (no more genomes are removed).

Example of an output can be seen [here](http://im.fm.ul.pt/chewBBACA/GenomeQual/GenomeQualityPlot_all_genomes.html) . This example uses an 
original set of 714 genomes and a scheme consisting of 3266 loci, using a parameter `-n 12`,`-s 5` and `-t 300`.

----------
## 4. Defining the cgMLST schema

 **Creating a clean allelic profile for PHYLOViZ** 
 
Clean a raw output file from an allele calling to a phyloviz readable file.


Basic usage:

```
chewBBACA.py ExtractCgMLST -i rawDataToClean.tsv -o output_folders
```
	
`-i` raw output file from an allele calling

`-o` output folder (created by the script if not existant yet)

`-r` (optional) list of genes to remove, one per line (e.g. the list of gene detected by ParalogPrunning.py)

`-g` (optional) list of genomes to remove, one per line (e.g. list of genomes to be removed selected based on testGenomeQuality results) 

`-p` (optional) minimum percentage of loci presence (e.g 0.95 to get a matrix with the loci that are present in at least 95% of the genomes)

----------
## 5. Visualize your schema

 **Create an html to help visualize your schema** 
 
 See an example [here](http://im.fm.ul.pt/chewBBACA/SchemaEval/rms/RmS.html)

Basic usage:

```
chewBBACA.py SchemaEvaluator -i genes/ -ta 11 -l rms/ratemyschema.html --cpu 3 --title "my title"
```
	
`-i` directory where the genes .fasta files are located or alternatively a .txt file containing the full path for each gene .fasta file per line

`-ta` (optional) which translation table to use (Default: 11 in case of bacteria)

`--title` (optional) title to appear on the final html.

`-l` Location/name of the final html output

`--cpu` number of cpu to use, will be used for mafft and clustalw2

----------
## FAQ

### Q: Step 2 is taking hours, will it ever end?  
A: Depending on the variability of the strains used to create the schema and the number 
of CPUs you have selected, the computing time used will vary. The more variable the strains, the more BLAST 
comparisons will be made, meaning more time will be needed for finishing the analysis.

### Q: Step 3 just crashed at 99% after 2 days running, do I need to start over?  
A: chewBBACA should allow you to continue where you stopped, just re-run the same command and you should be prompted to continue the allele call or use the flag --fc.

### Q: I ran all the steps and my cgMLST loci size is smaller than traditional MLST, does this even work?  
A: You probably forgot to eliminate from the analysis genomes responsible for a considerable loss of loci. 
Try to run again step 4, remove some of those genomes and check if the cgMLST loci number rises.

### Q: Can I use a schema from an external source?
A: Yes. Be sure to have a single fasta for each locus and use the "PrepExternalSchema​" function.

### Q: Which species already have a training file?  
A: At the moment:
 - *Acinetobacter baumannii*
 - *Campylobacter jejuni*
 - *Enterococcus faecium*
 - *Escherichia coli*
 - *Haemophilus influenzae*
 - *Legionella pneumophila*
 - *Listeria monocytogenes*
 - *Salmonella enterica enteritidis*
 - *Staphylococcus aureus*
 - *Staphylococcus haemolyticus*
 - *Streptococcus agalactiae*
 - *Streptococcus canis
 - *Streptococcus dysgalactiae
 - *Streptococcus equi
 - *Streptococcus pneumoniae
 - *Streptococcus pyogenes
 - *Yersinia enterocolitica*

get them [here](https://github.com/B-UMMI/chewBBACA/tree/master/CHEWBBACA/prodigal_training_files).
 
### Q: My favorite species has no training file. What can I do?
A: You can propose a new one to be added to the repository or create your own training 
files. To create a training file do:

```
prodigal -i myGoldStandardGenome.fna -t myTrainedFile.trn -p single
```

----------  

## Citation

Silva M, Machado M, Silva D, Rossi M, Moran-Gilad J, Santos S, Ramirez M, Carriço J. 15/03/2018. M Gen 4(3): [doi:10.1099/mgen.0.000166](doi:10.1099/mgen.0.000166)
