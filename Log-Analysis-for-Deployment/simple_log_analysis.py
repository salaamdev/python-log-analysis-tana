#!/usr/bin/env python3
"""
Simple Log Analysis Script for Policy Deployment Events
Addresses the specific requirements from the task.
"""

import csv

def main():
    """Main function that performs the required log analysis tasks."""
    
    print("=== Python-based Log Analysis for Deployment ===\n")
    
    # 1. Read the CSV file
    print("1. Reading application_logs.csv file...")
    
    csv_file = 'application_logs.csv'
    policy_deployments = []
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # 2. Filter for POLICY_DEPLOYMENT events
            print("2. Filtering for POLICY_DEPLOYMENT events...")
            
            for row in reader:
                if row['event_type'] == 'POLICY_DEPLOYMENT':
                    # 4. Extract relevant details
                    deployment = {
                        'timestamp': row['timestamp'],
                        'policy_id': row['policy_id'], 
                        'device_id': row['device_id'],
                        'status': row['status'],
                        'message': row['message']
                    }
                    policy_deployments.append(deployment)
        
        print(f"   Found {len(policy_deployments)} policy deployment events\n")
        
        # 3. Identify successful vs. failed deployments
        print("3. Identifying successful vs. failed deployments...")
        
        successful = []
        failed = []
        pending = []
        
        for deployment in policy_deployments:
            if deployment['status'] == 'SUCCESS':
                successful.append(deployment)
            elif deployment['status'] == 'FAILED':
                failed.append(deployment)
            elif deployment['status'] == 'PENDING':
                pending.append(deployment)
        
        print(f"   Successful deployments: {len(successful)}")
        print(f"   Failed deployments: {len(failed)}")
        print(f"   Pending deployments: {len(pending)}")
        print()
        
        # 4. Show extracted details
        print("4. Extracted details summary:")
        print("-" * 50)
        print(f"Total policy deployment events: {len(policy_deployments)}")
        print(f"Successful: {len(successful)} ({len(successful)/len(policy_deployments)*100:.1f}%)")
        print(f"Failed: {len(failed)} ({len(failed)/len(policy_deployments)*100:.1f}%)")
        print(f"Pending: {len(pending)} ({len(pending)/len(policy_deployments)*100:.1f}%)")
        print()
        
        # Show examples of extracted data
        print("Example successful deployment:")
        if successful:
            example = successful[0]
            print(f"  Timestamp: {example['timestamp']}")
            print(f"  Policy ID: {example['policy_id']}")
            print(f"  Device ID: {example['device_id']}")
            print(f"  Status: {example['status']}")
        print()
        
        print("Example failed deployment:")
        if failed:
            example = failed[0]
            print(f"  Timestamp: {example['timestamp']}")
            print(f"  Policy ID: {example['policy_id']}")
            print(f"  Device ID: {example['device_id']}")
            print(f"  Status: {example['status']}")
            print(f"  Message: {example['message']}")
        print()
        
        print("✅ All tasks completed successfully!")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()