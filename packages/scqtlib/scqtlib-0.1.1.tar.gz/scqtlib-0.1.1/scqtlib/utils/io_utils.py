## some utils functions for scanpy

import os
import anndata
import numpy as np
import pandas as pd
import scanpy as sc

from scipy import io
from scipy.sparse import hstack

def adata_hstack(blocks, sample_ids=None):
    X_blocks = [adata.X.transpose() for adata in blocks]
    obs_blocks = [adata.obs for adata in blocks]
    
    new_X = hstack(X_blocks).transpose()
    new_obs = pd.concat(obs_blocks, axis=0)
    new_var = blocks[0].var
    new_adata = anndata.AnnData(X=new_X, obs=new_obs, var=new_var)
    
    sample_ids_default = []
    for i in range(len(blocks)):
        sample_ids_default += ["S%d" %i] * blocks[i].shape[0]
    
    if sample_ids is not None:
        if len(sample_ids) != len(new_obs):
            print("sample ids has different size to observations, change to default.")
            sample_ids = sample_ids_default
    else:
        sample_ids = sample_ids_default
    cell_ids = [
        new_adata.obs.index.values[i] + ":" + 
        sample_ids[i] for i in range(len(sample_ids))]
    
    new_adata.obs['cell_id'] = cell_ids
    new_adata.obs['sample_id'] = sample_ids
    
    return new_adata


def adata_preprocess(adata, min_cells=3, min_genes=500, max_genes=5000, 
                     max_percent_mito=0.1):
    
    ## first filtering
    sc.pp.filter_cells(adata, min_genes=min_genes)
    print(adata.shape)
    sc.pp.filter_genes(adata, min_cells=min_cells)
    print(adata.shape)
    
    ## basic info
    mito_genes = [name for name in adata.var_names if name.startswith('MT-')]
    adata.obs['n_counts'] = np.sum(adata.X, axis=1).A1
    adata.obs['n_genes'] = np.sum(adata.X>=1, axis=1).A1
    adata.obs['n_mito'] = np.sum(adata[:, mito_genes].X, axis=1).A1
    adata.obs['percent_mito'] = adata.obs['n_mito'] / adata.obs['n_counts']
    
    ## filter cells
    adata = adata[adata.obs['n_genes'] < max_genes, :]
    adata = adata[adata.obs['percent_mito'] < max_percent_mito, :]
    
    ## log transform
    adata.raw = sc.pp.log1p(adata, copy=True)
    sc.pp.normalize_per_cell(adata, counts_per_cell_after=1e4)
    
    ## filter genes
    filter_result = sc.pp.filter_genes_dispersion(adata.X, min_mean=0.0125, 
                                                  max_mean=3, min_disp=0.2)
    adata = adata[:, filter_result.gene_subset]
    
    ## regress and scale
    sc.pp.log1p(adata)
    sc.pp.regress_out(adata, ['n_counts', 'percent_mito'])
    sc.pp.scale(adata, max_value=10)
    
    
    ### PCA, t-SNE, and UMAP
    sc.tl.pca(adata)
    adata.obsm['X_pca'] *= -1  # multiply by -1 to match Seurat

    sc.tl.tsne(adata, random_state=2, n_pcs=10)
    
    sc.pp.neighbors(adata, n_neighbors=10)
    sc.tl.umap(adata)
    
    return adata



def load_10X(path, min_counts=None, min_cells=None, version3=False):
    """
    Load 10X data from cellranger output matrix, into 
    scipy csr matrix, arrays for genes and cell barcodes
    
    Filter cells by min_counts and filter genes by min_cells
    """
    ## load 10X matrix folder
    if version3:
        mat = io.mmread(path + "/matrix.mtx.gz").tocsr()
        genes = np.genfromtxt(path + "/features.tsv.gz", dtype="str", delimiter="\t")
        cells = np.genfromtxt(path + "/barcodes.tsv.gz", dtype="str", delimiter="\t")
    else:
        mat = io.mmread(path + "/matrix.mtx").tocsr()
        genes = np.genfromtxt(path + "/genes.tsv", dtype="str", delimiter="\t")
        cells = np.genfromtxt(path + "/barcodes.tsv", dtype="str", delimiter="\t")
    
    ## filter cells
    if min_counts is not None and min_counts > 0:
        n_counts = np.array(np.sum(mat, axis=0)).reshape(-1)
        idx = n_counts >= min_counts
        mat = mat[:, idx]
        cells = cells[idx]
       
    ## filter genes
    if min_cells is not None and min_cells > 0:
        n_cells = np.array(np.sum(mat, axis=1)).reshape(-1)
        idx = n_counts >= min_counts
        mat = mat[idx, :]
        genes = genes[idx, ]

    return mat, genes, cells

def save_10X(path, mat, genes, barcodes, version3=False):
    """
    Save 10X matrix, genes and cell barcodes into under the path.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    
    io.mmwrite(path + '/matrix.mtx', mat)

    if version3:
        fid = open(path + '/features.tsv', 'w')
    else:
        fid = open(path + '/genes.tsv', 'w')    
    for ii in range(genes.shape[0]):
        fid.writelines("\t".join(genes[ii, :]) + "\n")
    fid.close()

    fid = open(path + '/barcodes.tsv', 'w')
    for _cell in barcodes:
        fid.writelines("%s\n" %(_cell))
    fid.close()
    
    if version3:
        import subprocess
        bashCommand = "gzip -f %s %s %s" %(path + '/matrix.mtx',
                                           path + '/features.tsv',
                                           path + '/barcodes.tsv')
        pro = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        pro.communicate()[0]
