"""
battery.py

This module contains core functionalities for ferd_batterpy module.
ferd_batterpy is Ferd's battery of python functions for data science projects.

Author: Ferdinand Feoli
Year: 2025
"""

import torch
import subprocess
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlDeviceGetName

def get_winsys_specs():
    """
    Gives your PC's main specs.

    Returns:
        string: Returns Windows version, CPU info, GPU info (only available for NVIDIA GPUs) and RAM info
    """
    response = "\n ============ OS Info ========================"
    os_info = subprocess.run([
        "powershell",
        "-Command",
        'Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version'
    ], capture_output=True, text=True).stdout.strip().splitlines()
    response += "\n" + os_info[0] + "\n" + os_info[2]
    response += "\n\n ============ CPU Info ======================="
    cpu_info = subprocess.run([
        "powershell",
        "-Command", 'Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors'
    ], capture_output=True, text=True).stdout.strip().splitlines()
    response += "\n" + cpu_info[0] + "\n" + cpu_info[2]
    response += "\n\n ============ GPU Info ======================="
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)  # 0 = first GPU
        info = nvmlDeviceGetMemoryInfo(handle)
        name = nvmlDeviceGetName(handle)
        total_memory_gb = info.total / (1024 ** 3)
        response += "\nGPU:        " + " " * len(name) + "VRAM\n" + f"{name}        {total_memory_gb:.2f} GB"
        if torch.cuda.is_available():
            response += "\n------------\n" + "CUDA device available:" + torch.cuda.get_device_name(0)
    except Exception as e:
        response += f"GPU info unavailable\nError message:{str(e)}\n------------------------\n" + \
            "No NVIDIA GPU?"
    response += "\n\n ============ RAM Info ======================="
    ram_info = subprocess.run([
        "powershell",
        "-Command",
        'Get-CimInstance Win32_PhysicalMemory | Select-Object BankLabel, Capacity, Speed'
    ], capture_output=True, text=True).stdout.strip().splitlines()
    if ram_info:
        response += "\n" + ram_info[0]
        for line in ram_info[2:]:
            parts = line.split()
            bank = parts[0] + parts[1]
            capacity = int(parts[2])
            speed = parts[3]
            capacity_gb = capacity / (1024 ** 3)
            response += "\n" + f"{bank:<12} {capacity_gb:.2f} GB  {speed} MHz"
    return response
