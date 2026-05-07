from api_calls import getAgents, createBlankOperation, deleteOperation, deleteFacts, getAbility, executeAbilityWithFact, getResult, getAbilities, executeAbility
import sys
from dfs import Graph
import json

def main():
    agents = getAgents()
    selectedAgent = None
    for agent in agents:
        if("Y" in input("Select agent on " + agent["host"] + ", running on " + agent["platform"] + " with address " + str(agent["host_ip_addrs"]) + "? [Y/n]\n")):
            selectedAgent = agent
            break
    if(selectedAgent is None):
        print("Must select an agent")
        sys.exit(0)
    
    
    # Create an operation for the nmap scan.
    status, operationID = createBlankOperation()
    if(status == 400):
        deleteOperation(operationID)
        status, operationID = createBlankOperation()
        if(status == 200):
            print("Operation creation error recovered")
            
    deleteFacts(operationID)

    g = Graph(18)
    with open('graph.json') as graph:
        data = json.load(graph)
        for entry in data["nodes"]:
            g.add_vertex(int(entry["identifier"][4:]), entry["identifier"], {'title':entry["title"], 'identifier':entry["caldera_id"]})
            for connection in entry["connected_to"]:
                g.add_edge(int(entry["identifier"][4:]), int(connection[4:]))
    nodes = g.dfs('node0')
    
    for node in nodes:
        if(node[1][0] == ""):
            break
        for ability in getAbilities():
            if(ability["name"] == node[2]):
                link = executeAbility(operationID, agent["paw"], ability)
                getResult(operationID, link)
if __name__ == "__main__":
    main()
