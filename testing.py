from api_calls import *

def main():
    ident = ""
    while(True):
        sel = input("\n\nSelect option to test:\n1 - Show agents\n2 - Delete agent\n3 - Show abilities\n4 - Show adversary profiles\n5 - Create manual operation\n6 - Get facts\n7 - Get specific ability\n8 - Execute fetched ability (option 7)\n9 - Execute fetched ability with fact (option 7)\n10 - Get ability result (options 8 or 9)\n")
        match sel:
            case "1":
                for agent in getAgents():
                    print("Agent [paw: " + agent["paw"] + ", platform: " + agent["platform"] + "]")
            case "2":
                print("Agents:")
                for agent in getAgents():
                    print("Agent [paw: " + agent["paw"] + ", platform: " + agent["platform"] + "]")
                sel = input("Agent to delete (paw):\n")
                deleteAgent(sel)
            case "3":
                for ability in getAbilities():
                    print("Name: " + ability["name"] + ", technique: " + ability["technique_name"])
            case "4":
                for adversary in getAdversaries():
                    print("Name: " + adversary["name"] + ", id: " + adversary["adversary_id"])
            case "5":
                print(createBlankOperation())
                
            case "6":
                oper = input("Select an operation to fetch facts from(ID)\n")
                for fact in getFacts(oper)["found"]:
                    print("Name: " + fact["name"] + ", value: " + fact["value"])
                    
            case "7":
                search = input("Term to search for (to use it after, only one should be found, if more than one is found, the lattest will be kept selected):\n")
                for ab in getAbilities():
                    if(search in ab["name"]):
                        ability = ab
                        print("Found ability: [Name: " + ability["name"] + ", technique: " + ability["technique_name"] +"]")
                        
            case "8":
                oper = input("Select the operation to execute the ability in (ID, ability should be fetched from previous search): \n")
                agent = input("The agent to use:\n")
                print("The ability was fetched from previous search")
                ident = executeAbility(oper, agent, ability)
            
            case "9":
                oper = input("Select the operation to execute the ability in (ID, ability should be fetched from previous search): \n")
                agent = input("The agent to use: \n")
                print("The ability was fetched from previous search")
                fact = []
                for factt in getFacts(oper)["found"]:
                    sel = input("Append: [" + factt["name"] + ", " + factt["value"] + "]? (Y/n): ")
                    if("Y" in sel):
                        fact.append(factt)
                ident = executeAbilityWithFact(oper, agent, ability, fact)
                
            case "10":
                result = getResult(oper, ident)
                if(result["link"]["status"] == -3):
                    print("Result is not ready yet, try later...")
                else:
                    print(getResult(oper, ident))

        

if __name__ == "__main__":
    main()