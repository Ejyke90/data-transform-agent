"""
Command Line Interface for Data Transform Agent.
"""

import click
import json
from pathlib import Path
from dotenv import load_dotenv

from .transformer import SchemaTransformer

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    Data Transform Agent - AI-powered schema transformation tool.

    Transform XSD schemas to JSON Schema or Avro format.
    """
    pass


@main.command()
@click.argument("xsd_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "avro"], case_sensitive=False),
    required=True,
    help="Output format (json or avro)",
)
@click.option(
    "--namespace",
    "-n",
    default="com.example",
    help="Namespace for Avro schemas (default: com.example)",
)
@click.option(
    "--use-ai",
    is_flag=True,
    default=False,
    help="Enable AI-powered enhancement (requires OPENAI_API_KEY)",
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="OpenAI API key (can also use OPENAI_API_KEY env var)",
)
def transform(xsd_file, output_file, format, namespace, use_ai, api_key):
    """
    Transform an XSD schema to JSON Schema or Avro format.

    Examples:

        # Convert XSD to JSON Schema
        data-transform transform schema.xsd output.json --format json

        # Convert XSD to Avro schema with custom namespace
        data-transform transform schema.xsd output.avsc --format avro --namespace com.myorg

        # Use AI enhancement
        data-transform transform schema.xsd output.json --format json --use-ai
    """
    try:
        transformer = SchemaTransformer(use_ai=use_ai, api_key=api_key)

        click.echo(f"Transforming {xsd_file} to {format.upper()} format...")

        result = transformer.transform(
            xsd_path=xsd_file, output_format=format.lower(), output_path=output_file, namespace=namespace
        )

        click.echo(f"✓ Successfully transformed to {output_file}")

        if click.confirm("Would you like to see the schema preview?", default=False):
            click.echo("\nSchema Preview:")
            click.echo(json.dumps(result, indent=2))

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument("xsd_file", type=click.Path(exists=True))
def analyze(xsd_file):
    """
    Analyze an XSD schema and display its structure.

    Example:

        data-transform analyze schema.xsd
    """
    try:
        from .xsd_parser import XSDParser

        click.echo(f"Analyzing {xsd_file}...")

        parser = XSDParser(xsd_file)
        schema_info = parser.get_schema_info()

        click.echo("\n=== XSD Schema Analysis ===\n")
        click.echo(f"Target Namespace: {schema_info.get('target_namespace', 'None')}")
        click.echo(f"\nElements: {len(schema_info.get('elements', {}))}")
        for name in schema_info.get("elements", {}).keys():
            click.echo(f"  - {name}")

        click.echo(f"\nTypes: {len(schema_info.get('types', {}))}")
        for name, type_info in schema_info.get("types", {}).items():
            category = type_info.get("category", "unknown")
            click.echo(f"  - {name} ({category})")

        click.echo(f"\nAttributes: {len(schema_info.get('attributes', {}))}")
        for name in schema_info.get("attributes", {}).keys():
            click.echo(f"  - {name}")

        if click.confirm("\nWould you like to see the full schema details?", default=False):
            click.echo("\nFull Schema Info:")
            click.echo(json.dumps(schema_info, indent=2))

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument("xsd_file", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "avro"], case_sensitive=False),
    required=True,
    help="Target format for suggestions",
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="OpenAI API key (can also use OPENAI_API_KEY env var)",
)
def suggest(xsd_file, format, api_key):
    """
    Get AI suggestions for schema transformation.

    Requires OPENAI_API_KEY environment variable or --api-key option.

    Example:

        data-transform suggest schema.xsd --format json
    """
    try:
        from .xsd_parser import XSDParser
        from .ai_agent import AIAgent

        if not api_key:
            click.echo(
                "✗ Error: OpenAI API key required. Set OPENAI_API_KEY env var or use --api-key",
                err=True,
            )
            raise click.Abort()

        click.echo(f"Analyzing {xsd_file} and getting AI suggestions...")

        parser = XSDParser(xsd_file)
        schema_info = parser.get_schema_info()

        agent = AIAgent(api_key=api_key)
        if not agent.is_available():
            click.echo("✗ Error: AI agent not available", err=True)
            raise click.Abort()

        suggestions = agent.suggest_improvements(schema_info, format.lower())

        click.echo(f"\n=== AI Suggestions for {format.upper()} Conversion ===\n")
        for suggestion in suggestions.get("suggestions", []):
            if suggestion.strip():
                click.echo(suggestion)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
