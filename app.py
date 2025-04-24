from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Get user input from the form
    try:
        func = request.form['function']
        start = float(request.form['start'])
        end = float(request.form['end'])
        color = request.form['color']
        chart_title = request.form.get('chart_title', f'{func.capitalize()} Wave')
    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400

    # Generate data
    x = np.linspace(start, end, 500)
    if func == 'sin':
        y = np.sin(x)
    elif func == 'cos':
        y = np.cos(x)
    elif func == 'tan':
        y = np.tan(x)
        y[np.abs(y) > 10] = np.nan  # Filter out extreme values for tangent
    else:
        return "Invalid function selected.", 400

    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, label=f'{func.capitalize()} Wave', color=color, linewidth=3, alpha=0.8)
    ax.fill_between(x, y, color=color, alpha=0.2)
    ax.set_title(chart_title, fontsize=22, fontweight='bold', color='#4fc3f7', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(axis='both', which='major', labelsize=12, colors='#cccccc')

    # Update axis labels to "X" and "Y"
    ax.set_xlabel('X', fontsize=16, color='#cccccc', labelpad=10)  # Changed from "X-axis" to "X"
    ax.set_ylabel('Y', fontsize=16, color='#cccccc', labelpad=10)  # Changed from "Y-axis" to "Y"

    ax.legend(frameon=False, fontsize=14, loc='upper right', labelcolor='#cccccc')
    ax.grid(color='#444444', linestyle='--', linewidth=0.5, alpha=0.7)
    fig.patch.set_facecolor('#1e1e2f')
    ax.set_facecolor('#2a2a40')
    plt.tight_layout()

    # Save the chart to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close(fig)

    # Return the image as a response
    return send_file(img, mimetype='image/png')

@app.route('/download_chart', methods=['POST'])
def download_chart():
    # Get user input from the form
    try:
        func = request.form['function']
        start = float(request.form['start'])
        end = float(request.form['end'])
        color = request.form['color']
        chart_title = request.form.get('chart_title', f'{func.capitalize()} Wave')
    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400

    # Generate data
    x = np.linspace(start, end, 500)
    if func == 'sin':
        y = np.sin(x)
    elif func == 'cos':
        y = np.cos(x)
    elif func == 'tan':
        y = np.tan(x)
        y[np.abs(y) > 10] = np.nan  # Filter out extreme values for tangent
    else:
        return "Invalid function selected.", 400

    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, label=f'{func.capitalize()} Wave', color=color, linewidth=3, alpha=0.8)
    ax.fill_between(x, y, color=color, alpha=0.2)
    ax.set_title(chart_title, fontsize=22, fontweight='bold', color='#4fc3f7', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(axis='both', which='major', labelsize=12, colors='#cccccc')

    # Update axis labels to "X" and "Y"
    ax.set_xlabel('X', fontsize=16, color='#cccccc', labelpad=10)  # Changed from "X-axis" to "X"
    ax.set_ylabel('Y', fontsize=16, color='#cccccc', labelpad=10)  # Changed from "Y-axis" to "Y"

    ax.legend(frameon=False, fontsize=14, loc='upper right', labelcolor='#cccccc')
    ax.grid(color='#444444', linestyle='--', linewidth=0.5, alpha=0.7)
    fig.patch.set_facecolor('#1e1e2f')
    ax.set_facecolor('#2a2a40')
    plt.tight_layout()

    # Save the chart to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close(fig)

    # Return the image as a downloadable file
    return send_file(img, mimetype='image/png', as_attachment=True, download_name='chart.png')

if __name__ == '__main__':
    app.run(debug=True)