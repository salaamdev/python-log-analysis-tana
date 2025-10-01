#!/usr/bin/env python3
"""
Improved Log Analysis Script for Policy Deployment Events
This script analyzes application_logs.csv to find and analyze policy deployment events.
"""

import csv
from collections import Counter

def analyze_policy_deployments(csv_file_path):
    """
    Analyze policy deployment events from the CSV log file.
    
    Args:
        csv_file_path (str): Path to the CSV file
    
    Returns:
        dict: Analysis results containing deployment statistics and details
    """
    all_deployments = []
    successful_deployments = []
    failed_deployments = []
    pending_deployments = []
    
    print(f"Reading CSV file: {csv_file_path}")
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Filter for POLICY_DEPLOYMENT events
                if row['event_type'] == 'POLICY_DEPLOYMENT':
                    deployment_data = {
                        'timestamp': row['timestamp'],
                        'policy_id': row['policy_id'],
                        'device_id': row['device_id'],
                        'status': row['status'],
                        'message': row['message']
                    }
                    
                    all_deployments.append(deployment_data)
                    
                    # Categorize by status
                    if row['status'] == 'SUCCESS':
                        successful_deployments.append(deployment_data)
                    elif row['status'] == 'FAILED':
                        failed_deployments.append(deployment_data)
                    elif row['status'] == 'PENDING':
                        pending_deployments.append(deployment_data)
    
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} not found!")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    # Calculate completed deployments (SUCCESS + FAILED)
    completed_deployments = len(successful_deployments) + len(failed_deployments)
    
    # Create analysis results
    results = {
        'total_deployments': len(all_deployments),
        'completed_deployments': completed_deployments,
        'successful_deployments': len(successful_deployments),
        'failed_deployments': len(failed_deployments),
        'pending_deployments': len(pending_deployments),
        'success_rate': (len(successful_deployments) / completed_deployments * 100) if completed_deployments > 0 else 0,
        'all_deployments': all_deployments,
        'successful_details': successful_deployments,
        'failed_details': failed_deployments,
        'pending_details': pending_deployments
    }
    
    return results

def analyze_deployment_patterns(results):
    """Analyze patterns in the deployment data."""
    if not results:
        return
    
    # Count deployments by policy ID
    policy_counts = Counter()
    policy_success_counts = Counter()
    
    # Count deployments by device ID
    device_counts = Counter()
    device_success_counts = Counter()
    
    for deployment in results['all_deployments']:
        policy_id = deployment['policy_id']
        device_id = deployment['device_id']
        
        policy_counts[policy_id] += 1
        device_counts[device_id] += 1
        
        if deployment['status'] == 'SUCCESS':
            policy_success_counts[policy_id] += 1
            device_success_counts[device_id] += 1
    
    # Analyze failure reasons
    failure_reasons = Counter()
    for deployment in results['failed_details']:
        message = deployment['message']
        if 'Invalid rule syntax' in message:
            failure_reasons['Invalid rule syntax'] += 1
        elif 'Connection timed out' in message:
            failure_reasons['Connection timed out'] += 1
        else:
            failure_reasons['Other'] += 1
    
    return {
        'top_policies': policy_counts.most_common(5),
        'top_devices': device_counts.most_common(5),
        'policy_success_rates': {pid: (policy_success_counts[pid] / policy_counts[pid] * 100) 
                                for pid in policy_counts.keys()},
        'device_success_rates': {did: (device_success_counts[did] / device_counts[did] * 100) 
                                for did in device_counts.keys()},
        'failure_reasons': failure_reasons
    }

def print_analysis_summary(results):
    """Print a comprehensive summary of the analysis results."""
    if not results:
        print("No results to display.")
        return
    
    print("\n" + "="*60)
    print("POLICY DEPLOYMENT ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"Total Policy Deployment Events: {results['total_deployments']}")
    print(f"Completed Deployments (Success + Failed): {results['completed_deployments']}")
    print(f"Successful Deployments: {results['successful_deployments']}")
    print(f"Failed Deployments: {results['failed_deployments']}")
    print(f"Pending Deployments: {results['pending_deployments']}")
    print(f"Success Rate (of completed): {results['success_rate']:.1f}%")
    
    # Analyze patterns
    patterns = analyze_deployment_patterns(results)
    
    if patterns:
        print("\n" + "-"*40)
        print("TOP POLICIES BY DEPLOYMENT COUNT:")
        print("-"*40)
        for policy_id, count in patterns['top_policies']:
            success_rate = patterns['policy_success_rates'][policy_id]
            print(f"Policy {policy_id}: {count} deployments ({success_rate:.1f}% success rate)")
        
        print("\n" + "-"*40)
        print("TOP DEVICES BY DEPLOYMENT COUNT:")
        print("-"*40)
        for device_id, count in patterns['top_devices']:
            success_rate = patterns['device_success_rates'][device_id]
            print(f"Device {device_id}: {count} deployments ({success_rate:.1f}% success rate)")
        
        print("\n" + "-"*40)
        print("FAILURE REASONS:")
        print("-"*40)
        for reason, count in patterns['failure_reasons'].items():
            percentage = (count / results['failed_deployments'] * 100) if results['failed_deployments'] > 0 else 0
            print(f"{reason}: {count} failures ({percentage:.1f}%)")
    
    print("\n" + "-"*40)
    print("SAMPLE SUCCESSFUL DEPLOYMENTS (first 5):")
    print("-"*40)
    for i, deployment in enumerate(results['successful_details'][:5], 1):
        print(f"{i}. Time: {deployment['timestamp']}")
        print(f"   Policy ID: {deployment['policy_id']}")
        print(f"   Device ID: {deployment['device_id']}")
        print(f"   Status: {deployment['status']}")
        print()
    
    print("-"*40)
    print("SAMPLE FAILED DEPLOYMENTS (first 5):")
    print("-"*40)
    for i, deployment in enumerate(results['failed_details'][:5], 1):
        print(f"{i}. Time: {deployment['timestamp']}")
        print(f"   Policy ID: {deployment['policy_id']}")
        print(f"   Device ID: {deployment['device_id']}")
        print(f"   Status: {deployment['status']}")
        print(f"   Message: {deployment['message']}")
        print()

def main():
    """Main function to run the log analysis."""
    csv_file_path = 'application_logs.csv'
    
    print("Starting Improved Policy Deployment Log Analysis...")
    
    # Analyze the log file
    results = analyze_policy_deployments(csv_file_path)
    
    if results:
        # Print the analysis summary
        print_analysis_summary(results)
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"Successfully processed {results['total_deployments']} policy deployment events.")
        print("Key findings:")
        print(f"- {results['successful_deployments']} successful deployments")
        print(f"- {results['failed_deployments']} failed deployments")
        print(f"- {results['pending_deployments']} pending deployments")
        print(f"- Overall success rate: {results['success_rate']:.1f}%")
    else:
        print("Analysis failed. Please check the CSV file.")

if __name__ == "__main__":
    main()