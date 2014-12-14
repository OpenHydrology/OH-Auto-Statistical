# Flood Estimation Report

Date: {{ report_date|default(None)|dateformat }}

River: {{ catchment.watercourse|default("Unnamed") }}
Location: {{ catchment.location|default("Unknown") }}

Catchment outlet: {{ catchment.point.x }}, {{ catchment.point.y }}  
Catchment centre: {{ catchment.descriptors.centroid_ngr.x }}, {{ catchment.descriptors.centroid_ngr.y }}    

Catchment descriptors:

Descriptor   |      Value | Descriptor  |      Value | Descriptor  |      Value 
:------------|-----------:|:------------|-----------:|:------------|-----------:
AREA         |{{ catchment.descriptors.dtm_area|floatformat(2) }}| FPEXT       |{{ catchment.descriptors.fpext|floatformat(4) }}| SPRHOST     |{{ catchment.descriptors.sprhost|floatformat(2) }}
ALTBAR       |{{ catchment.descriptors.altbar|floatformat(0) }}| LDP         |{{ catchment.descriptors.ldp|floatformat(2) }}| URBCONC1990 |{{ catchment.descriptors.urbconc1990|floatformat(3) }}
ASPBAR       |{{ catchment.descriptors.aspbar|floatformat(0) }}| PROPWET     |{{ catchment.descriptors.propwet|floatformat(2) }}| URBEXT1990  |{{ catchment.descriptors.urbext1990|floatformat(4) }}
ASPVAR       |{{ catchment.descriptors.aspvar|floatformat(2) }}| RMED-1H     |{{ catchment.descriptors.rmed_1h|floatformat(1) }}| URBLOC1990  |{{ catchment.descriptors.urbloc1990|floatformat(3) }}
BFIHOST      |{{ catchment.descriptors.bfihost|floatformat(3) }}| RMED-1D     |{{ catchment.descriptors.rmed_1d|floatformat(1) }}| URBCONC2000 |{{ catchment.descriptors.urbconc2000|floatformat(3) }}
DPLBAR       |{{ catchment.descriptors.dplbar|floatformat(2) }}| RMED-2D     |{{ catchment.descriptors.rmed_2d|floatformat(1) }}| URBEXT2000  |{{ catchment.descriptors.urbext2000|floatformat(4) }}
DPSBAR       |{{ catchment.descriptors.dpsbar|floatformat(1) }}| SAAR        |{{ catchment.descriptors.saar|floatformat(0) }}| URBLOC2000  |{{ catchment.descriptors.urbloc2000|floatformat(3) }}
FARL         |{{ catchment.descriptors.farl|floatformat(3) }}| SAAR4170    |{{ catchment.descriptors.saar4170|floatformat(0) }}

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

Donor river | Donor location | Similarity distance | L-variance | Weight | L-skew | Weight
:-----------|:---------------|--------------------:|-----------:|-------:|-------:|------:
River Don   | Bridge of Don  |                  23 |       1.23 |   0.61 |   0.12 |   0.45

Heterogeneity measure (H2): 2.3  
Interpretation: possibly heterogeneous  
Weighted L-variance: 1.23  
Weighted L-skew: 0.12

Probability distribution:

Selection: best fitting  
Name: generalised extreme value  
Parameters:  
Goodness of fit:  

Flood frequency curve:

AEP (%) | Growth factor | Flow (m³/s)
-------:|--------------:|-----------:
   50   |           1.0 |         1.6









 
 



