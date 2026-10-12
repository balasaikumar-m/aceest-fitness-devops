# ACEest Fitness & Gym — DevOps Assignment

Flask gym-management API demonstrating Git/GitHub, Pytest, Docker, GitHub Actions, Jenkins and SonarQube.

## Endpoints
- `GET /` — application information
- `GET /health` — health check
- `GET /members` — list demo members
- `POST /members` — add a member with JSON: `{"name":"Priya","plan":"Monthly"}`

**Demo limitation:** member records are in memory and reset when the app restarts. This is not a production database.

## Local setup
```bash
sudo apt update
sudo apt install -y python3 python3-venv git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -v
python app.py
```
Open `http://127.0.0.1:5000/health`.

## Docker
```bash
docker build -t aceest-fitness:1.0 .
docker run --rm -p 5000:5000 aceest-fitness:1.0
docker run --rm aceest-fitness:1.0 python -m pytest -v
```

## GitHub Actions
The workflow runs on push and pull requests. It installs dependencies, checks syntax, runs tests and coverage, builds the Docker image, and runs tests inside the image. Inspect the repository Actions tab.

## Jenkins setup
1. Install Jenkins, Git, Python 3, `python3-venv`, Docker and Jenkins Pipeline/Git plugins on the VM.
2. Ensure Jenkins can access Docker (Docker group membership grants root-equivalent privileges).
3. Create a Jenkins **Pipeline** job using **Pipeline script from SCM**, Git repository URL, branch `*/main`, and script path `Jenkinsfile`.
4. The pipeline polls SCM every five minutes; click **Build Now** for the first run.

## SonarQube setup
1. Start a local SonarQube server using Docker Compose (Docker Compose plugin required):
   ```bash
   docker compose -f docker-compose.sonarqube.yml up -d
   ```
2. Open `http://localhost:9000`, finish setup, create a project with key `aceest-fitness`, and generate a token.
3. In Jenkins, install the SonarQube Scanner plugin. Configure **Manage Jenkins → System → SonarQube servers** with server name exactly `SonarQube`, its URL, and a Jenkins Secret Text credential containing the token.
4. Configure a scanner named `SonarScanner` in **Manage Jenkins → Tools**, or ensure `sonar-scanner` is on the agent PATH. If your Jenkins installation uses a named scanner tool, adjust the Jenkinsfile invocation to use that configured installation.
5. Configure a SonarQube webhook to `http://JENKINS_URL/sonarqube-webhook/` so `waitForQualityGate` can receive the Quality Gate result. Jenkins must be reachable from SonarQube.
6. Ensure a Quality Gate exists and is assigned to the project. The pipeline fails if the gate fails.

Allocate adequate VM memory for Jenkins, Docker and SonarQube; 4 GB is a minimum starting point for SonarQube alone, not the whole stack.

## GitHub Actions and local SonarQube
GitHub-hosted runners cannot normally reach SonarQube running only on a private VM. This repository runs build/tests/Docker checks in GitHub Actions and runs SonarQube analysis plus Quality Gate in Jenkins on the VM. To run SonarQube analysis from GitHub Actions, you need a securely reachable SonarQube server and suitable GitHub secrets/network access. Do not expose Jenkins or SonarQube without proper access controls.

## Submission
Submit the public GitHub repository URL and verify successful GitHub Actions, Jenkins and SonarQube results.
