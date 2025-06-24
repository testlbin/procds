
rule_Prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Your task is to help me extract information. Below are the detailed instructions. Thanks for your help!
**Instructions Start**
(1) You should **strictly follow the following instructions**.
(2) Extract rules related to patient information.  
(3) Determine if missing values can be computed from the existing information. 
(4) Please **only give me the rules and formulas** and DO NOT show your reasoning steps and calculation.
**Instructions End**<|eot_id|><|start_header_id|>user<|end_header_id|>

---Example Start---
Below is an example:
#Example 1:
High Risk Group:
1. Overweight individuals: Body Mass Index (BMI) of 25 or higher.
2. Neck Size: 38 cm or more for males, 33 cm or more for females.
3. ESS Score: A score of 9 or greater indicates significant daytime sleepiness and increased risk.
4. Age and Gender: Middle-aged and older men over 50 years of age, post-menopausal women over 60 years of age.
5. Longest Apnea Duration: Apnea duration exceeding 40 seconds.
6. Waist-to-Hip Ratio: Greater than 0.9 for men, and greater than 0.8 for women.
7. Comorbidities: Hypertension, diabetes, heart disease, hyperlipidemia, etc., remain significant risk factors.
8. Individuals with abnormalities in head, neck skeletal and soft tissue structures.
9. Adults and children with Down syndrome.
10. Children with enlarged tonsils and adenoids.
11. Anyone with a family member diagnosed with OSA.
12. Individuals with endocrine disorders such as acromegaly and hypothyroidism.
13. Smokers.
14. Individuals experiencing nocturnal nasal congestion due to anatomical abnormalities, rhinitis, or both.

Patient info:
Patient ID: 4029.
Gender: Female.
Birth Date: August 10, 2015.
Height: 129 cm.
Weight: 31.9 kg.
Neck Circumference: 29 cm.
Waist Circumference: 66 cm.
Hip Circumference: 68 cm.
Longest Apnea Duration: 30.7 seconds.
Lowest Blood Oxygen Saturation (SPO2): 86%.
Average Blood Oxygen Saturation (SPO2): 97.1%.
Epworth Sleepiness Scale (ESS) Score: 6.
Age: 7 years old.
Total Sleep Time: 604.3 minutes.
Oxygen Desaturation (OD) Index: 2.7 events.
Sleep Apnea-Hypopnea Index (SAHI): 11.5.
Time spent with SPO2 < 90%: 3 minutes.
Time spent with SPO2 < 80%: 0 minutes.
Time spent with SPO2 < 70%: 0 minutes.
OD90: 0.8 events.
OD80: 0 events.
OD70: 0 events.
Positional Dependency: None. 

###Response:
Here are the extracted rules and equations related to patient information:

***Rules Start***

1. Overweight individual: BMI = 25 or higher, where BMI = weight / (height)^2.
2. Neck Size: 38 cm or more for males, 33 cm or more for females.
3. ESS Score: A score of 9 or greater indicates significant daytime sleepiness and increased risk.
4. Age and Gender: Middle-aged and older men over 50 years of age, post-menopausal women over 60 years of age.
5. Longest Apnea Duration: Apnea duration exceeding 40 seconds.
6. Waist-to-Hip Ratio: Greater than 0.9 for men, and greater than 0.8 for women, where Waist-to-Hip Ratio = Waist Circumference / Hip Circumference.

***Rules End***

---Example End---

Below is you need to handle:
High Risk Group:
1. Overweight individuals: Body Mass Index (BMI) of 25 or higher.
2. Neck Size: 38 cm or more for males, 33 cm or more for females.
3. ESS Score: A score of 9 or greater indicates significant daytime sleepiness and increased risk.
4. Age and Gender: Middle-aged and older men over 50 years of age, post-menopausal women over 60 years of age.
5. Longest Apnea Duration: Apnea duration exceeding 40 seconds.
6. Waist-to-Hip Ratio: Greater than 0.9 for men, and greater than 0.8 for women.
7. Comorbidities: Hypertension, diabetes, heart disease, hyperlipidemia, etc., remain significant risk factors.
8. Individuals with abnormalities in head, neck skeletal and soft tissue structures.
9. Adults and children with Down syndrome.
10. Children with enlarged tonsils and adenoids.
11. Anyone with a family member diagnosed with OSA.
12. Individuals with endocrine disorders such as acromegaly and hypothyroidism.
13. Smokers.
14. Individuals experiencing nocturnal nasal congestion due to anatomical abnormalities, rhinitis, or both.

Patient info:
{patient_info}
###Response:<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""



facts_Prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Your task is to help me extract information. Below are the detailed instructions. Thanks for your help!
**Instructions Start**
(1) You should **strictly follow the following instructions**.
(2) Extract ***patient*** information.  
(3) Based on the rules, match the patient information, and output the patient information.  
(4) DO NOT reason steps and calculate.
**Instructions End**<|eot_id|><|start_header_id|>user<|end_header_id|>

---Example Start---
Below are some examples:
#Example 1:
High Risk Rules Group:
Here are the extracted rules and equations related to patient information:
1. Overweight individual: BMI = 25 or higher, where BMI = weight / (height)^2.
2. Neck Size: 38 cm or more for males, 33 cm or more for females.
3. ESS Score: A score of 9 or greater indicates significant daytime sleepiness and increased risk.
4. Age and Gender: Middle-aged and older men over 50 years of age, post-menopausal women over 60 years of age.
5. Longest Apnea Duration: Apnea duration exceeding 40 seconds.
6. Waist-to-Hip Ratio: Greater than 0.9 for men, and greater than 0.8 for women, where Waist-to-Hip Ratio = Waist Circumference / Hip Circumference.
Note: The patient's BMI, Waist-to-Hip Ratio, and Comorbidities are not provided, so it is not possible to determine if they are high risk based on these factors.


Patient info:
Patient ID: 1.
Gender: Female.
Birth Date: August 10, 2015.
Height: 129 cm.
Weight: 31.9 kg.
Neck Circumference: 29 cm.
Waist Circumference: 66 cm.
Hip Circumference: 68 cm.
Longest Apnea Duration: 30.7 seconds.
Lowest Blood Oxygen Saturation (SPO2): 86%.
Average Blood Oxygen Saturation (SPO2): 97.1%.
Epworth Sleepiness Scale (ESS) Score: 6.
Comorbidities: No hypertension, diabetes, heart disease, or hyperlipidemia.
Age: 7 years old.
Total Sleep Time: 604.3 minutes.
Oxygen Desaturation (OD) Index: 2.7 events.
Sleep Apnea-Hypopnea Index (SAHI): 11.5.
Time spent with SPO2 < 90%: 3 minutes.
Time spent with SPO2 < 80%: 0 minutes.
Time spent with SPO2 < 70%: 0 minutes.
OD90: 0.8 events.
OD80: 0 events.
OD70: 0 events.
Positional Dependency: None. 

###Response:
***Summary Start***
Patient Information summary:
Patient ID: 1.
Gender: Female.
Birth Date: August 10, 2015.
Height: 129 cm.
Weight: 31.9 kg.
Neck Circumference: 29 cm.
Waist Circumference: 66 cm.
Hip Circumference: 68 cm.
Longest Apnea Duration: 30.7 seconds.
Epworth Sleepiness Scale (ESS) Score: 6.
Comorbidities: No hypertension, diabetes, heart disease, or hyperlipidemia.
Age: 7 years old.
***Summary End***

---Example End---

Below is you need handel:

High Risk Group:
{rules_info}


Patient info:
{patient_info}
###Response:<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""



prolog_Instruct = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Your task is to help me write ** Prolog ** code. Below are the detailed instructions. Thanks for your help!
**Instructions Start**
Follow these instructions strictly:
(1) Your code should be accurate, self-consistent, and complete. Use consistent variable names for co-referent entities or attributes across all triples and rules.
(2) Begin by coding the triples after the "/* Triples */" comment. Then, code the rules after the "/* Rules */" comment. Finally, code the question statements after the "/* Questions */" comment.
(3) Please **only give me the Prolog code** and DO NOT show your reasoning steps in natural language.
(4) Identify patients as high-risk if they meet 3 or more of the rules.
(5) You should **strictly follow the following instructions**.
**Instructions End**<|eot_id|><|start_header_id|>user<|end_header_id|>

---Example Start---
Below is an example:

```

Prolog Code:

/* Triples */
% patient information
patient(PatientID, Age, male).
height(PatientID, Height).
weight(PatientID, Weight).
body_size(PatientID, Neck Size, Waist Size, Hip Size).
apnea_duration(PatientID, Long Apnea Duration).
ess_score(PatientID, ESS score).


/* Rules */

calculate_bmi(PatientID, BMI) :- 
    weight(PatientID, Weight), 
    height(PatientID, Height),
    BMI is Weight / ((Height / 100) * (Height / 100)).

calculate_waist_hip_ratio(PatientID, Ratio) :- 
    body_size(PatientID, _, Waist, Hip),
    Ratio is Waist / Hip.

overweight(PatientID) :- 
    calculate_bmi(PatientID, BMI), 
    BMI >= 25.

large_neck_size(PatientID) :- 
    patient(PatientID, _, male), 
    body_size(PatientID, NeckSize, _, _),
    NeckSize >= 38.

high_ess_score(PatientID) :- 
    ess_score(PatientID, Value), 
    Value >= 9.

middle_aged(PatientID) :- 
    patient(PatientID, Age, male), 
    Age >= 50.

long_apnea_duration(PatientID) :- 
    apnea_duration(PatientID, Value), 
    Value >= 40.

high_waist_hip_ratio(PatientID) :- 
    calculate_waist_hip_ratio(PatientID, Ratio), 
    Ratio > 0.9.

risk_factor_count(PatientID, Count) :-
    findall(1, overweight(PatientID), Overweight),
    findall(1, large_neck_size(PatientID), LargeNeck),
    findall(1, high_ess_score(PatientID), HighEss),
    findall(1, middle_aged(PatientID), MiddleAged),
    findall(1, long_apnea_duration(PatientID), LongApneaDuration),
    findall(1, high_waist_hip_ratio(PatientID), HighWaistHipRatio),
    append([Overweight, LargeNeck, HighEss, MiddleAged, LongApneaDuration, HighWaistHipRatio], AllRisks),
    length(AllRisks, Count).

high_risk(PatientID) :-
    risk_factor_count(PatientID, Count),
    Count >= 3.
    
/* Question */
?- high_risk(PatientID). 

```

---Example End---


Below is you need to handle:

Patient information:
{Patient_Info}

High-risk criteria that the Prolog code might use when processing this patient data:

**High Risk Group Rules**

{High_Risk}

**High Risk Group Rules END**

Stay consistent with the example format, no need for extra explanations, just output the Prolog code.

###Response:<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""



varify_Code = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Your task is to help me ***Prolog*** Code. Below are the detailed instructions. Thanks for your help!
**Instructions Start**
(1) You should **strictly follow the following instructions**.
(2) You need to verify and correct errors in the Prolog, You only need to output the Prolog Code.  
(3) DO NOT show reason steps, explain.
**Instructions End**<|eot_id|><|start_header_id|>user<|end_header_id|>

Below you need to verify:
Facts:
{facts_info}

Rules:
{rules_info}

Prolog Code:
{prolog_info}

###Response:<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""