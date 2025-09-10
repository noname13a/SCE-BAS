import time
from openai import OpenAI
import secrets
import json
import base64
from api_calls import getAdversary, getAbilityLocally, executeAbility, getFacts, executeAbilityWithFact, getResult
import re
from utils import log, Node, Branch

def generateAttackTree(targetScanOutput, adversaries, abilities):
    log("Generating attack trees using Target Scan Output...")
    targetProfile = targetScanOutput
    prompt = (
        f"Given the following nmap scan output:\n\n{targetProfile}\n\n"
        f"And the following adversary profiles in JSON format:\n\n{json.dumps(adversaries, indent=2)}\n\n"
        f"Identify the adversary profiles (by their 'id') that are most relevant for attacking this target. "
        f"Include only adversary profiles that would let a worm propagate to this machine from another infected machine."
        f"Return the result as a JSON list of adversary IDs, and only return the list."
    )
    try:
        client = OpenAI(api_key=secrets.openai_key)
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="You are an assistant that matches target scan outputs with adversary profiles for attack simulation.",
            input=prompt
        )
        answer = response.output_text
        answer = re.sub("`", "", answer)
        answer = re.sub("json", "", answer)
        selectedIDs = json.loads(answer)
    except Exception as e:
        log(f"Error during LLM adversary matching: {e}")
        selectedIDs = []
    attackTree = []
    for adversaryId in selectedIDs:
        adversary = getAdversary(adversaryId)
        branch = Branch('undefined')
        branch.adversaries.append(adversary)
        try:
            for abilityId in adversary['atomic_ordering']:
                node = Node(
                    ability=getAbilityLocally(abilities, abilityId),
                )
                branch.nodes.append(node)
            if("Y" in input("Append branch " + adversary["name"].strip() + "? [Y/n]\n")):
                attackTree.append(branch)
        except:
            print("LLM hallucination, skipping this branch")

    log(f"Attack tree generated with {len(attackTree)} branch(es) based on LLM matching.")
    return attackTree

def generateReport(attackTree):
    log("Generating final report...")
    try:
        with open('final_report.txt', 'w') as f:
            f.write("=== Final Attack Report ===\n\n")
            for branch in attackTree:
                f.write("-----------------------------------------------------\n")
                f.write("Adversaries:\n")
                for adversary in branch.adversaries:
                    adversary_id = adversary.get('adversary_id', 'N/A')
                    name = adversary.get('name', 'Unnamed')
                    description = adversary.get('description', 'No description')
                    f.write(f"  * ID: {adversary_id} | Name: {name}\n")
                    f.write(f"    Description: {description}\n")
                    f.write("    Abilities:\n")
                    for ability in adversary.get('abilities', []):
                        f.write(f"      - {ability.get('name', 'Unnamed ability')}\n")
                f.write("Nodes:\n")
                for node in branch.nodes:
                    f.write(f"  * Node ID: {node.id}\n")
                    f.write(f"    Result: {node.result}\n")
                    f.write(f"    Output: {node.output}\n")
                f.write("-----------------------------------------------------\n\n")
    except Exception as e:
        log(f"Error writing final report: {e}")


def sortAttackTree(attackTree):
    # Sort attack profiles based on the number of nodes.
    return sorted(attackTree, key=lambda branch: len(branch.nodes))

def updateNodeOutput(node, nodeOutput):
    try:
        node.output = nodeOutput
        log(f"Updated node {node.id} with output: {nodeOutput}")
    except Exception as e:
        log(f"Error updating output for node {node.id}: {e}")

def updateNodeResult(node, nodeResult):
    try:
        node.result = nodeResult
        log(f"Saved result for node {node.id}: {nodeResult}")
    except Exception as e:
        log(f"Error updating result for node {node.id}: {e}")

def executeAttackNode(node, agentId, operationID):
    pattern = re.compile(r"#{([a-z\._]+)}")
    log(f"Executing attack: {node.ability.get('name')}")
    try:
        ability = node.ability
        requirements = []
        for match in pattern.finditer(json.dumps(ability)):
            requirements.append(match.group(1))
        if(not set(requirements)):
            linkID = executeAbility(operationID, agentId, ability)
            if linkID == -50:
                print("This ability doesnt have an executor for this platform, skipping to the next one")
                return 0,0
        else:
            print("Proceding to fact selection... Only facts required for this node will be prompted")
            fact = []
            facts = getFacts(operationID)["found"]
            for factIterator in facts:
                if(factIterator["name"] in set(requirements)):
                    counter = 0
                    for facttt in facts:
                        if(facttt["name"] in factIterator["name"]):
                            counter += 1
                    if(counter == 1):
                        print("Only one fact of the type " + factIterator["name"] + " found, appending automatically...")
                        fact.append(factIterator)
                    else:
                        sel = input("Append: [" + factIterator["name"] + ", " + factIterator["value"] + "]? [Y/n]\n")
                        if("Y" in sel):
                            fact.append(factIterator)
            linkID = executeAbilityWithFact(operationID, agentId, ability, fact)
            if linkID == -50:
                print("This ability doesnt have an executor for this platform, skipping to the next one")
                return 0,0
        result = getResult(operationID, linkID)
        while(result["link"]["status"] == -3):
            time.sleep(2)
            result = getResult(operationID, linkID)
        return base64.b64decode(result["result"]).decode("utf-8"), result["link"]["status"]
    except Exception as e:
        log(f"Error executing attack {node.ability.get('name')}: {e}")
        return "Error"