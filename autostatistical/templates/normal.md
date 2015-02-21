# Flood Estimation Report

Date:          {{ report_date|default(None)|dateformat }}

## Input data

River:         {{ catchment.watercourse|default("Unnamed") }}  
Location:      {{ catchment.location|default("Unknown") }}  
NGR outlet:    {{ catchment.point.x }}, {{ catchment.point.y }}    
NGR centroid:  {{ catchment.descriptors.centroid_ngr.x }}, {{ catchment.descriptors.centroid_ngr.y }}  

### Catchment descriptors

Source:        CEH (2009)

Descriptor   |      Value | Descriptor  |      Value | Descriptor  |      Value 
:------------|-----------:|:------------|-----------:|:------------|----------:
AREA         | {{ catchment.descriptors.dtm_area|floatcolumn(2, 10, 6) }} | FPEXT       | {{ catchment.descriptors.fpext|floatcolumn(4, 10, 6) }} | SPRHOST     | {{ catchment.descriptors.sprhost|floatcolumn(2, 10, 6) }}
ALTBAR       | {{ catchment.descriptors.altbar|floatcolumn(0, 10, 6) }} | LDP         | {{ catchment.descriptors.ldp|floatcolumn(2, 10, 6) }} | URBCONC1990 | {{ catchment.descriptors.urbconc1990|floatcolumn(3, 10, 6) }}
ASPBAR       | {{ catchment.descriptors.aspbar|floatcolumn(0, 10, 6) }} | PROPWET     | {{ catchment.descriptors.propwet|floatcolumn(2, 10, 6) }} | URBEXT1990  | {{ catchment.descriptors.urbext1990|floatcolumn(4, 10, 6) }}
ASPVAR       | {{ catchment.descriptors.aspvar|floatcolumn(2, 10, 6) }} | RMED-1H     | {{ catchment.descriptors.rmed_1h|floatcolumn(1, 10, 6) }} | URBLOC1990  | {{ catchment.descriptors.urbloc1990|floatcolumn(3, 10, 6) }}
BFIHOST      | {{ catchment.descriptors.bfihost|floatcolumn(3, 10, 6) }} | RMED-1D     | {{ catchment.descriptors.rmed_1d|floatcolumn(1, 10, 6) }} | URBCONC2000 | {{ catchment.descriptors.urbconc2000|floatcolumn(3, 10, 6) }}
DPLBAR       | {{ catchment.descriptors.dplbar|floatcolumn(2, 10, 6) }} | RMED-2D     | {{ catchment.descriptors.rmed_2d|floatcolumn(1, 10, 6) }} | URBEXT2000  | {{ catchment.descriptors.urbext2000|floatcolumn(4, 10, 6) }}
DPSBAR       | {{ catchment.descriptors.dpsbar|floatcolumn(1, 10, 6) }} | SAAR        | {{ catchment.descriptors.saar|floatcolumn(0, 10, 6) }} | URBLOC2000  | {{ catchment.descriptors.urbloc2000|floatcolumn(3, 10, 6) }}
FARL         | {{ catchment.descriptors.farl|floatcolumn(3, 10, 6) }} | SAAR4170    | {{ catchment.descriptors.saar4170|floatcolumn(0, 10, 6) }} |             | {{ None|floatcolumn(4, 10, 6) }}

{% if qmed.method == 'amax_records' %}
### Annual maximum flow data

  Water year |       Date |  Flow (m³/s)
------------:|-----------:|------------:
{% for amax in catchment.amax_records %}
{{ amax.water_year|intcolumn(12) }} | {{ amax.date|dateformat }} | {{ amax.flow|signifcolumn(2, 12, 11) }}
{% endfor%}

{% endif %}
### National River Flow Archive (NRFA) data

Source:        {{ nrfa.url }}  
Version:       {{ nrfa.version }}  
Published:     {{ nrfa.published_on|dateformat('%B %Y') }}  
Retrieved:     {{ nrfa.downloaded_on|dateformat }}

## Median annual flood (QMED)
{% set methods = {'descriptors': "Catchment descriptors regression model with nearby catchments adjustment", 
                  'amax_records': "Median of annual maximum flow data"} %}

{% if qmed.method == 'descriptors' %}
Methology:     Kjeldsen, Jones & Bayliss (2008, eqs. 8.1 & 8.2), Kjeldsen (2010, eq. 8), Kjeldsen, Jones & Morris 
               (2014), Open Hydrology Contributors (2015)  
Analysis type: {{ methods[qmed.method] }}

QMED, rural:   {{ qmed.qmed_descr_rural|signif(3) }} m³/s  
URBEXT, {{ report_date|default(None)|dateformat('%Y') }}:  {{ qmed.urban_extent|round(4) }}  
Adj. factor:   {{ qmed.urban_adj_factor|round(3) }}  
QMED, urban:   {{ qmed.qmed_descr_urban|signif(3) }} m³/s

### QMED donor catchments

Donor river         | Donor location                 | Distance (km)| Adjustment factor | Power
:-------------------|:-------------------------------|-------------:|------------------:|-----:
{% for d in qmed.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} | {{ d.dist|intcolumn(12) }} | {{ d.factor|floatcolumn(3, 17) }} | {{ d.weight|floatcolumn(3, 5) }}
{% endfor %}

Adj. factor:   {{ qmed.donor_adj_factor|round(3) }}
{% else %}
Analysis type: {{ methods[qmed.method] }}  
{% endif %}
QMED:          {{ qmed.qmed|signif(2) }} m³/s

## Growth curve
{% set methods = {'pooling_group': "Pooled catchments analysis (ungauged)", 
                  'enhanced_single_site': "Pooled catchments analysis (gauged)"} %}

Methology:     Kjeldsen, Jones & Bayliss (2008, eqs. 8.3‒8.12 & 8.16), Kjeldsen (2010, eqs. 10 & 11), Open Hydrology 
               Contributors (2015)  
Analysis type: {{ methods[gc.method] }}

### Growth curve donor catchments (pooling group)

Donor river         | Donor location                 | Sim. dist. | Rec. length | L-var. | Weight | L-skew | Weight
:-------------------|:-------------------------------|-----------:|------------:|-------:|-------:|-------:|------:
{% for d in gc.donors %}
{{ d.watercourse|strcolumn(19) }} | {{ d.location|strcolumn(30) }} | {{ d.similarity_dist|floatcolumn(2, 10) }} | {{ d.record_length|intcolumn(11) }} | {{ d.l_cv|floatcolumn(3, 6) }} | {{ d.l_cv_weight|floatcolumn(3, 6) }} | {{ d.l_skew|floatcolumn(3, 6) }} | {{ d.l_skew_weight|floatcolumn(3, 6) }}
{% endfor %}
Total/weighted avg. |                                |            | {{ gc.donors_record_length|intcolumn(11) }} | {{ gc.l_cv_rural|floatcolumn(3, 6) }} |  1.000 | {{ gc.l_skew_rural|floatcolumn(3, 6) }} |  1.000

L-var., urban: {{ gc.l_cv|round(3) }}  
L-skew, urban: {{ gc.l_skew|round(3) }}

### Flood frequency curve

Distribution:  {{ gc.distr_name }}  
Parameters:    {{ gc.distr_params['loc']|round(3) }}, {{ gc.distr_params['scale']|round(3) }}, {{ gc.distr_params['c']|round(3) if gc.distr_params['c'] else gc.distr_params['k']|round(3)}}  

AEP (%) | Growth factor | Flow (m³/s)
-------:|--------------:|-----------:
{% for aep in gc.aeps %}
{{ (aep * 100)|floatcolumn(1, 7) }} | {{ gc.growth_factors[loop.index0]|floatcolumn(2, 13) }} | {{ gc.flows[loop.index0]|signifcolumn(2, 11, 10) }}
{% endfor %}

## References

CEH (2009). FEH CD-ROM 3 (Software). Wallingford: Centre for Ecology & Hydrology.

Kjeldsen, T. R., Jones, D. A. & Bayliss, A. C. (2008). *Improving the FEH statistical procedures for flood frequency 
estimation* (No. SC050050). Bristol: Environment Agency.

Kjeldsen, T. R. (2010). *Modelling the impact of urbanization on flood frequency relationships in the UK*. Hydrology 
Research, 41 (5). pp. 391‒405

Kjeldsen, T. R., Jones, D. A. & Morris, D. G. (2014). *Using multiple donor sites for enhanced flood estimation in 
ungauged catchments*. Water Resour. Res., 50, pp. 6646‒6657

Open Hydrology Contributors (2015). OH Auto Statistical. http://docs.open-hydrology.org/projects/oh-auto-statistical
