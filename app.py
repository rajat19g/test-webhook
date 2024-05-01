from flask import Flask, request
import subprocess
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    
    headers = request.headers

    if headers.get('X-GitHub-Event') == 'ping':
        return 'Testing Passed', 200
    
    payload = request.form 
    payload = json.loads(payload['payload'])
    #print(payload['ref'])
    #print(type(payload.get('ref')))
    if (headers.get('X-GitHub-Event') == 'push') & (payload['ref'] == 'refs/heads/main') & (payload['head_commit']['committer'] == 'noreply@github.com'):
        # Extract information about the merge event
        #base_branch = payload['base']['ref']
        #merged_branch = payload['ref']
        #print(base_branch,merged_branch)
        # Trigger file update process
        update_file(payload)
    
        return 'Webhook received', 200
    
    else:
        return 'No actions taken', 200

@app.route('/webhook-pull', methods=['POST'])
def handle_webhook_pull():
    
    headers = request.headers
    if (headers.get('X-GitHub-Event') != 'pull_request'):
        return 'No actions taken', 200
    

    
    payload = request.form 
    payload = json.loads(payload['payload'])
    #print(payload['ref'])
    #print(type(payload.get('ref')))
    if  payload['action'] == 'closed' :
        # Extract information about the merge event
        #base_branch = payload['base']['ref']
        #merged_branch = payload['ref']
        #print(base_branch,merged_branch)
        # Trigger file update process
        update_file()
    
        return 'Webhook received', 200
    
    else:
        return 'No actions taken', 200

def update_file():
    # Fetch the latest version of the file from the repository
    subprocess.run(['git', 'pull'])
    with open('test.txt','w') as file:
        file.write('Final Commit made by bot Retest')
    # Perform necessary updates to the file
    # Example: Replace placeholder values in the file with new values

    # Commit and push changes back to the repository
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update file after merge'])
    subprocess.run(['git', 'push'])
 

# Define a route for the root URL
@app.route('/')
def hello_world():
    return 'Hello, World!'


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
