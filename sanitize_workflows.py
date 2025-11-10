#!/usr/bin/env python3
"""
Sanitize N8N workflow JSON files by removing sensitive credential information.
Usage: python sanitize_workflows.py
"""

import json
import os
from pathlib import Path

def sanitize_workflow(workflow_data):
    """Remove sensitive information from workflow JSON."""
    
    # Remove credential IDs and replace with placeholder
    if 'nodes' in workflow_data:
        for node in workflow_data['nodes']:
            if 'credentials' in node:
                for cred_type, cred_info in node['credentials'].items():
                    if isinstance(cred_info, dict) and 'id' in cred_info:
                        cred_info['id'] = 'YOUR_CREDENTIAL_ID_HERE'
                        cred_info['name'] = f'YOUR_{cred_type.upper()}_CREDENTIAL'
    
    # Remove any settings that might contain sensitive data
    if 'settings' in workflow_data:
        sensitive_keys = ['executionTimeout', 'timezone']
        for key in list(workflow_data['settings'].keys()):
            if key not in sensitive_keys:
                continue
    
    return workflow_data

def process_file(input_path, output_path):
    """Process a single workflow JSON file."""
    print(f"Processing: {input_path}")
    
    try:
        with open(input_path, 'r') as f:
            workflow_data = json.load(f)
        
        sanitized_data = sanitize_workflow(workflow_data)
        
        with open(output_path, 'w') as f:
            json.dump(sanitized_data, f, indent=2)
        
        print(f"✓ Sanitized file saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return False

def main():
    """Main function to sanitize all workflow files."""
    
    # Files to process
    workflows = [
        'document-ingestion-workflow.json',
        'query-interface-workflow.json'
    ]
    
    output_dir = Path('workflows')
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    
    for workflow_file in workflows:
        if not os.path.exists(workflow_file):
            print(f"⚠ Warning: {workflow_file} not found in current directory")
            continue
        
        output_path = output_dir / workflow_file
        if process_file(workflow_file, output_path):
            success_count += 1
    
    print(f"\n✓ Successfully sanitized {success_count}/{len(workflows)} workflows")
    print("\n⚠ IMPORTANT: Manually verify the sanitized files before committing!")

if __name__ == '__main__':
    main()
