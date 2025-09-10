from attack_simulator import generateReport, executeAttackNode, generateAttackTree, updateNodeOutput, updateNodeResult
from api_calls import getAgents, getAdversaries, createBlankOperation, deleteOperation, deleteFacts, getAbilities
import sys
import secrets
from utils import nmapScan, log

def main():
    agents = getAgents()
    adversaries = getAdversaries()
    selectedAgent = None
    for agent in agents:
        if("Y" in input("Select agent on " + agent["host"] + ", running on " + agent["platform"] + " with address " + str(agent["host_ip_addrs"]) + "? [Y/n]\n")):
            selectedAgent = agent
            break
    if(selectedAgent is None):
        print("Must select an agent")
        sys.exit(0)
    
    # The victim machine's IP is obtained from secrets.
    victimIP = secrets.victimIP
    
    # Create an operation for the nmap scan.
    status, operationID = createBlankOperation()
    if(status == 400):
        deleteOperation(operationID)
        status, operationID = createBlankOperation()
        if(status == 200):
            print("Operation creation error recovered")
            
    deleteFacts(operationID)
    # Execute nmap on the victim machine to generate the target scan output.
    nmapScanOutput = nmapScan(operationID, victimIP)
    
    # Build the semi-automatic attack tree with the generated target scan output.
    log("Starting attack tree generation")
    attackTree = generateAttackTree(nmapScanOutput, adversaries, getAbilities())
    #attackTree = sortAttackTree(attackTree)
    log("Finished attack tree generation")
    
    # Iterate over the attack tree to execute the planned attacks.
    for branch in attackTree:
        for node in branch.nodes.copy():
            attackOutput, attackResult = executeAttackNode(node, selectedAgent["paw"], operationID)
            updateNodeResult(node, attackResult)
            if(attackResult == 0):
                updateNodeOutput(node, attackOutput)
            if(attackResult == 1):
                print("Encountered error on branch, skipping to the next one")
                break
        continue
    generateReport(attackTree)

if __name__ == "__main__":
    main()
