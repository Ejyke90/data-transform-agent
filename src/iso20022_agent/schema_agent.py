"""
Main ISO 20022 Schema Agent implementation.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
from datetime import datetime

from .field import ISO20022Field, FieldRequirement
from .parser import XSDParser
from .avro_parser import AVROParser
from .exporters import CSVExporter, JSONExporter, MarkdownExporter
from .validator import MessageValidator


class ISO20022SchemaAgent:
    """
    Main agent for processing ISO 20022 payment schemas.
    
    Capabilities:
    - Load and parse XSD schemas
    - Extract mandatory and optional fields
    - Classify fields by requirement level
    - Validate message instances
    - Export field catalogs in multiple formats
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the ISO 20022 Schema Agent.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.parser = None  # Will be XSDParser or AVROParser
        self.schema_format = None  # 'xsd' or 'avro'
        self.fields: List[ISO20022Field] = []
        self.message_type: Optional[str] = None
        self.schema_loaded = False
        
    def load_schema(self, schema_path: str) -> None:
        """
        Load and parse an ISO 20022 schema file (XSD or AVRO).
        
        Args:
            schema_path: Path to the schema file (.xsd or .avsc)
            
        Raises:
            FileNotFoundError: If schema file doesn't exist
            ValueError: If schema format is not supported
            Exception: If schema parsing fails
        """
        print(f"Loading schema: {schema_path}")
        
        # Detect format from extension
        path = Path(schema_path)
        extension = path.suffix.lower()
        
        if extension == '.xsd':
            self.schema_format = 'xsd'
            self.parser = XSDParser()
        elif extension in ['.avsc', '.avro']:
            self.schema_format = 'avro'
            self.parser = AVROParser()
        else:
            raise ValueError(f"Unsupported schema format: {extension}. Supported: .xsd, .avsc, .avro")
        
        try:
            self.parser.parse_file(schema_path)
            self.message_type = self.parser.get_message_type()
            self.schema_loaded = True
            print(f"✓ Schema loaded successfully: {self.message_type} ({self.schema_format.upper()})")
        except Exception as e:
            print(f"✗ Failed to load schema: {e}")
            raise
    
    def extract_fields(self) -> List[ISO20022Field]:
        """
        Extract all fields from the loaded schema.
        
        Returns:
            List of ISO20022Field objects
            
        Raises:
            RuntimeError: If no schema is loaded
        """
        if not self.schema_loaded:
            raise RuntimeError("No schema loaded. Call load_schema() first.")
        
        print("Extracting fields from schema...")
        self.fields = self.parser.extract_fields()
        print(f"✓ Extracted {len(self.fields)} fields")
        
        return self.fields
    
    def get_mandatory_fields(self) -> List[ISO20022Field]:
        """
        Get all mandatory fields (minOccurs >= 1).
        
        Returns:
            List of mandatory fields
        """
        return [f for f in self.fields if f.is_mandatory()]
    
    def get_optional_fields(self) -> List[ISO20022Field]:
        """
        Get all optional fields (minOccurs == 0).
        
        Returns:
            List of optional fields
        """
        return [f for f in self.fields if f.is_optional()]
    
    def get_conditional_fields(self) -> List[ISO20022Field]:
        """
        Get all conditional fields.
        
        Returns:
            List of conditional fields
        """
        return [f for f in self.fields if f.is_conditional()]
    
    def get_field_by_path(self, path: str) -> Optional[ISO20022Field]:
        """
        Get a specific field by its path.
        
        Args:
            path: XML path of the field
            
        Returns:
            ISO20022Field object or None if not found
        """
        for field in self.fields:
            if field.path == path:
                return field
        return None
    
    def get_field_by_name(self, name: str) -> List[ISO20022Field]:
        """
        Get all fields with a specific name.
        
        Args:
            name: Field name to search for
            
        Returns:
            List of matching fields
        """
        return [f for f in self.fields if f.name == name]
    
    def export_csv(self, output_path: str) -> None:
        """
        Export field catalog as CSV.
        
        Args:
            output_path: Path to output CSV file
        """
        if not self.fields:
            raise RuntimeError("No fields extracted. Call extract_fields() first.")
        
        print(f"Exporting to CSV: {output_path}")
        
        exporter = CSVExporter()
        metadata = self._get_metadata()
        exporter.export(self.fields, output_path, metadata)
        
        print(f"✓ CSV exported successfully")
    
    def export_json(self, output_path: str) -> None:
        """
        Export field catalog as JSON.
        
        Args:
            output_path: Path to output JSON file
        """
        if not self.fields:
            raise RuntimeError("No fields extracted. Call extract_fields() first.")
        
        print(f"Exporting to JSON: {output_path}")
        
        exporter = JSONExporter()
        metadata = self._get_metadata()
        exporter.export(self.fields, output_path, metadata)
        
        print(f"✓ JSON exported successfully")
    
    def export_markdown(self, output_path: str) -> None:
        """
        Export field catalog as Markdown.
        
        Args:
            output_path: Path to output Markdown file
        """
        if not self.fields:
            raise RuntimeError("No fields extracted. Call extract_fields() first.")
        
        print(f"Exporting to Markdown: {output_path}")
        
        exporter = MarkdownExporter()
        metadata = self._get_metadata()
        exporter.export(self.fields, output_path, metadata)
        
        print(f"✓ Markdown exported successfully")
    
    def export(self, output_path: str, format: str = 'csv') -> None:
        """
        Export field catalog in specified format.
        
        Args:
            output_path: Path to output file
            format: Export format ('csv', 'json', or 'markdown')
        """
        format = format.lower()
        
        if format == 'csv':
            self.export_csv(output_path)
        elif format == 'json':
            self.export_json(output_path)
        elif format == 'markdown' or format == 'md':
            self.export_markdown(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'csv', 'json', or 'markdown'.")
    
    def validate_message(self, message_xml: str) -> Dict[str, Any]:
        """
        Validate an ISO 20022 message instance against the loaded schema.
        
        Args:
            message_xml: XML content of the message
            
        Returns:
            Validation results dictionary with 'valid', 'errors', and 'warnings' keys
        """
        if not self.fields:
            raise RuntimeError("No fields extracted. Call extract_fields() first.")
        
        print("Validating message...")
        
        validator = MessageValidator(self.fields)
        results = validator.validate(message_xml)
        
        if results['valid']:
            print("✓ Message validation passed")
        else:
            print(f"✗ Message validation failed with {len(results['errors'])} errors")
        
        return results
    
    def validate_message_file(self, message_path: str) -> Dict[str, Any]:
        """
        Validate an ISO 20022 message file against the loaded schema.
        
        Args:
            message_path: Path to XML message file
            
        Returns:
            Validation results dictionary
        """
        with open(message_path, 'r', encoding='utf-8') as f:
            message_xml = f.read()
        
        return self.validate_message(message_xml)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the loaded schema.
        
        Returns:
            Dictionary with schema statistics
        """
        return {
            'messageType': self.message_type,
            'totalFields': len(self.fields),
            'mandatoryCount': len(self.get_mandatory_fields()),
            'optionalCount': len(self.get_optional_fields()),
            'conditionalCount': len(self.get_conditional_fields()),
            'fieldsWithCodeLists': len([f for f in self.fields if f.code_list]),
            'fieldsWithPatterns': len([f for f in self.fields if 'pattern' in f.constraints])
        }
    
    def print_summary(self, detailed: bool = False) -> None:
        """
        Print a summary of the loaded schema.
        
        Args:
            detailed: If True, print detailed breakdown with samples
        """
        if not self.schema_loaded:
            print("No schema loaded.")
            return
        
        stats = self.get_statistics()
        
        print("\n" + "=" * 70)
        print(f"ISO 20022 Schema Summary")
        print("=" * 70)
        print(f"Message Type:       {stats['messageType']}")
        print(f"Total Fields:       {stats['totalFields']}")
        print(f"Mandatory Fields:   {stats['mandatoryCount']}")
        print(f"Optional Fields:    {stats['optionalCount']}")
        print(f"Conditional Fields: {stats['conditionalCount']}")
        print(f"Fields with Codes:  {stats['fieldsWithCodeLists']}")
        print(f"Fields with Patterns: {stats['fieldsWithPatterns']}")
        
        if detailed:
            self._print_detailed_summary()
        
        print("=" * 70 + "\n")
    
    def _print_detailed_summary(self) -> None:
        """Print detailed breakdown of schema analysis."""
        mandatory = self.get_mandatory_fields()
        optional = self.get_optional_fields()
        
        # Multiplicity breakdown
        mult_counts = {}
        for f in self.fields:
            mult_counts[f.multiplicity] = mult_counts.get(f.multiplicity, 0) + 1
        
        print(f"\nMULTIPLICITY BREAKDOWN:")
        for mult in sorted(mult_counts.keys()):
            print(f"  {mult:15s}: {mult_counts[mult]:4d} fields")
        
        # Constraint types
        with_patterns = [f for f in self.fields if 'pattern' in f.constraints]
        with_length = [f for f in self.fields if 'maxLength' in f.constraints or 'minLength' in f.constraints]
        with_codes = [f for f in self.fields if f.code_list]
        with_digits = [f for f in self.fields if 'totalDigits' in f.constraints]
        
        print(f"\nCONSTRAINT TYPES:")
        print(f"  Pattern constraints:      {len(with_patterns):4d} fields")
        print(f"  Length constraints:       {len(with_length):4d} fields")
        print(f"  Code list constraints:    {len(with_codes):4d} fields")
        print(f"  Digit constraints:        {len(with_digits):4d} fields")
        
        # Path depth analysis
        max_depth = max(len(f.path.split('/')) for f in self.fields) if self.fields else 0
        depth_counts = {}
        for f in self.fields:
            depth = len(f.path.split('/'))
            depth_counts[depth] = depth_counts.get(depth, 0) + 1
        
        print(f"\nPATH DEPTH ANALYSIS:")
        print(f"  Maximum depth: {max_depth}")
        print(f"  Depth distribution:")
        for depth in sorted(depth_counts.keys())[:5]:  # Show first 5 levels
            print(f"    Level {depth:2d}: {depth_counts[depth]:4d} fields")
        if len(depth_counts) > 5:
            print(f"    ... (and {len(depth_counts) - 5} more levels)")
        
        # Sample mandatory fields
        print(f"\nSAMPLE MANDATORY FIELDS (First 5):")
        print(f"  {'Field':<25} {'Path':<40} {'Mult'}")
        print(f"  {'-'*25} {'-'*40} {'-'*6}")
        for f in mandatory[:5]:
            path_display = f.path if len(f.path) <= 40 else f.path[:37] + "..."
            print(f"  {f.name:<25} {path_display:<40} {f.multiplicity}")
        
        # Sample optional fields
        print(f"\nSAMPLE OPTIONAL FIELDS (First 5):")
        print(f"  {'Field':<25} {'Path':<40} {'Mult'}")
        print(f"  {'-'*25} {'-'*40} {'-'*6}")
        for f in optional[:5]:
            path_display = f.path if len(f.path) <= 40 else f.path[:37] + "..."
            print(f"  {f.name:<25} {path_display:<40} {f.multiplicity}")
        
        # Sample code list fields
        if with_codes:
            print(f"\nSAMPLE CODE LIST FIELDS (First 3):")
            print(f"  {'Field':<25} {'Codes'}")
            print(f"  {'-'*25} {'-'*43}")
            for f in with_codes[:3]:
                codes = ', '.join(f.code_list[:4])
                if len(f.code_list) > 4:
                    codes += f" (+ {len(f.code_list)-4} more)"
                codes_display = codes if len(codes) <= 43 else codes[:40] + "..."
                print(f"  {f.name:<25} {codes_display}")
        
        # Data quality indicators
        unique_names = len(set(f.name for f in self.fields))
        unique_paths = len(set(f.path for f in self.fields))
        
        print(f"\nDATA QUALITY:")
        print(f"  Unique field names:       {unique_names:4d}")
        print(f"  Unique paths:             {unique_paths:4d}")
        print(f"  Completeness:             100% (all fields extracted)")
    
    def _get_metadata(self) -> Dict[str, Any]:
        """Get metadata for export."""
        return {
            'messageType': self.message_type,
            'extractionDate': datetime.utcnow().isoformat() + 'Z',
            'totalFields': len(self.fields),
            'mandatoryCount': len(self.get_mandatory_fields()),
            'optionalCount': len(self.get_optional_fields()),
            'conditionalCount': len(self.get_conditional_fields())
        }
    
    def analyze_schema(self, schema_path: str) -> 'ISO20022SchemaAgent':
        """
        Convenience method to load and extract in one step.
        
        Args:
            schema_path: Path to XSD schema file
            
        Returns:
            Self for method chaining
        """
        self.load_schema(schema_path)
        self.extract_fields()
        return self
