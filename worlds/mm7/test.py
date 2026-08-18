from pathlib import Path

ROM_PATH = Path("Megaman VII (USA).sfc")
MIN_LENGTH = 0x100  # 256 bytes

data = ROM_PATH.read_bytes()

def find_runs(byte_value: int):
    runs = []
    start = None

    for i, b in enumerate(data):
        if b == byte_value:
            if start is None:
                start = i
        else:
            if start is not None:
                length = i - start
                if length >= MIN_LENGTH:
                    runs.append((start, i - 1, length))
                start = None

    if start is not None:
        length = len(data) - start
        if length >= MIN_LENGTH:
            runs.append((start, len(data) - 1, length))

    return runs

for value in (0xFF,):
    print(f"\nRuns of {value:02X} >= ${MIN_LENGTH:X} bytes:\n")

    for start, end, length in find_runs(value):
        print(
            f"${start:06X} - ${end:06X}   "
            f"length=${length:04X} ({length} bytes)"
        )