

#!/usr/bin/env python3
"""
Script to update configuration with proper credentials
"""

import os
from pathlib import Path

def update_env_file():
    """Update .env file with proper credentials"""
    env_path = Path(__file__).parent / '.env'

    # Example credentials (replace with real values)
    example_credentials = {
        'MISTRAL_API_KEY': 'your_real_mistral_api_key_here',
        'S3_ACCESS_KEY': 'your_real_s3_access_key_here',
        'S3_SECRET_KEY': 'your_real_s3_secret_key_here'
    }

    # Read current .env file
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        print(f"❌ Error: {env_path} not found")
        return False

    # Update credentials
    updated_lines = []
    for line in lines:
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            updated_lines.append(line)
            continue

        # Update credentials
        for key, value in example_credentials.items():
            if line.startswith(f"{key}="):
                # Replace with example value
                updated_lines.append(f"{key}={value}\n")
                break
        else:
            # Keep original line if no match
            updated_lines.append(line)

    # Write updated .env file
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)

    print(f"✅ Updated {env_path} with example credentials")
    print("⚠️  NOTE: You need to replace the example credentials with real values!")
    print()
    print("Credentials that need to be updated:")
    for key, value in example_credentials.items():
        print(f"  {key}: {value}")
    print()
    print("Please update these with your actual credentials.")

    return True

if __name__ == "__main__":
    update_env_file()

