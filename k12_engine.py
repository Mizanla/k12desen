#!/usr/bin/env python3
import psutil
import time
import sys
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_DIR = "/var/lib/k12"
CONFIG_FILE = os.path.join(CONFIG_DIR, "last_choice.txt")
SUSPEND_MODE = "-s" in sys.argv

def print_banner(target):
    mode_label = f"{Fore.RED}DESTRUCTION" if not SUSPEND_MODE else f"{Fore.YELLOW}SUSPEND"
    banner = fr"""
{Fore.CYAN}{Style.BRIGHT}  ██╗  ██╗ ██╗██████╗     ██████╗ ███████╗███████╗███████╗███╗   ██╗
{Fore.CYAN}{Style.BRIGHT}  ██║ ██╔╝███║╚════██╗    ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║
{Fore.CYAN}{Style.BRIGHT}  █████╔╝ ╚██║ █████╔╝    ██║  ██║█████╗  ███████╗█████╗  ██╔██╗ ██║
{Fore.CYAN}{Style.BRIGHT}  ██╔═██╗  ██║██╔═══╝     ██║  ██║██╔══╝  ╚════██║██╔══╝  ██║╚██╗██║
{Fore.CYAN}{Style.BRIGHT}  ██║  ██╗ ██║███████╗    ██████╔╝███████╗███████║███████╗██║ ╚████║
{Fore.CYAN}{Style.BRIGHT}  ╚═╝  ╚═╝ ╚═╝╚══════╝    ╚═════╝ ╚══════╝╚══███╔╝╚══════╝╚═╝  ╚═══╝
{Fore.CYAN}{Style.BRIGHT}                                             ╚══╝               
                                                        
{Fore.WHITE}{Style.BRIGHT}               >> K12 SYSTEM SENTINEL v3.0 <<
{Fore.CYAN}      TARGET: {Fore.WHITE}{target.upper()} {Fore.CYAN}| MODE: {mode_label}
{Fore.CYAN}----------------------------------------------------------------------
    """
    print(banner)

def get_target():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    
    last_choice = None
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            last_choice = f.read().strip()

    if last_choice:
        print(f"{Fore.CYAN}[K12]{Fore.YELLOW} Last Session: {Fore.WHITE}{last_choice}")
        print(f"{Fore.CYAN} 1){Fore.WHITE} Resume Session")
        print(f"{Fore.CYAN} 2){Fore.WHITE} New Target")
        try:
            choice = input(f"\n{Fore.GREEN}Select (1/2): {Fore.WHITE}").strip()
            if choice == "1": return last_choice
        except EOFError: return last_choice

    new_target = input(f"{Fore.GREEN}Enter Process Name: {Fore.WHITE}").strip()
    with open(CONFIG_FILE, "w") as f:
        f.write(new_target)
    return new_target

def run():
    target = get_target()
    os.system('clear')
    print_banner(target)
    
    suspended_pids = set()

    try:
        while True:
            found_this_cycle = False
            # Scan with more info: user, create_time, cpu_percent, memory_info
            for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'memory_percent']):
                try:
                    if proc.info['name'] == target:
                        found_this_cycle = True
                        pid = proc.info['pid']
                        
                        # Fetch Parent / Source Info
                        p_obj = psutil.Process(pid)
                        parent = p_obj.parent()
                        parent_name = parent.name() if parent else "System/Unknown"
                        
                        # Extra metadata
                        user = proc.info['username']
                        start_time = datetime.fromtimestamp(proc.info['create_time']).strftime('%H:%M:%S')
                        mem = f"{proc.info['memory_percent']:.2f}%"

                        if SUSPEND_MODE and pid not in suspended_pids:
                            p_obj.suspend()
                            suspended_pids.add(pid)
                            tag = f"{Fore.YELLOW}[SUSPENDED]"
                        elif not SUSPEND_MODE:
                            p_obj.terminate()
                            tag = f"{Fore.RED}[TERMINATED]"
                        else:
                            continue # Already suspended

                        # Cleaner, multi-line colored output
                        print(f"{tag} {Fore.WHITE}{target.upper()} Identified")
                        print(f" {Fore.CYAN}├─ PID:      {Fore.WHITE}{pid}")
                        print(f" {Fore.CYAN}├─ USER:     {Fore.WHITE}{user}")
                        print(f" {Fore.CYAN}├─ MEMORY:   {Fore.WHITE}{mem}")
                        print(f" {Fore.CYAN}├─ STARTED:  {Fore.WHITE}{start_time}")
                        print(f" {Fore.CYAN}└─ SOURCE:   {Fore.YELLOW}{parent_name} ({p_obj.ppid()})")
                        print(f"{Fore.CYAN}" + "─"*40)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Pulse effect to show it's scanning
            if not found_this_cycle:
                sys.stdout.write(f"\r{Fore.BLUE}[*] Scanning system for {Fore.WHITE}{target}{Fore.BLUE}...{Style.RESET_ALL}")
                sys.stdout.flush()
            
            time.sleep(1)

    except KeyboardInterrupt:
        if SUSPEND_MODE and suspended_pids:
            print(f"\n\n{Fore.CYAN}[K12] {Fore.WHITE}Exiting Secure Mode...")
            print(f"{Fore.CYAN}[K12] {Fore.WHITE}Restoring {len(suspended_pids)} suspended threads...")
            for pid in suspended_pids:
                try:
                    psutil.Process(pid).resume()
                    print(f" {Fore.GREEN}OK {Fore.WHITE}PID {pid} resumed.")
                except: continue
        else:
            print(f"\n{Fore.CYAN}[!] K12 Session Closed.")
        sys.exit(0)

if __name__ == "__main__":
    run()
