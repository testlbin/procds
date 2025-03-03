# Anonymous Submission
Anonymous Submission for MICCAI 2025 Paper ID: 2399

This repository contains the anonymized materials for our submission to MICCAI 2025 (Paper ID: 2399). Below is an overview of the contents and structure of this repository. 

```
├── data/ # Example of Anonymized Dataset
├── figures/ # Figures
├── prompts/ # Prompts used in Stage 1 and Stage 2
└── README.md # This file
```

**The code will be made publicly available upon paper acceptance**

# Contents

1. [Overview](#1-overview)
2. [Prompts](#2-prompts)
   - [Stage 1 Prompt](#stage-1-prompt)
     - [Extract Rules & Facts](#prompts-for-extract-rules--facts)
     - [Verify Rules & Facts](#prompts-for-verify-rules--facts)
   - [Stage 2 Prompt](#stage-2-prompt)
     - [Translate to Prolog Code](#prompts-for-translate-to-prolog-code)
     - [Verify Errors Code](#prompts-for-verify-errors-code)

## 1. Overview
- **Framework**: The overall framework is illustrated as follows:
  
<img src="figure/overview.png" alt="The overall framework" width="800">

## 2. Prompts
### Stage 1 Prompt:

#### Prompts for Extract Rules & Facts:
  - ```
    ## Prompt: Extract Rules & Facts
    
    ### Instructions:
    Your task is to help me extract information. Below are the detailed instructions. Thanks for your help!
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
  
    Below is you need to handle:
  
    High Risk Group: {}
  
    Patient info: {}

    ### Response:
    ```
  
#### Prompts for Verify Rules & Facts:
  - ```
    ## Prompt: Verify Rules & Facts
    
    ### Instructions:
    Your task is to help me ***verify and edit text***. Below are the detailed instructions. Thanks for your help!
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
    
    Below you need to verify the numbers"
    
    {Rules} or {Facts}

    Stay consistent with the example format.
    ### Response:
    ```
    
### Stage 2 Prompt:

  
#### Prompts for Translate to Prolog Code:
  - ```
    ## Prompt: Translate to Prolog Code
    ### Instructions:
    Your task is to help me write ** Prolog ** code. Below are the detailed instructions. Thanks for your help!
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
    
    Below is you need to handle:
    
    Patient information:
    {Related Facts}
   
    High-risk criteria that the Prolog code might use when processing this patient data:
   
    High Risk Group Rules:
    {Related Rules}
  
    Stay consistent with the example format, no need for extra explanations, just output the Prolog code.
   
    ###Response:
  
    ```
  
#### Prompts for Verify Errors Code:
  - ```
    ## Prompt: Verify Errors Code
    
    ### Instructions:
    Your task is to help me verify and edit ***Prolog*** Code. Below are the detailed instructions. Thanks for your help!
    1. You should **strictly follow the following instructions**.
    2. You need to verify and correct errors in the Prolog, You only need to output the Prolog Code. 
    3. Begin by coding the triples after the "/* Triples */" comment. Then, code the rules after the "/* Rules */" comment. Finally, code the question statements after the "/* Questions */" comment.
    4. DO NOT show reason steps, explain.
    
    ### Example:
    
    #### Example 1:
    {}
    #### Example 2:
    {}
    #### Example 3:
    {}
    
    Below you need to verify:
   
    Facts:
    {Facts}
   
    Rules:
    {Rules}
   
    Prolog Code:
    {Prolog Code}
   
    ###Response:
    ```
    
---

This README file provides a comprehensive guide to the contents of this repository. All materials have been anonymized for double-blind review. For further details, please refer to the supplementary materials.

---
