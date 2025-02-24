# Anonymous Submission
Anonymous Submission for MICCAI 2025 Paper ID: 2399
This repository contains the anonymized materials for our submission to MICCAI 2025 (Paper ID: 2399). Below is an overview of the contents and structure of this repository. 

```
├── data/ # Anonymized dataset
├── figures/ # Figures
├── prompts/ # Prompts used in Stage 1 and Stage 2
├── code/ # Code for ProCDS
└── README.md # This file
```

**The code will be made publicly available upon paper acceptance**

# Table of Contents

1. [Overview](#1-overview)
2. [Prompts](#2-prompts)
   - [Stage 1 Prompt](#stage-1-prompt)
     - [Extract Rules & Facts](#prompts-for-extract-rules--facts)
     - [Verify Rules & Facts](#prompts-for-verify-rules--facts)
   - [Stage 2 Prompt](#stage-2-prompt)
     - [Translate to Prolog Code](#prompts-for-translate-to-prolog-code)
     - [Verify Errors Code](#prompts-for-verify-errors-code)


---

## 1. Overview
- **Framework**: The overall framework is illustrated as follows:
  
![The overall framework](figure/overview.png)

---

## 2. Prompts
### Stage 1 Prompt:

#### Prompts for Extract Rules & Facts:
  - ```
    ## Prompt: Extract Rules & Facts
    
    ### Instructions:
    
    1. You should **strictly follow the following instructions**.
    2. Extract rules related to patient information.
    3. Determine if missing values can be computed from the existing information.
    4. Please **only give me the rules and formulas** and DO NOT show your reasoning steps and calculation.
  
    ### Example:
  
    #### Example 1:
    {}
  
    #### Example 2:
    {}
  
    #### Example 3:
    {}
  
    ### Response:
  
    High Risk Group: {}
  
    Patient info: {}
    ```
  
#### Prompts for Verify Rules & Facts:
  - ```
    ## Prompt: Verify Rules & Facts
    
    ### Instructions:
    
    1. You should **strictly follow the following instructions**.
    2. You need to verify and correct errors in the input rules based on the provided rule set. You only need to output the corrected sentences with edits.
    3. DO NOT show reasoning steps, explanations, or calculations.
    
    ### Example:
    
    #### Example 1:
    {}
    
    #### Example 2:
    {}
    
    #### Example 3:
    {}
    
    ### Response:
    
    \{Rules\} or \{Facts\}
    
    
### Stage 2 Prompt:

  
#### Prompts for Translate to Prolog Code:
  -  ```
    ## Prompt: Translate to Prolog Code
    ### Instructions:
    
    1. Your code should be accurate, self-consistent, and complete. Use consistent variable names for co-referent entities or attributes across all triples and rules.
    2. Begin by coding the triples after the "/* Triples */" comment. Then, code the rules after the "/* Rules */" comment. Finally, code the question statements after the "/* Questions */" comment.
    3. Please **only give me the Prolog code** and DO NOT show your reasoning steps in natural language.
    4. Identify patients as high-risk if they meet 3 or more of the rules.
    5. You should **strictly follow the following instructions**.
    
    ### Example:
    
    #### Example 1:
    {}
    #### Example 2:
    {}
    #### Example 3:
    {}
    
    ### Response:
    
    Patient information:
    {Related Facts}
    
    High-risk criteria that the Prolog code might use when processing this patient data:
    
    **High Risk Group Rules**
    
    {Related Rules}
    
    **High Risk Group Rules END**
    
    Stay consistent with the example format, no need for extra explanations, just output the Prolog code.
  
    ```
  
#### Prompts for Verify Errors Code:
  
  - ```
    ## Prompt: Verify Errors Code
    
    ### Instructions:
    
    1. You should **strictly follow the following instructions**.
    2. You need to verify and correct errors in the Prolog code. You only need to output the Prolog code.
    3. Begin by coding the triples after the "/* Triples */" comment. Then, code the rules after the "/* Rules */" comment. Finally, code the question statements after the "/* Questions */" comment.
    4. DO NOT show reasoning steps or explanations.
    
    ### Example:
    
    #### Example 1:
    {}
    #### Example 2:
    {}
    #### Example 3:
    {}
    
    ### Response:
    
    Facts:
    {Facts}
    
    Rules:
    {Rules}
  
    ```
    
---

This README file provides a comprehensive guide to the contents of this repository. All materials have been anonymized for double-blind review. For further details, please refer to the supplementary materials.

---
