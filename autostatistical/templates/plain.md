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
Urban adjustment factor: {{ qmed.urban_adj_factor|round(2) }}   
QMED, urban: {{ qmed.qmed_descr_urban|round(1) }} m³/s

QMED donor catchments:

Donor river         | Donor location                 | Distance (km)| Adjustment factor | Weight
:-------------------|:-------------------------------|-------------:|------------------:|------:
{% for d in qmed.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} |{{ d.dist|floatcolumn(0, 14, 14) }}|{{ d.factor|floatcolumn(2, 19, 16) }}|{{ d.weight|floatcolumn(2, 7, 5) }}
{% endfor %}
Total/weighted avg. |                                |              |{{ qmed.donor_adj_factor|floatcolumn(2, 19, 16) }}|   1.00

QMED, adjusted: {{ qmed.qmed|round(1) }} m³/s

## Growth curve

Analysis type: ungauged, pooling group

Growth curve donor catchments (pooling group):

Donor river         | Donor location                 | Sim. dist. | Rec. length | L-variance | Weight | L-skew | Weight
:-------------------|:-------------------------------|-----------:|------------:|-----------:|-------:|-------:|------:
{% for d in gc.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} |{{ d.similarity_dist|floatcolumn(2, 12, 9) }}|{{ d.record_length|floatcolumn(0, 13, 13) }}|{{ d.l_cv|floatcolumn(2, 12, 9) }}|{{ d.l_cv_weight|floatcolumn(2, 8, 5) }}|{{ d.l_skew|floatcolumn(2, 8, 5) }}|{{ d.l_skew_weight|floatcolumn(2, 7, 5) }}
{% endfor %}
Total/weighted avg. |                                |            |{{ gc.donors_record_length|floatcolumn(0, 13, 13) }}|{{ gc.l_cv|floatcolumn(2, 12, 9) }}|   1.00 |{{ gc.l_skew|floatcolumn(2, 8, 5) }}|   1.00

Heterogeneity measure (H2): {{ gc.heterogeneity }}  
Interpretation: {{ gc.heterogeneity_text }}  

Probability distribution:

Selection: manual  
Name: {{ gc.distr_name }}  
Parameters: {{ gc.distr_params['loc']|round(2) }}, {{ gc.distr_params['scale']|round(2) }}, {{ gc.distr_params['c']|round(2) if gc.distr_params['c'] else gc.distr_params['k']|round(2)}}  
Goodness of fit:  {{ gc.distr_fit }}

Flood frequency curve:

AEP (%) | Growth factor | Flow (m³/s)
-------:|--------------:|-----------:
{% for aep in gc.aeps %}
{{ (aep * 100)|floatcolumn(1, 8, 6) }}|{{ gc.growth_factors[loop.index0]|floatcolumn(2, 15, 12) }}|{{ gc.flows[loop.index0]|floatcolumn(1, 12, 11) }}
{% endfor %}
