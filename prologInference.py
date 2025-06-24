import tempfile
import os
import re
import subprocess
import json
import jsonlines
from pathlib import Path

curr_dir = os.path.dirname(os.path.abspath(__file__))

def extract_clauses_from_code(prolog_code: str):
    """
    Extract clauses and predicates from Prolog code string.
    """
    lines = prolog_code.split("\n")
    clauses = []
    continue_signal = False
    for i, line in enumerate(lines):
        # Skip comment lines or empty lines
        if line.startswith("%") or line.startswith("/*") or line.strip() == '':
            continue_signal = False
            continue
        # Remove inline comments
        if "%" in line:
            line = line.split("%")[0].strip()
        if "/*" in line:
            line = line.split("/*")[0].strip()
        # Handle multi-line clauses
        if continue_signal and line.startswith(" "):
            clauses[-1] += ' ' + line.strip()
        else:
            clauses.append(line)
            continue_signal = True
    # Remove trailing periods and whitespace
    clauses = [_.strip().rstrip('.') for _ in clauses]
    predicates = []
    for clause in clauses:
        if clause.startswith(":-"):
            continue
        if ':-' in clause:
            head, body = clause.split(":-")
            predicates.extend(
                [_.strip() for _ in head.split("(")[:-1]]
            )
        else:
            predicates.append(clause.split('(')[0].strip())
    return clauses, set(predicates)

def consult_prolog(
        prolog_string,
        query_string,
        meta_interpreter="raw",
        max_depth=5,
        debug=False,
        dataset_name="vanilla",
):
    """
    Run Prolog code and query using a meta-interpreter.
    Args:
        prolog_string:
            string, the string of Prolog knowledge base to be consulted
        query_string:
            string, the string of Prolog query to be executed
        consult_raw_query:
            bool, whether to consult the raw query, i.e., **NO** special meta-interpreter is used.
        generate_proof_tree:
            bool, whether to generate the proof tree for the query
        max_depth:
            int, the maximum depth of the iterative deepening search
        debug:
            bool, whether to print all the inputs and outputs when interacting with SWI-Prolog
        dataset_name:
            string, the name of the dataset, determines which meta-interpreter_*.pl to use
    Returns:
        output: dict with 'answer' and 'proofs'
    """

    prolog_meta_interpreters = {
        "raw": "{}",
        "with_proof": "mi_tree(g({}), Proof)",  # With proof generation. One argument: Goal
        "iter_deep_with_proof": "mi_id_limit(g({}), Proof, {})",
        # Iterative deepening search, with proof generation. Two arguments: Goal, MaxDepth
        # "iter_deep_no_proof": prolog_output_all_answers.format("mi_id_limit_no_proof(g({}), {})"),  # Iterative deepening search. Two arguments: Goal, MaxDepth
        "iter_deep_no_proof": "mi_id_limit_no_proof(g({}), {})",
        # Iterative deepening search. Two arguments: Goal, MaxDepth
    }

    ########################################
    # Extract clauses and predicates from the Prolog code
    clauses, predicates = extract_clauses_from_code(prolog_string)
    ########################################

    # Remove trailing period from query string if present
    if query_string.endswith('.'):
        query_string = query_string[:-1].strip()
    # Select the meta-interpreter format for the query
    if "iter_deep" not in meta_interpreter:
        user_query = prolog_meta_interpreters[meta_interpreter].format(query_string)
    else:
        user_query = prolog_meta_interpreters[meta_interpreter].format(query_string, max_depth)

    # Write the Prolog knowledge base and query to a temporary file
    tmp_clause_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    with open(tmp_clause_file.name, 'w') as f:
        f.writelines(
            [clause.strip() + '\n' for clause in clauses] + [user_query + '\n']
        )
    tmp_output_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)

    file_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '\\\\')
    # mi_path = os.path.join(file_path, "prolog_utils", "meta_interpreter.pl").replace('\\', '\\\\')
    tmp_clause_path = os.path.abspath(tmp_clause_file.name).replace('\\', '\\\\')
    tmp_output_path = os.path.abspath(tmp_output_file.name).replace('\\', '\\\\')
    command = [
        "python",
        'individual_prologging.py',
        "--assert_path",
        tmp_clause_path,
        # "--mi_path",
        # mi_path,
        "--output_path",
        tmp_output_path,
    ]
    response = subprocess.run(
        command,
    )

    # Read results from the output file if the subprocess succeeded
    if response.returncode == 0:
        with open(tmp_output_file.name, 'r', encoding='utf-8') as f:
            results = [json.loads(_) for _ in f.readlines() if _.strip()]
    else:
        results = []
    output = {
        'answer': None
    }

    # Extract the query(Key). For example, given "query(Salary)"", we extract "Salary".
    target_key = re.findall(r'\((.*?)\)', query_string, re.DOTALL)
    assert len(target_key) == 1

    num_results = 0
    for r in results:
        num_results += 1
        if target_key[0] in r:
            if output["answer"] is None:
                output["answer"] = [r[target_key[0]]]
            else:
                output["answer"].append(r[target_key[0]])
        if "Proof" in r:
            if output["proofs"] is None:
                output["proofs"] = [r['Proof']]
            else:
                output["proofs"].append(r['Proof'])
    output['answer'] = list(set(output['answer'])) if output['answer'] is not None else [""]
    output['proofs'] = list(set(output['proofs'])) if output['proofs'] is not None else [""]

    # If there are results but no answer, set answer to "True"
    if (num_results > 0) and ((output['answer'] == [""]) or (output['answer'] is None)):
        output['answer'] = ["True"]
    # if (num_results == 0) and ((output['answer'] == [""]) or (output['answer'] is None)):
    #     output['answer'] = ["None"]

    tmp_clause_file.close()
    tmp_output_file.close()
    os.remove(tmp_clause_file.name)
    os.remove(tmp_output_file.name)

    return output

def preprocess_response_prolog(text: str) -> tuple:
    """
    Extract Prolog code and query from a text block.
    Returns:
        prolog_string: Prolog code as string
        query_string: Prolog query as string
    """
    try:
        # Use regex to match the Prolog code block
        pattern = r'```\n\nProlog Code:\n\n(.+?)\n\n```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            # If matched, return the Prolog code part
            prolog_string = match.group(1)
        else:
            # If not matched, return empty string
            prolog_string = ""
        clauses, _ = extract_clauses_from_code(prolog_string)
        def transform_prolog_statement(statement: str) -> str:
            # Replace " :- ..." with "."
            pattern = r'\s+:-.*'
            transformed_statement = re.sub(pattern, '.', statement)
            return transformed_statement

        query_string = transform_prolog_statement(clauses[-1])

        return prolog_string, query_string
    except Exception as e:
        # Re-raise the caught exception with modified message
        raise Exception(f"Error processing Prolog code: {str(e)}")

def process_prolog_jsonl(input_file, output_file, meta_interpreter="raw", max_depth=5):
    """
    Process a JSONL file containing Prolog code, run inference, and write results.
    Args:
        input_file: input JSONL file path
        output_file: output JSONL file path
        meta_interpreter: meta-interpreter type
        max_depth: max depth for iterative deepening
    """
    with jsonlines.open(input_file, mode='r') as reader, jsonlines.open(output_file, mode='w') as writer:
        for data in reader:
            try:
                prolog_code = data['prolog']
                # Call consult_prolog to process the prolog_code
                prolog_string, query_string = preprocess_response_prolog(prolog_code)
                result = consult_prolog(prolog_string, query_string, meta_interpreter, max_depth)
                # Add 'answer' and 'proofs' to the output dict, handle variable-length proofs
                if 'answer' in result and result['answer']:
                    data['prolog_answer'] = str(result['answer'][0])
                    if 'proofs' in result:
                        for i, proof in enumerate(result['proofs']):
                            data[f'proofs_{i}'] = proof
                writer.write(data)
            except Exception as e:
                print(f"Error processing record : {str(e)}")
                continue

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Prolog code inference and verification tool")
    parser.add_argument('--input', type=str, required=True, help='Input jsonl file path containing Prolog code')
    parser.add_argument('--output', type=str, required=True, help='Output jsonl file path for inference results')
    parser.add_argument('--meta_interpreter', type=str, default='raw', choices=['raw', 'with_proof'], help='Meta-interpreter type')
    parser.add_argument('--max_depth', type=int, default=5, help='Maximum recursion depth')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    process_prolog_jsonl(
        input_file=args.input,
        output_file=args.output,
        meta_interpreter=args.meta_interpreter,
        max_depth=args.max_depth
    )

# Example usage:
# python prologInference.py --input prolog_data/data/data_prolog.jsonl --output prolog_data/prolog_answer.jsonl --meta_interpreter raw

# Example usage for GSM8K dataset:
# gsm8k_code = Path('prolog_code/gsm8k_prolog.jsonl')
# gsm8k_answer = Path('prolog_code/gsm8k_prolog_answer.jsonl')
# process_prolog_jsonl(gsm8k_code, gsm8k_answer, "with_proof")

# Example usage for ProntoQA dataset:
# prontoqa_code = 'prolog_data/prolog_data.jsonl'
# prontoqa_answer = 'prolog_data/prolog_answer.jsonl'
# process_prolog_jsonl(prontoqa_code, prontoqa_answer, "raw")

# prolog_string, query_string = preprocess_response_prolog("""\n\nHere is the Prolog code to solve this problem:\n```prolog\n/* Context */\n\n% facts\neggs_per_day(16).\neggs_for_breakfast(3).\neggs_for_muffins(4).\n\n% calculate the number of eggs left over\neggs_left_over(Eggs) :-\n    eggs_per_day(PerDay),\n    eggs_for_breakfast(Breakfast),\n    eggs_for_muffins(Muffins),\n    Eggs is PerDay - Breakfast - Muffins.\n\n% calculate the daily income from selling eggs\ndaily_income(Income) :-\n    eggs_left_over(Eggs),\n    Income is Eggs * 2.\n\n/* Query */\nsolve(DailyIncome) :- daily_income(DailyIncome).\n```\nThis code first calculates the number of eggs left over after Janet eats three for breakfast and bakes four for muffins. Then, it calculates the daily income by multiplying the number of eggs left over by the price of $2 per egg.""")
# print(prolog_string, query_string)
# result = consult_prolog(prolog_string, query_string, "raw")
# print(result)