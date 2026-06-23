import subprocess


def main() -> None:
    result = subprocess.run(["bluetoothctl", "list"], check=False, text=True, capture_output=True)
    print(result.stdout or result.stderr)


if __name__ == "__main__":
    main()
