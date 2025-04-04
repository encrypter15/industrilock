# IndustriLock

## Overview
IndustriLock is a penetration testing tool designed for securing industrial door control systems integrated with SCADA environments. It simulates brute-force attacks and tests SCADA integration for vulnerabilities.

- **Author**: Rick Hayes
- **Version**: 1.0
- **License**: BSD

## Features
- Simulates brute-force attacks on serial (e.g., Wiegand) and API-based door controllers.
- Tests SCADA integration for unauthorized access detection.
- Feature-rich JSON logging for audit trails.
- Robust error handling for timeouts, protocol mismatches, and hardware failures.

## Requirements
- Python 3.6+
- Libraries:
  - `pyserial` (for serial communication)
  - `requests` (for API testing)
- Install dependencies:
  ```bash
  pip install pyserial requests
  ```

## Usage
Run the tool with a target IP or hostname:
```bash
python industrilock.py 192.168.1.100
```
Optional: Specify serial port or API endpoint:
```bash
python industrilock.py 192.168.1.100 --serial /dev/ttyUSB0 --api http://192.168.1.100/api
```

### Output
- Logs are saved to `industrilock.log`.
- A JSON audit log is generated with a timestamped filename (e.g., `industrilock_audit_20250404_123456.json`).

## Vendor Compatibility
- Honeywell
- HID
- Generic RFID-based systems

## Error Handling
- Handles serial communication errors, API timeouts, and network issues.
- Logs all errors to `industrilock.log` for troubleshooting.

## License
This software is licensed under the BSD License. See the LICENSE file for details.

## Disclaimer
Use this tool responsibly and only on systems you have permission to test. The author is not liable for misuse.
```

---

### Notes
- The code includes a simple brute-force simulation for demonstration. In a real-world scenario, you'd expand the PIN range or use a dictionary attack based on vendor-specific protocols.
- The SCADA integration test assumes a generic HTTP endpoint (`/scada`). Adjust the URL and payload based on the actual system being tested.
