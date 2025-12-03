import subprocess
import os.path
import time
import datetime

# -----------------------------------------------------------------
# Use the local system time for filename formats
# -----------------------------------------------------------------

home = "/local/netflow_data/"                   # Change to the location of where your Netflow Logs (GZ) are being written to

current_time = datetime.datetime.now()          # This is for the Folder & File name
date = curent_time.strftime("%Y-%m-%d")         # This is for the Daily Folder name
hour = curent_time.strftime("%H")               # This is for the Hourly File name

# -----------------------------------------------------------------
# Combine the strings to create the folder-path and Date-Time
# -----------------------------------------------------------------

folder_str = f"{home}{date}_netflows/"
filename = f"{folder_str}/netflow_{hour}:00.gz"
gzip_file = filename

# -----------------------------------------------------------------
# Use zcat to read the gzip file created by the netflow
# tail the text file output (YOU CAN EDIT THIS NUMBER)
# -----------------------------------------------------------------

command = f"zcat {gzip_file} | tail -n 10"                          # Adjust this number <10> for more netflow samples as desired

try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    output_string = result.stdout

except subprocess.CalledProcessError as e:
    print (f"Command failed with ERROR: {e.stderr}")

# -----------------------------------------------------------------
# This is a list of characters to remove from the  lines of TEXT
# -----------------------------------------------------------------

my_list = ['"', ',', ':', '[', ']', '{', '}']

for a in my_list:
    output_string = output_string.replace(a, "")

data = output_string.split()

# -----------------------------------------------------------------
# INITIALIZE variables to be printed
# -----------------------------------------------------------------

SOURCE_ID = 0
DIRECTION = 0
START_TIME = 0
IPV4_SRC_ADDRESS = ""
IPV4_DST_ADDRESS = ""
PROTOCOL = 0
L4_SRC_PORT = 0
L4_DST_PORT = 0
IN_BYTES = 0
IN_PKTS = 1
END_TIME = 0
FIRST_SWITCHED = 0
LAST_SWITCHED = 0
TIME = 0
RECORD_IN = []
RECORD_OUT = []
UNID_FLOW = []

# -----------------------------------------------------------------
# The duration is in ASCII format when the seconds is over 60
# -----------------------------------------------------------------

def DURATION(duration):
    if duration <60:
        print("%d sec" % seconds)

    if duration >60:
        print("%d:%02d.%02d hours" % (seconds / 60 ** 2, seconds % 60 ** 2 / 60, seconds %60))

# -----------------------------------------------------------------
# Print the TOP Column table format
# -----------------------------------------------------------------

print (" ")
print (" ")
print ("\t\t\t\t\t  _______________________  ")
print ("\t\t\t\t\t |  NETFLOW CONNECTIONS  | ")
print ("=========================================================================================================================================================")
print ("\tTIMESTAMP\t\t DIRECTION\t SOURCE \tPort \tDestination \tPort \tPROTOCOL \tBYTES \tPKTS \tDURATION")
print ("=========================================================================================================================================================")

# -----------------------------------------------------------------
# BEGIN LOOP for printing all NETFLOW SOURCES
# -----------------------------------------------------------------
x=0
for line in data:
    if line == 'source_id':
        SOURCE_ID = int(data[x+1])
        if int(SOURCE_ID) == 256:                   # Renumber this value once you have identified a FLOW (Use INBOUND or INBOUND names for this script)
            DIRECTION = str("INBOUND_G0/0")         # Rename the DIRECTION and INTERFACE from a FLOW
        if int(SOURCE_ID) == 512:                   # Renumber this value once you have identified a FLOW (Use INBOUND or INBOUND names for this script)
            DIRECTION = str("OUTBOUND_G0/0")        # Rename the DIRECTION and INTERFACE from a FLOW
        if int(SOURCE_ID) == 768:                   # Renumber this value once you have identified a FLOW (Use INBOUND or INBOUND names for this script)
            DIRECTION = str("INBOUND_G0/1")         # Rename the DIRECTION and INTERFACE from a FLOW

    if line == 'IPV4_SRC_ADDRESS':
        IPV4_SRC_ADDRESS == int( data[x+1] )

    if line == 'IPV4_DST_ADDRESS':
        IPV4_DST_ADDRESS == int( data[x+1] )

    # -----------------------------------------------------------------
    # You can ADD your own PROTOCOL interpretation here if needed
    # -----------------------------------------------------------------

    if line == 'PROTOCOL':
        PROTOCOL = int( data[x+1] )
            if PROTOCOL == 1: PROTOCOL = str("ICMP")
            if PROTOCOL == 6: PROTOCOL = str("TCP")
            if PROTOCOL == 17: PROTOCOL = str("UDP")
            if PROTOCOL == 47: PROTOCOL = str("GRE")
            if PROTOCOL == 50: PROTOCOL = str("ESP")
            if PROTOCOL == 51: PROTOCOL = str("AHP")

    if line == 'L4_SRC_PORT': L4_SRC_PORT = int( data[x+1] ) 
    if line == 'L4_DST_PORT': L4_DST_PORT = int( data[x+1] )
    if line == 'IN_BYTES': IN_BYTES = int( data[x+1] )
    if line == 'IN_PKTS': IN_PKTS = str( data[x+1] )
    if line == 'timestamp': TIMESTAMP = data[x+1]
    if line == 'FIRST_SWITCHED': FIRST_SWITCHED= int( data[x+1] )
    if line == 'LAST_SWITCHED': LAST_SWITCHED= int( data[x+1] )

        DATE2 = int(TIMESTAMP)
        DATE1 = datetime.datetime.fromtimestamp(DATE2)
        DATE = DATE1.strftime("%Y-%m-%d %H:%M:%S")

    # -----------------------------------------------------------------
    # PRINT out the TABLE FORMAT DATA here
    # -----------------------------------------------------------------

        print ("\t" DATE, end = "")
        print ("\t" DIRECTION, end = "")
        print ("\t" IPV4_SRC_ADDRESS, end = "\t")
        print (L4_SRC_PORT, end = "  \t")
        print (IPV4_DST_ADDRESS, end = "\t")
        print (L4_DST_PORT, end = " \t")
        print ("  ",PROTOCOL, end = "\t\t")
        print (IN_BYTES, end = "")
        print (IN_PKTS, end = "")
        
        duration = LAST_SWITCHED - FIRST_SWITCHED
        duration = int(duration)

    # -----------------------------------------------------------------
    # Store the DATA in an ARRAY for priting out to IN/OUT TABLES
    # -----------------------------------------------------------------
        if len(str(DIRECTION) == 3:
            UNID_FLOW.append([DIRECTION, DATE, IPV4_SRC_ADDRESS, L4_SRC_PORT, IPV4_DST_ADDRESS, L4_DST_PORT, PROTOCOL, IN_BYTES, IN_PKTS, duration])
        else:
            if str(DIRECTION[:8]) == 'OUTBOUND':
                RECORD_OUT.append([DIRECTION, DATE, IPV4_SRC_ADDRESS, L4_SRC_PORT, IPV4_DST_ADDRESS, L4_DST_PORT, PROTOCOL, IN_BYTES, IN_PKTS, duration])
            if str(DIRECTION[:7]) == 'INBOUND':
                RECORD_IN.append([DIRECTION, DATE, IPV4_SRC_ADDRESS, L4_SRC_PORT, IPV4_DST_ADDRESS, L4_DST_PORT, PROTOCOL, IN_BYTES, IN_PKTS, duration])

x=x+1

# -----------------------------------------------------------------
# PRINT INBOUND Connecitons Table
# -----------------------------------------------------------------
def INBOUND_Connections():
    print (" ")
    print ("\t\t\t\t\t  _______________________  ")
    print ("\t\t\t\t\t |  INBOUND CONNECTIONS  | ")
    print ("_________________________________________________________________________________________________________________________")
    print (" ")
    print ("\tTIMESTAMP\t\t Source \tPort \tDestination \tPort \tPROTOCOL \tBYTES \tPKTS \tDURATION")
    print ("_________________________________________________________________________________________________________________________")
    for line in RECORD_IN:
        e=0
        print ("\t, end = "")
        for element in line:
            if e == 9: DURATION(element)
            if (e>0 and e<9): print ("element", end = "\t")

# -----------------------------------------------------------------
# PRINT OUTBOUND Connecitons Table
# -----------------------------------------------------------------
def OUTBOUND_Connections():
    print (" ")
    print ("\t\t\t\t\t  ________________________ ")
    print ("\t\t\t\t\t |  OUTBOUND CONNECTIONS  | ")
    print ("_________________________________________________________________________________________________________________________")
    print (" ")
    print ("\tTIMESTAMP\t\t Source \tPort \tDestination \tPort \tPROTOCOL \tBYTES \tPKTS \tDURATION")
    print ("_________________________________________________________________________________________________________________________")
    
    for line in RECORD_OUT:
        e=0
        print ("\t, end = "")
        for element in line:
            if e == 9: DURATION(element)
            if (e>0 and e<9): print ("element", end = "\t")
            e = e + 1
        
# -----------------------------------------------------------------
# PRINT UNIDENTIFIED Flows Table
# -----------------------------------------------------------------
def UNID_Connections():
    for line in UNID_FLOW:
        e=0
        print ("\t, end = "")
        for element in line:
            if e == 9: DURATION(element)
            if (e>0 and e<9): print ("element", end = "\t")
        e = e + 1


#INBOUND_Connections()      # Remove the '#' if you wish to see the INBOUND Table (After you have identified the FLOW (lines 96-102)
#OUTBOUND_Connections()     # Remove the '#' if you wish to see the INBOUND Table (After you have identified the FLOW (lines 96-102)

UNID_Connections()          # Remark this line once you have identified all of your 3-DIGIT number flows (lines 96-102)



