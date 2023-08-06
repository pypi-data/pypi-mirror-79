from scProject import projection_object
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt


# print("Reading patterns...", file=sys.stderr)
patterns = sc.read_h5ad('patterns_anndata.h5ad')
print(patterns.X.shape, "patterns shape")

# print("Reading target geneset...", file=sys.stderr)
dataset = sc.read_h5ad('test_target.h5ad')
print(dataset.X.shape, "Target shape")
# target.var = target.var.set_index('gene_id')

# print("Doing projection...",file=sys.stderr)
# projection = scProject.projection.project(target,patterns)


dataset_filtered, patterns_filtered = projection_object.filterAnnDatas(dataset, patterns, 'gene_id')

projection_object.geneSelectivity(patterns_filtered, 'ENSMUSG00000036887', 24)
# projection_object.geneSelectivity(patterns_filtered, 'ENSMUSG00000036905', 5)
# projection_object.geneSelectivity(patterns_filtered, 'ENSMUSG00000036896', 6)
projection_object.NNLR_ElasticNet(dataset_filtered, patterns_filtered, 'retinaProject', .01, .25)
projection_object.geneDriver(dataset_filtered, patterns_filtered, 'ENSMUSG00000036887', "CellType", "Brain Fibroblasts", "retinaProject")

# projection_object.NNLR_positive_Lasso(dataset_filtered, patterns_filtered, 'retinaProject', 0.005)
# projection_object.NNLR_LeastSquares(dataset_filtered, patterns_filtered, 'retinaProject')
projection_object.pearsonMatrix(dataset_filtered, patterns_filtered, 'CellType', 12, 'retinaProject', 'PearsonRetina',
                                False)
projection_object.UMAP_Projection(dataset_filtered, 'CellType', 'retinaProject', 'retinaUMAP', 20)
projection_object.featureImportance(dataset_filtered, 80, 'retinaProject')
projection_object.featurePlots(dataset_filtered, [21], 'retinaProject', 'retinaUMAP')
