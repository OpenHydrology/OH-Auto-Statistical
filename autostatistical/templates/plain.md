# Flood Estimation Report

Date: {{ report_date|default(None)|dateformat }}

River: {{ catchment.watercourse|default("Unnamed") }}
Location: {{ catchment.location|default("Unknown") }}

Catchment outlet: {{ catchment.point.x }}, {{ catchment.point.y }}  
Catchment centre: {{ catchment.descriptors.centroid_ngr.x }}, {{ catchment.descriptors.centroid_ngr.y }}    

Catchment descriptors:

Descriptor   |      Value | Descriptor  |      Value | Descriptor  |      Value 
:------------|-----------:|:------------|-----------:|:------------|-----------:
AREA         |{{ catchment.descriptors.dtm_area|floatcolumn(2, 12, 7) }}| FPEXT       |{{ catchment.descriptors.fpext|floatcolumn(4, 12, 7) }}| SPRHOST     |{{ catchment.descriptors.sprhost|floatcolumn(2, 12, 7) }}
ALTBAR       |{{ catchment.descriptors.altbar|floatcolumn(0, 12, 7) }}| LDP         |{{ catchment.descriptors.ldp|floatcolumn(2, 12, 7) }}| URBCONC1990 |{{ catchment.descriptors.urbconc1990|floatcolumn(3, 12, 7) }}
ASPBAR       |{{ catchment.descriptors.aspbar|floatcolumn(0, 12, 7) }}| PROPWET     |{{ catchment.descriptors.propwet|floatcolumn(2, 12, 7) }}| URBEXT1990  |{{ catchment.descriptors.urbext1990|floatcolumn(4, 12, 7) }}
ASPVAR       |{{ catchment.descriptors.aspvar|floatcolumn(2, 12, 7) }}| RMED-1H     |{{ catchment.descriptors.rmed_1h|floatcolumn(1, 12, 7) }}| URBLOC1990  |{{ catchment.descriptors.urbloc1990|floatcolumn(3, 12, 7) }}
BFIHOST      |{{ catchment.descriptors.bfihost|floatcolumn(3, 12, 7) }}| RMED-1D     |{{ catchment.descriptors.rmed_1d|floatcolumn(1, 12, 7) }}| URBCONC2000 |{{ catchment.descriptors.urbconc2000|floatcolumn(3, 12, 7) }}
DPLBAR       |{{ catchment.descriptors.dplbar|floatcolumn(2, 12, 7) }}| RMED-2D     |{{ catchment.descriptors.rmed_2d|floatcolumn(1, 12, 7) }}| URBEXT2000  |{{ catchment.descriptors.urbext2000|floatcolumn(4, 12, 7) }}
DPSBAR       |{{ catchment.descriptors.dpsbar|floatcolumn(1, 12, 7) }}| SAAR        |{{ catchment.descriptors.saar|floatcolumn(0, 12, 7) }}| URBLOC2000  |{{ catchment.descriptors.urbloc2000|floatcolumn(3, 12, 7) }}
FARL         |{{ catchment.descriptors.farl|floatcolumn(3, 12, 7) }}| SAAR4170    |{{ catchment.descriptors.saar4170|floatcolumn(0, 12, 7) }}

## Median annual flood (QMED) 
                  
QMED, rural: {{ qmed.qmed_descr_rural|round(1) }} m³/s  
Urban adjustment factor: {{ qmed.urban_adj_factor|round(3) }}   
QMED, urban: {{ qmed.qmed_descr_urban|round(1) }} m³/s

QMED donor catchments:

Donor river         | Donor location                 | Distance (km)| Adjustment factor | Weight
:-------------------|:-------------------------------|-------------:|------------------:|------:
{% for d in qmed.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} |{{ d.dist|floatcolumn(0, 14, 14) }}|{{ d.factor|floatcolumn(3, 19, 15) }}|{{ d.weight|floatcolumn(2, 7, 5) }}
{% endfor %}

Weighted adjustment factor: {{ qmed.donor_adj_factor|round(3) }}  
QMED, adjusted: {{ qmed.qmed|round(1) }} m³/s

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









 
 



