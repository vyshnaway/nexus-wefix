# Deployment Guide: Nexus WeFix

This guide covers how to set up and run the Nexus WeFix platform using Docker across Linux, macOS, and Windows.

---

## 1. Prerequisites

Before starting, ensure you have **Git** installed on your system to clone the repository.
- Download Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)

You will also need **Docker** and **Docker Compose**. Choose your operating system below for installation instructions.

---

## 2. Install Docker

### 🐧 Linux (Ubuntu/Debian)
1. Update your packages:
   ```bash
   sudo apt-get update
   ```
2. Install Docker:
   ```bash
   sudo apt-get install -y docker.io docker-compose
   ```
3. Start and enable the Docker service:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```
4. Add your user to the Docker group (so you don't need `sudo` for every command):
   ```bash
   sudo usermod -aG docker $USER
   ```
   *(Note: You may need to log out and log back in for this to take effect.)*

### 🍏 macOS
1. Download **Docker Desktop for Mac**: [https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)
2. Open the downloaded `.dmg` file and drag the Docker icon into your Applications folder.
3. Open Docker from your Applications folder to ensure the Docker daemon is running in the background. (Docker Compose comes pre-installed with Docker Desktop).

### 🪟 Windows
1. We highly recommend installing **WSL 2** (Windows Subsystem for Linux) first. Open PowerShell as Administrator and run:
   ```powershell
   wsl --install
   ```
2. Restart your computer if prompted.
3. Download **Docker Desktop for Windows**: [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)
4. Run the installer. Ensure "Use WSL 2 instead of Hyper-V" is checked during installation.
5. Launch Docker Desktop and wait for the engine to start. (Docker Compose is included).

---

## 3. Clone the Project
Open your terminal (or Command Prompt / PowerShell / WSL) and run:
```bash
git clone <repository-url>
cd Nexus_WeFix
```

*(Note: If using Windows, it is highly recommended to clone the project directly inside your WSL filesystem, e.g., `/home/username/`, rather than the mounted C: drive for significantly better performance).*

---

## 4. Build and Run the Application

Once Docker is running, follow these steps to deploy the application stack (Web + Database).

1. **Build the images and start the containers** in detached mode:
   ```bash
   docker-compose up --build -d
   ```
2. **Apply database migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
3. **Populate the database with Demo Data** (Optional, but highly recommended for testing):
   ```bash
   docker-compose exec web python manage.py create_demo_data
   ```
   *(This script automatically creates a few demo worker and customer accounts, a base set of services, and an admin user).*

4. **Create a Superuser manually** (if you skipped the demo data):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 5. View the App

The deployment is complete! Open your browser and navigate to:
- **Main Website**: [http://localhost:8000](http://localhost:8000) (or `http://localhost:8001` depending on your active mappings).
- **Admin Panel**: `/admin/` (Login with your superuser credentials).

## 6. Helpful Commands

- **Stop the servers:**
  ```bash
  docker-compose down
  ```
- **View active logs:**
  ```bash
  docker-compose logs -f web
  ```
- **Access the Django shell:**
  ```bash
  docker-compose exec web python manage.py shell
  ```
