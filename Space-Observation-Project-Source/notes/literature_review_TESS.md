# Literature review: TESS transit photometry, by sub-method

150 papers, each checked on arXiv or Crossref (first-author surname and title overlap); 144 open-access PDFs downloaded to `literature/pdf/<group>/`.
Papers not found on arXiv or open access are listed without a PDF; none was fetched around a paywall. Candidates that could not be verified were dropped (McQuillan 2014, Lissauer 2012, Parmentier 2018, Montalto 2020, Cameron 2012, Winters 2019).

## A  Mission, catalogs and pipelines

What TESS observes, which stars it observes, and how raw pixels become the light curves we fit.

Sub-methods: Mission design and expected yield; Target catalogs (TIC, TOI); SPOC pipeline: presearch conditioning, data validation; Full-frame image photometry (QLP, eleanor, difference imaging); Gaia as the distance and radius anchor.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2010 | Jenkins | Overview of the Kepler Science Processing Pipeline | arXiv:1001.0258 |  | literature/pdf/A_Mission_data/Jenkins_2010_Overview_of_the_Kepler_Science_Processin.pdf |
| 2012 | Smith | Kepler Presearch Data Conditioning II - A Bayesian Approach to Systematic Error Correction | arXiv:1203.1383 | heritage of PDCSAP flux (TESS PDC) | literature/pdf/A_Mission_data/Smith_2012_Kepler_Presearch_Data_Conditioning_II_A_.pdf |
| 2012 | Stumpe | Kepler Presearch Data Conditioning I - Architecture and Algorithms for Error Correction in Kepler Light Curves | arXiv:1203.1382 | heritage of PDCSAP flux (TESS PDC) | literature/pdf/A_Mission_data/Stumpe_2012_Kepler_Presearch_Data_Conditioning_I_Arc.pdf |
| 2014 | Stumpe | Multiscale Systematic Error Correction via Wavelet-Based Bandsplitting in Kepler Data | doi:10.1086/674989 |  | literature/pdf/A_Mission_data/Stumpe_2014_Multiscale_Systematic_Error_Correction_v.pdf |
| 2015 | Ricker | The Transiting Exoplanet Survey Satellite | arXiv:1406.0151 | TESS mission (all data) | literature/pdf/A_Mission_data/Ricker_2015_The_Transiting_Exoplanet_Survey_Satellit.pdf |
| 2015 | Sullivan | The Transiting Exoplanet Survey Satellite: Simulations of planet detections and astrophysical false positives | arXiv:1506.03845 |  | literature/pdf/A_Mission_data/Sullivan_2015_The_Transiting_Exoplanet_Survey_Satellit.pdf |
| 2018 | Barclay | A Revised Exoplanet Yield from the Transiting Exoplanet Survey Satellite (TESS) | arXiv:1804.05050 |  | literature/pdf/A_Mission_data/Barclay_2018_A_Revised_Exoplanet_Yield_from_the_Trans.pdf |
| 2018 | Gaia Collaboration | Gaia Data Release 2. Summary of the contents and survey properties | arXiv:1804.09365 |  | literature/pdf/A_Mission_data/Gaia_Collaboration_2018_Gaia_Data_Release_2_Summary_of_the_conte.pdf |
| 2018 | Oelkers | Precision Light Curves from TESS Full-Frame Images: A Difference Imaging Approach | arXiv:1803.02316 |  | literature/pdf/A_Mission_data/Oelkers_2018_Precision_Light_Curves_from_TESS_Full_Fr.pdf |
| 2018 | Stassun | The TESS Input Catalog and Candidate Target List | arXiv:1706.00495 | TIC id and Tmag in the selection | literature/pdf/A_Mission_data/Stassun_2018_The_TESS_Input_Catalog_and_Candidate_Tar.pdf |
| 2018 | Twicken | Kepler Data Validation I -- Architecture, Diagnostic Tests, and Data Products for Vetting Transiting Planet Candidates | arXiv:1803.04526 | tests in the SPOC DV report (Kepler heritage) | literature/pdf/A_Mission_data/Twicken_2018_Kepler_Data_Validation_I_Architecture_Di.pdf |
| 2019 | Feinstein | eleanor: An open-source tool for extracting light curves from the TESS Full-Frame Images | arXiv:1903.09152 |  | literature/pdf/A_Mission_data/Feinstein_2019_eleanor_An_open_source_tool_for_extracti.pdf |
| 2019 | Li | Kepler Data Validation II -- Transit Model Fitting and Multiple-Planet Search | arXiv:1812.00103 |  | literature/pdf/A_Mission_data/Li_2019_Kepler_Data_Validation_II_Transit_Model_.pdf |
| 2019 | Stassun | The Revised TESS Input Catalog and Candidate Target List | arXiv:1905.10694 |  | literature/pdf/A_Mission_data/Stassun_2019_The_Revised_TESS_Input_Catalog_and_Candi.pdf |
| 2020 | Caldwell | TESS Science Processing Operations Center FFI Target List Products | arXiv:2011.05495 |  | literature/pdf/A_Mission_data/Caldwell_2020_TESS_Science_Processing_Operations_Cente.pdf |
| 2020 | Huang | Photometry of 10 Million Stars from the First Two Years of TESS Full Frame Images | arXiv:2011.06459 |  | literature/pdf/A_Mission_data/Huang_2020_Photometry_of_10_Million_Stars_from_the_.pdf |
| 2021 | Guerrero | The TESS Objects of Interest Catalog from the TESS Prime Mission | arXiv:2103.12538 |  | literature/pdf/A_Mission_data/Guerrero_2021_The_TESS_Objects_of_Interest_Catalog_fro.pdf |

## B  Detrending and stellar variability

Stars vary by more than a transit is deep. Each method trades transit depth against residual trend.

Sub-methods: Median / Savitzky-Golay filters (used here, via lightkurve); Spline and self-flat-fielding (K2SFF); Gaussian processes (celerite, K2SC); Trend filtering algorithm (TFA) and wotan biweight.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2005 | Kovacs | A Trend Filtering Algorithm for wide field variability surveys | arXiv:astro-ph/0411724 |  | literature/pdf/B_Detrending/Kovacs_2005_A_Trend_Filtering_Algorithm_for_wide_fie.pdf |
| 2014 | Vanderburg | A Technique for Extracting Highly Precise Photometry for the Two-Wheeled Kepler Mission | arXiv:1408.3853 |  | literature/pdf/B_Detrending/Vanderburg_2014_A_Technique_for_Extracting_Highly_Precis.pdf |
| 2016 | Aigrain | K2SC: Flexible systematics correction and detrending of K2 light curves using Gaussian Process regression | arXiv:1603.09167 |  | literature/pdf/B_Detrending/Aigrain_2016_K2SC_Flexible_systematics_correction_and.pdf |
| 2017 | Foreman-Mackey | Fast and scalable Gaussian process modeling with applications to astronomical time series | arXiv:1703.09710 |  | literature/pdf/B_Detrending/Foreman_Mackey_2017_Fast_and_scalable_Gaussian_process_model.pdf |
| 2019 | Hippke | Wotan: Comprehensive time-series de-trending in Python | arXiv:1906.00966 |  | literature/pdf/B_Detrending/Hippke_2019_Wotan_Comprehensive_time_series_de_trend.pdf |
| 2020 | Barros | Improving transit characterisation with Gaussian process modelling of stellar variability | arXiv:2001.07975 |  | literature/pdf/B_Detrending/Barros_2020_Improving_transit_characterisation_with_.pdf |

## C  Transit search and machine learning

Finding a periodic, box-like dip: least squares in a box, a physical shape, or a neural network trained on labelled candidates.

Sub-methods: Box Least Squares (BLS, used here); Transit Least Squares (physical shape); Lomb-Scargle for periodic signals (RV, rotation); Convolutional networks for triage and vetting; Citizen science (Planet Hunters TESS).

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2002 | Jenkins | Some Tests to Establish Confidence in Planets Discovered by Transit Photometry | doi:10.1086/324143 |  | literature/pdf/C_Transit_search/Jenkins_2002_Some_Tests_to_Establish_Confidence_in_Pl.pdf |
| 2002 | Kovacs | A box-fitting algorithm in the search for periodic transits | arXiv:astro-ph/0206099 | BLS (astropy BoxLeastSquares) | literature/pdf/C_Transit_search/Kovacs_2002_A_box_fitting_algorithm_in_the_search_fo.pdf |
| 2009 | Zechmeister | The generalised Lomb-Scargle periodogram. A new formalism for the floating-mean and Keplerian periodograms | arXiv:0901.2573 |  | literature/pdf/C_Transit_search/Zechmeister_2009_The_generalised_Lomb_Scargle_periodogram.pdf |
| 2013 | Petigura | A Plateau in the Planet Population Below Twice the Size of Earth | arXiv:1304.0460 |  | literature/pdf/C_Transit_search/Petigura_2013_A_Plateau_in_the_Planet_Population_Below.pdf |
| 2016 | Hartman | VARTOOLS: A Program for Analyzing Astronomical Time-Series Data | arXiv:1605.06811 |  | literature/pdf/C_Transit_search/Hartman_2016_VARTOOLS_A_Program_for_Analyzing_Astrono.pdf |
| 2018 | Ansdell | Scientific Domain Knowledge Improves Exoplanet Transit Classification with Deep Learning | arXiv:1810.13434 |  | literature/pdf/C_Transit_search/Ansdell_2018_Scientific_Domain_Knowledge_Improves_Exo.pdf |
| 2018 | Pearson | Searching for Exoplanets Using Artificial Intelligence | arXiv:1706.04319 |  | literature/pdf/C_Transit_search/Pearson_2018_Searching_for_Exoplanets_Using_Artificia.pdf |
| 2018 | Shallue | Identifying Exoplanets with Deep Learning: A Five Planet Resonant Chain around Kepler-80 and an Eighth Planet around Kepler-90 | arXiv:1712.05044 |  | literature/pdf/C_Transit_search/Shallue_2018_Identifying_Exoplanets_with_Deep_Learnin.pdf |
| 2018 | VanderPlas | Understanding the Lomb-Scargle Periodogram | arXiv:1703.09824 |  | literature/pdf/C_Transit_search/VanderPlas_2018_Understanding_the_Lomb_Scargle_Periodogr.pdf |
| 2019 | Dattilo | Identifying Exoplanets with Deep Learning II: Two New Super-Earths Uncovered by a Neural Network in K2 Data | arXiv:1903.10507 |  | literature/pdf/C_Transit_search/Dattilo_2019_Identifying_Exoplanets_with_Deep_Learnin.pdf |
| 2019 | Heller | Transit least-squares survey - I. Discovery and validation of an Earth-sized planet in the four-planet system K2-32 near the 1:2:5:7 resonance | arXiv:1904.00651 |  | literature/pdf/C_Transit_search/Heller_2019_Transit_least_squares_survey_I_Discovery.pdf |
| 2019 | Hippke | Transit Least Squares: Optimized transit detection algorithm to search for periodic transits of small planets | arXiv:1901.02015 |  | literature/pdf/C_Transit_search/Hippke_2019_Transit_Least_Squares_Optimized_transit_.pdf |
| 2019 | Yu | Identifying Exoplanets with Deep Learning III: Automated Triage and Vetting of TESS Candidates | arXiv:1904.02726 |  | literature/pdf/C_Transit_search/Yu_2019_Identifying_Exoplanets_with_Deep_Learnin.pdf |
| 2020 | Osborn | Rapid Classification of TESS Planet Candidates with Convolutional Neural Networks | arXiv:1902.08544 |  | literature/pdf/C_Transit_search/Osborn_2020_Rapid_Classification_of_TESS_Planet_Cand.pdf |
| 2021 | Armstrong | Exoplanet Validation with Machine Learning: 50 new validated Kepler planets | arXiv:2008.10516 |  | literature/pdf/C_Transit_search/Armstrong_2021_Exoplanet_Validation_with_Machine_Learni.pdf |
| 2021 | Eisner | Planet Hunters TESS II: Findings from the first two years of TESS | arXiv:2011.13944 |  | literature/pdf/C_Transit_search/Eisner_2021_Planet_Hunters_TESS_II_Findings_from_the.pdf |

## D  Transit modelling and inference

Turn a dip into Rp/R, b and a/R with errors that include correlated noise.

Sub-methods: Analytic limb-darkened light curves (Mandel-Agol, batman: used here); Geometry from the light curve (Seager and Mallen-Ornelas, Winn); Limb-darkening laws and priors (Kipping q1,q2: used here; Claret for TESS); MCMC samplers (emcee, affine-invariant: used here); Packages: EXOFAST, juliet, exoplanet; Red noise and finite exposure time (Pont, Kipping).

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 1992 | Gelman | Inference from Iterative Simulation Using Multiple Sequences | doi:10.1214/ss/1177011136 |  | no open PDF |
| 2002 | Mandel | Analytic Light Curves for Planetary Transit Searches | doi:10.1086/345520 | transit model inside batman | literature/pdf/D_Transit_modelling/Mandel_2002_Analytic_Light_Curves_for_Planetary_Tran.pdf |
| 2003 | Seager | On the Unique Solution of Planet and Star Parameters from an Extrasolar Planet Transit Light Curve | arXiv:astro-ph/0206228 | course formulas: depth, duration | literature/pdf/D_Transit_modelling/Seager_2003_On_the_Unique_Solution_of_Planet_and_Sta.pdf |
| 2006 | Pont | The effect of red noise on planetary transit detection | arXiv:astro-ph/0608597 | red-noise factor beta (slide R3) | literature/pdf/D_Transit_modelling/Pont_2006_The_effect_of_red_noise_on_planetary_tra.pdf |
| 2008 | Carter | Analytic Approximations for Transit Light Curve Observables, Uncertainties, and Covariances | arXiv:0805.0238 |  | literature/pdf/D_Transit_modelling/Carter_2008_Analytic_Approximations_for_Transit_Ligh.pdf |
| 2010 | Goodman | Ensemble samplers with affine invariance | doi:10.2140/camcos.2010.5.65 | affine-invariant sampler in emcee | literature/pdf/D_Transit_modelling/Goodman_2010_Ensemble_samplers_with_affine_invariance.pdf |
| 2010 | Hogg | Data analysis recipes: Fitting a model to data | arXiv:1008.4686 |  | literature/pdf/D_Transit_modelling/Hogg_2010_Data_analysis_recipes_Fitting_a_model_to.pdf |
| 2010 | Kipping | Binning is sinning: morphological light-curve distortions due to finite integration time | arXiv:1004.3741 |  | literature/pdf/D_Transit_modelling/Kipping_2010_Binning_is_sinning_morphological_light_c.pdf |
| 2010 | Winn | Transits and Occultations | arXiv:1001.2010 | course formulas: depth, duration | literature/pdf/D_Transit_modelling/Winn_2010_Transits_and_Occultations.pdf |
| 2013 | Eastman | EXOFAST: A fast exoplanetary fitting suite in IDL | arXiv:1206.5798 |  | literature/pdf/D_Transit_modelling/Eastman_2013_EXOFAST_A_fast_exoplanetary_fitting_suit.pdf |
| 2013 | Foreman-Mackey | emcee: The MCMC Hammer | arXiv:1202.3665 | emcee sampler | literature/pdf/D_Transit_modelling/Foreman_Mackey_2013_emcee_The_MCMC_Hammer.pdf |
| 2013 | Kipping | Efficient, uninformative sampling of limb darkening coefficients for two-parameter laws | arXiv:1308.0009 | q1, q2 limb-darkening parameters | literature/pdf/D_Transit_modelling/Kipping_2013_Efficient_uninformative_sampling_of_limb.pdf |
| 2015 | Kreidberg | batman: BAsic Transit Model cAlculatioN in Python | arXiv:1507.08285 | batman light curves | literature/pdf/D_Transit_modelling/Kreidberg_2015_batman_BAsic_Transit_Model_cAlculatioN_i.pdf |
| 2017 | Claret | Limb and gravity-darkening coefficients for the TESS satellite at several metallicities, surface gravities, and microturbulent velocities | arXiv:1804.10295 |  | literature/pdf/D_Transit_modelling/Claret_2017_Limb_and_gravity_darkening_coefficients_.pdf |
| 2017 | Sharma | Markov Chain Monte Carlo Methods for Bayesian Data Analysis in Astronomy | arXiv:1706.01629 |  | literature/pdf/D_Transit_modelling/Sharma_2017_Markov_Chain_Monte_Carlo_Methods_for_Bay.pdf |
| 2018 | Hogg | Data analysis recipes: Using Markov Chain Monte Carlo | arXiv:1710.06068 |  | literature/pdf/D_Transit_modelling/Hogg_2018_Data_analysis_recipes_Using_Markov_Chain.pdf |
| 2019 | Espinoza | Juliet: a versatile modelling tool for transiting and non-transiting exoplanetary systems | arXiv:1812.08549 |  | literature/pdf/D_Transit_modelling/Espinoza_2019_Juliet_a_versatile_modelling_tool_for_tr.pdf |
| 2020 | Agol | Analytic Planetary Transit Light Curves and Derivatives for Stars with Polynomial Limb Darkening | arXiv:1908.03222 |  | literature/pdf/D_Transit_modelling/Agol_2020_Analytic_Planetary_Transit_Light_Curves_.pdf |
| 2021 | Foreman-Mackey | exoplanet: Gradient-based probabilistic inference for exoplanet data & other astronomical time series | arXiv:2105.01994 |  | literature/pdf/D_Transit_modelling/Foreman_Mackey_2021_exoplanet_Gradient_based_probabilistic_i.pdf |

## E  Vetting and statistical validation

A dip is not a planet until blends and eclipsing binaries are excluded.

Sub-methods: Odd-even depth and secondary-eclipse tests; Centroid and background tests; Blend scenarios and false-positive probability (vespa, TRICERATOPS); False-positive rates of Kepler; Ground-based photometric follow-up.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2011 | Torres | Modeling Kepler transit light curves as false positives: Rejection of blend scenarios for Kepler-9, and validation of Kepler-9d, a super-Earth-size planet in a multiple system | arXiv:1008.4393 |  | literature/pdf/E_Vetting_validation/Torres_2011_Modeling_Kepler_transit_light_curves_as_.pdf |
| 2012 | Morton | An Efficient Automated Validation Procedure for Exoplanet Transit Candidates | arXiv:1206.1568 |  | literature/pdf/E_Vetting_validation/Morton_2012_An_Efficient_Automated_Validation_Proced.pdf |
| 2013 | Bryson | Identification of Background False Positives from Kepler Data | arXiv:1303.0052 |  | literature/pdf/E_Vetting_validation/Bryson_2013_Identification_of_Background_False_Posit.pdf |
| 2013 | Fressin | The false positive rate of Kepler and the occurrence of planets | arXiv:1301.0842 |  | literature/pdf/E_Vetting_validation/Fressin_2013_The_false_positive_rate_of_Kepler_and_th.pdf |
| 2016 | Morton | FALSE POSITIVE PROBABILITIES FOR ALL KEPLER OBJECTS OF INTEREST: 1284 NEWLY VALIDATED PLANETS AND 428 LIKELY FALSE POSITIVES | doi:10.3847/0004-637x/822/2/86 |  | literature/pdf/E_Vetting_validation/Morton_2016_FALSE_POSITIVE_PROBABILITIES_FOR_ALL_KEP.pdf |
| 2016 | Santerne | SOPHIE velocimetry of Kepler transit candidates XVII. The physical properties of giant exoplanets within 400 days of period | arXiv:1511.00643 |  | literature/pdf/E_Vetting_validation/Santerne_2016_SOPHIE_velocimetry_of_Kepler_transit_can.pdf |
| 2017 | Collins | AstroImageJ: Image Processing and Photometric Extraction for Ultra-Precise Astronomical Light Curves | arXiv:1601.02622 |  | literature/pdf/E_Vetting_validation/Collins_2017_AstroImageJ_Image_Processing_and_Photome.pdf |
| 2017 | Gunther | Centroid vetting of transiting planet candidates from the Next Generation Transit Survey | arXiv:1707.07978 |  | literature/pdf/E_Vetting_validation/Gunther_2017_Centroid_vetting_of_transiting_planet_ca.pdf |
| 2021 | Giacalone | Vetting of 384 TESS Objects of Interest with TRICERATOPS and Statistical Validation of 12 Planet Candidates | arXiv:2002.00691 |  | literature/pdf/E_Vetting_validation/Giacalone_2021_Vetting_of_384_TESS_Objects_of_Interest_.pdf |

## F  Stellar characterisation

The planet radius is only as good as the stellar radius: 1 to 7 % of our error budget.

Sub-methods: Masses and radii of normal stars; Gaia-based radii (Berger, Fulton and Petigura); Stellar evolution models (Dartmouth); M-dwarf scaling relations (Mann); Asteroseismology.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2008 | Dotter | The Dartmouth Stellar Evolution Database | arXiv:0804.4473 |  | literature/pdf/F_Stellar_characterisation/Dotter_2008_The_Dartmouth_Stellar_Evolution_Database.pdf |
| 2010 | Torres | Accurate masses and radii of normal stars: modern results and applications | arXiv:0908.2624 |  | literature/pdf/F_Stellar_characterisation/Torres_2010_Accurate_masses_and_radii_of_normal_star.pdf |
| 2013 | Huber | Fundamental Properties of Stars using Asteroseismology from Kepler & CoRoT and Interferometry from the CHARA Array | arXiv:1210.0012 |  | literature/pdf/F_Stellar_characterisation/Huber_2013_Fundamental_Properties_of_Stars_using_As.pdf |
| 2015 | Dressing | The Occurrence of Potentially Habitable Planets Orbiting M Dwarfs Estimated from the Full Kepler Dataset and an Empirical Measurement of the Detection Sensitivity | arXiv:1501.01623 |  | literature/pdf/F_Stellar_characterisation/Dressing_2015_The_Occurrence_of_Potentially_Habitable_.pdf |
| 2015 | Mann | How to Constrain Your M Dwarf: measuring effective temperature, bolometric luminosity, mass, and radius | arXiv:1501.01635 |  | literature/pdf/F_Stellar_characterisation/Mann_2015_How_to_Constrain_Your_M_Dwarf_measuring_.pdf |
| 2015 | Winn | The Occurrence and Architecture of Exoplanetary Systems | arXiv:1410.4199 |  | literature/pdf/F_Stellar_characterisation/Winn_2015_The_Occurrence_and_Architecture_of_Exopl.pdf |
| 2018 | Berger | Revised Radii of Kepler Stars and Planets Using Gaia Data Release 2 | arXiv:1805.00231 |  | literature/pdf/F_Stellar_characterisation/Berger_2018_Revised_Radii_of_Kepler_Stars_and_Planet.pdf |
| 2018 | Fulton | The California Kepler Survey VII. Precise Planet Radii Leveraging Gaia DR2 Reveal the Stellar Mass Dependence of the Planet Radius Gap | arXiv:1805.01453 |  | literature/pdf/F_Stellar_characterisation/Fulton_2018_The_California_Kepler_Survey_VII_Precise.pdf |

## G  Populations, occurrence and composition

What a radius means once you know many: the radius valley, mass-radius laws, composition curves, occurrence rates.

Sub-methods: Radius valley and evaporation; Mass-radius relations and composition curves (Zeng: used in our figure); Probabilistic mass-radius (Chen and Kipping, Wolfgang); Occurrence rates from Kepler; Core-powered mass loss.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2007 | Seager | Mass-Radius Relationships for Solid Exoplanets | arXiv:0707.2895 |  | literature/pdf/G_Population_composition/Seager_2007_Mass_Radius_Relationships_for_Solid_Exop.pdf |
| 2012 | Howard | Planet Occurrence within 0.25 AU of Solar-type Stars from Kepler | arXiv:1103.2541 |  | literature/pdf/G_Population_composition/Howard_2012_Planet_Occurrence_within_0_25_AU_of_Sola.pdf |
| 2013 | Owen | Kepler planets: a tale of evaporation | arXiv:1303.3899 |  | literature/pdf/G_Population_composition/Owen_2013_Kepler_planets_a_tale_of_evaporation.pdf |
| 2014 | Lopez | The Role of Core Mass in Controlling Evaporation: the Kepler Radius Distribution and the Kepler-36 Density Dichotomy | arXiv:1305.0269 |  | literature/pdf/G_Population_composition/Lopez_2014_The_Role_of_Core_Mass_in_Controlling_Eva.pdf |
| 2014 | Weiss | The Mass-Radius Relation for 65 Exoplanets Smaller than 4 Earth Radii | arXiv:1312.0936 |  | literature/pdf/G_Population_composition/Weiss_2014_The_Mass_Radius_Relation_for_65_Exoplane.pdf |
| 2015 | Burke | Terrestrial Planet Occurrence Rates for the Kepler GK Dwarf Sample | arXiv:1506.04175 |  | literature/pdf/G_Population_composition/Burke_2015_Terrestrial_Planet_Occurrence_Rates_for_.pdf |
| 2015 | Rogers | MOST 1.6 EARTH-RADIUS PLANETS ARE NOT ROCKY | doi:10.1088/0004-637x/801/1/41 |  | literature/pdf/G_Population_composition/Rogers_2015_i_MOST_i_1_6_EARTH_RADIUS_PLANETS_ARE_NO.pdf |
| 2016 | Wolfgang | Probabilistic Mass-Radius Relationship for Sub-Neptune-Sized Planets | arXiv:1504.07557 |  | literature/pdf/G_Population_composition/Wolfgang_2016_Probabilistic_Mass_Radius_Relationship_f.pdf |
| 2016 | Zeng | Mass-Radius Relation for Rocky Planets based on PREM | arXiv:1512.08827 |  | literature/pdf/G_Population_composition/Zeng_2016_Mass_Radius_Relation_for_Rocky_Planets_b.pdf |
| 2017 | Chen | Probabilistic Forecasting of the Masses and Radii of Other Worlds | arXiv:1603.08614 |  | literature/pdf/G_Population_composition/Chen_2017_Probabilistic_Forecasting_of_the_Masses_.pdf |
| 2017 | Fulton | The California-Kepler Survey. III. A Gap in the Radius Distribution of Small Planets | arXiv:1703.10375 |  | literature/pdf/G_Population_composition/Fulton_2017_The_California_Kepler_Survey_III_A_Gap_i.pdf |
| 2017 | Owen | The evaporation valley in the Kepler planets | arXiv:1705.10810 |  | literature/pdf/G_Population_composition/Owen_2017_The_evaporation_valley_in_the_Kepler_pla.pdf |
| 2018 | Petigura | The California-Kepler Survey. IV. Metal-rich Stars Host a Greater Diversity of Planets | arXiv:1712.04042 |  | literature/pdf/G_Population_composition/Petigura_2018_The_California_Kepler_Survey_IV_Metal_ri.pdf |
| 2018 | Van Eylen | An asteroseismic view of the radius valley: stripped cores, not born rocky | arXiv:1710.05398 |  | literature/pdf/G_Population_composition/Van_Eylen_2018_An_asteroseismic_view_of_the_radius_vall.pdf |
| 2019 | Gupta | Sculpting the Valley in the Radius Distribution of Small Exoplanets as a by-product of Planet Formation: The Core-Powered Mass-Loss Mechanism | arXiv:1811.03202 |  | literature/pdf/G_Population_composition/Gupta_2019_Sculpting_the_Valley_in_the_Radius_Distr.pdf |
| 2019 | Hardegree-Ullman | Scaling K2. I. Revised Parameters for 222,088 K2 Stars and a K2 Planet Radius Valley at 1.9 R ⊕ | doi:10.3847/1538-4365/ab7230 |  | literature/pdf/G_Population_composition/Hardegree_Ullman_2019_Scaling_K2_I_Revised_Parameters_for_222_.pdf |
| 2019 | Hsu | Occurrence Rates of Planets orbiting FGK Stars: Combining Kepler DR25, Gaia DR2 and Bayesian Inference | arXiv:1902.01417 |  | literature/pdf/G_Population_composition/Hsu_2019_Occurrence_Rates_of_Planets_orbiting_FGK.pdf |
| 2019 | Zeng | Growth Model Interpretation of Planet Size Distribution | arXiv:1906.04253 | composition curves in the mass-radius plot | literature/pdf/G_Population_composition/Zeng_2019_Growth_Model_Interpretation_of_Planet_Si.pdf |
| 2020 | Kunimoto | Searching the Entirety of Kepler Data. II. Occurrence Rate Estimates for FGK Stars | arXiv:2004.05296 |  | literature/pdf/G_Population_composition/Kunimoto_2020_Searching_the_Entirety_of_Kepler_Data_II.pdf |
| 2021 | Bryson | The Occurrence of Rocky Habitable Zone Planets Around Solar-Like Stars from Kepler Data | arXiv:2010.14812 |  | literature/pdf/G_Population_composition/Bryson_2021_The_Occurrence_of_Rocky_Habitable_Zone_P.pdf |

## H  Classic discoveries and science cases

From the first exoplanet around a Sun-like star to atmospheres: why a transit radius matters.

Sub-methods: Radial-velocity discovery (51 Peg b); First transits (HD 209458 b); Kepler and K2; TESS first results; Atmospheres and clouds; Habitable zone and TSM metrics.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 1995 | Mayor | A Jupiter-mass companion to a solar-type star | doi:10.1038/378355a0 |  | no open PDF |
| 2000 | Charbonneau | Detection of Planetary Transits Across a Sun-like Star | arXiv:astro-ph/9911436 | planet 3 (HD 209458 b) and classic transit | literature/pdf/H_Classic_discoveries/Charbonneau_2000_Detection_of_Planetary_Transits_Across_a.pdf |
| 2000 | Henry | A Transiting “51 Peg–like” Planet | doi:10.1086/312458 |  | literature/pdf/H_Classic_discoveries/Henry_2000_A_Transiting_51_Peg_like_Planet.pdf |
| 2002 | Charbonneau | Detection of an Extrasolar Planet Atmosphere | arXiv:astro-ph/0111544 |  | literature/pdf/H_Classic_discoveries/Charbonneau_2002_Detection_of_an_Extrasolar_Planet_Atmosp.pdf |
| 2007 | Knutson | A map of the day-night contrast of the extrasolar planet HD 189733b | arXiv:0705.0993 |  | literature/pdf/H_Classic_discoveries/Knutson_2007_A_map_of_the_day_night_contrast_of_the_e.pdf |
| 2010 | Borucki | Kepler Planet-Detection Mission: Introduction and First Results | doi:10.1126/science.1185402 |  | literature/pdf/H_Classic_discoveries/Borucki_2010_Kepler_Planet_Detection_Mission_Introduc.pdf |
| 2013 | Batalha | Planetary Candidates Observed by Kepler, III: Analysis of the First 16 Months of Data | arXiv:1202.5852 |  | literature/pdf/H_Classic_discoveries/Batalha_2013_Planetary_Candidates_Observed_by_Kepler_.pdf |
| 2013 | Kopparapu | Habitable Zones Around Main-Sequence Stars: New Estimates | arXiv:1301.6674 |  | literature/pdf/H_Classic_discoveries/Kopparapu_2013_Habitable_Zones_Around_Main_Sequence_Sta.pdf |
| 2014 | Howell | The K2 Mission: Characterization and Early results | arXiv:1402.5163 |  | literature/pdf/H_Classic_discoveries/Howell_2014_The_K2_Mission_Characterization_and_Earl.pdf |
| 2014 | Kreidberg | Clouds in the atmosphere of the super-Earth exoplanet GJ 1214b | arXiv:1401.0022 |  | literature/pdf/H_Classic_discoveries/Kreidberg_2014_Clouds_in_the_atmosphere_of_the_super_Ea.pdf |
| 2016 | Fischer | State of the Field: Extreme Precision Radial Velocities | arXiv:1602.07939 |  | literature/pdf/H_Classic_discoveries/Fischer_2016_State_of_the_Field_Extreme_Precision_Rad.pdf |
| 2016 | Sing | A continuum from clear to cloudy hot-Jupiter exoplanets without primordial water depletion | arXiv:1512.04341 |  | literature/pdf/H_Classic_discoveries/Sing_2016_A_continuum_from_clear_to_cloudy_hot_Jup.pdf |
| 2017 | Gillon | Seven temperate terrestrial planets around the nearby ultracool dwarf star TRAPPIST-1 | arXiv:1703.01424 |  | literature/pdf/H_Classic_discoveries/Gillon_2017_Seven_temperate_terrestrial_planets_arou.pdf |
| 2018 | Gandolfi | TESS's first planet: a super-Earth transiting the naked-eye star $π$ Mensae | arXiv:1809.07573 | independent analysis of pi Men c | literature/pdf/H_Classic_discoveries/Gandolfi_2018_TESS_s_first_planet_a_super_Earth_transi.pdf |
| 2018 | Huang | TESS Discovery of a Transiting Super-Earth in the $π$ Mensae System | arXiv:1809.05967 | paper rebuilt in section 2 | literature/pdf/H_Classic_discoveries/Huang_2018_TESS_Discovery_of_a_Transiting_Super_Ear.pdf |
| 2018 | Kempton | A Framework for Prioritizing the TESS Planetary Candidates Most Amenable to Atmospheric Characterization | arXiv:1805.03671 |  | literature/pdf/H_Classic_discoveries/Kempton_2018_A_Framework_for_Prioritizing_the_TESS_Pl.pdf |
| 2018 | Thompson | Planetary Candidates Observed by Kepler. VIII. A Fully Automated Catalog With Measured Completeness and Reliability Based on Data Release 25 | arXiv:1710.06758 |  | literature/pdf/H_Classic_discoveries/Thompson_2018_Planetary_Candidates_Observed_by_Kepler_.pdf |
| 2019 | Dragomir | TESS delivers its first Earth-sized planet and a warm sub-Neptune | arXiv:1901.00051 |  | literature/pdf/H_Classic_discoveries/Dragomir_2019_TESS_delivers_its_first_Earth_sized_plan.pdf |
| 2019 | Vanderspek | TESS Discovery of an ultra-short-period planet around the nearby M dwarf LHS 3844 | arXiv:1809.07242 |  | literature/pdf/H_Classic_discoveries/Vanderspek_2019_TESS_Discovery_of_an_ultra_short_period_.pdf |

## I  Discovery papers of the planets in this project

Primary literature behind each catalog value that we compare to.

Sub-methods: One or two discovery or confirmation papers per planet.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2005 | Bouchy | ELODIE metallicity-biased search for transiting Hot Jupiters II. A very hot Jupiter transiting the bright K star HD189733 | arXiv:astro-ph/0510119 | planet 2, HD 189733 b | literature/pdf/I_Project_planets/Bouchy_2005_ELODIE_metallicity_biased_search_for_tra.pdf |
| 2009 | Hellier | An orbital period of 0.94 days for the hot-Jupiter planet WASP-18b | doi:10.1038/nature08245 | planet 4, WASP-18 b | no open PDF |
| 2012 | Hellier | Seven transiting hot Jupiters from WASP-South, Euler and TRAPPIST: WASP-47b, WASP-55b, WASP-61b, WASP-62b, WASP-63b, WASP-66b and WASP-67b | doi:10.1111/j.1365-2966.2012.21780.x | planet 5, WASP-62 b | literature/pdf/I_Project_planets/Hellier_2012_Seven_transiting_hot_Jupiters_from_WASP_.pdf |
| 2015 | Berta-Thompson | A rocky planet transiting a nearby low-mass star | arXiv:1511.03550 | planet 9, GJ 1132 b | literature/pdf/I_Project_planets/Berta_Thompson_2015_A_rocky_planet_transiting_a_nearby_low_m.pdf |
| 2016 | Crossfield | 197 Candidates and 104 Validated Planets in K2's First Five Fields | arXiv:1607.05263 |  | literature/pdf/I_Project_planets/Crossfield_2016_197_Candidates_and_104_Validated_Planets.pdf |
| 2018 | Malavolta | An ultra-short period rocky super-Earth with a secondary eclipse and a Neptune-like companion around K2-141 | arXiv:1801.03502 | planet 10, K2-141 b | literature/pdf/I_Project_planets/Malavolta_2018_An_ultra_short_period_rocky_super_Earth_.pdf |
| 2019 | Gunther | A super-Earth and two sub-Neptunes transiting the nearby and quiet M dwarf TOI-270 | arXiv:1903.06107 | planet 7, TOI-270 c | literature/pdf/I_Project_planets/Gunther_2019_A_super_Earth_and_two_sub_Neptunes_trans.pdf |
| 2019 | Newton | TESS Hunt for Young and Maturing Exoplanets (THYME): A Planet in the 45 Myr Tucana–Horologium Association | doi:10.3847/2041-8213/ab2988 | stress test, DS Tuc A b | literature/pdf/I_Project_planets/Newton_2019_TESS_Hunt_for_Young_and_Maturing_Exoplan.pdf |
| 2020 | Jenkins | An Ultra-Hot Neptune in the Neptune desert | arXiv:2009.12832 | planet 6, LTT 9779 b | literature/pdf/I_Project_planets/Jenkins_2020_An_Ultra_Hot_Neptune_in_the_Neptune_dese.pdf |
| 2020 | Pepper | TESS Reveals HD 118203 b to be a Transiting Planet | arXiv:1911.05150 | planet 1, HD 118203 b | literature/pdf/I_Project_planets/Pepper_2020_TESS_Reveals_HD_118203_b_to_be_a_Transit.pdf |
| 2020 | Plavchan | A planet within the debris disk around the pre-main-sequence star AU Microscopii | arXiv:2006.13248 | stress test, AU Mic b | literature/pdf/I_Project_planets/Plavchan_2020_A_planet_within_the_debris_disk_around_t.pdf |
| 2021 | Winters | A Second Planet Transiting LTT 1445A and a Determination of the Masses of Both Worlds | arXiv:2107.14737 | planet 8, LTT 1445 A b | literature/pdf/I_Project_planets/Winters_2021_A_Second_Planet_Transiting_LTT_1445A_and.pdf |

## J  Phase curves, eclipses and timing

Light from the planet itself, and the time system we measure in.

Sub-methods: Phase curve and secondary eclipse (WASP-18 b); Barycentric Julian date accuracy (BTJD = BJDTDB  2457000).

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 2010 | Eastman | Achieving better than 1 minute accuracy in the Heliocentric and Barycentric Julian Dates | arXiv:1005.4415 | BTJD time system | literature/pdf/J_Phase_curves_timing/Eastman_2010_Achieving_better_than_1_minute_accuracy_.pdf |
| 2019 | Shporer | TESS full orbital phase curve of the WASP-18b system | arXiv:1811.06020 | WASP-18 b phase 0.5 deficit | literature/pdf/J_Phase_curves_timing/Shporer_2019_TESS_full_orbital_phase_curve_of_the_WAS.pdf |

## K  Search history: how exoplanets were found

The path from pulsar timing and Doppler velocities to ground transit surveys, space photometry and atmosphere studies, with the paper behind each step.

Sub-methods: Doppler and pulsar timing (1992, 1995, ESPRESSO); Ground transit surveys (HD 209458 b, TrES, HAT, SuperWASP, KELT, MEarth); Space photometry (CoRoT, Kepler, K2, TESS, CHEOPS, PLATO); Atmospheres and follow-up (HST, Spitzer, JWST); Microlensing and direct imaging for context.

| Year | First author | Title | Reference | Used in this project | PDF |
|---|---|---|---|---|---|
| 1984 | Borucki | The photometric method of detecting other planetary systems | doi:10.1016/0019-1035(84)90102-7 |  | no open PDF |
| 1992 | Wolszczan | A planetary system around the millisecond pulsar PSR1257 + 12 | doi:10.1038/355145a0 |  | no open PDF |
| 2003 | Konacki | An extrasolar planet that transits the disk of its parent star | doi:10.1038/nature01379 |  | no open PDF |
| 2004 | Alonso | TrES-1: The Transiting Planet of a Bright K0 V Star | doi:10.1086/425256 |  | literature/pdf/K_Search_history/Alonso_2004_TrES_1_The_Transiting_Planet_of_a_Bright.pdf |
| 2004 | Bakos | Wide‐Field Millimagnitude Photometry with the HAT: A Tool for Extrasolar Planet Detection | doi:10.1086/382735 |  | literature/pdf/K_Search_history/Bakos_2004_Wide_Field_Millimagnitude_Photometry_wit.pdf |
| 2004 | Bond | OGLE 2003-BLG-235/MOA 2003-BLG-53: A planetary microlensing event | arXiv:astro-ph/0404309 |  | literature/pdf/K_Search_history/Bond_2004_OGLE_2003_BLG_235_MOA_2003_BLG_53_A_plan.pdf |
| 2005 | Charbonneau | Detection of Thermal Emission from an Extrasolar Planet | arXiv:astro-ph/0503457 |  | literature/pdf/K_Search_history/Charbonneau_2005_Detection_of_Thermal_Emission_from_an_Ex.pdf |
| 2005 | Deming | Infrared radiation from an extrasolar planet | arXiv:astro-ph/0503554 |  | literature/pdf/K_Search_history/Deming_2005_Infrared_radiation_from_an_extrasolar_pl.pdf |
| 2006 | Gardner | The James Webb Space Telescope | arXiv:astro-ph/0606175 |  | literature/pdf/K_Search_history/Gardner_2006_The_James_Webb_Space_Telescope.pdf |
| 2006 | Pollacco | The WASP Project and the SuperWASP Cameras | arXiv:astro-ph/0608454 |  | literature/pdf/K_Search_history/Pollacco_2006_The_WASP_Project_and_the_SuperWASP_Camer.pdf |
| 2007 | Pepper | The Kilodegree Extremely Little Telescope (KELT): A Small Robotic Telescope for Large-Area Synoptic Surveys | arXiv:0704.0460 |  | literature/pdf/K_Search_history/Pepper_2007_The_Kilodegree_Extremely_Little_Telescop.pdf |
| 2008 | Barge | Transiting exoplanets from the CoRoT space mission I - CoRoT-Exo-1b: a low-density short-period planet around a G0V star | arXiv:0803.3202 |  | literature/pdf/K_Search_history/Barge_2008_Transiting_exoplanets_from_the_CoRoT_spa.pdf |
| 2008 | Marois | Direct Imaging of Multiple Planets Orbiting the Star HR 8799 | arXiv:0811.2606 |  | literature/pdf/K_Search_history/Marois_2008_Direct_Imaging_of_Multiple_Planets_Orbit.pdf |
| 2008 | Nutzman | Design Considerations for a Ground-based Transit Search for Habitable Planets Orbiting M dwarfs | arXiv:0709.2879 |  | literature/pdf/K_Search_history/Nutzman_2008_Design_Considerations_for_a_Ground_based.pdf |
| 2009 | Auvergne | The CoRoT satellite in flight : description and performance | arXiv:0901.2206 |  | literature/pdf/K_Search_history/Auvergne_2009_The_CoRoT_satellite_in_flight_descriptio.pdf |
| 2010 | Koch | Kepler Mission Design, Realized Photometric Performance, and Early Science | arXiv:1001.0268 |  | literature/pdf/K_Search_history/Koch_2010_Kepler_Mission_Design_Realized_Photometr.pdf |
| 2011 | Borucki | Characteristics of Kepler Planetary Candidates Based on the First Data Set: The Majority are Found to be Neptune-Size and Smaller | arXiv:1006.2799 |  | literature/pdf/K_Search_history/Borucki_2011_Characteristics_of_Kepler_Planetary_Cand.pdf |
| 2014 | Rauer | The PLATO 2.0 Mission | arXiv:1310.0696 |  | literature/pdf/K_Search_history/Rauer_2014_The_PLATO_2_0_Mission.pdf |
| 2015 | Vanderburg | Planetary Candidates from the First Year of the K2 Mission | arXiv:1511.07820 |  | literature/pdf/K_Search_history/Vanderburg_2015_Planetary_Candidates_from_the_First_Year.pdf |
| 2021 | Benz | The CHEOPS mission | arXiv:2009.11633 |  | literature/pdf/K_Search_history/Benz_2021_The_CHEOPS_mission.pdf |
| 2021 | Pepe | ESPRESSO@VLT -- On-sky performance and first results | arXiv:2010.00316 |  | literature/pdf/K_Search_history/Pepe_2021_ESPRESSO_VLT_On_sky_performance_and_firs.pdf |
| 2023 | Ahrer | Early Release Science of the exoplanet WASP-39b with JWST NIRCam | arXiv:2211.10489 |  | literature/pdf/K_Search_history/Ahrer_2023_Early_Release_Science_of_the_exoplanet_W.pdf |
