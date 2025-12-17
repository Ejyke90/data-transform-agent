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
