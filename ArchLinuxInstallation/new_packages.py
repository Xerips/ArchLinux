import subprocess
import sys


def read_file(file_path):
    with open(file_path, "r") as file:
        return set(file.read().splitlines())


def get_installed_packages():
    try:
        output = subprocess.check_output(
            ["sudo", "pacman", "-Q"], stderr=subprocess.STDOUT
        )
        return set(output.decode("utf-8").splitlines())
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.decode('utf-8')}")
        sys.exit(1)


def write_file(file_path, data):
    with open(file_path, "w") as file:
        file.write("\n".join(data))


def find_differences(input_file, output_file):
    input_packages = read_file(input_file)
    installed_packages = get_installed_packages()
    differences = input_packages.difference(installed_packages)
    write_file(output_file, differences)
    print(f"Differences written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python new_packages.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    find_differences(input_file, output_file)
