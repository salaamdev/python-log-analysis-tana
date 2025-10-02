import csv
import re
from collections import defaultdict

LOG_FILE = 'application_logs.csv'
COMPONENTS = {'PolicyService', 'NetworkMonitor'}
ERROR_LEVELS = {'ERROR', 'WARNING'}
POLICY_DEPLOYMENT_FAILURE = 'POLICY_DEPLOYMENT failed'

# Patterns to count (customize as needed)
ERROR_PATTERNS = [
    r'authentication failed',
    r'connection timeout',
    r'disk space low',
    r'POLICY_DEPLOYMENT failed',
]

def read_logs(filename):
    with open(filename, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def filter_logs(logs, levels, components):
    return [
        log for log in logs
        if log.get('log_level') in levels and log.get('component') in components
    ]

def count_error_patterns(logs, patterns):
    counts = defaultdict(int)
    for log in logs:
        message = log.get('message', '')
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                counts[pattern] += 1
    return counts

def correlate_policy_deployment_failures(logs):
    # Find POLICY_DEPLOYMENT failures and preceding ERROR logs
    correlations = []
    for i, log in enumerate(logs):
        if (log.get('event_type') == 'POLICY_DEPLOYMENT' and 
            log.get('status') == 'FAILED'):
            # Look back for preceding ERROR logs (within last 5 entries)
            preceding_errors = []
            for j in range(max(0, i-5), i):
                if logs[j].get('log_level') == 'ERROR':
                    preceding_errors.append(logs[j])
            correlations.append({
                'failure_log': log,
                'preceding_errors': preceding_errors
            })
    return correlations

def main():
    logs = read_logs(LOG_FILE)
    print(f"Total logs read: {len(logs)}")
    
    # Filter for ERROR/WARNING logs from specific components
    filtered_logs = filter_logs(logs, ERROR_LEVELS, COMPONENTS)
    print(f"Filtered logs (ERROR/WARNING from PolicyService/NetworkMonitor): {len(filtered_logs)}")
    
    # Count error patterns in all logs (not just filtered)
    error_counts = count_error_patterns(logs, ERROR_PATTERNS)
    
    # Find policy deployment failures and correlate with preceding errors
    correlations = correlate_policy_deployment_failures(logs)

    print('\n--- Error/Warning Logs from PolicyService and NetworkMonitor ---')
    for log in filtered_logs[:10]:  # Show first 10
        print(f"{log['timestamp']} | {log['log_level']} | {log['component']} | {log['message']}")
    if len(filtered_logs) > 10:
        print(f"... and {len(filtered_logs) - 10} more")

    print('\n--- Error/Warning Counts by Pattern ---')
    for pattern, count in error_counts.items():
        print(f"Pattern '{pattern}': {count} occurrences")

    print(f'\n--- POLICY_DEPLOYMENT Failure Correlations (showing first 5 of {len(correlations)}) ---')
    for idx, corr in enumerate(correlations[:5], 1):
        failure_log = corr['failure_log']
        print(f"Failure #{idx}: {failure_log['timestamp']} - {failure_log['message']}")
        print('Preceding ERROR logs:')
        for err in corr['preceding_errors']:
            print(f"  - {err['timestamp']} | {err['component']} | {err['message']}")
        print()
    
    if len(correlations) > 5:
        print(f"... and {len(correlations) - 5} more policy deployment failures with correlations")

if __name__ == '__main__':
    main()
