# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TunixHack is a project for the Google Tunix Hackathon focused on generating reasoning traces for training data. The project processes multiple datasets and enriches them by generating structured reasoning traces that lead to final answers using LM Studio.

**Datasets Processed:**
- **Databricks Dolly 15k** - Multi-category instruction-following dataset (completed)
- **Creative Writing** - Creative writing prompts requiring narrative reasoning
- **SciQA** - Science question-answering with supporting text
- **GSM8K** - Grade school math word problems (reformatting existing reasoning)

**Project Goals:**
- Generate short, concise reasoning traces (avoiding the verbosity of large models like DeepSeek R1)
- Cover diverse task types: creative writing, science QA, math problems, general instruction-following
- Create training data suitable for smaller models (research shows smaller models struggle with long CoT reasoning)
- Use Qwen3-14B for local generation (60 tokens/sec, good instruction following, short reasoning traces)

**Dataset Completion:**
- Databricks: Full generation took 1 day, 23 hours, 18 minutes, and 8 seconds to process all ~15k examples

## Development Environment

**Python Version:** 3.12+

**Package Manager:** uv (ultraviolet)

**Key Dependencies:**
- `lmstudio>=1.5.0` - LM Studio SDK for LLM interactions
- `pandas>=2.3.3` - Data manipulation and CSV handling
- `pyarrow>=22.0.0` - Efficient data serialization
- `transformers>=4.57.3` - Tokenizer for text analysis (used in dataset filtering)

**Environment Setup:**
```bash
# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run the main processing script (generates reasoning traces)
python generate_databricks.py

# Optional: Reorganize CSV output format
python rework_databricks.py

# Optional: Analyze dataset and filter by token count
python anaylze_databricks.py

# Optional: Test LM Studio connection
python test.py
```

**Project Maintenance:**

Python automatically generates `__pycache__/` folders containing compiled bytecode files (`.pyc`) for performance optimization:
- Created when you import modules (e.g., `from prompts import PROMPTS`)
- Contains files like `module_name.cpython-312.pyc` (compiled bytecode for faster execution)
- Python checks if source files changed and recompiles as needed
- Safe to delete - Python regenerates them automatically

**Git Ignore Patterns:**
The following files/folders should be excluded from version control:
- `__pycache__/` - Python bytecode cache folders
- `*.pyc` - Compiled Python files
- `.idea/` - PyCharm/IntelliJ IDE configuration
- `.venv/` - Virtual environment (managed by uv)
- `uv.lock` - Lock file (may be project-specific preference)

Add to `.gitignore`:
```
__pycache__/
*.pyc
.idea/
.venv/
uv.lock
```

## Project Architecture

### Core Data Flow

1. **Input:** `databricks.jsonl` - 13MB JSONL file containing the Databricks Dolly 15k dataset with fields:
   - `instruction` - The task/question to perform
   - `context` - Optional contextual information (may be empty string)
   - `response` - The expected answer/output
   - `category` - Classification of task type (8 types total)

2. **Processing Pipeline** (`generate_databricks.py`):
   - `process_file()` - Reads JSONL line-by-line, extracts system prompts, categories, and original instructions
   - `create_system_prompt()` - Builds category-specific prompts using the PROMPTS dictionary
   - `generate_responses()` - Calls LM Studio model (qwen3-14b) to generate reasoning traces with time tracking and error handling
   - `print_status()` - Displays generation progress with elapsed time (DD:HH:MM:SS format)
   - `replace_thinking()` - Strips `<think>` tags from model output using regex
   - `write_csv()` - Outputs prompts, categories, and responses to CSV
   - `write_log()` - Writes any generation errors to `generation_errors.log` file

3. **Output:** `databricks_with_reason.csv` - CSV with columns:
   - `Generation Prompt` - The constructed system prompt with category-specific instructions
   - `Prompt` - The original instruction from the dataset
   - `Model_Response` - Generated reasoning + answer (with thinking removed)
   - `Categories` - The task category type

### Task Categories

The dataset includes 8 different task categories, each with specialized prompts in `prompts.py`:

**Categories requiring context:**
- `closed_qa` - Question answering with provided context
- `open_qa` - Question answering with correct answer provided
- `summarization` - Text summarization from context
- `information_extraction` - Extracting specific information from supplementary text
- `classification` - Categorization with correct answer provided

**Categories not requiring context:**
- `creative_writing` - Creative content generation
- `brainstorming` - Idea generation
- `general_qa` - Open-ended questions

### Prompt Construction Logic

`create_system_prompt()` uses pattern matching to append context appropriately:

```python
# Base prompt from PROMPTS dictionary + instruction
sys_prompt = PROMPTS[category] + "Prompt: " + prompt

# Then append category-specific fields:
# - summarization: "\nContext: " + context
# - closed_qa: "\nContext: " + context
# - open_qa: "\nCorrect Answer: " + response
# - information_extraction: "\nSupplementary Text: " + context
# - classification: "\nCorrect Answer: " + response
```

### Output Format

All generated responses follow this structured format:
```xml
<reasoning>reasoning goes here</reasoning><answer>answer goes in here</answer>
```

The model may also include `<think>` tags which are stripped via regex before output.

## Implementation Details

**LM Studio Integration:**
- Uses `lms.llm("qwen3-14b")` model
- Calls `model.respond(prompt).content` for each prompt
- Time tracking using Python's `time` module
- Progress tracking with elapsed time displayed in DD:HH:MM:SS format (or HH:MM:SS if under 1 day)
- Displays total generation time in minutes at completion

**Prompt Engineering:**
- `prompts.py` contains a `PROMPTS` dictionary mapping category names to prompt strings
- Each category has specific instructions for reasoning structure
- Comments indicate which categories need context vs. don't need context
- For `open_qa` and `classification`, prompts explicitly instruct not to reference that the correct answer was provided

**Data Handling:**
- JSONL processed line-by-line to manage memory with large dataset
- `process_file()` returns three parallel lists: generation prompts, categories, and original instructions
- CSV output uses `zip()` to combine all four data streams (generation prompts, original prompts, responses, categories)
- All responses are stripped of whitespace after removing thinking tags
- CSV includes both the original instruction and the full generation prompt for analysis

**Error Handling:**
- Try-except blocks catch generation errors for individual prompts
- Errors logged with index, prompt snippet (first 50 chars), and error message
- Failed prompts get empty string responses and processing continues
- Error log written to `generation_errors.log` at completion if any errors occurred

**Post-Processing Tools:**
- `rework_databricks.py` reorganizes CSV output format for different downstream use cases
- `anaylze_databricks.py` provides dataset analysis and token-based filtering using the transformers library
  - Uses gemma-3-1b-it tokenizer for accurate token counting
  - Filters combined prompt+response pairs to stay within specified token limits
  - Useful for preparing data for smaller models with limited context windows

## Creative Writing Dataset Processing

The `CreativeWriting/` folder contains a separate pipeline for processing creative writing prompts with reasoning trace generation.

### CreativeWriting Pipeline

**Input:** `writing-prompt.csv` - CSV file with creative writing prompts
- Data format: Python literal syntax stored as strings: `"[{'from': 'human', 'value': '...'}]"`
- Each row contains a "conversations" column with prompt data

**Processing Script:** `CreativeWriting/generate.py`
- `read_csv()` - Reads CSV and extracts prompts from conversations column
- `process_line()` - Parses Python literal strings using `ast.literal_eval()` (not JSON)
  - IMPORTANT: Uses `ast.literal_eval()` instead of `json.loads()` because data contains single-quoted Python dictionaries
  - Extracts the "value" field from the first element of the list
- `generate_thinking()` - Generates reasoning traces using LM Studio (qwen3-14b model)
  - Includes test mode with break condition (stops after 3 iterations for testing)
  - Shows progress: "i/total generated"
- `replace_thinking()` - Strips `<think>` tags from model output using regex
- `writer_csv()` - Outputs prompts and responses to CSV with columns: generation-prompt, prompt, response

**Output:** `writing-thinking.csv` - CSV with generation prompts, original prompts, and generated reasoning traces

**Key Implementation Details:**
- Uses `ast.literal_eval()` to parse Python dictionary syntax (single quotes) instead of JSON (double quotes)
- Data structure: `[{'from': 'human', 'value': 'prompt text'}]` - list containing dictionary
- Accesses first element `[0]` to get the dictionary, then extracts the 'value' key
- Follows same reasoning trace format as Databricks pipeline: `<reasoning>...</reasoning><answer>...</answer>`
- Uses a general, concise prompt for creative writing that allows flexible reasoning structure without prescriptive guidelines
- **CRITICAL:** Uses scoped `lms.Client()` context manager pattern to prevent server-side KV cache accumulation
  - Creates fresh client for each prompt using `with lms.Client() as client:` pattern in `llm_instance()` function
  - Each client is properly disposed when exiting the context
  - Prevents context overflow issues where LM Studio server accumulates conversation history
  - Symptoms of improper implementation: context shifting (n_ctx full), slower generation, discarded tokens
  - See `crap.py` for the shared `llm_instance()` implementation used across all generation pipelines

**Running the Script:**
```bash
# From project root directory
python CreativeWriting/generate.py

# Or execute the main function directly
python -m CreativeWriting.generate
```

## SciQA Dataset Processing

The `SciQA/` folder contains a pipeline for processing science question-answering data with reasoning trace generation.

### SciQA Pipeline

**Input:** `sciqa-3k.csv` - CSV file with science questions
- Data format: CSV with columns: `question`, `correct_answer`, `support`
- Contains general science questions with correct answers and supporting text paragraphs

**Processing Script:** `SciQA/generate.py`
- `read_csv()` - Reads CSV and extracts questions, answers, and support text
- `create_prompt()` - Constructs generation prompts combining system prompt with question, answer, and support text
- `generate_thinking()` - Generates reasoning traces using LM Studio (qwen3-14b model)
  - Uses shared `llm_instance()` function from `crap.py`
  - Shows progress with token counts for each generation
- `llm_instance()` - Creates scoped LM Studio client with Chat for stateless requests
- `replace_thinking()` - Strips `<think>` tags from model output using regex
- `write_csv()` - Outputs generation prompts, questions, and responses to CSV

**Prompt Template:**
```
You will be given a general science question along with the correct answer and a paragraph of supporting text.
Generate the reasoning traces that get to the final correct answer.
Your reasoning should logically lead to the final answer, think about how you will structure the reasoning traces.
Do not reference that the correct answer and a paragraph of supporting text is provided in the reasoning traces.
Your final answer should follow this format:
<reasoning>reasoning goes here</reasoning><answer>answer goes here</answer>
```

**Output:** `sciqa-thinking.csv` - CSV with columns: generation_prompt, prompt (question), response

**Running the Script:**
```bash
python SciQA/generate.py
```

## GSM8K Dataset Processing

The `gsm8k/` folder contains a pipeline for processing GSM8K math word problem data. Unlike other pipelines, this one **reformats existing reasoning** rather than generating new traces.

### GSM8K Pipeline

**Input:** `gsm8k.csv` - CSV file with grade school math word problems
- Data format: CSV with columns: `question`, `answer`
- The `answer` field contains both reasoning steps and final answer separated by `####`
- Example format: `"Step 1...\nStep 2...\n#### 42"`

**Processing Script:** `gsm8k/generate.py`
- `read_csv()` - Reads CSV and extracts questions and answers
- `process_answer()` - Reformats existing solutions into structured format
  - Replaces `####` separator with `</reasoning><answer>` tags
  - Wraps entire solution in `<reasoning>` and `</answer>` tags
  - Converts: `"reasoning\n#### answer"` → `"<reasoning>reasoning</reasoning><answer>answer</answer>"`
- `write()` - Outputs questions and reformatted answers to CSV

**Key Difference:** This pipeline does NOT use LM Studio or generate new reasoning - it only reformats the existing GSM8K dataset into the standardized format used by other pipelines.

**Output:** `gsm8k-thinking.csv` - CSV with columns: question, answer (reformatted)

**Running the Script:**
```bash
python gsm8k/generate.py
```

## Shared Utilities

**`crap.py`** - Shared utility module containing common functions used across all generation pipelines

**Functions:**
- `llm_instance(prompt: str)` - Creates scoped LM Studio client and generates response
  - Uses `with lms.Client() as client:` context manager pattern
  - Creates fresh Chat object for each request
  - Returns LLM response with stats (token counts)
  - Ensures stateless requests without context accumulation

- `replace_thinking(response: str)` - Removes `<think>` tags from model output
  - Uses regex with `re.DOTALL` flag to handle multiline thinking blocks
  - Strips whitespace after removal

**Usage in other modules:**
```python
import sys
sys.path.append('..')
from crap import llm_instance, replace_thinking

# Use in generation loop
result = llm_instance(prompt)
response = replace_thinking(result.content.strip())
```

## Files

### Core Scripts
- `generate_databricks.py` - Main processing pipeline that generates reasoning traces
  - Includes error handling and logging to `generation_errors.log`
  - Processes all 15k examples from databricks.jsonl
- `prompts.py` - Category-specific prompt templates with PROMPTS dictionary mapping
- `databricks.jsonl` - Input dataset (13MB, ~15k examples)

### Utility Scripts
- `rework_databricks.py` - Post-processing script to fix/reorganize CSV output
  - `create_prompt()` - Reconstructs prompts from JSONL with context appropriately added
  - `read_csv()` - Reads the generated CSV file
  - `write_csv()` - Writes reorganized CSV with columns: generation-prompt, prompt, model-response, categories
  - Outputs to `fixed_databricks.csv`

- `anaylze_databricks.py` - Dataset analysis and filtering script
  - `count_categories()` - Counts distribution of 8 task categories
  - `count_tokens()` - Uses transformers tokenizer (gemma-3-1b-it) to count tokens
  - `filter_csv()` - Filters dataset by max token limit (default 1024 tokens for prompt+response)
  - `in_limit()` - Checks if text is within token limit
  - `write_categories()` - Outputs category counts to CSV
  - Outputs to `databricks_filtered_1024.csv` and `categories_count.csv`

- `test.py` - Simple test script for LM Studio connection and thinking tag removal

### CreativeWriting Scripts
- `CreativeWriting/generate.py` - Creative writing prompt processing pipeline
  - `read_csv()` - Reads CSV with conversation data
  - `process_line()` - Parses Python literals using ast.literal_eval() and extracts prompt values
  - `generate_thinking()` - Generates reasoning traces using shared utilities from crap.py
  - `writer_csv()` - Writes prompts and generated responses to CSV with columns: generation-prompt, prompt, response
- `CreativeWriting/prompts.py` - Contains the creative_writing prompt template and PROMPTS dictionary
- `CreativeWriting/writing-prompt.csv` - Input dataset with creative writing prompts in Python literal format
- `CreativeWriting/writing-prompt.parquet` - Parquet format of the writing prompts dataset

### SciQA Scripts
- `SciQA/generate.py` - Science question-answering processing pipeline
  - `read_csv()` - Reads CSV with questions, answers, and support text
  - `create_prompt()` - Constructs generation prompts with system prompt + question + answer + support
  - `generate_thinking()` - Generates reasoning traces using shared utilities from crap.py
  - `llm_instance()` - Local copy of scoped client function (duplicates crap.py)
  - `replace_thinking()` - Local copy of thinking tag removal (duplicates crap.py)
  - `write_csv()` - Outputs generation prompts, questions, and responses
- `SciQA/sciqa.csv` - Full SciQA input dataset
- `SciQA/sciqa-3k.csv` - Subset of 3000 examples for faster testing/generation

### GSM8K Scripts
- `gsm8k/generate.py` - GSM8K math problem reformatting pipeline
  - `read_csv()` - Reads CSV with questions and answers
  - `process_answer()` - Reformats existing reasoning by replacing #### separator with XML tags
  - `write()` - Outputs reformatted questions and answers
  - **Note:** Does NOT generate new reasoning, only reformats existing GSM8K solutions
- `gsm8k/gsm8k.csv` - Full GSM8K input dataset
- `gsm8k/gsm3k.csv` - Subset of 3000 examples

### Shared Utilities
- `crap.py` - Common utility functions used across all generation pipelines
  - `llm_instance()` - Scoped LM Studio client with Chat for stateless requests
  - `replace_thinking()` - Regex-based removal of <think> tags
  - Imported by generation scripts using `sys.path.append('..')` pattern

### Output Files

**Databricks Pipeline Outputs:**
- `databricks_with_reason.csv` - Main output with reasoning traces (32MB)
- `generation_errors.log` - Error log from generation process (if errors occurred)
- `fixed_databricks.csv` - Reorganized CSV from rework_databricks.py
- `databricks_filtered_1024.csv` - Filtered dataset within token limits
- `categories_count.csv` - Category distribution statistics

**CreativeWriting Pipeline Outputs:**
- `writing-thinking.csv` - Generated reasoning traces for creative writing prompts

**SciQA Pipeline Outputs:**
- `SciQA/sciqa-thinking.csv` - Generated reasoning traces for science questions

**GSM8K Pipeline Outputs:**
- `gsm8k/gsm8k-thinking.csv` - Reformatted math problems with structured reasoning tags
