from attack_simulator import *

def main():
    agents, adversaries = initialize_system()
    selected_agent = None
    for agent in agents:
        if("Y" in input("Select agent on " + agent["host"] + ", running on " + agent["platform"] + " with address " + str(agent["host_ip_addrs"]) + "? [Y/n]\n")):
            selected_agent = agent
            break
    if(selected_agent is None):
        print("Must select an agent")
        sys.exit(0)
    
    # The victim machine's IP is obtained from secrets.
    victim_ip = secrets.victim_ip
    
    # Create an operation for the nmap scan.
    status, operation_id = createBlankOperation()
    if(status == 400):
        deleteOperation(operation_id)
        status, operation_id = createBlankOperation()
        if(status == 200):
            print("Operation creation error recovered")
            
    deleteFacts(operation_id)
    # Execute nmap on the victim machine to generate the target scan output.
    target_scan_output = execute_nmap_scan(operation_id, victim_ip)
    
    # Build the semi-automatic attack tree with the generated target scan output.
    log("Starting attack tree generation")
    attack_profiles = generate_attack_trees(target_scan_output, adversaries, getAbilities())
    attack_profiles = decide_attack_goals(attack_profiles)
    log("Finished attack tree generation")
    
    # Iterate over the attack tree to execute the planned attacks.
    for profile in attack_profiles:
        for node in profile.nodes.copy():
            if node.type.lower() == "attack":
                update_execution_state(
                    new_thread=current_thread,
                    used_agents_param=used_agents,
                    used_abilities_param=used_abilities,
                    attack_output=None
                )
                
                attack_output, attack_status = execute_attack(node, selected_agent["paw"], operation_id)
                save_result(node, attack_status)
                
                if(attack_status == 0):
                    update_tree_with_output(node, attack_output)
                if(attack_status == 1):
                    print("Encountered error on branch, skipping to the next one")
                    break
        continue
                    
    
    generate_report(attack_profiles)

if __name__ == "__main__":
    main()
