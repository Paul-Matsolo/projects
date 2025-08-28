# Maritime Dashboard

A comprehensive dashboard for analyzing maritime events and activities using Dash and Plotly.

## Features

- Interactive maps showing maritime events
- Statistical charts and visualizations
- Real-time data filtering and analysis
- Responsive design with modern UI

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python Main.py
```

3. Open your browser and navigate to `http://127.0.0.1:8050`

## Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. Push your code to a GitHub repository
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file and deploy your application

### Option 2: Manual Setup

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following configuration:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn Main:app.server --bind 0.0.0.0:$PORT`
   - **Environment**: Python 3.9

## Data

The application uses maritime event data from CSV files. Make sure your data files are included in the repository or uploaded to the deployment environment.

## Dependencies

- Dash 2.14.2
- Pandas 2.1.4
- Plotly 5.17.0
- NumPy 1.24.3
- Scikit-learn 1.3.2
- Gunicorn 21.2.0 (for production)
