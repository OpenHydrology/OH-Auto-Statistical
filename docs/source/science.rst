Scientific background
=====================

Flood Estimation Handbook
-------------------------

The methodologies used by OH Auto Statistical are directly based on the Flood Estimation Handbook (FEH), *the* standard
in the United Kingdom for flood flow estimation. The statistical methods for estimating flood flows in the FEH were
first revised in 2008 and additional improvements were subsequently published between 2010 and 2014. These latest
revisions to the FEH statistical methods are fully incorporated into OH Auto Statistical.

The revisions to the FEH statistical methods are described in the following papers:

- Kjeldsen, T. R., Jones, D. A. & Bayliss, A. C. (2008). *Improving the FEH statistical procedures for flood frequency
  estimation* (No. SC050050). Bristol: `Environment Agency <https://www.gov.uk/government/publications/improving-the-flood-estimation-handbook-feh-statistical-procedures-for-flood-frequency-estimation>`_

- Kjeldsen, T. R. (2010). *Modelling the impact of urbanization on flood frequency relationships in the UK*. Hydrology
  Research, 41 (5). pp. 391‒405 `doi:10.2166/nh.2010.056 <http://doi.org/10.2166/nh.2010.056>`_

- Kjeldsen, T. R., Jones, D. A. & Morris, D. G. (2014). *Using multiple donor sites for enhanced flood estimation in
  ungauged catchments*. Water Resour. Res., 50, pp. 6646‒6657 `doi:10.1002/2013WR015203 <http://doi.org/10.1002/2013WR015203>`_.


.. note::
   Why a fully automated implementation?

   The FEH recommends and other publications recommend that hydrologist should use expert judgement to improve flood
   estimates where possible. For example, the most suitable QMED or growth curve donor catchment should be decided based
   on catchment similarity, local knowledge, other datasets etc. However, as practicioners, hydrologist often do not
   have access to other data or information not already included in the National River Flow Archive (NRFA). In absence
   of any additional data, there is a danger that subjective decisions are made which could potentially render the
   estimates less accurate that purely based on the calibrated national methodologies.

   OH Auto Statistical purely follows FEH methodologies taking into account the latest NRFA datasets.

Assumptions
-----------

The following assumptions are made by OH Auto Statistical:

- NRFA catchment data are assumed correct, including their indicated suitability for QMED estimation and growth curve
  pooling.
- QMED adjustment using donors always includes the `URBEXT` parameter (known as "urban adjustment") to estimate QMED
  from catchment descriptors. Both for the donor (may include urban catchments) and the subject location.
- QMED donor requirements:

  - Suitable for QMED estimation
  - Same country (as in: UK mainland versus Northern Ireland).
  - At least 10 years of data
  - Not more than 500 km from the subject location.

- Growth curve donor requirements:

  - Suitable for pooling
  - `URBEXT2000` less than 0.03, if provided.
  - At least 10 year of data

- Pooled growth curve donors have at least 500 years of data in total.
- For gauged catchments analysis, the catchment is always used to estimated QMED and is always used in the pooling
  group regardless whether the catchment is flagged as being suitable for QMED or growth curve donor analyses.
- The Generalised Logistic statistical distribution is used to create a frequency curve. Future versions of OH Auto
  Statistical will choose the best fitting distribution.
