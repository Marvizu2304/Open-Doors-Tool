from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename

from utils.mappings import auto_column_mapping
from utils.normalizers import normalize_sex
from utils.duration import categorize_duration

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'Output Analysis'
ALLOWED_EXTENSIONS = {'xlsx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            try:
                output_files = process_file(filepath)
                return render_template('index.html', success=True, files=output_files)
            except Exception as e:
                flash(f"Error processing file: {str(e)}")
                return redirect(request.url)
    return render_template('index.html', success=False)

def process_file(file_path):
    sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
    df = pd.concat(sheets.values(), ignore_index=True)

    mapping = auto_column_mapping(df)

    analysis_df = pd.DataFrame()
    for key, col in mapping.items():
        analysis_df[key] = df[col] if col else None

    analysis_df["Sex"] = analysis_df["Sex"].apply(normalize_sex)
    analysis_df["Program Start Date"] = pd.to_datetime(analysis_df["Program Start Date"], errors='coerce')
    analysis_df["Program End Date"] = pd.to_datetime(analysis_df["Program End Date"], errors='coerce')
    analysis_df["Duration"] = analysis_df.apply(
        lambda row: categorize_duration(row["Program Start Date"], row["Program End Date"]),
        axis=1
    )

    total_students = len(analysis_df)
    by_level = analysis_df["Academic Level"].value_counts().rename_axis("Academic Level").reset_index(name="Count")
    by_sex = analysis_df["Sex"].value_counts().rename_axis("Sex").reset_index(name="Count")
    by_disability = analysis_df["Disability"].value_counts().rename_axis("Disability").reset_index(name="Count")
    by_major = analysis_df["Major"].value_counts().rename_axis("Major").reset_index(name="Count")
    by_country = analysis_df["Destination Country"].value_counts().rename_axis("Destination Country").reset_index(name="Count")
    by_duration = analysis_df["Duration"].value_counts().rename_axis("Duration Category").reset_index(name="Count")

    excel_output = os.path.join(OUTPUT_FOLDER, 'openDoors_Analysis.xlsx')
    with pd.ExcelWriter(excel_output) as writer:
        pd.DataFrame({"Metric": ["Total Students"], "Count": [total_students]}).to_excel(writer, sheet_name='Summary', index=False)
        by_level.to_excel(writer, sheet_name='By Academic Level', index=False)
        by_sex.to_excel(writer, sheet_name='By Sex', index=False)
        by_disability.to_excel(writer, sheet_name='By Disability', index=False)
        by_major.to_excel(writer, sheet_name='By Major', index=False)
        by_country.to_excel(writer, sheet_name='By Destination', index=False)
        by_duration.to_excel(writer, sheet_name='By Duration', index=False)

    txt_output = os.path.join(OUTPUT_FOLDER, 'openDoors_Analysis.txt')
    with open(txt_output, 'w') as f:
        f.write(f"TOTAL NUMBER OF U.S. STUDY ABROAD STUDENTS: {total_students}\n\n")
        f.write("2. Academic Level:\n")
        f.write(by_level.to_string(index=False))
        f.write("\n\n3. Sex:\n")
        f.write(by_sex.to_string(index=False))
        f.write("\n\n4. Disability:\n")
        f.write(by_disability.to_string(index=False))
        f.write("\n\n5. Major Field of Study:\n")
        f.write(by_major.to_string(index=False))
        f.write("\n\n6. Destination Country:\n")
        f.write(by_country.to_string(index=False))
        f.write("\n\n7. Duration of Study Abroad:\n")
        f.write(by_duration.to_string(index=False))
        f.write("\n")

    return [os.path.basename(excel_output), os.path.basename(txt_output)]

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
