from flask import render_template, request, flash, Flask
from website import extract_action_items
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Password'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Gets the note from the HTML
        note = request.form.get('note')
        # If note length is too short
        if len(note) < 1:
            flash('Text is too short!', category='error')
        # Minimum len for the model generation
        elif len(note) > 10:
            action_items, original_text = extract_action_items(note)
            flash(' Task Done!', category='success')
            return render_template("nlp_model.html", action_items = action_items, original_text = original_text)

    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']

        if file and file.filename.endswith('.csv'):
            data = []

            # Read the CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_data = csv.reader(stream)
            for row in csv_data:
                data.append(row)

            return render_template('display_csv.html', data=data)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug = True, port = 4245)
