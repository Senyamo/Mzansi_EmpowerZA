
# app.py

from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

ADZUNA_API_APP_ID = 'cdaac121'
ADZUNA_API_KEY = '00acf8194e67c2aeacdc57d68ff8cf9b'
ADZUNA_API_URL = 'https://api.adzuna.com/v1/api/jobs/za/search/1'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/api/jobs', methods=['GET'])
def fetch_jobs():
    keyword = request.args.get('keyword')
    location = request.args.get('location', 'South Africa')
    page = request.args.get('page', 1, type=int)  # Get page from request, default to 1

    # Removing the page parameter temporarily to test
    params = {
        'app_id': ADZUNA_API_APP_ID,
        'app_key': ADZUNA_API_KEY,
        'results_per_page': 10,
        'where': location,
        # 'page': page  # Commented out to test if this is causing the issue
    }
    if keyword:
        params['what'] = keyword

    try:
        response = requests.get(ADZUNA_API_URL, params=params)
        response.raise_for_status()
        job_data = response.json()

        jobs = [
            {
                'title': job['title'],
                'company': job.get('company', {}).get('display_name', 'N/A'),
                'location': job.get('location', {}).get('display_name', 'South Africa'),
                'description': job.get('description', 'No description available'),
                'url': job['redirect_url']
            }
            for job in job_data.get('results', [])
        ]

        return jsonify(jobs)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return jsonify({"error": "Failed to retrieve job listings."}), 500

if __name__ == '__main__':
    app.run(debug=True)
