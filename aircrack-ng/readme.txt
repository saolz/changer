1. Basic Command
Purpose: Crack a WPA-PSK password using a wordlist and a capture file.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user123 --input_file capture_file.cap --attack_mode 2 --wordlist /path/to/wordlist.txt
Explanation:

--user_id user123: Unique user identifier.
--input_file capture_file.cap: The captured handshake file to analyze.
--attack_mode 2: Use WPA-PSK attack mode.
--wordlist /path/to/wordlist.txt: Path to the wordlist for brute-forcing passwords.
2. Targeting a Specific Network
Purpose: Target a specific ESSID and BSSID for cracking.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user456 --input_file capture_file.cap --attack_mode 2 --essid MyNetwork --bssid 00:11:22:33:44:55 --wordlist /path/to/wordlist.txt
Explanation:

--essid MyNetwork: Specify the network's ESSID (Wi-Fi name).
--bssid 00:11:22:33:44:55: Specify the target access point's MAC address.
3. Quiet Mode
Purpose: Run Aircrack-ng in quiet mode (no status updates) for minimal output.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user789 --input_file capture_file.cap --attack_mode 2 --wordlist /path/to/wordlist.txt --quiet_mode
Explanation:

--quiet_mode: Suppresses detailed status output from Aircrack-ng.
4. Using Additional Flags
Purpose: Add custom Aircrack-ng flags for advanced use cases.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user101 --input_file capture_file.cap --attack_mode 2 --wordlist /path/to/wordlist.txt --other_flags "-C 00:11:22:33:44:55"
Explanation:

--other_flags "-C 00:11:22:33:44:55": Merges the specified AP into a virtual one for cracking.
5. WEP Cracking Example
Purpose: Crack a WEP-encrypted network.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user202 --input_file capture_file.cap --attack_mode 1 --essid WEPNetwork --bssid 00:AA:BB:CC:DD:EE
Explanation:

--attack_mode 1: Use WEP cracking mode.
--essid WEPNetwork: Target the WEP-encrypted network.
6. Multi-CPU Usage
Purpose: Speed up cracking by utilizing multiple CPUs.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user303 --input_file capture_file.cap --attack_mode 2 --wordlist /path/to/wordlist.txt --other_flags "-p 4"
Explanation:

-p 4 (in --other_flags): Utilize 4 CPUs for processing.
7. Debugging with Quiet Mode and Specific SIMD
Purpose: Enable quiet mode and specify a SIMD architecture for debugging.

bash
Copy
Edit
python3 aircrack_tool.py --user_id user404 --input_file capture_file.cap --attack_mode 2 --wordlist /path/to/wordlist.txt --quiet_mode --other_flags "--simd=avx2"
Explanation:

--simd=avx2 (in --other_flags): Use the AVX2 SIMD architecture for optimized cracking.
