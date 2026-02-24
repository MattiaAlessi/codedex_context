from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load your dataset
df = pd.read_csv('breached_services_info.csv')

# Convert 'BreachDate' and 'AddedDate' to datetime
df['BreachDate'] = pd.to_datetime(df['BreachDate'], errors='coerce')
df['AddedDate'] = pd.to_datetime(df['AddedDate'], errors='coerce')

# Create a visualization for "Breaches per Year"
df['BreachYear'] = df['BreachDate'].dt.year
breach_counts = df['BreachYear'].value_counts().sort_index()

# Plot the data interactively using Plotly
fig = px.bar(breach_counts,
             x=breach_counts.index,
             y=breach_counts.values,
             labels={'x': 'Year', 'y': 'Number of Breaches'},
             title='Number of Breaches per Year')
fig.update_layout(template='plotly_dark')

# Save the interactive plot as an HTML file
fig.write_html('templates/breach_years_interactive.html')

# Route for the main page
@app.route('/')
def home():
    return render_template('index.html')

# Route for Breach Year Interactive Plot
@app.route('/breach_years')
def breach_years():
    return render_template('breach_years_interactive.html')

if __name__ == '__main__':
    app.run(debug=True)