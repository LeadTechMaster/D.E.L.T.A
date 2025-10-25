#!/usr/bin/env python3
"""
Initialize All API Ability Databases
Creates all database schemas for the API Abilities system
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def init_all_databases():
    """Initialize all databases with their schemas"""
    
    services = [
        ('Mapbox', 'Mapbox API'),
        ('SerpApi', 'SerpApi'),
        ('Meta_Ads', 'Meta Ads Library'),
        ('US_Census', 'US Census Bureau'),
        ('Google_Places', 'Google Places & GMB'),
        ('Brightlocal', 'Brightlocal'),
        ('Google_OAuth', 'Google OAuth')
    ]
    
    print("="*60)
    print("API ABILITIES - DATABASE INITIALIZATION")
    print("="*60)
    print()
    
    for service_dir, service_name in services:
        try:
            print(f"Initializing {service_name} database...")
            
            # Import the init function
            module_path = f"{service_dir}.DB.db_helper"
            module = __import__(module_path, fromlist=['init_database'])
            init_db = getattr(module, 'init_database')
            
            # Initialize the database
            init_db()
            
            print(f"✓ {service_name} database initialized successfully")
            print()
            
        except Exception as e:
            print(f"✗ Error initializing {service_name}: {str(e)}")
            print()
    
    print("="*60)
    print("DATABASE INITIALIZATION COMPLETE")
    print("="*60)
    print()
    print("Database files created in:")
    for service_dir, _ in services:
        db_path = os.path.join(os.path.dirname(__file__), service_dir, 'DB')
        print(f"  - {db_path}")
    print()

if __name__ == "__main__":
    init_all_databases()

