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
from iso20022_agent.ai_agent import SchemaAIAgent
from iso20022_agent.semantic_matcher import SemanticFieldMatcher

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
    """Main unified page with tabs for analyze and compare"""
    # List existing schemas
    schema_files = []
    if os.path.exists('schemas'):
        for f in os.listdir('schemas'):
            if f.endswith(('.xsd', '.avsc', '.avro')):
                schema_files.append(f)
    
    return render_template('index.html', schemas=schema_files)


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
        
        # === SEMANTIC MATCHING WITH LLM (Primary Strategy) ===
        # Check if user wants to use LLM for semantic matching
        use_semantic = request.form.get('use_semantic', 'true').lower() == 'true'
        
        matched_pairs = {}
        xsd_matched = set()
        avro_matched = set()
        
        if use_semantic:
            try:
                # Initialize AI agent for semantic matching
                ai_agent = SchemaAIAgent()
                semantic_matcher = SemanticFieldMatcher(ai_agent)
                
                print("🧠 Using LLM-powered semantic matching...")
                
                # Perform semantic matching
                matched_pairs_result = semantic_matcher.match_fields(
                    xsd_fields, 
                    avro_fields, 
                    use_llm=True,
                    batch_size=20
                )
                
                # Convert to our format
                for xsd_id, (xsd_field, avro_field, confidence) in matched_pairs_result.items():
                    matched_pairs[xsd_id] = (xsd_field, avro_field)
                    xsd_matched.add(xsd_id)
                    avro_matched.add(id(avro_field))
                
                print(f"✓ Semantic matching found {len(matched_pairs)} matches")
                
            except Exception as e:
                print(f"⚠️ Semantic matching error, falling back to fuzzy: {e}")
                use_semantic = False
        
        # === FUZZY MATCHING (Fallback Strategy) ===
        if not use_semantic:
            print("🔤 Using fuzzy string matching...")
            semantic_matcher = SemanticFieldMatcher(None)
            matched_pairs_result = semantic_matcher.match_fields(
                xsd_fields,
                avro_fields,
                use_llm=False
            )
            
            for xsd_id, (xsd_field, avro_field, confidence) in matched_pairs_result.items():
                matched_pairs[xsd_id] = (xsd_field, avro_field)
                xsd_matched.add(xsd_id)
                avro_matched.add(id(avro_field))
        
        # Build comparison rows
        # Build comparison rows
        comparison_rows = []
        matched_count = 0
        xsd_only_count = 0
        avro_only_count = 0
        
        # Add matched pairs
        for xsd_id, (xsd_field, avro_field) in matched_pairs.items():
            row = {
                'normalized_path': xsd_field.path.replace('/', '.'),
                'xsd_exists': True,
                'avro_exists': True,
                'xsd_name': xsd_field.name,
                'avro_name': avro_field.name,
                'xsd_path': xsd_field.path,
                'avro_path': avro_field.path,
                'xsd_multiplicity': xsd_field.multiplicity,
                'avro_multiplicity': avro_field.multiplicity,
                'xsd_requirement': xsd_field.requirement.value,
                'avro_requirement': avro_field.requirement.value,
                'match_status': 'both'
            }
            comparison_rows.append(row)
            matched_count += 1
        
        # Add XSD-only fields
        for xsd_field in xsd_fields:
            if id(xsd_field) not in xsd_matched:
                row = {
                    'normalized_path': xsd_field.path.replace('/', '.'),
                    'xsd_exists': True,
                    'avro_exists': False,
                    'xsd_name': xsd_field.name,
                    'avro_name': '',
                    'xsd_path': xsd_field.path,
                    'avro_path': '',
                    'xsd_multiplicity': xsd_field.multiplicity,
                    'avro_multiplicity': '',
                    'xsd_requirement': xsd_field.requirement.value,
                    'avro_requirement': '',
                    'match_status': 'xsd_only'
                }
                comparison_rows.append(row)
                xsd_only_count += 1
        
        # Add AVRO-only fields
        for avro_field in avro_fields:
            if id(avro_field) not in avro_matched:
                row = {
                    'normalized_path': avro_field.path,
                    'xsd_exists': False,
                    'avro_exists': True,
                    'xsd_name': '',
                    'avro_name': avro_field.name,
                    'xsd_path': '',
                    'avro_path': avro_field.path,
                    'xsd_multiplicity': '',
                    'avro_multiplicity': avro_field.multiplicity,
                    'xsd_requirement': '',
                    'avro_requirement': avro_field.requirement.value,
                    'match_status': 'avro_only'
                }
                comparison_rows.append(row)
                avro_only_count += 1
        
        # Sort by path for better readability
        comparison_rows.sort(key=lambda x: x['normalized_path'])
        
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


@app.route('/chat', methods=['POST'])
def chat():
    """AI chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        history = data.get('history', [])
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize AI agent
        ai_agent = SchemaAIAgent()
        
        # Get response
        response = ai_agent.chat(message, history)
        
        # Update history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        
        return jsonify({
            'success': True,
            'response': response,
            'history': history
        })
        
    except ValueError as e:
        # API key not configured
        return jsonify({
            'error': str(e) + '. Please configure your API keys in .env file.'
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ai/query-schema', methods=['POST'])
def ai_query_schema():
    """Natural language query against a schema"""
    try:
        data = request.get_json()
        schema_path = data.get('schema_path')
        query = data.get('query', '')
        
        if not schema_path or not query:
            return jsonify({'error': 'Schema path and query required'}), 400
        
        # Load schema
        agent = ISO20022SchemaAgent()
        agent.load_schema(schema_path)
        fields = agent.extract_fields()
        
        # Use AI to answer query
        ai_agent = SchemaAIAgent()
        answer = ai_agent.query_schema(fields, query)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'field_count': len(fields)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ai/suggest-mappings', methods=['POST'])
def ai_suggest_mappings():
    """AI-powered field mapping suggestions"""
    try:
        data = request.get_json()
        xsd_path = data.get('xsd_path')
        avro_path = data.get('avro_path')
        
        if not xsd_path or not avro_path:
            return jsonify({'error': 'Both XSD and AVRO paths required'}), 400
        
        # Load both schemas
        xsd_agent = ISO20022SchemaAgent()
        xsd_agent.load_schema(xsd_path)
        xsd_fields = xsd_agent.extract_fields()
        
        avro_agent = ISO20022SchemaAgent()
        avro_agent.load_schema(avro_path)
        avro_fields = avro_agent.extract_fields()
        
        # Get AI suggestions
        ai_agent = SchemaAIAgent()
        suggestions = ai_agent.suggest_field_mappings(xsd_fields, avro_fields)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'xsd_field_count': len(xsd_fields),
            'avro_field_count': len(avro_fields)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ai/generate-docs', methods=['POST'])
def ai_generate_docs():
    """Generate documentation for schema using AI"""
    try:
        data = request.get_json()
        schema_path = data.get('schema_path')
        schema_name = data.get('schema_name', 'Schema')
        
        if not schema_path:
            return jsonify({'error': 'Schema path required'}), 400
        
        # Load schema
        agent = ISO20022SchemaAgent()
        agent.load_schema(schema_path)
        fields = agent.extract_fields()
        
        # Generate docs with AI
        ai_agent = SchemaAIAgent()
        documentation = ai_agent.generate_documentation(fields, schema_name)
        
        return jsonify({
            'success': True,
            'documentation': documentation,
            'field_count': len(fields)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
