# SCALEX: Single-cell Analysis via latent Feature Extraction Universally 

## Installation  	
#### install from PyPI

    pip install scalex
    
#### install from GitHub

	git clone git://github.com/jsxlei/scalex.git
	cd scalex
	python setup.py install
    
scalex is implemented in [Pytorch](https://pytorch.org/) framework.  
Running scalex on CUDA is recommended if available.   
Installation only requires a few minutes.  

## Quick Start

    scalex.py --name name --data_list data1 data2 ... datan --batch_categories batch1 batch2 ... batch n 
    
    data_list: different batches of dataset, single
    batch_categories: is optional
    

#### Output
Output will be saved in the output folder including:
* **checkpoint**:  saved model to reproduce results cooperated with option --checkpoint or -c
* **adata.h5ad**:  preprocessed data and results including, latent, clustering and imputation
* **umap.png**:  UMAP visualization of latent representations of cells 
* **log.txt**:  log file of training process

     
#### Useful options  
* save results in a specific folder: [-o] or [--outdir] 
* filter rare genes, default 3: [--min_cell]
* filter low quality cells, default 600: [--min_gene]  
* select the number of highly variable genes, keep all genes with -1, default 2000: [--n_top_genes]
	
    
#### Help
Look for more usage of scalex

	scalex.py --help 
    
    
#### Tutorial
