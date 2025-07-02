import datetime
import sys
import time
from openai import OpenAI
import secrets
import subprocess
import json
import base64
from api_calls import *
import re

# Global execution state variables
current_thread = None
used_agents = []
used_abilities = []
last_execution_agents = []
last_execution_abilities = []
execution_outputs = []
last_output = None
additional_parameters = {}

def execute_nmap_scan(operation_id, victim_ip):
    log(f"Executing nmap scan on victim: {victim_ip}")
    # Construct the nmap command with -sC and -sV options.
    command = f"nmap -sC -sV {victim_ip}"
    attack_output = subprocess.getoutput(command)
    return(attack_output)

def log(message):
    with open("attack_execution_log.txt", "a") as log_file:
        log_file.write(message + "\n")
        print(message)

# =====================================================
# Module: Threat Intelligence Database
# =====================================================

def show_agents(agents):
    for agent in agents:
        log(f"Agent - ID: {agent['paw']}, Group: {agent['group']}, Host: {agent['host']}, "
            f"Platform: {agent['platform']}, Privilege: {agent['privilege']}, Trusted: {agent['trusted']}")

def show_abilities(abilities):
    for ability in abilities:
        log(f"Ability - ID: {ability['id']}, Technique: {ability['technique']}, Tactic: {ability['tactic']}, "
            f"Name: {ability['name']}, Description: {ability['description']}, Command: {ability['command']}, "
            f"Platform: {ability['platform']}")

def show_adversaries(adversaries):
    for adversary in adversaries:
        log(f"Attack Goal: {adversary['attack_goal']}")
        log("  Adversary:")
        log(f"    - ID-ADVERSARY: {adversary['id']}, Name: {adversary['name']}, Description: {adversary['description']}")
        for ability in adversary['abilities']:
            log(f"      - ID-ABILITY: {ability.get('ability_id')}, Name: {ability.get('name')}")
        log("")

# =====================================================
# Module: Chaos Experiment Designer
# =====================================================

def update_execution_state(new_thread=None, used_agents_param=None, used_abilities_param=None, attack_output=None):
    global current_thread, used_agents, used_abilities
    global last_execution_agents, last_execution_abilities
    global execution_outputs, last_output, additional_parameters
    try:
        last_execution_agents = used_agents.copy()
        last_execution_abilities = used_abilities.copy()
        last_output = attack_output
        if new_thread:
            current_thread = new_thread
        if used_agents_param:
            used_agents = used_agents_param.copy()
        if used_abilities_param:
            used_abilities = used_abilities_param.copy()
        if attack_output:
            execution_outputs.append(attack_output)
        additional_parameters['timestamp'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    except Exception as e:
        log(f"Error updating execution state: {e}")

def get_execution_state():
    return {
        'current_thread': current_thread,
        'used_agents': used_agents,
        'used_abilities': used_abilities,
        'last_execution_agents': last_execution_agents,
        'last_execution_abilities': last_execution_abilities,
        'execution_outputs': execution_outputs,
        'last_output': last_output,
        'additional_parameters': additional_parameters
    }

def getAbilitiesFromProfile(adversary, abilities):
    ordered_abilities = []
    for ability_id in adversary['atomic_ordering']:
        ability_obj = getAbilityLocally(abilities, ability_id)
        ordered_abilities.append(ability_obj)
    return ordered_abilities

def initialize_system():
    log("Initializing system...")
    agents = getAgents()
    show_agents(agents)
    abilities = getAbilities()
    log(f"Number of agents: {len(agents)}")
    adversaries = getAdversaries()
    total_abilities = sum(len(getAbilitiesFromProfile(adversary, abilities)) for adversary in adversaries)
    log(f"Number of adversaries: {len(adversaries)}")
    log(f"Total number of abilities from adversaries: {total_abilities}")
    update_execution_state()
    return agents, adversaries

# =====================================================
# Module: Attack Tree Generator
# =====================================================

class Node:
    def __init__(self, id, type, data, dependencies=None):
        self.id = id
        self.type = type  # "attack" or "validation"
        self.data = data
        self.dependencies = dependencies or []
        self.result = None
        self.output = None

class AttackProfile:
    def __init__(self, attack_goal):
        self.attack_goal = attack_goal
        self.nodes = []
        self.adversaries = []

def generate_attack_trees(target_scan_output, adversaries, abilities):
    log("Generating attack trees using Target Scan Output...")
    target_profile = target_scan_output


    prompt = (
        f"Given the following nmap scan output:\n\n{target_profile}\n\n"
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
        selected_ids = json.loads(answer)
    except Exception as e:
        log(f"Error during LLM adversary matching: {e}")
        selected_ids = []

    attack_profiles = []
    for adversaryId in selected_ids:
        adversary = getAdversary(adversaryId)
        profile = AttackProfile('undefined')
        profile.adversaries.append(adversary)
        try:
            for abilityId in adversary['atomic_ordering']:
                node = Node(
                    id=abilityId,
                    type="attack",
                    data=getAbilityLocally(abilities, abilityId),
                )
                profile.nodes.append(node)
            if("Y" in input("Append profile " + adversary["name"].strip() + "? [Y/n]\n")):
                attack_profiles.append(profile)
        except:
            print("LLM hallucination, skipping this profile")

    log(f"Attack tree generated with {len(attack_profiles)} branch(es) based on LLM matching.")
    return attack_profiles


# =====================================================
# Module: Continuous Validator
# =====================================================

def update_tree_with_output(node, attack_output):
    try:
        node.output = attack_output
        log(f"Updated node {node.id} with output: {attack_output}")
    except Exception as e:
        log(f"Error updating tree for node {node.id}: {e}")

def save_result(node, result):
    try:
        if node:
            node.result = result
            log(f"Saved result for node {node.id}: {result}")
        else:
            log(f"Saved result: {result}")
    except Exception as e:
        log(f"Error saving result for node {node.id}: {e}")

# =====================================================
# Module: Terminator
# =====================================================

def generate_report(attack_profiles):
    log("Generating final report...")
    try:
        with open('final_report.txt', 'w') as f:
            f.write("=== Final Attack Report ===\n\n")
            for profile in attack_profiles:
                f.write("-----------------------------------------------------\n")
                f.write(f"Attack Goal: {profile.attack_goal}\n")
                f.write("Adversaries:\n")
                for adversary in profile.adversaries:
                    adversary_id = adversary.get('adversary_id', 'N/A')
                    name = adversary.get('name', 'Unnamed')
                    description = adversary.get('description', 'No description')
                    f.write(f"  * ID: {adversary_id} | Name: {name}\n")
                    f.write(f"    Description: {description}\n")
                    f.write("    Abilities:\n")
                    for ability in adversary.get('abilities', []):
                        f.write(f"      - {ability.get('name', 'Unnamed ability')}\n")
                f.write("Nodes:\n")
                for node in profile.nodes:
                    f.write(f"  * Node ID: {node.id} | Type: {node.type}\n")
                    f.write(f"    Result: {node.result}\n")
                    f.write(f"    Output: {node.output}\n")
                f.write("-----------------------------------------------------\n\n")
    except Exception as e:
        log(f"Error writing final report: {e}")

# =====================================================
# Module: Rollback Controller
# =====================================================

def rollback_execution():
    try:
        global current_thread, used_agents, used_abilities
        global last_execution_agents, last_execution_abilities
        global execution_outputs, last_output, additional_parameters
        
        # Reset the internal execution state variables.
        current_thread = None
        used_agents = []
        used_abilities = []
        last_execution_agents = []
        last_execution_abilities = []
        execution_outputs = []
        last_output = None
        additional_parameters = {}

        log("Initializing system..")
        log("Rollback executed: Global state has been reset.")
        
        # Additional API rollback actions can be added here if supported.
    except Exception as e:
        log(f"Error during rollback execution: {e}")

# =====================================================
# Module: Attacks Goals Decider
# =====================================================

def decide_attack_goals(attack_profiles):
    # Sort attack profiles based on the number of nodes.
    return sorted(attack_profiles, key=lambda profile: len(profile.nodes))

# =====================================================
# Module: Exploiter
# =====================================================

def execute_attack(node, agentId, operation_id):
    pattern = re.compile(r"#{([a-z\._]+)}")
    log(f"Executing attack: {node.data.get('name')}")
    try:
        for abi in getAbilities():
            if(node.data.get('ability_id') == abi["ability_id"]):
                ability = abi
        requirements = []
        for match in pattern.finditer(json.dumps(ability)):
            requirements.append(match.group(1))
        if(not set(requirements)):
            link_id = executeAbility(operation_id, agentId, ability)
            print(link_id)
            if link_id == -50:
                print("This ability doesnt have an executor for this platform, skipping to the next one")
                return 0,0
        else:
            print("Proceding to fact selection... Only facts required for this node will be prompted")
            fact = []
            facts = getFacts(operation_id)["found"]
            for factt in facts:
                if(factt["name"] in set(requirements)):
                    counter = 0
                    for facttt in facts:
                        if(facttt["name"] in factt["name"]):
                            counter += 1
                    if(counter == 1):
                        print("Only one fact of the type " + factt["name"] + " found, appending automatically")
                        fact.append(factt)
                    else:
                        sel = input("Append: [" + factt["name"] + ", " + factt["value"] + "]? [Y/n]\n")
                        if("Y" in sel):
                            fact.append(factt)
            link_id = executeAbilityWithFact(operation_id, agentId, ability, fact)
            if link_id == -50:
                print("This ability doesnt have an executor for this platform, skipping to the next one")
                return 0,0
        result = getResult(operation_id, link_id)
        while(result["link"]["status"] == -3):
            time.sleep(2)
            result = getResult(operation_id, link_id)
        return base64.b64decode(result["result"]).decode("utf-8"), result["link"]["status"]
    except Exception as e:
        log(f"Error executing attack {node.data.get('name')}: {e}")
        return "Error"
