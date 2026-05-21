from data_extraction_M1 import extract_answers_sequence

def generate_means_sequence(collated_answers_path):
    with open(collated_answers_path, "r") as f:
        content = f.read()
    
    sections = content.split("*\n")
    # Remove any empty sections (e.g. trailing asterisk)
    sections = [s.strip() for s in sections if s.strip()]
    
    all_sequences = []
    for section in sections:
        # Write section to a temp file so extract_answers_sequence can read it
        with open("temp_respondent.txt", "w") as tmp:
            tmp.write(section)
        sequence = extract_answers_sequence("temp_respondent.txt")
        all_sequences.append(sequence)
    
    means = []
    for q in range(100):
        answered = [seq[q] for seq in all_sequences if seq[q] != 0]
        if len(answered) == 0:
            means.append(0.0)
        else:
            means.append(sum(answered) / len(answered))
    
    return means


def visualize_data(collated_answers_path, n):
    if n != 1 and n != 2:
        print("Error: n must be 1 or 2")
        return

    means = generate_means_sequence(collated_answers_path)
    questions = list(range(1, 101))

    if n == 1:
        # Scatter plot of means
        print("Scatter plot of mean answer values per question:")
        for i, mean in enumerate(means):
            bar = "*" * int(round(mean))
            print(f"Q{i+1:>3}: {mean:.2f} {bar}")

    elif n == 2:
        # Line plot - all individual answer sequences
        with open(collated_answers_path, "r") as f:
            content = f.read()
        
        sections = content.split("*\n")
        sections = [s.strip() for s in sections if s.strip()]
        
        all_sequences = []
        for section in sections:
            with open("temp_respondent.txt", "w") as tmp:
                tmp.write(section)
            sequence = extract_answers_sequence("temp_respondent.txt")
            all_sequences.append(sequence)
        
        print("Line plot of all respondent answer sequences (Q1-Q100):")
        for i, seq in enumerate(all_sequences):
            row = "".join(str(v) for v in seq)
            print(f"R{i+1:>3}: {row}")