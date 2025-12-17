"""
Example: Basic usage of the ISO 20022 Schema Agent

This script demonstrates how to:
1. Load an ISO 20022 schema
2. Extract fields
3. Get mandatory and optional fields
4. Export to CSV
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from iso20022_agent import ISO20022SchemaAgent


def main():
    print("=" * 70)
    print("ISO 20022 Schema Agent - Basic Example")
    print("=" * 70)
    print()
    
    # Initialize the agent
    agent = ISO20022SchemaAgent()
    
    # For this example, we'll create a simple mock schema
    # In real usage, you would provide an actual XSD file path
    schema_path = "schemas/pain.001.001.09.xsd"
    
    print(f"Note: This example expects a schema file at: {schema_path}")
    print("If you don't have a schema file, the agent won't be able to run.")
    print()
    
    # Check if schema exists
    if not Path(schema_path).exists():
        print(f"⚠️  Schema file not found: {schema_path}")
        print()
        print("To use this example:")
        print("1. Download an ISO 20022 schema (XSD file) from https://www.iso20022.org/")
        print("2. Place it in the schemas/ directory")
        print("3. Update the schema_path variable above")
        print()
        return
    
    try:
        # Load the schema
        agent.load_schema(schema_path)
        
        # Extract fields
        fields = agent.extract_fields()
        
        # Print summary
        agent.print_summary()
        
        # Get mandatory fields
        mandatory = agent.get_mandatory_fields()
        print(f"\n📋 Mandatory Fields ({len(mandatory)}):")
        print("-" * 70)
        for field in mandatory[:5]:  # Show first 5
            print(f"  • {field.name}")
            print(f"    Path: {field.path}")
            print(f"    Type: {field.data_type}")
            print(f"    Definition: {field.definition[:80]}...")
            print()
        
        if len(mandatory) > 5:
            print(f"  ... and {len(mandatory) - 5} more mandatory fields\n")
        
        # Get optional fields
        optional = agent.get_optional_fields()
        print(f"\n📋 Optional Fields ({len(optional)}):")
        print("-" * 70)
        for field in optional[:5]:  # Show first 5
            print(f"  • {field.name}")
            print(f"    Path: {field.path}")
            print()
        
        if len(optional) > 5:
            print(f"  ... and {len(optional) - 5} more optional fields\n")
        
        # Export to different formats
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        print("\n📤 Exporting field catalog:")
        print("-" * 70)
        
        # Export as CSV (recommended for testing)
        csv_path = output_dir / "fields.csv"
        agent.export_csv(str(csv_path))
        print(f"✓ CSV exported to: {csv_path}")
        
        # Export as JSON
        json_path = output_dir / "fields.json"
        agent.export_json(str(json_path))
        print(f"✓ JSON exported to: {json_path}")
        
        # Export as Markdown
        md_path = output_dir / "fields.md"
        agent.export_markdown(str(md_path))
        print(f"✓ Markdown exported to: {md_path}")
        
        print("\n" + "=" * 70)
        print("✅ Analysis complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
