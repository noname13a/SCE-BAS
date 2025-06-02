import secrets
import requests
import json
import re

def getAgents():
    r = requests.get(secrets.url + "api/v2/agents", headers=secrets.auth)
    if(r.status_code == 200):
        j = json.loads(r.content)
        agents = []
        for agent in j:
          agents.append(agent)
        return agents
    else:
        print("API call error on agent retrieval: " + str(r.status_code))
        return r.status_code
    
def getAbilities():
    r = requests.get(secrets.url + "api/v2/abilities", headers = secrets.auth)
    if(r.status_code == 200):
        j = json.loads(r.content)
        abilities = []
        for ability in j:
            abilities.append(ability)
        return abilities
    else:
        print("API call error on ability retrieval: " + str(r.status_code))
        return r.status_code
        
def getAbility(id):
    r = requests.get(secrets.url + "api/v2/abilities/" + id, headers = secrets.auth)
    if(r.status_code == 200):
        j = json.loads(r.content)
        for ability in j:
            if (ability['ability_id']==id):
                return ability
    else:
        print("API call error on adversary retrieval: " + str(r.status_code))
        return r.status_code    
    
def getAbilityLocally(abilities, id):
    for ability in abilities:
        if(ability["ability_id"] == id):
            return ability
    
def getAdversaries():
    r = requests.get(secrets.url + "api/v2/adversaries", headers = secrets.auth)
    if(r.status_code == 200):
        j = json.loads(r.content)
        adversaries = []
        for adversary in j:
            adversaries.append(adversary)
        return adversaries
    else:
        print("API call error on adversary retrieval: " + str(r.status_code))
        return r.status_code
    
def getAdversary(id):
    r = requests.get(secrets.url + "api/v2/adversaries/" + id, headers = secrets.auth)
    if(r.status_code == 200):
        j = json.loads(r.content)
        return j
    else:
        print("API call error on adversary retrieval: " + str(r.status_code))
        return r.status_code
      
def createAgent(id):
    r = requests.put(secrets.url + "api/v2/agents/" + id, headers=secrets.auth, data=secrets.blank)
    if(r.status_code == 200):
        return r.status_code
    else:
        print("API call error on agent creation: " + str(r.status_code))
        return r.status_code
      
def deleteAgent(id):
    r = requests.delete(secrets.url + 'api/v2/agents/' + id, headers=secrets.auth)
    if(r.status_code == 204):
        return r.status_code
    else:
        print("API call error on agent deletion: " + str(r.status_code))
        return r.status_code
        
def getFacts(id):
    r = requests.get(secrets.url + 'api/v2/facts/' + id, headers=secrets.auth)
    if(r.status_code == 200):
        j = json.loads(r.content)
        facts = {}
        for fact in j:
            facts[fact] = j[fact]
        return facts
    else:
        print("API call error on fact retrieval: " + str(r.status_code))
        return r.status_code
    
    
def deleteFacts(id):
    facts = getFacts(id)
    for fact in facts["found"]:
        data = {"name": fact["name"],
                "value": fact["value"]
            }
        r = requests.delete(secrets.url + 'api/v2/facts', headers=secrets.auth, json=data)
        if(r.status_code == 200):
            pass
        else:
            print("API call error on fact deletion: " + str(r.status_code))
            return r.status_code
    return 200
        
        
def createBlankOperation():
    data = {
        "planner": {
            "module": "app.planners.atomic",
            "id": "aaa7c857-37a0-4c4a-85f7-4e9f7f30e31a",
            "description": "During each phase of the operation, the atomic planner iterates through each agent and sends the next\navailable ability it thinks that agent can complete. This decision is based on the agent matching the operating\nsystem (execution platform) of the ability and the ability command having no unsatisfied variables.\nThe planner then waits for each agent to complete its command before determining the subsequent abilities.\nThe abilities are processed in the order set by each agent's atomic ordering.\nFor instance, if agent A has atomic ordering (A1, A2, A3) and agent B has atomic ordering (B1, B2, B3), then\nthe planner would send (A1, B1) in the first phase, then (A2, B2), etc.\n",
            "stopping_conditions": [],
            "ignore_enforcement_modules": [],
            "params": {},
            "name": "atomic"
        },
        "state": "running",
        "chain": [],
        "auto_close": "false",
        "id": "1e83868f-2f62-472c-8d3b-7da1c48f4a0a",
        "obfuscator": "plain-text",
        "objective": {
            "id": "495a9828-cab1-44dd-a0ca-66e58177d8cc",
            "description": "This is a default objective that runs forever.",
            "percentage": 0,
            "goals": [
                {
                    "achieved": "false",
                    "target": "exhaustion",
                    "count": 1048576,
                    "value": "complete",
                    "operator": "=="
                }
            ],
            "name": "default"
        },
        "group": "",
        "source": {
            "plugin": "stockpile",
            "id": "ed32b9c3-9593-4c33-b0db-e2007315096b",
            "relationships": [],
            "adjustments": [],
            "facts": [
                {
                    "links": [],
                    "technique_id": "null",
                    "score": 1,
                    "limit_count": -1,
                    "unique": "file.sensitive.extensionwav",
                    "source": "ed32b9c3-9593-4c33-b0db-e2007315096b",
                    "value": "wav",
                    "created": "2025-01-23T18:40:24Z",
                    "origin_type": "SEEDED",
                    "relationships": [],
                    "collected_by": [],
                    "trait": "file.sensitive.extension",
                    "name": "file.sensitive.extension"
                },
                {
                    "links": [],
                    "technique_id": "null",
                    "score": 1,
                    "limit_count": -1,
                    "unique": "file.sensitive.extensionyml",
                    "source": "ed32b9c3-9593-4c33-b0db-e2007315096b",
                    "value": "yml",
                    "created": "2025-01-23T18:40:24Z",
                    "origin_type": "SEEDED",
                    "relationships": [],
                    "collected_by": [],
                    "trait": "file.sensitive.extension",
                    "name": "file.sensitive.extension"
                },
                {
                    "links": [],
                    "technique_id": "null",
                    "score": 1,
                    "limit_count": -1,
                    "unique": "file.sensitive.extensionpng",
                    "source": "ed32b9c3-9593-4c33-b0db-e2007315096b",
                    "value": "png",
                    "created": "2025-01-23T18:40:24Z",
                    "origin_type": "SEEDED",
                    "relationships": [],
                    "collected_by": [],
                    "trait": "file.sensitive.extension",
                    "name": "file.sensitive.extension"
                },
                {
                    "links": [],
                    "technique_id": "null",
                    "score": 1,
                    "limit_count": -1,
                    "unique": "server.malicious.urlkeyloggedsite.com",
                    "source": "ed32b9c3-9593-4c33-b0db-e2007315096b",
                    "value": "keyloggedsite.com",
                    "created": "2025-01-23T18:40:24Z",
                    "origin_type": "SEEDED",
                    "relationships": [],
                    "collected_by": [],
                    "trait": "server.malicious.url",
                    "name": "server.malicious.url"
                }
            ],
            "rules": [
                {
                    "action": "DENY",
                    "trait": "file.sensitive.extension",
                    "match": ".*"
                },
                {
                    "action": "ALLOW",
                    "trait": "file.sensitive.extension",
                    "match": "png"
                },
                {
                    "action": "ALLOW",
                    "trait": "file.sensitive.extension",
                    "match": "yml"
                },
                {
                    "action": "ALLOW",
                    "trait": "file.sensitive.extension",
                    "match": "wav"
                }
            ],
            "name": "basic"
        },
        "host_group": [],
        "autonomous": 1,
        "start": "2025-01-23T18:40:24Z",
        "visibility": 51,
        "adversary": {
            "adversary_id": "ad-hoc",
            "tags": [],
            "plugin": "",
            "objective": "495a9828-cab1-44dd-a0ca-66e58177d8cc",
            "description": "an empty adversary profile",
            "has_repeatable_abilities": "true",
            "atomic_ordering": [],
            "name": "ad-hoc"
        },
        "use_learning_parsers": "true",
        "name": "Manual",
        "jitter": "2/8"
    }
    r = requests.post(secrets.url + "api/v2/operations", headers=secrets.auth, json=data)
    if(r.status_code == 200):
        return r.status_code, "1e83868f-2f62-472c-8d3b-7da1c48f4a0a"
    else:
        print("API call error on operation creation: " + str(r.status_code))
        return r.status_code, "1e83868f-2f62-472c-8d3b-7da1c48f4a0a"
    
def deleteOperation(oper):
    r = requests.delete(secrets.url + "api/v2/operations/" + oper, headers=secrets.auth)
    if(r.status_code == 204):
        return r.status_code
    else:
        print("API call error on operation deletion: " + str(r.status_code))
        return r.status_code
    
def executeAbility(oper, agent, ability):
    for agen in getAgents():
        if(agent in agen["paw"]):
            ag = agen
    for exe in ability["executors"]:
        if(ag["platform"] in exe["platform"]):
            executor = exe
    data = {
        "ability":{
            "technique_id":ability["technique_id"],
            "additional_info":ability["additional_info"],
            "access":ability["access"],
            "ability_id":ability["ability_id"],
            "name":ability["name"],
            "buckets":ability["buckets"],
            "technique_name":ability["technique_name"],
            "requirements":ability["requirements"],
            "delete_payload":ability["delete_payload"],
            "tactic":ability["tactic"],
            "description":ability["description"],
            "singleton":ability["singleton"],
            "plugin":ability["plugin"],
            "privilege":ability["privilege"],
            "repeatable":ability["repeatable"],
            "executors":ability["executors"]
        },
        "paw":str(agent),
        "executor":{
            'uploads': executor["uploads"], 
            'payloads': executor["payloads"], 
            'code': executor["code"], 
            'build_target': executor["build_target"],
            'additional_info': executor["additional_info"], 
            'name': executor["name"], 
            'variations': executor["variations"], 
            'platform': executor["platform"], 
            'language': executor["language"], 
            'cleanup': executor["cleanup"], 
            'command': executor["command"], 
            'parsers': executor["parsers"], 
            'timeout': executor["timeout"]
        }
    }

    r = requests.post(secrets.url + "api/v2/operations/" + str(oper) + "/potential-links", headers=secrets.auth, json=data)
    j = json.loads(r.content)
    if(r.status_code == 200):
        return(j["id"])
    else:
        print("API call error: on factless ability execution: " + str(r.status_code))
        return r.status_code
    
def getResult(oper, ident):
    r = requests.get(secrets.url + "api/v2/operations/" + str(oper) + "/links/" + str(ident) + "/result", headers=secrets.auth)
    j = json.loads(r.content)
    if(r.status_code == 200):
        #-3 collect 0 success 1 failed
        #return base64.b64decode(j["result"]).decode("utf-8"), j["result"], j["link"]["status"]
        return j
    else:
        print("API call error on result retrieval: " + str(r.status_code))
        return r.status_code
    
def executeAbilityWithFact(oper, agent, ability, facts):
    pattern = re.compile(r"#{([a-z\._]+)}")
    for agen in getAgents():
        if(agent in agen["paw"]):
            ag = agen
    for exe in ability["executors"]:
        if(ag["platform"] in exe["platform"]):
            executor = exe

    
    command = executor["command"]        
    for match in pattern.finditer(command):
        for fact in facts:
            if(match.group(1) in fact["name"]):
                command = re.sub(match.group(0), fact["value"], command)

    data = {
        "ability":{
            "technique_id":ability["technique_id"],
            "additional_info":ability["additional_info"],
            "access":ability["access"],
            "ability_id":ability["ability_id"],
            "name":ability["name"],
            "buckets":ability["buckets"],
            "technique_name":ability["technique_name"],
            "requirements":ability["requirements"],
            "delete_payload":ability["delete_payload"],
            "tactic":ability["tactic"],
            "description":ability["description"],
            "singleton":ability["singleton"],
            "plugin":ability["plugin"],
            "privilege":ability["privilege"],
            "repeatable":ability["repeatable"],
            "executors":ability["executors"]
        },
        "paw":str(agent),
        "executor":{
            'uploads': executor["uploads"], 
            'payloads': executor["payloads"], 
            'code': executor["code"], 
            'build_target': executor["build_target"],
            'additional_info': executor["additional_info"], 
            'name': executor["name"], 
            'variations': executor["variations"], 
            'platform': executor["platform"], 
            'language': executor["language"], 
            'cleanup': executor["cleanup"], 
            'command': command, 
            'parsers': executor["parsers"], 
            'timeout': executor["timeout"]
        }
    }
    r = requests.post(secrets.url + "api/v2/operations/" + str(oper) + "/potential-links", headers=secrets.auth, json=data)
    j = json.loads(r.content)
    if(r.status_code == 200):
        return(j["id"])
    else:
        print("API call error on ability execution: " + str(r.status_code))
        print(r.content)
        return r.status_code
