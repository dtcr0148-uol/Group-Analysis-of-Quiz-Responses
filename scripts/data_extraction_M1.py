def extract_answers_sequence(file_path):
    answers = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        
    options = []

    for line in lines:
        line = line.strip()
        if line.startswith("["):
            options.append(line)

            if len(options) == 4:
                answer = 0
                for i in range(4):
                    if options[i].startswith("[X]"):
                        answer = i + 1
                        break

                answers.append(answer)
                options = []

    while len(answers) < 100:
        answers.append(0)

    return answers[:100]


def write_answers_sequence(answers, n, destination_path):
    filename = destination_path + "/answers_list_respondent_" + str(n) + ".txt"
    with open(filename, "w") as file:
        for answer in answers:
            file.write(str(answer) + "\n")