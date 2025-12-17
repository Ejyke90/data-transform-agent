"""
Web UI for ISO 20022 Schema Agent Demo
Simple Flask application for business team demonstrations
"""

from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import tempfile
from datetime import datetime

from iso20022_agent import ISO20022SchemaAgent

app = Flask(__name__)
app.secret_key = 'iso20022-demo-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xsd', 'avsc', 'avro'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    # List existing schemas
    schema_files = []
    if os.path.exists('schemas'):
        for f in os.listdir('schemas'):
            if f.endswith(('.xsd', '.avsc', '.avro')):
                schema_files.append(f)
    
    return render_template('index.html', schemas=schema_files)


@app.route('/compare')
def compare_page():
    """Comparison page"""
    schema_files = []
    if os.path.exists('schemas'):
        for f in os.listdir('schemas'):
            if f.endswith(('.xsd', '.avsc', '.avro')):
                schema_files.append(f)
    return render_template('compare.html', schemas=schema_files)


@app.route('/compare', methods=['POST'])
def compare():
    """Compare XSD and AVRO schemas"""
    try:
        xsd_path = None
        avro_path = None
        xsd_name = None
        avro_name = None
        
        # Handle XSD
        if 'xsd_file' in request.files and request.files['xsd_file'].filename:
            file = request.files['xsd_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                xsd_path = filepath
                xsd_name = filename
        elif 'existing_xsd' in request.form and request.form['existing_xsd']:
            xsd_name = request.form['existing_xsd']
            xsd_path = os.path.join('schemas', xsd_name)
        
        # Handle AVRO
        if 'avro_file' in request.files and request.files['avro_file'].filename:
            file = request.files['avro_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                avro_path = filepath
                avro_name = filename
        elif 'existing_avro' in request.form and request.form['existing_avro']:
            avro_name = request.form['existing_avro']
            avro_path = os.path.join('schemas', avro_name)
        
        if not xsd_path or not avro_path:
            return jsonify({'error': 'Please provide both XSD and AVRO files.'}), 400
        
        # Analyze both
        xsd_agent = ISO20022SchemaAgent()
        xsd_agent.load_schema(xsd_path)
        xsd_fields = xsd_agent.extract_fields()
        
        avro_agent = ISO20022SchemaAgent()
        avro_agent.load_schema(avro_path)
        avro_fields = avro_agent.extract_fields()
        
        # Normalize paths and match
        def normalize_path(path, format_type):
            if format_type == 'xsd':
                return path.replace('/', '.')
            return path
        
        xsd_map = {normalize_path(f.path, 'xsd'): f for f in xsd_fields}
        avro_map = {f.path: f for f in avro_fields}
        
        all_keys = set(xsd_map.keys()) | set(avro_map.keys())
        
        comparison_rows = []
        matched_count = 0
        xsd_only_count = 0
        avro_only_count = 0
        
        for key in sorted(all_keys):
            xsd_field = xsd_map.get(key)
            avro_field = avro_map.get(key)
            
            row = {
                'normalized_path': key,
                'xsd_exists': xsd_field is not None,
                'avro_exists': avro_field is not None,
                'xsd_name': xsd_field.name if xsd_field else '',
                'avro_name': avro_field.name if avro_field else '',
                'xsd_path': xsd_field.path if xsd_field else '',
                'avro_path': avro_field.path if avro_field else '',
                'xsd_multiplicity': xsd_field.multiplicity if xsd_field else '',
                'avro_multiplicity': avro_field.multiplicity if avro_field else '',
                'xsd_requirement': xsd_field.requirement.value if xsd_field else '',
                'avro_requirement': avro_field.requirement.value if avro_field else '',
                'match_status': 'both' if (xsd_field and avro_field) else ('xsd_only' if xsd_field else 'avro_only')
            }
            
            comparison_rows.append(row)
            
            if xsd_field and avro_field:
                matched_count += 1
            elif xsd_field:
                xsd_only_count += 1
            else:
                avro_only_count += 1
        
        # Export CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"comparison_{timestamp}.csv"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# XSD: {xsd_name}, AVRO: {avro_name}\n")
            f.write(f"# Matched: {matched_count}, XSD Only: {xsd_only_count}, AVRO Only: {avro_only_count}\n#\n")
            f.write("FieldName,XSD_Path,AVRO_Path,XSD_Mult,AVRO_Mult,XSD_Req,AVRO_Req,Status\n")
            
            for row in comparison_rows:
                name = row['xsd_name'] or row['avro_name']
                f.write(f"{name},{row['xsd_path']},{row['avro_path']},{row['xsd_multiplicity']},{row['avro_multiplicity']},{row['xsd_requirement']},{row['avro_requirement']},{row['match_status']}\n")
        
        return jsonify({
            'success': True,
            'xsd_schema': xsd_name,
            'avro_schema': avro_name,
            'output_file': output_file,
            'download_url': url_for('download', filename=output_file),
            'stats': {
                'total_fields': len(comparison_rows),
                'matched': matched_count,
                'xsd_only': xsd_only_count,
                'avro_only': avro_only_count,
                'match_percentage': round(matched_count / len(comparison_rows) * 100, 1) if comparison_rows else 0
            },
            'sample_rows': comparison_rows[:20]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded or selected schema"""
    try:
        # Check if file was uploaded
        if 'schema_file' in request.files and request.files['schema_file'].filename:
            file = request.files['schema_file']
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                schema_path = filepath
                schema_name = filename
            else:
                return jsonify({'error': 'Invalid file type. Please upload an XSD (.xsd) or AVRO (.avsc, .avro) file.'}), 400
        
        # Or use existing schema
        elif 'existing_schema' in request.form and request.form['existing_schema']:
            schema_name = request.form['existing_schema']
            schema_path = os.path.join('schemas', schema_name)
            
            if not os.path.exists(schema_path):
                return jsonify({'error': f'Schema file not found: {schema_name}'}), 404
        else:
            return jsonify({'error': 'Please select or upload a schema file.'}), 400
        
        # Get format preference
        output_format = request.form.get('format', 'csv')
        detailed = request.form.get('detailed') == 'on'
        
        # Analyze schema
        agent = ISO20022SchemaAgent()
        agent.load_schema(schema_path)
        agent.extract_fields()
        
        # Get statistics
        stats = agent.get_statistics()
        
        # Generate output filename
        base_name = os.path.splitext(schema_name)[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format == 'csv':
            output_file = f"{base_name}_{timestamp}.csv"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file)
            agent.export_csv(output_path)
        elif output_format == 'json':
            output_file = f"{base_name}_{timestamp}.json"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file)
            agent.export_json(output_path)
        else:  # markdown
            output_file = f"{base_name}_{timestamp}.md"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file)
            agent.export_markdown(output_path)
        
        # Get sample fields for preview
        mandatory_samples = [
            {
                'name': f.name,
                'path': f.path,
                'multiplicity': f.multiplicity,
                'constraints': ', '.join([f"{k}: {v}" for k, v in f.constraints.items()]) if f.constraints else 'None'
            }
            for f in agent.get_mandatory_fields()[:10]
        ]
        
        optional_samples = [
            {
                'name': f.name,
                'path': f.path,
                'multiplicity': f.multiplicity,
                'constraints': ', '.join([f"{k}: {v}" for k, v in f.constraints.items()]) if f.constraints else 'None'
            }
            for f in agent.get_optional_fields()[:10]
        ]
        
        code_list_samples = [
            {
                'name': f.name,
                'codes': ', '.join(f.code_list[:5]) + (f' (+ {len(f.code_list)-5} more)' if len(f.code_list) > 5 else '')
            }
            for f in agent.fields if f.code_list
        ][:5]
        
        return jsonify({
            'success': True,
            'schema_name': schema_name,
            'output_file': output_file,
            'download_url': url_for('download', filename=output_file),
            'stats': stats,
            'mandatory_samples': mandatory_samples,
            'optional_samples': optional_samples,
            'code_list_samples': code_list_samples,
            'detailed': detailed
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download(filename):
    """Download generated file"""
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404


@app.route('/api/schemas')
def list_schemas():
    """API endpoint to list available schemas"""
    schemas = []
    if os.path.exists('schemas'):
        for f in os.listdir('schemas'):
            if f.endswith('.xsd'):
                schemas.append(f)
    return jsonify(schemas)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    print("\n" + "="*70)
    print("ISO 20022 Schema Agent - Web UI")
    print("="*70)
    print(f"Starting server at http://localhost:5001")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Output folder: {app.config['OUTPUT_FOLDER']}")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
