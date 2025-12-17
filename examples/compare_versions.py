"""
Example: Compare mandatory fields across schema versions

This script shows how to compare mandatory fields between
different versions of the same message type.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from iso20022_agent import ISO20022SchemaAgent


def main():
    print("=" * 70)
    print("ISO 20022 Schema Version Comparison")
    print("=" * 70)
    print()
    
    # Two schema versions to compare
    schema_v09 = "schemas/pain.001.001.09.xsd"
    schema_v11 = "schemas/pain.001.001.11.xsd"
    
    if not Path(schema_v09).exists() or not Path(schema_v11).exists():
        print("⚠️  Schema files not found.")
        print(f"Expected: {schema_v09} and {schema_v11}")
        return
    
    try:
        # Load version 09
        print("Loading version 09...")
        agent_v09 = ISO20022SchemaAgent()
        agent_v09.analyze_schema(schema_v09)
        fields_v09 = set(f.path for f in agent_v09.get_mandatory_fields())
        
        # Load version 11
        print("Loading version 11...")
        agent_v11 = ISO20022SchemaAgent()
        agent_v11.analyze_schema(schema_v11)
        fields_v11 = set(f.path for f in agent_v11.get_mandatory_fields())
        
        # Compare
        print("\n" + "=" * 70)
        print("Comparison Results")
        print("=" * 70)
        
        # Fields added in v11
        added = fields_v11 - fields_v09
        if added:
            print(f"\n✨ New mandatory fields in v11 ({len(added)}):")
            for path in sorted(added):
                print(f"  + {path}")
        
        # Fields removed in v11
        removed = fields_v09 - fields_v11
        if removed:
            print(f"\n🗑️  Mandatory fields removed in v11 ({len(removed)}):")
            for path in sorted(removed):
                print(f"  - {path}")
        
        # Unchanged
        unchanged = fields_v09 & fields_v11
        print(f"\n✓ Unchanged mandatory fields: {len(unchanged)}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
