# BanffApplicationSystem
To apply the Banff classification based on individual Banff scores and additional clinico-biological parameters.

This repository contains the code of the web-based application Banff Application System, available at: **pending**.

**Current supported Banff classificatio is: 2022-2024 updates.**

**Usage instructions**:
A pandas dataframe should be provided (from a csv or excel file). The first row (header) should include the name of the variables. Use the provided template to know the exact name of the variables that should be provided. Do not duplicate any columns, each variable should have only one column. Missing variables should be blank cells. The order of the variables in the excel sheet does not matter.
The process will create four additional columns to your input excel:
- **TI diagnosis**: tubulo-interstitial-related diagnosis (TCMR and/or polyomavirus nephropathy). Blank if no reached rejection phenotype.
- **MVI diagnosis**: microvascular inflammation-related diagnosis (MVI/AMR). Blank if no reached rejection phenotype.
- **warning**: warnings are displayed when major variables are missing, that could lead to miss some rejection cases.
- **comment**: when appropriate, comments are proposed, according to the 2024 Banff classification report.

An example is provided in the jupyter notebook.

The list of variables is:
- **g**, **ptc**, **i**, **t**, **v**, **ci**, **ct**, **ti**, **i_IFTA**, **t_IFTA**: corresponding Banff scores, from 0 to 3
- **cg**: cg Banff score, from 0 to 3 (1a/1b => 1)
- **C4d**: **C4d score as a binary variable 0/1**. It is up to you to binarize the C4d Banff score from 0 to 3 into 0/1 based on your technics (immunofluorescence positive if Banff score > 1, chromogenic IHC positive if Banff score > 0).
- **pvl**: pvl Banff score, from 0 to 3
- **TMA**: binary variable 0/1, 1 if histological lesions of thrombotic microangiopathy are observed.
- **ATI**: binary variable 0/1, 1 if histological acute tubular injury is present
- **ptcml**: binary variable 0/1, 1 if severe peritubular capillary basement membrane multilayering is present by electron microscopy
- **current_DSA**: binary variable 0/1, 1 if presence of DSA in the serum at time of the biopsy
- **historical_DSA**: binary variable 0/1, 1 if anteriority of DSA detection
- h**istorical_AMR**: binary variable 0/1, 1 if anteriority of AMR
- **transcripts_MVI**: binary variable 0/1, 1 if tissue transcriptomics is in favor of an MVI/AMR-related diagnosis
- **transcripts_TI**: binary variable 0/1, 1 if tissue transcriptomics is in favor of an tubulo-interstitial/TCMR-related diagnosis
- **infection**: binary variable 0/1, 1 if presence of an infection-related nephritis. Will be automatically set to 1 if pvl is > 0.
- **recurrent_GN**: binary variable 0/1, 1 if presence of recurrent or de novo glomerulonephritis.
- **chronic_transplant_arteriopathy**: binary variable 0/1, 1 if presence of “chronic allograft arteriopathy” is present (arterial intimal fibrosis with mononuclear cell infiltration in fibrosis, and formation of neointima).
- **ABOi**: binary variable 0/1, 1 if current transplantation is in a ABO incompatible context


