# Flood Estimation Report

Date: {{ report_date|default(None)|dateformat }}

River: {{ catchment.watercourse|default("Unnamed") }}
Location: {{ catchment.location|default("Unknown") }}

Catchment outlet: {{ catchment.point.x }}, {{ catchment.point.y }}  
Catchment centre: {{ catchment.descriptors.centroid_ngr.x }}, {{ catchment.descriptors.centroid_ngr.y }}    

Catchment descriptors:

Descriptor   |      Value | Descriptor  |      Value | Descriptor  |      Value 
:------------|-----------:|:------------|-----------:|:------------|-----------:
AREA         |{{ catchment.descriptors.dtm_area|floatcolumn(2) }}| FPEXT       |{{ catchment.descriptors.fpext|floatcolumn(4) }}| SPRHOST     |{{ catchment.descriptors.sprhost|floatcolumn(2) }}
ALTBAR       |{{ catchment.descriptors.altbar|floatcolumn(0) }}| LDP         |{{ catchment.descriptors.ldp|floatcolumn(2) }}| URBCONC1990 |{{ catchment.descriptors.urbconc1990|floatcolumn(3) }}
ASPBAR       |{{ catchment.descriptors.aspbar|floatcolumn(0) }}| PROPWET     |{{ catchment.descriptors.propwet|floatcolumn(2) }}| URBEXT1990  |{{ catchment.descriptors.urbext1990|floatcolumn(4) }}
ASPVAR       |{{ catchment.descriptors.aspvar|floatcolumn(2) }}| RMED-1H     |{{ catchment.descriptors.rmed_1h|floatcolumn(1) }}| URBLOC1990  |{{ catchment.descriptors.urbloc1990|floatcolumn(3) }}
BFIHOST      |{{ catchment.descriptors.bfihost|floatcolumn(3) }}| RMED-1D     |{{ catchment.descriptors.rmed_1d|floatcolumn(1) }}| URBCONC2000 |{{ catchment.descriptors.urbconc2000|floatcolumn(3) }}
DPLBAR       |{{ catchment.descriptors.dplbar|floatcolumn(2) }}| RMED-2D     |{{ catchment.descriptors.rmed_2d|floatcolumn(1) }}| URBEXT2000  |{{ catchment.descriptors.urbext2000|floatcolumn(4) }}
DPSBAR       |{{ catchment.descriptors.dpsbar|floatcolumn(1) }}| SAAR        |{{ catchment.descriptors.saar|floatcolumn(0) }}| URBLOC2000  |{{ catchment.descriptors.urbloc2000|floatcolumn(3) }}
FARL         |{{ catchment.descriptors.farl|floatcolumn(3) }}| SAAR4170    |{{ catchment.descriptors.saar4170|floatcolumn(0) }}

## Median annual flood (QMED) 
                  
QMED, rural: {{ qmed.qmed.descr_rural|round(1) }} m³/s  
QMED, urban: {{ qmed.qmed.descr_urban|round(1) }} m³/s

QMED donor catchments:

Donor river         | Donor location                 | Distance (km)| Adjustment factor | Weight
:-------------------|:-------------------------------|-------------:|------------------:|------:
River Don           | Bridge of Don                  |           23 |              1.23 |   0.86
{% for d in qmed.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} |{{ d.dist|floatcolumn(0, 14, 14) }}|
{% endfor %}

Weighted adjustment factor: 1.21  
QMED, adjusted: {{ qmed.qmed.adjusted|round(1) }} m³/s

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

Selection: {{ gc.distribution_selection }}  
Name: {{ gc.distribution_name }}  
Parameters:  
Goodness of fit:  

Flood frequency curve:

AEP (%) | Growth factor | Flow (m³/s)
-------:|--------------:|-----------:
   50   |           1.0 |         1.6









 
 



