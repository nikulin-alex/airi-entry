import ollama
import time
import json
from tasks import HARD_TASKS
# --- КОНФИГУРАЦИЯ ---
WORKER_MODEL = 'qwen2.5-coder:7b' # Поменяем в цикле
CRITIC_MODEL = 'llama3.1:8b'      # Поменяем в цикле
MAX_ITERATIONS = 2 

# Те же сложные задачи


def get_completion(model, system_prompt, user_prompt, temperature=0.2):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    try:
        response = ollama.chat(
            model=model,
            messages=messages,
            options={'temperature': temperature, 'num_predict': 512}
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error with {model}: {e}")
        return ""

def extract_and_fix_code(raw_text, task_prompt, entry_point):
    code = raw_text.strip()
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    if f"def {entry_point}(" not in code:
        lines = task_prompt.split('\n')
        sig_lines = []
        for line in lines:
            sig_lines.append(line)
            if line.strip().endswith(':'): 
                break
        signature = '\n'.join(sig_lines)
        code = signature + "\n" + code
    return code

def run_tests(code_str, test_code_str, entry_point):
    try:
        namespace = {}
        exec(code_str, namespace)
        exec(test_code_str, namespace)
        
        if 'check' in namespace and entry_point in namespace:
            namespace['check'](namespace[entry_point])
            return True, "Passed"
        else:
            return False, "Missing check or entry point"
    except Exception as e:
        return False, str(e)

def run_cross_model_experiment():
    # Конфигурации для перекрестного теста
    configs = [
        {"name": "Qwen(Worker) + Llama(Critic)", "worker": "qwen2.5-coder:7b", "critic": "llama3.1:8b"},
        {"name": "Llama(Worker) + Qwen(Critic)", "worker": "llama3.1:8b", "critic": "qwen2.5-coder:7b"}
    ]
    
    all_results = {}

    for config in configs:
        print(f"\n{'='*20} STARTING CONFIG: {config['name']} {'='*20}")
        worker_model = config['worker']
        critic_model = config['critic']
        
        results = []
        WORKER_SYSTEM = "You are a Python developer. Write the COMPLETE function code including 'def' line and imports."
        CRITIC_SYSTEM = "You are a strict Code Reviewer. Analyze the code for logical errors. If the code is correct and robust, reply exactly with 'APPROVED'. Otherwise, explain the error concisely."

        for i, task in enumerate(HARD_TASKS):
            print(f"\n--- Task {i+1}/{len(HARD_TASKS)}: {task['task_id']} ---")
            
            # 1. BASELINE (Worker alone)
            prompt_baseline = f"Complete the function:\n{task['prompt']}"
            current_code = extract_and_fix_code(get_completion(worker_model, WORKER_SYSTEM, prompt_baseline), task['prompt'], task['entry_point'])
            
            passed_base, err_base = run_tests(current_code, task['test_code'], task['entry_point'])
            print(f"Baseline ({worker_model}): {'PASS' if passed_base else 'FAIL'}")

            # 2. CROSS-MODEL REFINEMENT
            iteration = 0
            while iteration < MAX_ITERATIONS:
                iteration += 1
                
                # Critic (Other Model) reviews
                prompt_feedback = f"Review this code:\n```python\n{current_code}\n```\nTask: {task['prompt']}"
                feedback = get_completion(critic_model, CRITIC_SYSTEM, prompt_feedback)
                
                is_approved = "APPROVED" in feedback.upper()
                
                if is_approved:
                    print(f"Iter {iteration}: Critic ({critic_model}) approved.")
                    passed_check, _ = run_tests(current_code, task['test_code'], task['entry_point'])
                    if passed_check:
                        print("Tests passed. Stopping.")
                        break
                    else:
                        print("Critic was wrong! Tests failed. Forcing refinement...")
                        prompt_refine = f"The reviewer said code is OK, but it fails tests. Fix it.\nCode:\n```python\n{current_code}\n```\nOutput ONLY fixed code."
                else:
                    prompt_refine = f"Fix the code based on feedback from {critic_model}.\nCurrent Code:\n```python\n{current_code}\n```\nFeedback: {feedback}\nOutput ONLY the fixed complete code."

                # Worker fixes
                new_code_raw = get_completion(worker_model, WORKER_SYSTEM, prompt_refine)
                new_code = extract_and_fix_code(new_code_raw, task['prompt'], task['entry_point'])
                
                if new_code == current_code:
                    print(f"Iter {iteration}: Code unchanged. Stopping.")
                    break
                
                current_code = new_code
                
                passed_curr, _ = run_tests(current_code, task['test_code'], task['entry_point'])
                if passed_curr:
                    print(f"Iter {iteration}: Fixed! Tests passed.")
                    break
                else:
                    print(f"Iter {iteration}: Still failing.")

            final_passed, _ = run_tests(current_code, task['test_code'], task['entry_point'])
            
            results.append({
                "task_id": task['task_id'],
                "baseline_passed": passed_base,
                "final_passed": final_passed,
            })
            print(f"Final Result: {'PASS' if final_passed else 'FAIL'}")

        total = len(results)
        pass_base = sum(1 for r in results if r['baseline_passed'])
        pass_final = sum(1 for r in results if r['final_passed'])
        
        print(f"\n✅ Config Done!")
        print(f"Baseline Pass@1: {pass_base}/{total} ({pass_base/total*100:.1f}%)")
        print(f"Refined Pass@1:  {pass_final}/{total} ({pass_final/total*100:.1f}%)")
        
        all_results[config['name']] = {
            "baseline": pass_base,
            "refined": pass_final,
            "total": total
        }

    # Итоговый отчет
    print("\n\n" + "="*30)
    print("FINAL COMPARISON REPORT")
    print("="*30)
    for name, data in all_results.items():
        print(f"{name}:")
        print(f"  Baseline: {data['baseline']}/{data['total']}")
        print(f"  Refined:  {data['refined']}/{data['total']}")
        delta = data['refined'] - data['baseline']
        print(f"  Delta:    {delta:+d}")

if __name__ == "__main__":
    run_cross_model_experiment()