import argparse
import json
from Prompt import varify_Code
from vllm import LLM, SamplingParams

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Verify and correct Prolog code using LLM.")
    parser.add_argument('--input', type=str, required=True, help='Input jsonl file path containing facts, rules, and prolog fields.')
    parser.add_argument('--output', type=str, required=True, help='Output jsonl file path to write validated Prolog code.')
    parser.add_argument('--model_path', type=str, default="pathtoyourmodel/Llama-3-8B-Chat", help='Path to the LLM model.')
    parser.add_argument('--tensor_parallel_size', type=int, default=4, help='Tensor parallel size for the model.')
    parser.add_argument('--temperature', type=float, default=0.6, help='Sampling temperature.')
    parser.add_argument('--top_p', type=float, default=0.9, help='Top-p sampling.')
    parser.add_argument('--max_tokens', type=int, default=2048, help='Maximum number of tokens to generate.')
    return parser.parse_args()

def generate_prompts_from_jsonl(jsonl_path, fact_prompt):
    """
    Generate prompt list from a jsonl file.
    """
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]

    prompts = []
    for item in data:
        patient_info = "\n".join([f"{key}: {value}" for key, value in item.items() if key != 'patient info'])
        rules_info = "\n".join([f"{key}: {value}" for key, value in item.items() if key != 'rules'])
        prolog = "\n".join([f"{key}: {value}" for key, value in item.items() if key != 'prolog'])
        prompt = fact_prompt.replace("{patient_info}", patient_info)
        prompt = fact_prompt.replace("{rules_info}", rules_info)
        prompt = fact_prompt.replace("{prolog_info}", prolog)
        prompts.append(prompt)

    return prompts, data

def main():
    args = parse_args()

    # Initialize sampling parameters and model
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        stop="<|eot_id|>"
    )
    llm = LLM(model=args.model_path, tensor_parallel_size=args.tensor_parallel_size)

    # Generate prompts
    prompts, data = generate_prompts_from_jsonl(args.input, varify_Code)

    # LLM generation
    outputs = llm.generate(prompts, sampling_params)

    # Update original data with validated Prolog code
    for output, original_data in zip(outputs, data):
        generated_text = output.outputs[0].text
        original_data['prolog_valid'] = generated_text

    # Write updated data back to file
    with open(args.output, 'w', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

    print("Validated Prolog code has been saved to: {}".format(args.output))

if __name__ == "__main__":
    main()

# Example command:
# python Stage2_verifyCode.py --input data/data_prolog.jsonl --output data/data_prolog_verify.jsonl --model_path pathtoyourmodel/Llama-3-8B-Chat