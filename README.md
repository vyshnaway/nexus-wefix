# Nexus WeFix

Nexus WeFix is a modern web platform connecting urban users with skilled workers (masons, carpenters, plumbers, painters) and contractors.

## Features

- **Multi-Role Authentication**: Seamless registration and login for Customers, Workers, and Admins.
- **Worker Discovery**: Find and book skilled professionals based on location and expertise.
- **Booking Management**: Streamlined workflow for service requests and confirmations.
- **Feedback System**: Integrated rating and review system for transparency and trust.
- **Modern UI**: Built with Bootstrap 5 and HTMX for a responsive and dynamic user experience.

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL 15 (Docker)
- **Frontend**: Bootstrap 5, HTMX, Alpine.js
- **Auth**: Django Allauth
- **Containerization**: Docker & Docker Compose

## Deployment & Installation

Detailed instructions for installing Docker and deploying the application across Linux, macOS, and Windows can be found in our **[Deployment Guide](deploy.md)**.

### Quick Start (If Docker is already installed)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Nexus_WeFix
   ```

2. **Start the environment**:
   ```bash
   docker-compose up --build -d
   ```

3. **Initialize the database** (Run in a new terminal):
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py create_demo_data
   ```

4. **Access the Application**:
   - Web App: [http://localhost:8000](http://localhost:8000)
   - Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)

### Run Locally Without Docker (Windows)

Install Python 3.11 and open PowerShell in the project folder. Run:

```powershell
.\run-local.ps1
```

The script creates a `.venv`, installs the requirements, initializes a local SQLite database, and starts the app at [http://localhost:8000](http://localhost:8000). The first run needs an internet connection to install dependencies. To also create demo accounts and data, run:

```powershell
.\run-local.ps1 -CreateDemoData
```

Stop the server with `Ctrl+C`.
If PowerShell blocks the script, run it with:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-local.ps1
```

## Project Structure

```
Nexus_WeFix/
├── .docs/              # Project documentation
├── src/                # Source code
│   ├── apps/           # Django applications (accounts, workers, bookings, feedback)
│   ├── nexus/          # Root project configuration
│   ├── static/         # Static files
│   └── templates/      # HTML templates
├── Dockerfile          # Web service container configuration
├── docker-compose.yml  # Multi-container orchestration
└── requirements.txt    # Python dependencies
```

## Development

- To run tests: `docker-compose exec web pytest`
- To access Django shell: `docker-compose exec web python manage.py shell`
