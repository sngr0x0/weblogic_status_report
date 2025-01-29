# WebLogic Status Reporter

## Overview

The `weblogic_status_reporter.py` script is a monitoring tool designed to check the health and status of WebLogic servers. It generates an HTML report and emails it to a predefined recipient. The report includes details on server health, memory usage, JDBC connections, and JMS queues.

## Features

- Connects to a WebLogic server using WLST (WebLogic Scripting Tool).
- Generates an HTML report with:
  - Server status and health
  - Heap memory usage
  - JDBC runtime details
  - JMS status information
- Automatically categorizes report severity (Informative, Warning, or Critical).
- Sends the report via email using SMTP.

## Prerequisites

- Python with Jython support
- WebLogic Server with WLST enabled
- Access to the WebLogic domain
- A valid SMTP email account for sending reports

## Installation

1. Clone or download the script.
2. Ensure WebLogic's WLST is available in your environment.
3. Install any required Python dependencies (if applicable).

## Usage

Run the script with the following command:

For Windows:

```sh
wlst.cmd weblogic_status_reporter.py <WebLogic_Server_IP>
```

For Linux:

```sh
wlst.sh weblogic\_status\_reporter.py \<WebLogic\_Server\_IP>
```

Replace `<WebLogic_Server_IP>` with the target WebLogic server's IP or use `localhost` if running locally.

## Configuration

### Modify the following variables inside the script:

- `username`: WebLogic admin username.
- `password`: WebLogic admin password (Replace default value for security!).
- `html_file_path`: Path where the report will be saved.
- `sender_email`: Email address sending the report.
- `app_pwd`: SMTP app password for the sender email.
- `receiver_email`: Email address receiving the report.

## Example Output

The script generates an HTML report similar to `report_example.html`, displaying:

- Server and runtime details
- Color-coded health indicators (green for OK, yellow for warning, red for critical issues)
- JDBC and JMS statistics

## Security Notes

- **DO NOT** store passwords in plaintext. Use environment variables or encrypted storage.
- Ensure that SMTP credentials are secure and avoid using personal accounts for automated emails.

## Troubleshooting

- If connection fails, check if WebLogic is running and verify credentials.
- Ensure correct SMTP settings for email delivery.
- Review logs for any script execution errors.

## License

This script is provided as-is, without any warranties. Modify and use it at your own risk.

