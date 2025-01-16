python3 script.py -u 001 --domain google.com --connect --wide --output /path/to/output/directory


1. Traverse Nearby IPs



python3 script.py -u 002 --domain example.com --traverse 5 --output /path/to/custom/directory
Explanation:

-u 002: User ID is 002.
--domain example.com: Tests the domain example.com.
--traverse 5: Scans 5 IPs near discovered records.
--output /path/to/custom/directory: Specifies a custom directory for the output.
2. Search Specific Domains



python3 script.py -u 003 --domain test.com --search example.com sub.example.com
Explanation:

-u 003: User ID is 003.
--domain test.com: Scans the domain test.com.
--search example.com sub.example.com: Expands the lookup only for example.com and sub.example.com.
3. Scan a Specific IP Range (CIDR Notation)



python3 script.py -u 004 --range 192.168.0.0/24 --delay 5
Explanation:

-u 004: User ID is 004.
--range 192.168.0.0/24: Scans the entire IP range 192.168.0.0/24.
--delay 5: Waits 5 seconds between lookups.
4. Use Subdomains from a File



python3 script.py -u 005 --domain mydomain.com --subdomain-file subdomains.txt
Explanation:

-u 005: User ID is 005.
--domain mydomain.com: Tests the domain mydomain.com.
--subdomain-file subdomains.txt: Reads subdomains from the file subdomains.txt (one per line).
5. Specify Custom DNS Servers



python3 script.py -u 006 --domain company.com --dns-servers 8.8.8.8 1.1.1.1 --tcp
Explanation:

-u 006: User ID is 006.
--domain company.com: Tests the domain company.com.
--dns-servers 8.8.8.8 1.1.1.1: Uses Google’s and Cloudflare’s DNS servers for reverse lookups.
--tcp: Forces the tool to use TCP instead of UDP.
6. Use a Combination of Options



python3 script.py -u 007 --domain sample.com --connect --wide --dns-file dnslist.txt --delay 10
Explanation:

-u 007: User ID is 007.
--domain sample.com: Tests the domain sample.com.
--connect: Attempts HTTP connections.
--wide: Scans the entire class C of discovered records.
--dns-file dnslist.txt: Uses DNS servers listed in the file dnslist.txt.
--delay 10: Adds a 10-second delay between lookups.
7. No Custom Output Directory



python3 script.py -u 008 --domain testing.com --subdomains www mail ftp
Explanation:

-u 008: User ID is 008.
--domain testing.com: Tests the domain testing.com.
--subdomains www mail ftp: Uses the subdomains www, mail, and ftp.
Default Output: The script creates the folder fierce_results/008_<timestamp>/ and saves the file fierce_008_<timestamp>_domain_testing_com.csv.
