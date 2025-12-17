"""
Command-line interface for ISO 20022 Schema Agent
"""

import argparse
import sys
from pathlib import Path

from iso20022_agent import ISO20022SchemaAgent


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ISO 20022 Schema Agent - Analyze and validate payment message schemas"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a schema file")
    analyze_parser.add_argument("schema", help="Path to XSD schema file")
    analyze_parser.add_argument(
        "-o", "--output",
        help="Output file path (default: output/fields.csv)",
        default="output/fields.csv"
    )
    analyze_parser.add_argument(
        "-f", "--format",
        choices=["csv", "json", "markdown"],
        default="csv",
        help="Output format (default: csv)"
    )
    analyze_parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Show detailed summary with samples and breakdown"
    )
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a message file")
    validate_parser.add_argument("schema", help="Path to XSD schema file")
    validate_parser.add_argument("message", help="Path to XML message file")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two schema versions")
    compare_parser.add_argument("schema1", help="Path to first XSD schema file")
    compare_parser.add_argument("schema2", help="Path to second XSD schema file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "analyze":
            return analyze_command(args)
        elif args.command == "validate":
            return validate_command(args)
        elif args.command == "compare":
            return compare_command(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def analyze_command(args):
    """Execute analyze command."""
    print(f"Analyzing schema: {args.schema}")
    
    agent = ISO20022SchemaAgent()
    agent.analyze_schema(args.schema)
    agent.print_summary(detailed=args.detailed)
    
    # Export
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    agent.export(str(output_path), args.format)
    print(f"\n✓ Results exported to: {output_path}")
    
    return 0


def validate_command(args):
    """Execute validate command."""
    print(f"Validating message against schema...")
    print(f"  Schema: {args.schema}")
    print(f"  Message: {args.message}")
    print()
    
    agent = ISO20022SchemaAgent()
    agent.analyze_schema(args.schema)
    
    results = agent.validate_message_file(args.message)
    
    if results['valid']:
        print("✅ Message is VALID")
        return 0
    else:
        print("❌ Message is INVALID")
        print(f"\nErrors ({len(results['errors'])}):")
        for i, error in enumerate(results['errors'], 1):
            print(f"  {i}. {error}")
        return 1


def compare_command(args):
    """Execute compare command."""
    print(f"Comparing schemas:")
    print(f"  Schema 1: {args.schema1}")
    print(f"  Schema 2: {args.schema2}")
    print()
    
    # Load first schema
    agent1 = ISO20022SchemaAgent()
    agent1.analyze_schema(args.schema1)
    fields1 = set(f.path for f in agent1.get_mandatory_fields())
    
    # Load second schema
    agent2 = ISO20022SchemaAgent()
    agent2.analyze_schema(args.schema2)
    fields2 = set(f.path for f in agent2.get_mandatory_fields())
    
    # Compare
    added = fields2 - fields1
    removed = fields1 - fields2
    unchanged = fields1 & fields2
    
    print("Comparison Results:")
    print("=" * 70)
    print(f"Mandatory fields in schema 1: {len(fields1)}")
    print(f"Mandatory fields in schema 2: {len(fields2)}")
    print(f"Fields added: {len(added)}")
    print(f"Fields removed: {len(removed)}")
    print(f"Fields unchanged: {len(unchanged)}")
    
    if added:
        print(f"\n✨ Added fields:")
        for path in sorted(added)[:10]:
            print(f"  + {path}")
        if len(added) > 10:
            print(f"  ... and {len(added) - 10} more")
    
    if removed:
        print(f"\n🗑️  Removed fields:")
        for path in sorted(removed)[:10]:
            print(f"  - {path}")
        if len(removed) > 10:
            print(f"  ... and {len(removed) - 10} more")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
