1. Start Kismet as a Server



python3 script.py -u 101 --server
Explanation:

-u 101: User ID is 101.
--server: Starts Kismet as a server.
Output: Saved in the default directory kismet_results/101_<timestamp>/.
2. Specify a Capture Source



python3 script.py -u 102 --source wlan0 --output /path/to/custom/output
Explanation:

-u 102: User ID is 102.
--source wlan0: Uses wlan0 as the capture source.
--output /path/to/custom/output: Saves results to the specified directory.
3. Log Specific Types



python3 script.py -u 103 --log-types pcap,gpsxml --log-prefix kismet_logs
Explanation:

-u 103: User ID is 103.
--log-types pcap,gpsxml: Logs packets in pcap format and GPS data in gpsxml.
--log-prefix kismet_logs: Prepends kismet_logs to the log file names.
4. Monitor Specific Channels



python3 script.py -u 104 --channels 1,6,11 --daemonize
Explanation:

-u 104: User ID is 104.
--channels 1,6,11: Monitors Wi-Fi channels 1, 6, and 11.
--daemonize: Runs Kismet in the background as a daemon.
5. Capture Sources with Alerts



python3 script.py -u 105 --source wlan1 --alerts alert1,alert2 --capture-sources wlan1,wlan2
Explanation:

-u 105: User ID is 105.
--source wlan1: Uses wlan1 as the capture source.
--alerts alert1,alert2: Logs specific alerts.
--capture-sources wlan1,wlan2: Specifies multiple capture sources.
