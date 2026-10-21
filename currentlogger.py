import argparse
from datetime import datetime
from pathlib import Path
import sys
import serial




def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', help='Arduino port, for example COM3')
    parser.add_argument('--output', type=Path, default=Path(
        datetime.now().strftime('ina219_%Y%m%d_%H%M%S.txt')))
    args = parser.parse_args()
    try:
        with args.output.open('x', encoding='utf-8', buffering=1) as output:
            output.write('time_ms,load_voltage_V,current_mA\n')
            with serial.Serial(args.port, 115200, timeout=1) as device:
                print(f'Saving to {args.output.resolve()}. Press Ctrl+C to stop.')
                pending = b''
                while True:
                    pending += device.read_until(b'\n')
                    if not pending.endswith(b'\n'):
                        if len(pending) > 4096:
                            pending = b''
                        continue
                    line = pending.decode('ascii', errors='replace').strip()
                    pending = b''
                    if line.startswith('#'):
                        print(line, file=sys.stderr)
                        continue
                    fields = line.split(',')
                    if len(fields) != 3:
                        continue
                    try:
                        int(fields[0])
                        float(fields[1])
                        float(fields[2])
                    except ValueError:
                        continue  # Skip startup header or incomplete/corrupt rows.
                    output.write(line + '\n')
                    print(line)
    except KeyboardInterrupt:
        print('\nRecording stopped; file closed.')
    except (OSError, serial.SerialException) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
