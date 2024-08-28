import os
import shutil
import subprocess
import argparse
import requests
version = "1.5.3"

def clear_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def clear_remote_directory(adb_path, device_identifier, remote_path):
    adb_command = f'"{adb_path}" -s {device_identifier} shell "rm -rf {remote_path}/*"'
    subprocess.run(adb_command, shell=True)

def adb_connect_and_copy(adb_path, device_identifier, src, dest):
    adb_connect_command = f'"{adb_path}" connect {device_identifier}'
    connect_result = subprocess.run(adb_connect_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if b'already connected' in connect_result.stdout or connect_result.returncode == 0:
        print(f"Connected to {device_identifier}.")
        
        # Ensure destination directory exists
        adb_command = f'"{adb_path}" -s {device_identifier} shell "mkdir -p {dest}"'
        subprocess.run(adb_command, shell=True)
        
        # Use adb shell to copy files from src to dest
        adb_cp_command = f'"{adb_path}" -s {device_identifier} shell "cp -r {src}/* {dest}"'
        subprocess.run(adb_cp_command, shell=True)
        print(f"Files successfully copied from {src} to {dest} on {device_identifier}.")
        return True
    else:
        print(f"Failed to connect to {device_identifier}.")
        return False

def get_available_devices(adb_path):
    adb_devices_command = f'"{adb_path}" devices'
    result = subprocess.run(adb_devices_command, shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip().splitlines()

    devices = []
    for line in output[1:]:  # Skip the first line 'List of devices attached'
        if 'device' in line:
            device_id = line.split()[0]
            devices.append(device_id)
    
    return sorted(devices)  # Sort devices in ascending order

def sort_groups(devices, group_size=5):
    groups = []
    for i in range(0, len(devices), group_size):
        group = devices[i:i + group_size]
        groups.append(group)
    return groups

def create_gem_folders(tools_path):
    username_url = "https://raw.githubusercontent.com/mitbingoo/robloxtools/main/account/username.txt"
    response = requests.get(username_url)
    lines = response.content.decode('utf-8').splitlines()

    x = int(input("Enter the starting line number (x): "))
    y = int(input("Enter the ending line number (y): "))

    username_lines = lines[x-1:y]  # Adjust for 0-based indexing
    num_groups = len(username_lines) // 5  # Calculate the number of groups

    for group_number in range(1, num_groups + 1):
        user_folder = os.path.join(tools_path, f"gem/Group{group_number}")
        clear_directory(user_folder)
        
        user_index = (group_number - 1) * 5
        if user_index < len(username_lines):
            user = username_lines[user_index].strip()
            user_file = os.path.join(user_folder, f"{user}.txt")
            github_url = "https://raw.githubusercontent.com/mitbingoo/robloxtools/main/script/gem.txt"
            response = requests.get(github_url)
            response = response.content.decode('utf-8').replace('\r\n', '\n')  # Decode and replace newline characters
            response = response.replace("{user}", user)
            with open(user_file, 'w') as uf:
                uf.write(response)
            print(f"Created {user_file} for Group {group_number}")

def update_files(tools_path, script_name):
    # Define the files to update
    farm_url = (
        f"https://raw.githubusercontent.com/mitbingoo/robloxtools/main/script/farm{script_name}.txt"
    )
    files_to_update = {
        os.path.join(tools_path, "gem2", "mitbingo.txt"): "https://raw.githubusercontent.com/mitbingoo/robloxtools/main/script/mitbingo.txt",
        os.path.join(tools_path, "gemmain", "main.txt"): "https://raw.githubusercontent.com/mitbingoo/robloxtools/main/script/main.txt",
        os.path.join(tools_path, "autoexec", "farm.txt"): farm_url
    }

    # Update the files
    for file_path, url in files_to_update.items():
        response = requests.get(url)
        content = response.content.decode('utf-8').replace('\r\n', '\n')  # Decode and replace newline characters
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Finished updating {url}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="ADB Device Management Script")
    parser.add_argument("--adb-path", help="Path to adb executable")
    parser.add_argument("--tools-path", help="Path to tools directory")
    parser.add_argument("--pictures-path", help="Path to pictures directory")
    return parser.parse_args()


def main():    
    args = parse_arguments()
    adb_path = args.adb_path or r"C:\LDPlayer\LDPlayer9\adb.exe"
    tools_path = args.tools_path or os.path.join(os.environ['USERPROFILE'], "Downloads", "tools")
    pictures_path = args.pictures_path or os.path.join(os.environ['USERPROFILE'], "Documents", "XuanZhi9", "Pictures", "autoexec")
    
    remote_pictures_path = "/sdcard/Pictures/autoexec"
    remote_autoexec_path = "/sdcard/Delta/Autoexecute/"

    # Get available adb devices
    devices = get_available_devices(adb_path)

    print("========================================================================================================")
    # Assign devices to groups
    groups = sort_groups(devices)
    for group_number, group in enumerate(groups, start=1):
        print(f"Group {group_number}: {', '.join(group)}")

    # Ask the user to choose between modes
    print("========================================================================================================")
    print(f"Gem Tools v{version} - by @mitbingoo")
    print("1: Collect Gem")
    print("2: Send Gem")
    print("4: Create Gem Folders")
    print("3: Copy autoexec")
    print("5: Update txt files")
    print("6: Reload Code")
    print("7: Quit")
    print(" ")
    mode = int(input("Choose mode: "))

    if mode == 1:
        for group_number, group in enumerate(groups, start=1):
            for i, device in enumerate(group):
                leader = i == 0  # The first device in the group is the leader
                print(f"Processing device {device} in Group {group_number}")

                # Clear and prepare the pictures_path on the computer
                clear_directory(pictures_path)

                if leader:
                    # Copy files from GemMain to pictures_path
                    shutil.copytree(os.path.join(tools_path, "GemMain"), pictures_path, dirs_exist_ok=True)
                else:
                    # Copy files from Gem/Group{GroupNumber} to pictures_path
                    group_path = os.path.join(tools_path, f"Gem/Group{group_number}")
                    shutil.copytree(group_path, pictures_path, dirs_exist_ok=True)

                # Move files from remote_pictures_path to remote_autoexec_path
                clear_remote_directory(adb_path, device, remote_autoexec_path)
                adb_connect_and_copy(adb_path, device, remote_pictures_path, remote_autoexec_path)
        print("Rerunning script...")
        main()  # Call the main function again

    elif mode == 2:
        for group_number, group in enumerate(groups, start=1):
            leader_device = group[0]
            print(f"Processing leader device {leader_device} in Group {group_number}")

            # Clear and prepare the pictures_path on the computer
            clear_directory(pictures_path)

            # Copy files from Gem2 to pictures_path
            shutil.copytree(os.path.join(tools_path, "Gem2"), pictures_path, dirs_exist_ok=True)
 
            # Move files from remote_pictures_path to remote_autoexec_path
            clear_remote_directory(adb_path, leader_device, remote_autoexec_path)
            adb_connect_and_copy(adb_path, leader_device, remote_pictures_path, remote_autoexec_path)
        main()  # Call the main function again

    elif mode == 3:
        create_gem_folders(tools_path)
        main()  # Call the main function again
        
    elif mode== 5:
        # Clear and write files
        print("Choose script mode:")
        print("(X): Use farm(X).txt")
        script_mode = (input("Enter script mode: "))
        update_files(tools_path, script_mode)
        main()

    elif mode == 4:  # Farm mode
        for device in devices:
            print(f"Processing device {device}")

            # Clear and prepare the pictures_path on the computer
            clear_directory(pictures_path)

            # Copy files from Autoexec to pictures_path
            shutil.copytree(os.path.join(tools_path, "Autoexec"), pictures_path, dirs_exist_ok=True)

            # Move files from@mai remote_pictures_path to remote_autoexec_path
            clear_remote_directory(adb_path, device, remote_autoexec_path)
            adb_connect_and_copy(adb_path, device, remote_pictures_path, remote_autoexec_path)
        main()  # Call the main function again

    elif mode == 6:
        main()  # Call the main function again

    elif mode == 7:
        print("Goodbye!")
        exit()  # Quit the script

    elif mode == 8:
        device_number = int(input("Enter the device number: "))
        if device_number <= len(devices):
            device = devices[device_number - 1]  # Adjust for 0-based indexing
            print(f"Processing device {device}")

            # Clear and prepare the pictures_path on the computer
            clear_directory(pictures_path)

            # Copy files from Autoexec to pictures_path
            shutil.copytree(os.path.join(tools_path, "Autoexec"), pictures_path, dirs_exist_ok=True)

            # Move files from remote_pictures_path to remote_autoexec_path
            clear_remote_directory(adb_path, device, remote_autoexec_path)
            adb_connect_and_copy(adb_path, device, remote_pictures_path, remote_autoexec_path)
        else:
            print("Invalid device number. Please try again.")
        main()  # Call
if __name__ == "__main__":
    main()
