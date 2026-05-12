
# MacChangerPy

A Python script for changing the MAC address of a network interface. This tool allows users to change the MAC address to a specified value or a randomly generated one, and it supports timing the changes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ElzobeirM/MacChangerPy.git
   ```

2. Install the required dependencies:
   - Python 3.x installed.

3. Make the script executable:
   ```bash
   chmod +x MacChangerPy.py
   ```

## Usage

### Change to a specific MAC address:
```bash
python MacChangerPy.py -i eth0 -m XX:XX:XX:XX:XX:XX
```

### Show the current MAC address:
```bash
python MacChangerPy.py -i eth0 -c
```

### Change the MAC address to a random value every specified time interval:
```bash
python MacChangerPy.py -i eth0 -r -t 10
```

## Available Options:
- `-i` : Network interface (required)
- `-m` : New MAC address
- `-r` : Generate a random MAC address
- `-t` : Time interval (in seconds) for changing the MAC address (used with `-r`)
- `-c` : Show the current MAC address
- `-V` : Show the script version
