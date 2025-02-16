from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_type = request.form.get('ID')
        id_value = request.form.get('id_value')

        # Read the CSV file
        try:
            df = pd.read_csv('data.csv', skipinitialspace=True)
        except Exception as e:
            return render_template('error.html', 
                message=f"Error reading the data file: {str(e)}")

        if not id_value:
            return render_template('error.html', message="Please enter an ID value.")

        if id_type == 'student_id':
            # Filter data for the specific student
            student_data = df[df['Student id'] == int(id_value)]
            
            if student_data.empty:
                return render_template('error.html', message="Invalid Student ID!")
            
            # Prepare data for template
            records = []
            for _, row in student_data.iterrows():
                records.append({
                    'Student ID': row['Student id'],
                    'Course ID': row['Course id'],
                    'Marks': row['Marks']
                })
            
            total_marks = student_data['Marks'].sum()
            return render_template('student_details.html', 
                                data=records,
                                total_marks=total_marks)

        elif id_type == 'course_id':
            # Filter data for the specific course
            course_data = df[df['Course id'] == int(id_value)]
            
            if course_data.empty:
                return render_template('error.html', message="Invalid Course ID!")
            
            marks = course_data['Marks']
            avg_marks = round(marks.mean(), 2)
            max_marks = marks.max()

            # Create histogram
            plt.figure(figsize=(10, 6))
            plt.hist(marks, bins=10, edgecolor='black')
            plt.title(f'Marks Distribution for Course {id_value}')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            
            # Save plot to base64 string
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            plt.close()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            return render_template('course_details.html',
                                avg_marks=avg_marks,
                                max_marks=max_marks,
                                plot_url=plot_url)
        else:
            return render_template('error.html', message="Please select an ID type.")

    return render_template('index.html')

app.run()