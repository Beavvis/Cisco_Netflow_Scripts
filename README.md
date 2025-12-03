NOTE: Some editing of the "active_flows_script.py" will be needed to identify

LINE 10            Directory you with to run the script (home diresctory)

LINES 100-104      Netflow DIRECTION and INTERFACE
                   Cosmetic, but you can do whatever you want)
                   Use INBOUND or OUTBOUND in the name for parsing/sorting displayed data.

LINES 219-221      At the bottom of the script, you can un-remark some functions once you have identified INBOUND/OUTBOUND flow records which is a 3-digit number
 


To run the script on LINUX:

1) Create a folder on your local machine /local/netflow_data   (Or wherever yuo wish to store netflow log files)
   
2) Copy all the files from: "https://github.com/bitkeks/python-netflow-v9-softflowd/tree/release/netflow"  to \local\netflow_data
  - Rename the collector.py file to collector.orig

3) Copy the collector.py file from my github: "https://github.com/Beavvis/Cisco_Netflow_Scripts/collectoy.py"  to \local\netflow_data
4) Copy the active_flows.py from my github: "https://github.com/Beavvis/Cisco_Netflow_Scripts/active_netflows_script.py"  to \local\netflow_data

5) Make sure your Cisco Router/Switch is configured to send NETFLOWS to your machine FIRST!  
   (If you don't have the first/last - the scripts will not display netflows)

flow record FLOW_OUTBOUND
  match ipv4 tos
  match ipv4 protocol
  match ipv4 source address
  match ipv4 destination address
  match transport source-port
  match transport destination-port
  collect counter bytes long
  collect counter packets long
  collect timestamp absolute first    <---
  collect timestamp absolute last     <---



6) To run the collector on your LINUX box, first, make sure your local PC (LINUX) firewall is not blocking UDP 2055
   - I have not done this in a Windows Machine yet, I will test in the future.

   Run the python script from /local/netflow_data  : NOTE: I need sudo on my machine
   sudo python3.11 collector.py -p 2055 -D

   As netflows stream to your machinem you should see a DEBUG output scrolling on your screen.


7) Now you are ready to display the active flow = open up a second CLI terminal in /local/netflow_data

   python3.11 active_flows_script.py

You should see a TABLE format of netflow data at this point.
NOTE: You should read the script: active_flows_script   and make changes (MANUALLY) to identify the FLOW-DIRECTION and INTERFACE that you have configured your Cisco switch with.





   
