#!/usr/bin/python

TEMP_FILE = "temp.txt"
IP_FILE = "ip.txt"
IP_MAC_FILE = "ipMac.txt"
RM_FILE = "rm temp.txt -f"
READ_MODE = "r"
WRITE_MODE = "w"
APPEND_MODE = "a"

GREP = "grep"
GREP_OPT_E = "-e"
GREP_OPT_O = "-o"

TR ="tr"
REPLACE = "-s"
SINGLE_SPACE  = " "

CUT = "cut"
CUT_FIELD = "-f"
DELIMITER = "-d"

NO_DNS = "-n"

ARP = "arp"

NMAP = "nmap"
NMAP_OPT_O = "-O"
NMAP_OPT_SN = "-sn"
NMAP_OPT_SL = "-sL"


PING = "ping"
PING_COUNT = "-c 1"
PING_TIMEOUT = "-W 2"

SPACE_PATTERN = '\s+'
BRACE_PATTERN = '\)'
MAC_PATTERN = "MAC"
PORT_PATTERN = "[0-9]/"
IP_PATTERN = "10.102.**.***"


SSH_CMD = "ssh root@{} "

