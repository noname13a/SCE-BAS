from api_calls import *

def main():
    ident = ""
    while(True):
        sel = input("\n\nSelecciona una opcion:\n1 - Mostrar agentes\n3 - Mostrar abilities\n4 - Mostrar adversarios\n5 - Crear operacion manual\n6 - Get facts\n7 - Get specific ability\n8 - Ejecutar ability\n9 - Execute ability with fact\n10 - Obtener resultado del ability\n")
        match sel:
            case "1":
                for agent in getAgents():
                    print(agent["paw"], agent["platform"])
            case "2":
                print("Agentes:")
                for agent in getAgents():
                    print(agent["paw"])
                sel = input("ID del agente a eliminar\n")
                deleteAgent(sel)
            case "3":
                for ability in getAbilities():
                    print(ability["name"] + ", " + ability["technique_name"])
            case "4":
                for adversary in getAdversaries():
                    print(adversary["name"] + ", " + adversary["adversary_id"])
            case "5":
                print(createBlankOperation())
                
            case "6":
                oper = input("Seleccione la operacion sobre la cual obtener los facts\n")
                for fact in getFacts(oper)["found"]:
                    print(fact["name"], fact["value"])
                    
            case "7":
                search = input("Termino\n")
                for ab in getAbilities():
                    if(search in ab["name"]):
                        ability = ab
                        print("One found")
                        
            case "8":
                oper = input("Seleccione la operacion sobre la cual ejecutar el ability\n")
                agent = input("El agente a utilizar\n")
                print("La ability es obtenida de la busqueda previa")
                ident = executeAbility(oper, agent, ability)
            
            case "9":
                oper = input("Seleccione la operacion sobre la cual ejecutar el ability\n")
                agent = input("El agente a utilizar\n")
                print("La ability es obtenida de la busqueda previa")
                fact = []
                for factt in getFacts(oper)["found"]:
                    sel = input("Append: [" + factt["name"] + ", " + factt["value"] + "]?")
                    if("Y" in sel):
                        fact.append(factt)
                ident = executeAbilityWithFact(oper, agent, ability, fact)
                
            case "10":
                if(getResult(oper, ident) == ""):
                    print("El resultado no esta listo todavia")
                else:
                    print(getResult(oper, ident))

        

if __name__ == "__main__":
    main()