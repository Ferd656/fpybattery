import torch
import subprocess

def get_winsys_specs():
    print("=== OS Info ===")
    os_cmd = 'Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version'
    result = subprocess.run(["powershell", "-Command", os_cmd], capture_output=True, text=True)
    print(result.stdout.strip())

    print("=== CPU Info ===")
    cpu_cmd = 'Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors'
    result = subprocess.run(["powershell", "-Command", cpu_cmd], capture_output=True, text=True)
    print(result.stdout.strip())

    print("=== GPU Info & VRAM ===")
    gpu_cmd = 'Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM'
    result = subprocess.run(["powershell", "-Command", gpu_cmd], capture_output=True, text=True)
    output = result.stdout.strip()
    # Convert AdapterRAM from bytes to GB (if possible)
    lines = output.splitlines()
    print(lines[0])
    for line in lines[1:]:
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[1].strip().isdigit():
            vram_gb = int(parts[1]) / (1024 ** 3)
            print(f"{parts[0]:<40} {vram_gb:.2f} GB VRAM")
        else:
            print(line)

    print("=== RAM Info (Per Module) ===")
    ram_cmd = (
        'Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity'
    )
    result = subprocess.run(["powershell", "-Command", ram_cmd], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    if lines:
        print(lines[0])  # Header
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 5:
                # Assume last parts are Manufacturer and PartNumber (may contain spaces)
                bank = parts[0]
                capacity = int(parts[1])
                speed = parts[2]
                manufacturer = parts[3]
                part_number = ' '.join(parts[4:])
                capacity_gb = capacity / (1024 ** 3)
                print(f"{bank:<12} {capacity_gb:.2f} GB  {speed} MHz  {manufacturer}  {part_number}")
            else:
                print(line)


# Call the function
get_winsys_specs()