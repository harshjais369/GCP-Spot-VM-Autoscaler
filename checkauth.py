import google.auth
import google.cloud.compute_v1 as compute_v1

# Create a credentials object
credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
projects_client = compute_v1.ProjectsClient(credentials=credentials)

try:
    project = projects_client.get(project=project)
    print("Your environment is setup and configured with your GCP account.")
except Exception as e:
    # Auth falied
    print(f"Error: {e}")
