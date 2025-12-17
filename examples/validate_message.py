"""
Example: Validate an ISO 20022 message

This script demonstrates how to validate a payment message
against a schema.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from iso20022_agent import ISO20022SchemaAgent


def main():
    print("=" * 70)
    print("ISO 20022 Message Validator")
    print("=" * 70)
    print()
    
    # Initialize agent
    agent = ISO20022SchemaAgent()
    
    # Load schema
    schema_path = "schemas/pain.001.001.09.xsd"
    message_path = "tests/messages/sample_pain001.xml"
    
    if not Path(schema_path).exists():
        print(f"⚠️  Schema file not found: {schema_path}")
        return
    
    if not Path(message_path).exists():
        print(f"⚠️  Message file not found: {message_path}")
        print("\nCreate a sample message file first.")
        return
    
    try:
        # Load and analyze schema
        print("Loading schema...")
        agent.analyze_schema(schema_path)
        agent.print_summary()
        
        # Validate message
        print("\nValidating message...")
        print("-" * 70)
        results = agent.validate_message_file(message_path)
        
        # Display results
        if results['valid']:
            print("✅ Message is VALID")
        else:
            print("❌ Message is INVALID")
            print(f"\nFound {len(results['errors'])} errors:")
            for i, error in enumerate(results['errors'], 1):
                print(f"  {i}. {error}")
        
        if results['warnings']:
            print(f"\n⚠️  {len(results['warnings'])} warnings:")
            for i, warning in enumerate(results['warnings'], 1):
                print(f"  {i}. {warning}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
