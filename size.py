import os
import subprocess



def calculate_size_in_mb(path):
    total_size = 0
    
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Get the size of the file in bytes
                    file_size = os.path.getsize(file_path)
                    # Convert bytes to centimeters (1 byte = 0.000000000000026455 centimeters)
                    file_size_mb = file_size / 1024**2
                    total_size += file_size_mb
                except OSError:
                    # Handle file permission errors or other exceptions
                    pass
    
    else:
        file_size = os.path.getsize(path)
        total_size = file_size / 1024**2
    return total_size

def main(root):
    list_files = subprocess.run(["dir", "/b" ,root], shell=True, capture_output=True)

    paths = str(list_files.stdout).split("\\r")
    paths[0] = paths[0].replace("b'","")
    paths = [path.strip("\\n") for path in paths ]
    paths.pop()
    print(paths)
        

    with open(f"{root}\sizes.txt", 'w') as f:
        for path in paths:
            print(f"{root}\\{path}")
            size = calculate_size_in_mb(f"{root}\\{path}")
            f.write(f"{path:20}------------------ {size:.2f} mb")
            f.write("\n")
        
        
if __name__ == "__main__":
    while True:
        root = input("Path: ")
        if root == "0":
            break
        main(root)
    
    
        
