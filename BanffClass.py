#the core function
import pandas as pd
import numpy as np

def apply_Banff_2024(df):
  TI_df_list = []
  MVI_df_list = []
  IFTA_df_list = []
  warn_df_list = []
  comment_df_list = []
  MVI_index_list = []
  TI_index_list = []
  activity_index_list = []
  chronicity_index_list = []
  borderline_list = []
  aTCMR_list = []
  caTCMR_list = []
  pvn_list = []
  for y in range(0, len(df)): #iterate through rows
      g = df.loc[y, 'g'] if 'g' in df.columns else np.nan
      ptc = df.loc[y, 'ptc'] if 'ptc' in df.columns else np.nan
      i = df.loc[y, 'i'] if 'i' in df.columns else np.nan
      t = df.loc[y, 't'] if 't' in df.columns else np.nan
      v = df.loc[y, 'v'] if 'v' in df.columns else np.nan
      cg = df.loc[y, 'cg']  if 'cg' in df.columns else np.nan #convert 1a or 1b to 1; beware of chronic TMA and recurrent GN
      ci = df.loc[y, 'ci'] if 'ci' in df.columns else np.nan
      ct = df.loc[y, 'ct'] if 'ct' in df.columns else np.nan
      ti = df.loc[y, 'ti'] if 'ti' in df.columns else np.nan
      i_IFTA = df.loc[y, 'i_IFTA'] if 'i_IFTA' in df.columns else np.nan
      t_IFTA = df.loc[y, 't_IFTA'] if 't_IFTA' in df.columns else np.nan
      C4d = df.loc[y, 'C4d'] if 'C4d' in df.columns else np.nan #binary variable 0 or 1
      pvl = df.loc[y, 'pvl'] if 'pvl' in df.columns else np.nan
      TMA = df.loc[y, 'TMA'] if 'TMA' in df.columns else np.nan #or acute and chronic, perhaps would be better and then 1
      ptcml = df.loc[y, 'ptcml'] if 'ptcml' in df.columns else np.nan
      current_DSA = df.loc[y, 'current_DSA']  if 'current_DSA' in df.columns else np.nan
      historical_DSA = df.loc[y, 'historical_DSA'] if 'historical_DSA' in df.columns else np.nan
      historical_AMR = df.loc[y, 'historical_AMR'] if 'historical_AMR' in df.columns else np.nan
      transcripts_MVI = df.loc[y, 'transcripts_MVI'] if 'transcripts_MVI' in df.columns else np.nan #how to interpret moderate probability? below threshold?
      transcripts_TI = df.loc[y, 'transcripts_TI'] if 'transcripts_TI' in df.columns else np.nan 
      infection = df.loc[y, 'infection'] if 'infection' in df.columns else np.nan  #to modify is PVN diagnosed
      recurrent_GN = df.loc[y, 'recurrent_GN'] if 'recurrent_GN' in df.columns else np.nan #np.nan #recurrent or de novo GN, should be proliferative
      ATI = df.loc[y, 'ATI'] if 'ATI' in df.columns else np.nan
      chronic_transplant_arteriopathy = df.loc[y, 'chronic_transplant_arteriopathy'] if 'chronic_transplant_arteriopathy' in df.columns else np.nan
      ABOi = df.loc[y, 'ABOi'] if 'ABOi' in df.columns else np.nan #np.nan
      cv = df.loc[y, 'cv'] if 'cv' in df.columns else np.nan
      
      #check for missing core variables
      warn_var_list = []
      core_variables_names = ['g', 'ptc', 'i', 't', 'v', 'cg', 'C4d', 'current_DSA', 'ti', 'i_IFTA'] #caTCMR can rely on t
      core_variables = [g, ptc, i, t, v, cg, C4d, current_DSA, ti, i_IFTA]
      nan_variables = []
      nan_var_dict = {'g':'AMR', 'ptc':'AMR', 'i':'TCMR', 't':'TCMR', 'v':'TCMR and/or AMR', 'cg':'cAMR', 'C4d':'AMR', 'current_DSA':'AMR', 'ti':'caTCMR', 'i_IFTA':'caTCMR'}
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
      if i >=2 and t >=2 or transcripts_TI==1:
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
      if ti >=2 and i_IFTA >=2 and (t == 2 or t_IFTA == 2) and "Chronic active TCMR IB" not in TCMR_diagnosis_list: #otherwise IB and IA can co-occur when t3/t-IFTA2
          TCMR_diagnosis_list.append("Chronic active TCMR IA")
      if chronic_transplant_arteriopathy ==1:
          TCMR_diagnosis_list.append("Chronic active TCMR II")
      
      #check for diagnosis combination
      #accepting infection-related nephritis and v+ as combined rejection and nephritis. Warning otherwise while favoring infection.
      if len(infection_list)>0 and len(TCMR_diagnosis_list)>0 and any(['TCMR II' in element for element in TCMR_diagnosis_list]):
          TI_diagnosis_list = infection_list + TCMR_diagnosis_list
      elif len(infection_list)>0 and len(TCMR_diagnosis_list)>0 and not any(['TCMR II' in element for element in TCMR_diagnosis_list]):
          TI_diagnosis_list = infection_list
          warn_TI_list.append('Tubulo-interstitial infiltrate could be related to infection, but is also above threshold for T cell-mediated alloimmune process; consider treatment depending on clinical evolution/consider re-biopsy')
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
      if (np.nansum([g, ptc]) >= 2 and not ((g==0 or np.isnan(g)) and (any(['TCMR' in element for element in TI_diagnosis_list]) or 'Borderline changes' in TI_diagnosis_list or 'Polyomavirus nephropathy' in TI_diagnosis_list or infection==1))) and C4d==0 and current_DSA==0:
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
      borderline_list.append(result[0])
      aTCMR_list.append(result[1])
      caTCMR_list.append(result[2])
      pvn_list.append(result[3])
      
      #append diagnoses and indices
      TI_df_list.append(', '.join(TI_diagnosis_list))
      MVI_df_list.append(', '.join(MVI_diagnosis_list))
      IFTA_df_list.append(IFTA)
      warn_df_list.append(' '.join(warn_list))
      comment_df_list.append(' '.join(comment_list))
      MVI_index_list.append(MVI_index)
      TI_index_list.append(TI_index)
      activity_index_list.append(activity_index)
      chronicity_index_list.append(chronicity_index)
  
  df['TI diagnosis'] = TI_df_list
  df['MVI diagnosis'] = MVI_df_list
  df['IFTA grade'] = IFTA_df_list
  df['warning'] = warn_df_list
  df['comment'] = comment_df_list
  df['borderline'] = borderline_list
  df['aTCMR'] = aTCMR_list
  df['caTCMR'] = caTCMR_list
  df['PVN'] = pvn_list
  df['AMR/MVI index'] = MVI_index_list
  df['TCMR/TI index'] = TI_index_list
  df['Activity index'] = activity_index_list
  df['Chronicity index'] = chronicity_index_list


