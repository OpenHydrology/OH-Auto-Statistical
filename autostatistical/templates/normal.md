# Flood Estimation Report

Date: {{ report_date|default(None)|dateformat }}

River: {{ catchment.watercourse|default("Unnamed") }}  
Location: {{ catchment.location|default("Unknown") }}

Catchment outlet: {{ catchment.point.x }}, {{ catchment.point.y }}  
Catchment centre: {{ catchment.descriptors.centroid_ngr.x }}, {{ catchment.descriptors.centroid_ngr.y }}    

Catchment descriptors:

Descriptor   |      Value | Descriptor  |      Value | Descriptor  |      Value 
:------------|-----------:|:------------|-----------:|:------------|----------:
AREA         | {{ catchment.descriptors.dtm_area|floatcolumn(2, 10, 6) }} | FPEXT       | {{ catchment.descriptors.fpext|floatcolumn(4, 10, 6) }} | SPRHOST     | {{ catchment.descriptors.sprhost|floatcolumn(2, 10, 6) }}
ALTBAR       | {{ catchment.descriptors.altbar|floatcolumn(0, 10, 6) }} | LDP         | {{ catchment.descriptors.ldp|floatcolumn(2, 10, 6) }} | URBCONC1990 | {{ catchment.descriptors.urbconc1990|floatcolumn(3, 10, 6) }}
ASPBAR       | {{ catchment.descriptors.aspbar|floatcolumn(0, 10, 6) }} | PROPWET     | {{ catchment.descriptors.propwet|floatcolumn(2, 10, 6) }} | URBEXT1990  | {{ catchment.descriptors.urbext1990|floatcolumn(4, 10, 6) }}
ASPVAR       | {{ catchment.descriptors.aspvar|floatcolumn(2, 10, 6) }} | RMED-1H     | {{ catchment.descriptors.rmed_1h|floatcolumn(1, 10, 6) }} | URBLOC1990  | {{ catchment.descriptors.urbloc1990|floatcolumn(3, 10, 6) }}
BFIHOST      | {{ catchment.descriptors.bfihost|floatcolumn(3, 10, 6) }} | RMED-1D     | {{ catchment.descriptors.rmed_1d|floatcolumn(1, 10, 6) }} | URBCONC2000 | {{ catchment.descriptors.urbconc2000|floatcolumn(3, 10, 6) }}
DPLBAR       | {{ catchment.descriptors.dplbar|floatcolumn(2, 10, 6) }} | RMED-2D     | {{ catchment.descriptors.rmed_2d|floatcolumn(1, 10, 6) }} | URBEXT2000  | {{ catchment.descriptors.urbext2000|floatcolumn(4, 10, 6) }}
DPSBAR       | {{ catchment.descriptors.dpsbar|floatcolumn(1, 10, 6) }} | SAAR        | {{ catchment.descriptors.saar|floatcolumn(0, 10, 6) }} | URBLOC2000  | {{ catchment.descriptors.urbloc2000|floatcolumn(3, 10, 6) }}
FARL         | {{ catchment.descriptors.farl|floatcolumn(3, 10, 6) }} | SAAR4170    | {{ catchment.descriptors.saar4170|floatcolumn(0, 10, 6) }}

## Median annual flood (QMED) 

QMED, rural: {{ qmed.qmed_descr_rural|signif(2) }} m³/s  
Urban adjustment factor: {{ qmed.urban_adj_factor|round(2) }}   
QMED, urban: {{ qmed.qmed_descr_urban|signif(2) }} m³/s

QMED donor catchments:

Donor river         | Donor location                 | Distance (km)| Adjustment factor | Weight
:-------------------|:-------------------------------|-------------:|------------------:|------:
{% for d in qmed.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} | {{ d.dist|intcolumn(12) }} | {{ d.factor|floatcolumn(2, 17) }} | {{ d.weight|floatcolumn(2, 6) }}
{% endfor %}
Total/weighted avg. |                                |              | {{ qmed.donor_adj_factor|floatcolumn(2, 17) }} |   1.00

QMED, adjusted: {{ qmed.qmed|signif(2) }} m³/s

## Growth curve

Analysis type: ungauged, pooling group

Growth curve donor catchments (pooling group):

Donor river         | Donor location                 | Sim. dist. | Rec. length | L-variance | Weight | L-skew | Weight
:-------------------|:-------------------------------|-----------:|------------:|-----------:|-------:|-------:|------:
{% for d in gc.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} | {{ d.similarity_dist|floatcolumn(2, 10) }} | {{ d.record_length|intcolumn(11) }} | {{ d.l_cv|floatcolumn(2, 10) }} | {{ d.l_cv_weight|floatcolumn(2, 6) }} | {{ d.l_skew|floatcolumn(2, 6) }} | {{ d.l_skew_weight|floatcolumn(2, 6) }}
{% endfor %}
Total/weighted avg. |                                |            | {{ gc.donors_record_length|intcolumn(11) }} | {{ gc.l_cv|floatcolumn(2, 10) }} |   1.00 | {{ gc.l_skew|floatcolumn(2, 6) }} |   1.00

Probability distribution:

Selection: manual  
Name: {{ gc.distr_name }}  
Parameters: {{ gc.distr_params['loc']|round(2) }}, {{ gc.distr_params['scale']|round(2) }}, {{ gc.distr_params['c']|round(2) if gc.distr_params['c'] else gc.distr_params['k']|round(2)}}  

Flood frequency curve:

AEP (%) | Growth factor | Flow (m³/s)
-------:|--------------:|-----------:
{% for aep in gc.aeps %}
{{ (aep * 100)|floatcolumn(1, 7) }} | {{ gc.growth_factors[loop.index0]|floatcolumn(1, 13) }} | {{ gc.flows[loop.index0]|signifcolumn(2, 11, 10) }}
{% endfor %}


Report created using OH Auto Statistical (open-hydrology.org). OH Auto Statistical is open source software implementing 
the Flood Estimation Handbook statistical method.

© Copyright 2014‒{{ report_date|default(None)|dateformat('%Y') }} Open Hydrology contributors.
