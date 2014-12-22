Scientific background
=====================

Flood Estimation Handbook
-------------------------

The methodologies used by OH Auto Statistical are directly based on the Flood Estimation Handbook (FEH), *the* standard
in the United Kingdom for flood flow estimation. The statistical methods for estimating flood flows in the FEH were
revised in 2008. The revised methodologies and evidence are described in `Kjeldsen, Jones and Bayliss (2008)
<https://www.gov.uk/government/publications/improving-the-flood-estimation-handbook-feh-statistical-procedures-for-flood-frequency-estimation>`_.
These latest revisions to the FEH statistical methods are fully incorporated into OH Auto Statistical.

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

 - QMED donors' adjustment factors are weighted using an Inverse Distance Weighting scheme with a power of 3. This has
   been calibrated against all catchments used in `Kjeldsen, Jones and Bayliss (2008)
   <https://www.gov.uk/government/publications/improving-the-flood-estimation-handbook-feh-statistical-procedures-for-flood-frequency-estimation>`_
   and is shown to reduce the RMSE slightly compared with selecting the nearest donor only.
 - Growth curve donor requirements:

   - Suitable for pooling
   - `URBEXT2000` less than 0.03, if provided.
   - At least 10 year of data

 - Pooled growth curve donors have at least 500 years of data in total.
 - The Generalised Logistic statistical distribution is used to create a frequency curve. Future versions of OH Auto
   Statistical will choose the best fitting distribution.

OH Auto Statistical is open source software. `Review the code on GitHub
<https://github.com/OpenHydrology/OH-Auto-Statistical>`_.




