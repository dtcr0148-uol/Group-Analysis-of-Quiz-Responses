import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

import data_preparation_M2 as M2
import data_analysis_M3 as M3
from data_extraction_M1 import extract_answers_sequence

# ── Configuration ──────────────────────────────────────────────
CLOUD_URL         = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
DATA_FOLDER       = os.path.join(os.path.dirname(__file__), "../data")
OUTPUT_FOLDER     = os.path.join(os.path.dirname(__file__), "../output")
COLLATED_FILE     = os.path.join(OUTPUT_FOLDER, "collated_answers.txt")
TOTAL_RESPONDENTS = 64

# ── Setup ───────────────────────────────────────────────────────
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ── Step 1: Download answer files ───────────────────────────────
print("Step 1: Downloading answer files...")
M2.download_answer_files(CLOUD_URL, DATA_FOLDER, TOTAL_RESPONDENTS)
print(f"  Downloaded {TOTAL_RESPONDENTS} files to {DATA_FOLDER}/")

# ── Step 2: Collate into single file ────────────────────────────
print("\nStep 2: Collating answer files...")
M2.collate_answer_files(DATA_FOLDER)
print(f"  Collated answers written to {COLLATED_FILE}")

# ── Step 3: Extract individual sequences ────────────────────────
print("\nStep 3: Extracting answer sequences per respondent...")
all_sequences = []
for n in range(1, TOTAL_RESPONDENTS + 1):
    file_path = os.path.join(DATA_FOLDER, "answers_respondent_" + str(n) + ".txt")
    seq = extract_answers_sequence(file_path)
    all_sequences.append(seq)
print(f"  Extracted sequences for {len(all_sequences)} respondents")

# ── Step 4: Compute means ────────────────────────────────────────
print("\nStep 4: Computing means sequence...")
means = M3.generate_means_sequence(COLLATED_FILE)
print(f"  Means computed for {len(means)} questions")
print(f"  Questions with responses: {sum(1 for m in means if m != 0.0)}")

# ── Step 5: Detect patterns ──────────────────────────────────────
print("\nStep 5: Analysing for deliberate patterns in correct answers...")

# Check for repeating cycle
for cycle_len in range(2, 11):
    pattern = means[:cycle_len]
    is_cycle = all(
        abs(means[i] - pattern[i % cycle_len]) < 0.5
        for i in range(100)
        if means[i] != 0.0
    )
    if is_cycle:
        print(f"  Possible repeating cycle of length {cycle_len} detected: {pattern}")

# Check for arithmetic progression
diffs = [means[i+1] - means[i] for i in range(99) if means[i] != 0.0 and means[i+1] != 0.0]
avg_diff = sum(diffs) / len(diffs) if diffs else 0
print(f"  Average step between consecutive means: {avg_diff:.4f}")

# Most common answer per question
print("\n  Most common answer per question (first 10):")
for q in range(10):
    answers = [all_sequences[r][q] for r in range(TOTAL_RESPONDENTS) if all_sequences[r][q] != 0]
    if answers:
        most_common = max(set(answers), key=answers.count)
        print(f"    Q{q+1:>3}: most common answer = {most_common}, mean = {means[q]:.2f}")

# ── Step 6: Visualise ────────────────────────────────────────────
print("\nStep 6: Visualising data...")
print("\n--- Scatter plot (n=1) ---")
M3.visualize_data(COLLATED_FILE, 1)

print("\n--- Line plot (n=2) ---")
M3.visualize_data(COLLATED_FILE, 2)

print("\nFull analysis complete.")