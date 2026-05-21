def download_answer_files(cloud_url, path_to_data_folder, total_respondents):
    import urllib.request

    for n in range(1, total_respondents + 1):
        url = cloud_url + "/a" + str(n) + ".txt"
        destination = path_to_data_folder + "/answers_respondent_" + str(n) + ".txt"
        urllib.request.urlretrieve(url, destination)

download_answer_files(
    "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main",
    "data",
    65
)

def collate_answer_files(data_folder_path):
    output_path = "output/collated_answers.txt"
    
    with open(output_path, "w") as output_file:
        n = 1
        while True:
            file_path = data_folder_path + "/answers_respondent_" + str(n) + ".txt"
            try:
                with open(file_path, "r") as f:
                    output_file.write(f.read())
                output_file.write("*\n")
                n += 1
            except FileNotFoundError:
                break