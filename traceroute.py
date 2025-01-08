import argparse
import subprocess
import re
import platform

def traceroute(destination, progressive=False, output_file=None):
    """
    Execute a traceroute command to the specified destination.

    :param destination: Target URL or IP address for traceroute.
    :param progressive: If True, display results progressively.
    :param output_file: File to save the output (if provided).
    """
    try:
        # Validate the destination by attempting to resolve it
        if platform.system() == "Windows":
            ping_command = ["ping", "-n", "1", destination]
        else:
            ping_command = ["ping", "-c", "1", destination]

        resolution_check = subprocess.run(
            ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if resolution_check.returncode != 0:
            raise ValueError(f"Unable to resolve target system name: {destination}")

        # Use traceroute or equivalent command
        if platform.system() == "Windows":
            traceroute_command = ["tracert", destination]
        else:
            traceroute_command = ["traceroute", destination]

        process = subprocess.Popen(
            traceroute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        results = []

        for line in process.stdout:
            # Extract IP addresses from each line using regex
            ip_match = re.search(r'\b(\d+\.\d+\.\d+\.\d+)\b', line)
            if ip_match:
                ip_address = ip_match.group(1)
                results.append(ip_address)

                if progressive:
                    print(ip_address)

        process.wait()

        if not progressive:
            # Display all results at once
            print("\n".join(results))

        if output_file:
            with open(output_file, "w") as file:
                file.write("\n".join(results))

    except ValueError as ve:
        print(ve)

    except KeyboardInterrupt:
        print("Traceroute interrupted.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'process' in locals():
            process.kill()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traceroute Script")
    parser.add_argument(
        "destination",
        type=str,
        help="The URL or IP address to traceroute.",
    )
    parser.add_argument(
        "-p", "--progressive",
        action="store_true",
        help="Display IP addresses progressively.",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        help="Save the traceroute result to the specified file.",
    )

    args = parser.parse_args()
    traceroute(args.destination, args.progressive, args.output_file)
