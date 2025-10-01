#!/usr/bin/env python3
"""
Log Analysis Script for Policy Deployment Events
This script analyzes application_logs.csv to find and analyze policy deployment events.
"""

import csv
from datetime import datetime

def analyze_policy_deployments(csv_file_path):
    """
    Analyze policy deployment events from the CSV log file.
    
    Args:
        csv_file_path (str): Path to the CSV file
    
    Returns:
        dict: Analysis results containing deployment statistics and details
    """
    policy_deployments = []
    successful_deployments = []
    failed_deployments = []
    
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
                    
                    policy_deployments.append(deployment_data)
                    
                    # Categorize by status
                    if row['status'] == 'SUCCESS':
                        successful_deployments.append(deployment_data)
                    elif row['status'] == 'FAILED':
                        failed_deployments.append(deployment_data)
    
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} not found!")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    # Create analysis results
    results = {
        'total_deployments': len(policy_deployments),
        'successful_deployments': len(successful_deployments),
        'failed_deployments': len(failed_deployments),
        'success_rate': (len(successful_deployments) / len(policy_deployments) * 100) if policy_deployments else 0,
        'all_deployments': policy_deployments,
        'successful_details': successful_deployments,
        'failed_details': failed_deployments
    }
    
    return results

def print_analysis_summary(results):
    """Print a summary of the analysis results."""
    if not results:
        print("No results to display.")
        return
    
    print("\n" + "="*60)
    print("POLICY DEPLOYMENT ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"Total Policy Deployments: {results['total_deployments']}")
    print(f"Successful Deployments: {results['successful_deployments']}")
    print(f"Failed Deployments: {results['failed_deployments']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    
    print("\n" + "-"*40)
    print("SUCCESSFUL DEPLOYMENTS:")
    print("-"*40)
    for deployment in results['successful_details']:
        print(f"Time: {deployment['timestamp']}")
        print(f"Policy ID: {deployment['policy_id']}")
        print(f"Device ID: {deployment['device_id']}")
        print(f"Status: {deployment['status']}")
        print()
    
    print("-"*40)
    print("FAILED DEPLOYMENTS:")
    print("-"*40)
    for deployment in results['failed_details']:
        print(f"Time: {deployment['timestamp']}")
        print(f"Policy ID: {deployment['policy_id']}")
        print(f"Device ID: {deployment['device_id']}")
        print(f"Status: {deployment['status']}")
        print(f"Message: {deployment['message']}")
        print()

def main():
    """Main function to run the log analysis."""
    csv_file_path = 'application_logs.csv'
    
    print("Starting Policy Deployment Log Analysis...")
    
    # Analyze the log file
    results = analyze_policy_deployments(csv_file_path)
    
    if results:
        # Print the analysis summary
        print_analysis_summary(results)
        
        # Additional detailed information
        print("\n" + "="*60)
        print("DETAILED DEPLOYMENT DATA:")
        print("="*60)
        
        print("\nAll Policy Deployment Events (with extracted details):")
        for i, deployment in enumerate(results['all_deployments'], 1):
            print(f"{i}. Timestamp: {deployment['timestamp']}")
            print(f"   Policy ID: {deployment['policy_id']}")
            print(f"   Device ID: {deployment['device_id']}")
            print(f"   Status: {deployment['status']}")
            print(f"   Message: {deployment['message']}")
            print()
    else:
        print("Analysis failed. Please check the CSV file.")

if __name__ == "__main__":
    main()