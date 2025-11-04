import time
import shutil
import ctypes
import argparse
import os
import sys
import subprocess

def get_free_space_gb(drive):
    total, used, free = shutil.disk_usage(drive)
    return free / (1024 ** 3)

def send_notification(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def monitor_disk_space(drive, interval, threshold):
    while True:
        free_space = get_free_space_gb(drive)
        if free_space < threshold:
            send_notification("⚠️ Espacio en disco bajo",
                              f"Quedan solo {free_space:.2f} GB libres en {drive}")
        time.sleep(interval)

def run():
    parser = argparse.ArgumentParser(description="Monitor de espacio en disco")
    parser.add_argument("--drive", type=str, default="C:\\", help="Letra del disco a revisar (ej. C:\\)")
    parser.add_argument("--interval", type=int, default=30, help="Intervalo en segundos")
    parser.add_argument("--threshold", type=float, default=10.0, help="Umbral en GB")
    parser.add_argument("--mode", choices=["foreground", "background"], default="background",
                        help="Modo de ejecución: foreground o background")
    args = parser.parse_args()

    if args.mode == "background":
        subprocess.Popen([sys.executable, __file__,
                          "--drive", args.drive,
                          "--interval", str(args.interval),
                          "--threshold", str(args.threshold),
                          "--mode", "foreground"],
                         creationflags=subprocess.CREATE_NO_WINDOW)
        print("✅ Monitor iniciado en segundo plano.")
        sys.exit(0)
    else:
        monitor_disk_space(args.drive, args.interval, args.threshold)

if __name__ == "__main__":
    run()
