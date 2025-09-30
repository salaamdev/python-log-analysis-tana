#!/usr/bin/env python3
"""
Python script to analyze log files and find duplicate IP addresses.
This script reads a log file, extracts client IP addresses, and identifies
IPs that appear more than once.
"""

import re
from collections import Counter


def read_log_file(filename):
    """
    Read the log file and return all lines as a list.
    """
    print(f"Reading log file: {filename}")
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        print(f"Successfully read {len(lines)} lines from the log file")
        return lines
    except FileNotFoundError:
        print(f"Error: Could not find the file '{filename}'")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def extract_ip_addresses(log_lines):
    """
    Extract all IP addresses from the log lines using regex.
    The log format is: client IP#port: query: domain...
    """
    print("Extracting IP addresses from log lines...")

    # Regular expression to match IP addresses in the format: client IP#port
    # This matches: client followed by IP address for example 192.168.0.1 followed by #
    ip_pattern = r"client\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})#"

    ip_addresses = []

    # Go through each line and extract IP addresses
    for line in log_lines:
        matches = re.findall(ip_pattern, line)
        ip_addresses.extend(matches)

    print(f"Found {len(ip_addresses)} total IP address entries")
    return ip_addresses


def count_ip_occurrences(ip_list):
    """
    Count how many times each IP address appears in the list.
    Returns a Counter object with IP addresses and their counts.
    """
    print("Counting IP address occurrences...")

    # Use Counter to count occurrences of each IP
    ip_counts = Counter(ip_list)

    print(f"Found {len(ip_counts)} unique IP addresses")
    return ip_counts


def find_duplicate_ips(ip_counts):
    """
    Find IP addresses that appear more than once.
    Returns a dictionary of duplicate IPs and their counts.
    """
    print("Identifying IP addresses that appear more than once...")

    # Filter IPs that appear more than once
    duplicate_ips = {ip: count for ip, count in ip_counts.items() if count > 1}

    print(f"Found {len(duplicate_ips)} IP addresses with multiple occurrences")
    return duplicate_ips


def print_results(duplicate_ips):
    """
    Print the results in a nice format.
    """
    print("\n" + "=" * 50)
    print("SUSPICIOUS IP ADDRESSES (appearing more than once):")
    print("=" * 50)

    if not duplicate_ips:
        print("No IP addresses found with multiple occurrences.")
        return

    # Sort by count (highest first) for better readability
    sorted_duplicates = sorted(duplicate_ips.items(), key=lambda x: x[1], reverse=True)

    for ip, count in sorted_duplicates:
        print(f"IP: {ip:15} | Count: {count} times")

    print("=" * 50)
    print(f"Total suspicious IPs: {len(duplicate_ips)}")


def main():
    """
    Main function that orchestrates the entire process.
    """
    print("Starting IP Address Analysis...")
    print("-" * 40)

    # Step 1: Read the log file
    log_filename = "logs.txt"
    log_lines = read_log_file(log_filename)

    if not log_lines:
        print("No log data to process. Exiting.")
        return

    # Step 2: Extract IP addresses from log lines
    ip_addresses = extract_ip_addresses(log_lines)

    if not ip_addresses:
        print("No IP addresses found in the log file. Exiting.")
        return

    # Step 3: Count occurrences of each IP address
    ip_counts = count_ip_occurrences(ip_addresses)

    # Step 4: Find IPs that appear more than once
    duplicate_ips = find_duplicate_ips(ip_counts)

    # Step 5: Print the results
    print_results(duplicate_ips)

    print("\nAnalysis complete!")


# Run the script when executed directly
if __name__ == "__main__":
    main()
