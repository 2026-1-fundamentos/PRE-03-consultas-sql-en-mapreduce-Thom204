import glob
import os

def hadoop(input_directory, output_directory, mapper, reducer):

    def read_records_from_input(input_directory):
        sequence = []
        files = glob.glob(f"{input_directory}/*")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append((file, line))
        return sequence

    def save_results_to_output(result):
        with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
            for key, value in result:
                f.write(f"{key}\t{value}\n")

    def create_success_file(output_directory):
        with open(os.path.join(output_directory, "_SUCCESS"), "w", encoding="utf-8") as f:
            f.write("")

    def create_output_directory(output_directory):
        if os.path.exists(output_directory):
            raise FileExistsError(f"The folder '{output_directory}' already exists.")
        else:
            os.makedirs(output_directory)

    sequence = read_records_from_input(input_directory)
    pairs_sequence = mapper(sequence)
    pairs_sequence = sorted(pairs_sequence)
    result = reducer(pairs_sequence)
    create_output_directory(output_directory)
    save_results_to_output(result)
    create_success_file(output_directory)