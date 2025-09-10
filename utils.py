import subprocess

def nmapScan(operationID, victimIP):
    log(f"Executing nmap scan on victim: {victimIP}")
    # Construct the nmap command with -sC and -sV options.
    command = f"nmap -sC -sV {victimIP}"
    scanOutput = subprocess.getoutput(command)
    return(scanOutput)

def log(message):
    with open("attack_execution_log.txt", "a") as logFile:
        logFile.write(message + "\n")
        
class Node:
    def __init__(self, ability):
        self.ability = ability
        self.result = None
        self.output = None

class Branch:
    def __init__(self):
        self.nodes = []
        self.adversaries = []