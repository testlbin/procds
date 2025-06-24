import argparse
import json
from vllm import LLM, SamplingParams
from Prompt import rule_Prompt, facts_Prompt

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Extract rules and facts from patient data using an LLM.")
    parser.add_argument("--model_path", type=str, default="pathtoyourmodel/Llama-3-8B-Chat",
                        help="Path to the LLM.")
    parser.add_argument("--tensor_parallel_size", type=int, default=4,
                        help="Tensor parallel size for the model.")
    parser.add_argument("--input_path", type=str, required=True,
                        help="Path to the input JSONL file with patient data.")
    parser.add_argument("--output_path", type=str, required=True,
                        help="Path for the output JSONL file with extracted rules and facts.")
    parser.add_argument("--temperature", type=float, default=0.2,
                        help="Sampling temperature for the LLM.")
    parser.add_argument("--top_p", type=float, default=0.9,
                        help="Top-p sampling for the LLM.")
    parser.add_argument("--max_tokens", type=int, default=2048,
                        help="Maximum number of tokens to generate.")
    return parser.parse_args()

def generate_rule_prompts_from_jsonl(jsonl_path, rule_prompt_template):
    """Generates rule prompts from a JSONL file."""
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]

    prompts = []
    for item in data:
        patient_info_items = [f"{key}: {value}" for key, value in item.items() if key != 'patient info']
        patient_info = "\n".join(patient_info_items)
        prompt = rule_prompt_template.replace("{patient_info}", patient_info)
        prompts.append(prompt)

    return prompts, data

def extract_rules_from_text(text):
    """Extracts text between '***Rules Start***' and '***Rules End***'."""
    start_marker = "***Rules Start***"
    end_marker = "***Rules End***"
    start_index = text.find(start_marker)
    if start_index != -1:
        start_index += len(start_marker)
        end_index = text.find(end_marker, start_index)
        if end_index != -1:
            return text[start_index:end_index].strip()
    return ""

def generate_facts_prompts_from_jsonl(jsonl_path, facts_prompt_template):
    """Generates facts prompts from a JSONL file."""
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]

    prompts = []
    for item in data:
        patient_info = "\n".join([f"{key}: {value}" for key, value in item.items() if key != 'patient info'])
        rules_info = "\n".join([f"{key}: {value}" for key, value in item.items() if key != 'rules'])
        prompt = facts_prompt_template.replace("{patient_info}", patient_info)
        prompt = prompt.replace("{rules_info}", rules_info)
        prompts.append(prompt)

    return prompts, data

def extract_facts_from_text(text):
    """Extracts text between '***Summary Start***' and '***Summary End***'."""
    start_marker = "***Summary Start***"
    end_marker = "***Summary End***"
    start_index = text.find(start_marker)
    if start_index != -1:
        start_index += len(start_marker)
        end_index = text.find(end_marker, start_index)
        if end_index != -1:
            return text[start_index:end_index].strip()
    return ""

def run_rule_extraction(args, llm, sampling_params):
    print(f"Generating rule prompts from {args.input_path}...")
    prompts, original_data = generate_rule_prompts_from_jsonl(args.input_path, rule_Prompt)

    print("Generating rules with the language model...")
    outputs = llm.generate(prompts, sampling_params)

    print(f"Processing generated outputs and saving to {args.output_path}...")
    with open(args.output_path, 'w', encoding='utf-8') as outfile:
        for output, data_item in zip(outputs, original_data):
            generated_text = output.outputs[0].text
            extracted_rules = extract_rules_from_text(generated_text)
            data_item['rules'] = extracted_rules
            json.dump(data_item, outfile)
            outfile.write('\n')
    print(f"Rule extraction complete. Output saved to {args.output_path}.")

def run_facts_extraction(args, llm, sampling_params):
    print(f"Generating facts prompts from {args.output_path}...")
    prompts, original_data = generate_facts_prompts_from_jsonl(args.output_path, facts_Prompt)

    print("Generating facts with the language model...")
    outputs = llm.generate(prompts, sampling_params)

    print(f"Processing generated outputs and saving to {args.output_path}...")
    with open(args.output_path, 'w', encoding='utf-8') as outfile:
        for output, data_item in zip(outputs, original_data):
            generated_text = output.outputs[0].text
            extracted_facts = extract_facts_from_text(generated_text)
            data_item['facts'] = extracted_facts
            json.dump(data_item, outfile)
            outfile.write('\n')
    print(f"Facts extraction complete. Output saved to {args.output_path}.")

def main():
    args = parse_arguments()

    print("Initializing language model...")
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        stop="<|eot_id|>"
    )
    llm = LLM(
        model=args.model_path,
        tensor_parallel_size=args.tensor_parallel_size
    )

    # Step 1: Extract rules
    run_rule_extraction(args, llm, sampling_params)
    # Step 2: Extract facts based on rules
    run_facts_extraction(args, llm, sampling_params)

if __name__ == "__main__":
    main()

    # Example command line usage
    # python Stage1_extractInfo.py --input_path data/patient.jsonl --output_path data/data_extract.jsonl --model_path pathtoyourmodel/Llama-3-8B-Chat