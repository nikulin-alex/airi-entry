# Cross-Model Refinement: Local LLM Evaluation 🧠🤖

> **Research Proposal for AIRI Summer School 2026**
> *Author: Alexandr Nikulin (1st year student, Ural Federal University)*

## 📌 Overview

This repository contains the code and results of an experimental study on the efficiency of **Self-Refine** and **Cross-Model Refinement** methods applied to local Large Language Models (LLMs).

The core hypothesis was that while single-model self-reflection often leads to degradation due to "echo chamber" effects, using heterogeneous models (different architectures/training data) for generation and criticism can significantly improve code generation accuracy on complex tasks.

## 🚀 Key Findings

We conducted experiments on 10 complex tasks from the **HumanEval** dataset using two popular open-source models: **Llama-3.1-8B** and **Qwen-2.5-Coder-7B**.

### Results Summary

| Configuration | Worker Model | Critic Model | Baseline Accuracy | Refined Accuracy | Delta |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Config A** | Qwen-2.5-Coder-7B | Llama-3.1-8B | 70% | 30% | 🔴 **-40%** |
| **Config B** | Llama-3.1-8B | Qwen-2.5-Coder-7B | 50% | 70% | 🟢 **+20%** |

### Insights
1.  **The "Echo Chamber" Problem:** When a model critiques its own code (or when a less capable model critiques a better one), it often fails to identify logical errors or introduces new ones through hallucinated feedback. This led to a significant drop in accuracy in Config A.
2.  **Power of Heterogeneity:** In Config B, **Qwen-2.5-Coder** (specialized in code) acted as a strict critic for **Llama-3.1** (general purpose). Qwen successfully identified logical flaws that Llama missed, leading to a **20% improvement** in pass rate on hard tasks.
3.  **Local Constraints:** These results were achieved on consumer hardware (RTX 3060 Mobile, 6GB VRAM), proving that sophisticated multi-agent pipelines are feasible locally with proper quantization and memory management.

## 🛠️ Methodology

### The Pipeline
The experiment uses an adaptive refinement loop:
1.  **Generate:** The *Worker* model generates initial code.
2.  **Critique:** The *Critic* model reviews the code.
    *   If `APPROVED`, the code is tested. If tests fail, the critique is ignored, and refinement is forced.
    *   If errors are found, specific feedback is generated.
3.  **Refine:** The *Worker* model rewrites the code based on feedback.
4.  **Validate:** Unit tests (from HumanEval) are run to determine success.

### Tech Stack
*   **Models:** Llama-3.1-8B-Instruct, Qwen-2.5-Coder-7B-Instruct
*   **Runtime:** Ollama (for local inference)
*   **Language:** Python 3.10+
*   **Dataset:** HumanEval (subset of hard tasks: #51, #63, #72, #85, #99, #105, #112, #124, #138, #150)

## 💻 Installation & Usage

### Prerequisites
1.  Install [Ollama](https://ollama.com/).
2.  Pull the required models:
    ```bash
    ollama pull llama3.1:8b
    ollama pull qwen2.5-coder:7b
    ```
3.  Install Python dependencies:
    ```bash
    pip install ollama
    ```

### Running the Experiment
Execute the main script to run the cross-model comparison:

```bash
python cross_model_test.py
```

The script will automatically iterate through both configurations (Qwen→Llama and Llama→Qwen) and save results to `humaneval_cross_results.json`.

## 📂 Project Structure

```text
├── README.md                  # This file
├── cross_model_test.py        # Main experimental script
├── humaneval_hard_tasks.py    # Dataset definition (10 hard tasks)
├── logs/                      # Raw output logs from experiments
└── results/                   # JSON files with detailed metrics
```

## 🤝 Acknowledgments & Methodology Note

This research was conducted with the assistance of an AI coding assistant (Qwen/Llama via Ollama) for infrastructure setup, boilerplate code generation, and debugging. 

**However:**
*   All **hypotheses**, **experimental design**, and **interpretation of results** were developed independently by the author.
*   The insight regarding "Cross-Model Refinement" efficacy and the analysis of "echo chamber" degradation are original contributions of this study.
*   The use of AI tools allowed focusing on high-level research logic rather than syntactic implementation details.

## 📬 Contact

For questions about the methodology or results, please reach out:
*   **Email:** nikulinalexandr7824@gmail.com
*   **GitHub:** @nikulin-alex
