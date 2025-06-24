import argparse
import json
from vllm import LLM, SamplingParams
from Prompt import prolog_Instruct

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Prolog code from facts and high-risk rules using LLM.")
    parser.add_argument('--input', type=str, required=True, help='Input jsonl file path containing facts and rules.')
    parser.add_argument('--output', type=str, required=True, help='Output jsonl file path to write generated Prolog code.')
    parser.add_argument('--model_path', type=str, default="pathtoyourmodel/Llama-3-8B-Chat", help='Path to the LLM model.')
    parser.add_argument('--tensor_parallel_size', type=int, default=4, help='Tensor parallel size for the model.')
    parser.add_argument('--temperature', type=float, default=0.6, help='Sampling temperature.')
    parser.add_argument('--top_p', type=float, default=0.9, help='Top-p sampling.')
    parser.add_argument('--max_tokens', type=int, default=2048, help='Maximum number of tokens to generate.')
    return parser.parse_args()

def generate_filled_prompts(jsonl_path, template):
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    filled_prompts = []
    for entry in data:
        filled_template = template.replace("{Patient_Info}", entry['facts']).replace("{High_Risk}", entry['rules'])
        filled_prompts.append(filled_template)
    return filled_prompts, data

def main():
    args = parse_args()
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        stop="<|eot_id|>"
    )
    llm = LLM(model=args.model_path, tensor_parallel_size=args.tensor_parallel_size)
    prompts, data = generate_filled_prompts(args.input, prolog_Instruct)
    outputs = llm.generate(prompts, sampling_params)
    for output, original_data in zip(outputs, data):
        generated_text = output.outputs[0].text
        original_data['prolog'] = generated_text
    with open(args.output, 'w', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')
    print("Generated Prolog code has been saved to: {}".format(args.output))

if __name__ == "__main__":
    main()

# Example command
# python Stage2_prologGenerate.py --input data/data_extract.jsonl --output data/data_prolog.jsonl