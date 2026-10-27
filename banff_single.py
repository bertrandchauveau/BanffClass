# COPYRIGHT © 2026 KU Leuven and Université de Bordeaux

import numpy as np
import pandas as pd

#apply Banff 2024 on a single case
def apply_Banff_2024_single(banff_dict):
    #define variable
    g = banff_dict['g']
    ptc = banff_dict['ptc']
    i = banff_dict['i']
    t = banff_dict['t']
    v = banff_dict['v']
    cg = banff_dict['cg']
    ci = banff_dict['ci']
    ct = banff_dict['ct']
    ti = banff_dict['ti']
    i_IFTA = banff_dict['i-IFTA']
    t_IFTA = banff_dict['t-IFTA']
    C4d = banff_dict['C4d']
    pvl = banff_dict['pvl']
    TMA = banff_dict['TMA']
    ptcml = banff_dict['ptcml']
    current_DSA = banff_dict['current DSA']
    historical_DSA = banff_dict['historical DSA']
    historical_AMR = banff_dict['historical AMR']
    transcripts_MVI = banff_dict['transcripts MVI']
    transcripts_TI = banff_dict['transcripts TI']
    infection = banff_dict['infection']
    recurrent_GN = banff_dict['recurrent/de novo GN']
    ATI = banff_dict['ATI']
    chronic_transplant_arteriopathy = banff_dict['chronic transplant arteriopathy']
    ABOi = banff_dict['ABOi']
    cv = banff_dict['cv']
    
    #check for missing core variables
    warn_var_list = []
    core_variables_names = ['g', 'ptc', 'i', 't', 'v', 'cg', 'C4d', 'current DSA', 'ti', 'i-IFTA', 't-IFTA']
    core_variables = [g, ptc, i, t, v, cg, C4d, current_DSA, ti, i_IFTA, t_IFTA]
    nan_variables = []
    nan_var_dict = {'g':'AMR', 'ptc':'AMR', 'i':'TCMR', 't':'TCMR', 'v':'TCMR and/or AMR', 'cg':'cAMR', 'C4d':'AMR', 'current DSA':'AMR', 'ti':'caTCMR', 'i-IFTA':'caTCMR', 't-IFTA':'caTCMR'}
    impact_cat = []
    for var_name, variable in zip(core_variables_names, core_variables):
        if np.isnan(variable):
            nan_variables.append(var_name)
            impact_cat.append(nan_var_dict[var_name])
    if len(nan_variables)>0:
        impact_cat = list(np.unique(impact_cat))
        warn_var_list.append(f'Missing core variables for correct classification of {", ".join(impact_cat)}: {", ".join(nan_variables)}')
    
    #TI related diagnoses
    TI_diagnosis_list = []
    TCMR_diagnosis_list = []
    infection_list = []
    warn_TI_list = []
    
    if infection >0:
        infection_list.append("Infection-related nephritis")
    if pvl >0:
        infection_list.append("Polyomavirus nephropathy")
        infection=1
    
    #Acute TCMR
    if i >=2 and t >=2:
        if v==1:
            TCMR_diagnosis_list.append("Acute TCMR IIA")
        if v==2:
            TCMR_diagnosis_list.append("Acute TCMR IIB")
        if v==3:
            TCMR_diagnosis_list.append("Acute TCMR III")
        if (v == 0 or np.isnan(v)):
            if t==2:
                TCMR_diagnosis_list.append("Acute TCMR IA")
            if t==3:
                TCMR_diagnosis_list.append("Acute TCMR IB")
    else:
        if v==1:
            TCMR_diagnosis_list.append("Acute TCMR IIA")
        if v==2:
            TCMR_diagnosis_list.append("Acute TCMR IIB")
        if v==3:
            TCMR_diagnosis_list.append("Acute TCMR III")
        if (v == 0 or np.isnan(v)) and i > 0 and t > 0:
            TCMR_diagnosis_list.append("Borderline changes")
            
    #Chronic active TCMR
    if ti >=2 and i_IFTA >=2 and (t == 3 or t_IFTA == 3):
        TCMR_diagnosis_list.append("Chronic active TCMR IB")
    if ti >=2 and i_IFTA >=2 and (t == 2 or t_IFTA == 2) and t != 3 and t_IFTA != 3: #not IB
        TCMR_diagnosis_list.append("Chronic active TCMR IA")
    if chronic_transplant_arteriopathy ==1:
        TCMR_diagnosis_list.append("Chronic active TCMR II")
    
    #check for diagnosis combination
    #accepting infection-related nephritis and v+ as combined rejection and nephritis. Warning otherwise while favoring infection.
    if len(infection_list)>0 and len(TCMR_diagnosis_list)>0 and any(['TCMR II' in element for element in TCMR_diagnosis_list]):
        #subselect only TCMR grade >= II diagnoses (if concomittant caTCMR)
        TCMR_diagnosis_list = [dg for dg in TCMR_diagnosis_list if 'TCMR II' in dg]
        TI_diagnosis_list = infection_list + TCMR_diagnosis_list
    elif len(infection_list)>0 and len(TCMR_diagnosis_list)>0 and not any(['TCMR II' in element for element in TCMR_diagnosis_list]):
        TI_diagnosis_list = infection_list
        warn_TI_list.append('Tubulo-interstitial infiltrate could be related to infection, but is also above threshold for T cell-mediated alloimmune process. Clinicopathological correlation is required.')
    elif len(infection_list)>0 and len(TCMR_diagnosis_list)==0:
        TI_diagnosis_list = infection_list
    else:
        TI_diagnosis_list = TCMR_diagnosis_list
    
    #MVI/AMR
    #consider C4d as negative if ABOi transplantation
    if ABOi > 0:
        C4d=0
    
    MVI_diagnosis_list = []
    criterion_list = []
    warn_MVI_list = []
    
    #(chronic) active AMR
    #criterion 1
    if v > 0 or TMA > 0 or (g > 0 or (ptc > 0 and not (any(['TCMR' in element for element in TI_diagnosis_list]) or 'Borderline changes' in TI_diagnosis_list or 'Polyomavirus nephropathy' in TI_diagnosis_list or infection==1))):
        criterion_list.append('criterion 1')
    #criterion 2
    if transcripts_MVI==1 or C4d > 0 or (np.nansum([g, ptc]) >= 2 and not ((g==0 or np.isnan(g)) and (any(['TCMR' in element for element in TI_diagnosis_list]) or 'Borderline changes' in TI_diagnosis_list or 'Polyomavirus nephropathy' in TI_diagnosis_list or infection==1))): 
        criterion_list.append('criterion 2')
    #criterion 3
    if current_DSA > 0 or C4d > 0:
        criterion_list.append('criterion 3')
    if len(criterion_list)==3 and (cg==0 or np.isnan(cg)) and (ptcml==0 or np.isnan(ptcml)):
        MVI_diagnosis_list.append("Active AMR")
    elif 'criterion 2' in criterion_list and 'criterion 3' in criterion_list and (cg>0 or ptcml>0):
        MVI_diagnosis_list.append("Chronic active AMR")
        if cg >0:
            warn_MVI_list.append("No evidence of chronic TMA or chronic recurrent/de novo glomerulonephritis is required to retain the chronicity of AMR.")
    
    #chronic AMR
    if (cg>0 or ptcml>0) and 'criterion 2' not in criterion_list and (historical_AMR>0 or historical_DSA>0 or current_DSA>0):
        MVI_diagnosis_list.append("Chronic AMR")
    
    #C4d without evidence of rejection
    if C4d >0 and 'criterion 1' not in criterion_list and (cg==0 or np.isnan(cg)) and (ptcml==0 or np.isnan(ptcml)) and transcripts_MVI==0 and not (any(['TCMR' in element for element in TI_diagnosis_list]) or 'Borderline changes' in TI_diagnosis_list):
        MVI_diagnosis_list.append("C4d without evidence of rejection")
    
    #Microvascular inflammation/injury (MVI), DSA-negative and C4d-negative
    if (transcripts_MVI==1 or (np.nansum([g, ptc]) >= 2 and not ((g==0 or np.isnan(g)) and (any(['TCMR' in element for element in TI_diagnosis_list]) or 'Borderline changes' in TI_diagnosis_list or 'Polyomavirus nephropathy' in TI_diagnosis_list or infection==1)))) and C4d==0 and current_DSA==0:
        MVI_diagnosis_list.append("MVI C4d/DSA negative")
    
    #Probable AMR
    if 'criterion 1' in criterion_list and (cg==0 or np.isnan(cg)) and (ptcml==0 or np.isnan(ptcml)) and 'criterion 2' not in criterion_list and current_DSA >0:
        MVI_diagnosis_list.append("Probable AMR")
    
    #C4d staining with acute tubular injury (ATI)
    if ATI>0 and C4d>0 and 'criterion 1' not in criterion_list and (cg==0 or np.isnan(cg)) and (ptcml==0 or np.isnan(ptcml)):
        MVI_diagnosis_list.append("C4d staining with acute tubular injury")
    
    #warning about recurrent GN and MVI related diagnoses
    if (any(['ctive AMR' in element for element in MVI_diagnosis_list]) or "Probable AMR" in MVI_diagnosis_list or "MVI C4d/DSA negative" in MVI_diagnosis_list) and g >0 and recurrent_GN>0:
        warn_MVI_list.append("MVI with glomerulitis is present, matching an MVI-related diagnosis, in the context of recurrent or de novo glomerulonephritis. Clinicopathological correlation is required.")
    
    
    #add MVI and TI related features for final diagnosis
    diagnosis_list = TI_diagnosis_list + MVI_diagnosis_list
    warn_list = warn_var_list + warn_TI_list + warn_MVI_list
    
    #add IFTA
    if ci==3 or ct==3:
        diagnosis_list.append("IFTA grade III")
        IFTA = 3
    elif ci==2 or ct==2:
        diagnosis_list.append("IFTA grade II")
        IFTA = 2
    elif ci==1 or ct==1:
        diagnosis_list.append("IFTA grade I")
        IFTA = 1
    elif ci==0 and ct==0:
        IFTA = 0
    else:
        IFTA = 'NA'
    
    #comment for ABOi transplantation
    if ABOi >0:
        warn_list.append("C4d interpreted as negative for ABOi cases.")
    if len(warn_list)==0:
        warn_list.append("no")
    
    #Banff comments for incomplete/complex phenotype
    comment_list = []
    if (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) and len(MVI_diagnosis_list)==0 and ptc > 0:
        comment_list.append("Comment: Peritubular capillaritis is present. This feature can be seen in TCMR and does not reach an additional diagnosis of AMR on its own. Biopsy-based transcript diagnostics for AMR could be considered, if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) and any(['AMR' in element for element in diagnosis_list]) is False and C4d > 0: 
        comment_list.append("C4d staining is positive. In the context of ABO-incompatible transplantation, this does not represent AMR. In sensitised patients early post-transplant, this indicates probable AMR as there is typically some degree of ATI in cases with BL or TCMR. In DSA-negative conventional transplants, the findings do not reach criteria for AMR (“C4d-positive without other histological features of AMR”). Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) and len(MVI_diagnosis_list)==0 and current_DSA > 0:
        comment_list.append("The histologic findings do not reach Banff criteria for AMR in this DSA-positive patient. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) and ("Probable AMR" in diagnosis_list or "Chronic AMR" in diagnosis_list) and current_DSA>0:
        comment_list.append("Comment: In the context of circulating DSA, individual lesions of MVI (g, ptc, v, acute TMA, cg, ptcml) below the histological threshold for MVI (g+ptc<2) and in the absence of C4d deposition in peritubular capillaries, probably indicate antibody involvement. This phenotype can be diagnosed in patients with normal or abnormal kidney function. Depending on the clinical context, antibody-targeted treatment could be considered. Further research is necessary to determine the prevalence, impact, and best treatment for this phenotype.")
    if any(['AMR' in element for element in diagnosis_list]) and any(['TCMR II' in element for element in diagnosis_list]) and (i==0 or t==0):
        comment_list.append("Comment: The biopsy fulfills criteria for AMR. According to current Banff criteria this biopsy also has TCMR based on the presence of the v lesion on its own, without tubulointerstitial inflammation above threshold. More data is needed to determine whether a dual AMR + TCMR diagnosis is justified in such cases. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if len(MVI_diagnosis_list)==0 and any(['TCMR II' in element for element in diagnosis_list]) and (i<1 or t <1):
        comment_list.append("Comment: According to current Banff criteria this biopsy has TCMR based on the presence of the v lesion on its own, without tubulointerstitial inflammation above threshold. More data is needed to determine whether a TCMR diagnosis is justified in such cases. Alternative causes of v lesions should be considered (infarction; severe endothelial injury, systemic vasculitis). Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making.")
    if len(MVI_diagnosis_list)==0 and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and g==1 and (TMA==0 or np.isnan(TMA)) and (recurrent_GN==0 or np.isnan(recurrent_GN)) and ptc==0 and C4d==0 and current_DSA==0:
        comment_list.append("Comment: Mild glomerulitis (g1) present on its own without ptc, DSA or C4d does not reach criteria for a diagnosis of AMR. Its significance is not known. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if len(MVI_diagnosis_list)==0 and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and ptc==1 and C4d==0 and current_DSA==0 and g==0 and (TMA==0 or np.isnan(TMA)):
        comment_list.append("Comment: Mild peritubular capillaritis (ptc1) present on its own without g, DSA or C4d does not reach criteria for a diagnosis of AMR. Its significance is not known. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy")
    if len(MVI_diagnosis_list)==0 and g > 0 and C4d==0 and current_DSA==0 and ptc==0 and (TMA==0 or np.isnan(TMA)) and (v==0 or np.isnan(v))and (cg==0 or np.isnan(cg)) and (ptcml==0 or np.isnan(ptcml)) and recurrent_GN==1:
        comment_list.append("Comment: Glomerulitis is present along with a glomerulonephritis that might explain it. In the absence of C4d or DSA or ptc, this lesion is attributed to the recurrent/de novo glomerulonephritis. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if g > 0 and C4d > 0 and current_DSA==0 and ptc==0 and recurrent_GN==1 and (TMA==0 or np.isnan(TMA)) and (v==0 or np.isnan(v))and (cg==0 or np.isnan(cg)) and (ptcml==0 or np.isnan(ptcml)):
        comment_list.append("Comment: Glomerulitis is present along with a glomerulonephritis that might explain it; C4d is positive in peritubular capillaries, and DSA is negative. It is not possible to be certain whether the glomerulitis is related to the recurrent/de novo glomerulonephritis and/or to antibody-mediated rejection. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if g > 0 and C4d == 0 and current_DSA > 0 and ptc==0 and recurrent_GN==1:
        comment_list.append("Comment: Glomerulitis is present along with a glomerulonephritis that might explain it; the patient also has a DSA. It is not possible to be certain whether the glomerulitis is related to the recurrent/de novo glomerulonephritis and/or to antibody-mediated rejection. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if len(MVI_diagnosis_list)==0 and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and TMA==1 and C4d==0 and current_DSA==0:
        comment_list.append("Comment: Criteria for AMR are not met. In view of the presence of TMA, potential triggers (including transplant, infection, drugs, malignancy, paraprotein, pregnancy, etc) and underlying etiologies (genetic or metabolic) should be considered and standard nomenclature followed (ref: https://doi.org/10.1016/j.kint.2024.05.021). In an early post-transplant biopsy, the TMA findings could be inherited from the donor or due to peri-operative injury. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and TMA==1 and C4d==1:
        comment_list.append("Comment: In view of the presence of TMA, in addition to AMR, other potential triggers (including transplant, infection, drugs, malignancy, paraprotein, pregnancy, etc) and underlying etiologies (genetic or metabolic) should be considered and standard nomenclature followed (ref: https://doi.org/10.1016/j.kint.2024.05.021). In an early post-transplant biopsy, the TMA findings could be inherited from the donor or due to peri-operative injury. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and TMA==1 and C4d==0 and current_DSA==1 and g+ptc <2:
        comment_list.append("Comment: In the context of circulating DSA, TMA in the absence of C4d deposition in peritubular capillaries probably indicates antibody activity. Other potential triggers (including transplant, infection, drugs, malignancy, paraprotein, pregnancy, etc) and underlying etiologies (genetic or metabolic) should be considered and standard nomenclature followed (ref: https://doi.org/10.1016/j.kint.2024.05.021). In an early post-transplant biopsy, the TMA findings could be inherited from the donor or due to peri-operative injury. Biopsy-based transcript diagnostics could be considered if available and validated for this purpose. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if any(['AMR' in element for element in diagnosis_list]) is False and any(['MVI' in element for element in diagnosis_list]) is False and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and C4d==1 and np.isnan(transcripts_MVI) and current_DSA==0:
        comment_list.append("Comment: In ABO-i transplants: This represents accommodation. In sensitised patients early post-transplant: This represents probable AMR. In DSA-negative ABO-compatible transplants: No AMR.")
    if any(['AMR' in element for element in diagnosis_list]) is False and any(['MVI' in element for element in diagnosis_list]) is False and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and C4d==1 and np.isnan(transcripts_MVI) and current_DSA==1:
        comment_list.append("Comment: In ABO-i transplants: This represents accommodation. In sensitised patients early post-transplant: This represents probable AMR. In DSA-positive ABO-compatible transplants, later post-transplant: The significance of the C4d-positivity is currently unknown.")
    if any(['AMR' in element for element in diagnosis_list]) is False and any(['MVI' in element for element in diagnosis_list]) is False and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and C4d==1 and transcripts_MVI==0 and current_DSA==1:
        comment_list.append("Comment: In ABO-i transplants: This represents accommodation. In ABO-compatible transplants: C4d is positive in the absence of any other histological features of AMR; DSA is positive; biopsy-based transcriptomic analysis is negative for evidence of AMR. The significance of the positive C4d is currently not known.")
    if any(['AMR' in element for element in diagnosis_list]) is False and any(['MVI' in element for element in diagnosis_list]) is False and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and C4d==1 and transcripts_MVI==0 and current_DSA==0:
        comment_list.append("Comment: In ABO-i transplants: This represents accommodation. In ABO-compatible transplants: C4d is positive in the absence of any other histological features of AMR; DSA is negative; biopsy-based transcriptomic analysis is negative for evidence of AMR. The significance of the positive C4d is currently not known.")
    if any(['AMR' in element for element in diagnosis_list]) is False and any(['MVI' in element for element in diagnosis_list]) is False and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and C4d==1 and transcripts_MVI==1 and current_DSA==1:
        comment_list.append("Comment: C4d is positive in peritubular capillaries in the absence of any other histological features of AMR; DSA is positive. Biopsy-based transcriptomic analysis is positive for evidence of AMR. To date, there is no consensus on whether this represents AMR. Further research is necessary to determine the prevalence, impact, and best treatment for this phenotype. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if any(['AMR' in element for element in diagnosis_list]) is False and any(['MVI' in element for element in diagnosis_list]) is False and (any(['TCMR' in element for element in diagnosis_list]) or 'Borderline changes' in diagnosis_list) is False and C4d==1 and transcripts_MVI==1 and current_DSA==0:
        comment_list.append("Comment: C4d is positive in peritubular capillaries in the absence of any other histological features of AMR; DSA is negative. Biopsy-based transcriptomic analysis is positive for evidence of AMR. To date, there is no consensus on whether this represents AMR. Further research is necessary to determine the prevalence, impact, and best treatment for this phenotype. More information on the clinical context may be of help for clinical decision making, including consideration of repeat biopsy.")
    if len(comment_list)==0:
        comment_list.append("no")
    
    #add indices
    MVI_index = g * 0.938 + ptc * 0.762 + cg * 0.728 + C4d * 2.716
    #TCMR/TI index
    TI_index = i * 0.970 + t * 0.623 + v * 1.540 + ct * 0.195
    #activity index
    activity_index = t + i + v + g + ptc + 2 * C4d   
    #chronicity index
    chronicity_index = ci + ct + cv + 2 * cg
    
    #add dummy variables for each TCMR diagnosis, not mutually exclusive
    diagnosis_positions = {
        'Borderline':                0,
        'Acute TCMR':                1,
        'Chronic active TCMR':       2,
        'Polyomavirus nephropathy': 3,
    }
    #Start with all zeros (five elements)
    result = [0] * len(diagnosis_positions)
    for keyword, idx in diagnosis_positions.items():
        if any(keyword in element for element in TI_diagnosis_list):
            result[idx] = 1
    
    result_dict = {'TI_diagnosis_list': TI_diagnosis_list,
                  'MVI_diagnosis_list': MVI_diagnosis_list,
                  'IFTA': IFTA,
                  'warn_list': warn_list,
                  'comment_list': comment_list,
                  'MVI_index': MVI_index,
                  'TI_index': TI_index,
                  'activity_index': activity_index,
                  'chronicity_index': chronicity_index,
                  'Borderline': result[0],
                  'Acute TCMR': result[1],
                  'Chronic active TCMR': result[2],
                  'Polyomavirus nephropathy': result[3]}
    return result_dict
