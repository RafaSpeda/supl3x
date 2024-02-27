The SUPL3X is a Denial of Service (DoS) tool, the application use threads to send requests http (in case of web DoS) or ICMP (in case of ping flood DoS).

How to use?
To start, in the terminal, execute the command python3 supl3x.py --[argument]
The arguments are:
-h or --help	> Open the help menu of application
-w or --web	> Set the target as a website	> python3 supl3x.py -w https://example.com
-n or --network		> Set the target as a network  specified by IP address	> python3 supl3x.py -n 192.168.10.1

Optional Arguments:
-t or --threads		> modify the number of threads to be used (default = 60)
-r or --requests	> modify the number of requests to be sended (default = 100000)
Example: python3 supl3x.py -w https://example.com -t 800 -r 2000000
