import os
import subprocess
import platform


OS_NAME = platform.system()


def calculate_size_in_mb(path):
    total_size = 0

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Get the size of the file in bytes
                    file_size = os.path.getsize(file_path)
                    file_size_mb = file_size / 1024**2
                    total_size += file_size_mb
                except Exception as e:
                    print("Error: ", e)
    else:
        file_size = os.path.getsize(path)
        total_size = file_size / 1024**2
    return total_size


def main(root):
    if OS_NAME == "Windows":
        slash = "\\"
        if "powershell" in os.environ.get("SHELL", "").lower():
            list_files = subprocess.run(["dir", "-name"])

        else:
            try:
                list_files = subprocess.run(
                    ["dir", "/b", root], shell=True, capture_output=True
                )
            except Exception as e:
                print("Error: ", e)
    elif OS_NAME == "Linux":
        list_files = subprocess.run(["ls", root], shell=True, capture_output=True)
        slash = "/"

    paths = list_files.stdout.decode("utf-8").split("\n")
    paths.pop()
    print(paths)
    if not paths:
        print("Wrong path or it's empty!")
        return

    len_greater = max(map(len, paths))
    layout_header = "{:^{width}} | {:^6}"
    layout_body = "{:^{width}} | {:^6.2f}"

    header = layout_header.format("Paths", "Size (mb)\n", width=len_greater)
    divider = f'{"-" * (len_greater + 10)}\n'

    with open("sizes.txt", "a") as f:
        f.write(f"**{root}**\n")
        f.write(header)
        f.write(divider)
        for path in paths:
            print(f"{root}{slash}{path}")
            size = calculate_size_in_mb(f"{root}{slash}{path}")
            body = layout_body.format(path, size, width=len_greater)
            f.write(f"{body}\n")

        f.write(f"{divider}\n")


if __name__ == "__main__":
    while True:
        root = input("Path: ")
        if root == "0":
            break
        main(root)
