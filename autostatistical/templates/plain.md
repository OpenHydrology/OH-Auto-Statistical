# Flood Estimation Analysis Report

River: River Dee  
Location: Aberdeen  

Catchment outlet: 123456, 789123  
Catchment centre: 123456, 789123  

Catchment descriptors:

Descriptor |  Value     | Descriptor  | Value 
:----------|-----------:|:------------|---------:
DTM AREA   |    416.56  | RMED-1H     |    8.8     
ALTBAR     |    151     | RMED-1D     |   35.5     
ASPBAR     |    123     | RMED-2D     |   47.1     
ASPVAR     |     0.22   | SAAR        |   947          
BFIHOST    |     0.511  | SAAR4170    |   951     
DPLBAR     |    26.93   | SPRHOST     |   34.62     
DPSBAR     |    62.9    | URBCONC1990 |    0.754
FARL       |     0.824  | URBEXT1990  |    0.0173 
FPEXT      |     0.1009 | URBLOC1990  |    0.738 
LDP        |    48.74   | URBCONC2000 |    0.830
PROPWET    |     0.45   | URBEXT2000  |    0.0361 
           |            | URBLOC2000  |    0.702 

## Median annual flood (QMED) 
                  
QMED, rural: 1.2 m³/s  
QMED, urban: 1.3 m³/s

QMED donor catchments:

Donor river | Donor location | Distance (km)| Adjustment factor | Weight
:-----------|:---------------|-------------:|------------------:|------:
River Don   | Bridge of Don  |           23 |              1.23 |   0.86

Weighted adjustment factor: 1.21  
QMED, adjusted: 1.6 m³/s

## Growth curve

Analysis type: ungauged, pooling group

Growth curve donor catchments (pooling group):

Donor river | Donor location | Similarity distance | Variance weight | Skew weight
:-----------|:---------------|--------------------:|----------------:|-----------:
River Don   | Bridge of Don  |                  23 |            0.61 |        0.45

Heterogeneity measure (H2): 2.3  
Interpretation: possibly heterogeneous

Probability distribution:

Selection: best fitting  
Name: generalised extreme value  
Goodness of fit:

Flood frequency curve:

AEP (%) | Growth factor | Flow (m³/s)
-------:|--------------:|-----------:
   50   |           1.0 |         1.6









 
 



