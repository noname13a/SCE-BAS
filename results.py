from pyvis.network import Network
import json

# Create a network
net = Network(height="1500px", width="100%", directed=True)
net.toggle_physics(False)

# net.add_node(1, label="A", color="red", size=20)
# net.add_edge(0, 1, value=5, title="Connection strength")

net.add_node(0, "Download Macro-Enabled Phishing Attachment", color="green")
net.add_node(1, "Collect ARP details", color="green")
net.add_node(2, "Discover system services", color="green")
net.add_node(3, "Juicy potato", color="green")

net.add_node(4, "Scheduled Task Executing Base64 Encoded Commands From Registry", color="red")
net.add_node(5, "Screen Capture", color="grey")

net.add_node(6, "Credentials in Registry - HKCU", color="green")
net.add_node(7, "Credentials in Registry - HKLM", color="red")
net.add_node(8, "List Credential Files via PowerShell", color="green")

net.add_node(9, "Compress Data for Exfiltration With PowerShell", color="green")
net.add_node(10, "Compress Data for Exfiltration With Rar", color="red")
net.add_node(11, "Scheduled Exfiltration", color="red")
net.add_node(12, "Curl Upload File", color="green")
net.add_node(13, "C2 Data Exfiltration", color="green")
net.add_node(14, "Exfiltration Over Alternative Protocol - ICMP", color="red")
net.add_node(15, "Exfiltration Over Alternative Protocol - HTTP", color="red")
net.add_node(16, "Data exfiltration", color="green")

net.add_edge(0, 1, color="green")
net.add_edge(1, 2, color="green")
net.add_edge(2, 3, color="green")
net.add_edge(3, 4, color="green")
net.add_edge(4, 5, color="red")

net.add_edge(3, 6, color="green")
net.add_edge(3, 7, color="green")
net.add_edge(3, 8, color="green")


#net.add_edge(5, 9, color="grey")
#net.add_edge(5, 10, color="grey")
#net.add_edge(5, 13, color="grey")
#net.add_edge(5, 14, color="grey")
#net.add_edge(5, 15, color="grey")

net.add_edge(6, 9, color="green")
net.add_edge(6, 10, color="green")
net.add_edge(6, 13, color="green")
net.add_edge(6, 14, color="green")
net.add_edge(6, 15, color="green")

#net.add_edge(7, 9, color="grey")
#net.add_edge(7, 10, color="grey")
#net.add_edge(7, 13, color="grey")
#net.add_edge(7, 14, color="grey")
#net.add_edge(7, 15, color="grey")

net.add_edge(8, 9, color="green")
net.add_edge(8, 10, color="green")
net.add_edge(8, 13, color="green")
net.add_edge(8, 14, color="green")
net.add_edge(8, 15, color="green")


net.add_edge(9, 11, color="green")
net.add_edge(9, 12, color="green")

#net.add_edge(10, 11, color="grey")
#net.add_edge(10, 12, color="grey")

#net.add_edge(11, 16, color="grey")
net.add_edge(12, 16, color="green")
net.add_edge(13, 16, color="green")
#net.add_edge(14, 16, color="grey")
#net.add_edge(15, 16, color="grey")

net.set_edge_smooth("discrete")
net.barnes_hut()
net.write_html("result.html")