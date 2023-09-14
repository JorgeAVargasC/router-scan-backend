 # Router Scan Backend API

## Table of Contents

- [Router Scan Backend API](#router-scan-backend-api)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Description

This API provides a set of endpoints to scan a router for vulnerabilities and generate reports.

## Requirements 

* Python 3.9 or higher
* Nmap 
* Microsoft Visual C++ Redistributable (Necessary for the operation of netifaces in windows)
* (Windows) cd C:\Program Files (x86)\Nmap\scripts
* (Linux) cd /usr/share/nmap/scripts/
* git clone https://github.com/vulnersCom/nmap-vulners.git 

## Installation

To install the API, clone the repository and run the following commands:

```
git clone https://github.com/JorgeAVargasC/router-scan-backend
cd router-scan-backend
```

Then, create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

Windows Users

```
python -m venv env
.\env\Scripts\activate
```

Finally, install the dependencies:

```
pip install -r requirements.txt
python app.py
```

## Usage

The API can be accessed by making requests to the following endpoints:

* `/scan`: Scans the network for vulnerabilities and saves the results in the database.
* `/scan/all`: Gets all the scan results from the database.
* `/scan/filter`: Gets the scan results from the database based on a filter.
* `/register`: Registers a new user.
* `/login`: Logs in a user.
* `/reports`: Gets all the reports from the database.
* `/reports/cve`: Gets the top CVEs from the database.
* `/reports/ip`: Gets the top IPs from the database.
* `/reports/isp`: Gets the top ISPs from the database.
* `/reports/isp/cve`: Gets the top CVEs for each ISP from the database.
* `/reports/port/cve`: Gets the top CVEs for each port from the database.
* `/reports/vendor`: Gets the top vendors from the database.
* `/reports/vendor/cve`: Gets the top CVEs for each vendor from the database.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

The API is licensed under the MIT license.



