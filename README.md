# Multimedia Capstone Project

## Installing and Deploying using Docker

### For Windows 11

    1. Download WSL2 and install Ubuntu
        a. Open Windows PowerShell as Administrator and run:
            wsl --install (2 dashes before install)
        b. This will install the WSL2 kernel, set WSL2 as default, and pull down Ubuntu
    2. Open Ubuntu from the Start menu. You will be prompted to create a Linux user/password
    3. Download, install, and configure Docker Desktop
        a. In the same Windows Powershell as Administrator, run this command to download and install Docker Desktop:
                winget install --id Docker.DockerDesktop -e --source winget
        b. After installation is complete, launch Docker Desktop, go to Settings → General, check “Use the WSL2 based engine”. Then
           under Settings → Resources → WSL Integration, check “Enable integration with my default WSL distro”. Make sure to click
           “Apply and restart” to save these changes if not enabled by default.
    4. Clone the repo in WSL2/Ubuntu
        a. Back in the Ubuntu shell, run the following commands:
                cd ~
                git clone https://github.com/tyymr23/DiscoveryPortal.git
                cd DiscoveryPortal
    5. Add necessary .env file
        a. Run the following command to reach the backend folder:
                cd backend
        b. Then run nano .env and enter the following:
                TOKEN_KEY=admin
                MYSQL_HOST=localhost
                MYSQL_USER=root
                MYSQL_PASSWORD=admin
                MYSQL_DB=portal
                MYSQL_PORT=3306
                PORT=3001
                # Admin Username and Password
                # Username: VT_ADMIN
                # Password: C$-P0rt@l_ADMIN-passWrd
        c. After adding these lines, enter ctrl+X and then click y and enter to save these changes
    6. Build the Docker image
        a. Return to the main project directory using:
                cd ..
        b. Run the following command to build the Docker image (do not forget the period):
                docker build -t library .
        c. If you receive an error such as the one below, consider closing Ubuntu/Docker Desktop and reopening them to assure all
           changes are synced. After reopening, return to step 6b.
                ERROR: permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Head
                "http://%2Fvar%2Frun%2Fdocker.sock/_ping": dial unix /var/run/docker.sock: connect: permission denied
    7. Run the container
        a. Run the followings command to run the container (this is one single command):
                docker run -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock library
    8. The project is now running on http://localhost:80/

### For Linux

    1. Download, install, and configure Docker Desktop
        a. run this command (if using apt) to download and install Docker Desktop using your distro's package manager for linux (e.g
           apt, dnf, pacman): 
                sudo apt-get install ./docker-desktop-amd64.deb
        b. If the following error appears at the end of installation, it can be ignored:
                N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by
                user '_apt'. - pkgAcquire::Run (13: Permission denied)
        c. After installation is complete, launch Docker Desktop
    2. Clone the project where the application is wanting to run:
        a. Open a terminal on VS code (or where you will run the project) and type the following commands in:
                cd ~
                git clone https://github.com/tyymr23/DiscoveryPortal.git
                cd DiscoveryPortal
    3. Add necessary .env file
        a. Run the following command to reach the backend folder:
                cd backend
        b. Then run nano .env and enter the following:
                TOKEN_KEY=admin
                MYSQL_HOST=localhost
                MYSQL_USER=root
                MYSQL_PASSWORD=admin
                MYSQL_DB=portal
                MYSQL_PORT=3306
                PORT=3001
                # Admin Username and Password
                # Username: VT_ADMIN
                # Password: C$-P0rt@l_ADMIN-passWrd
        c. After adding these lines, save the changes and the file can be closed
    4. Build the Docker image
        a. Return to the main project directory using:
                cd ..
        b. Run the following command to build the Docker image (do not forget the period):
                docker build -t library .
        c. If you receive an error such as the one below, consider closing Docker Desktop and reopening it to assure all changes are
           synced. After reopening, return to step 4b.
                Cannot connect to the Docker daemon at unix:///Users/josh/.docker/run/docker.sock.
    5. Run the container
        a. Run the followings command to run the container (this is one single command):
                docker run -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock library
    6. The project is now running on http://localhost:80/

### For Mac

    1. Download, install, and configure Docker Desktop
        a. Run this command using HomeBrew to download and install Docker Desktop: 
                brew install --cask docker
        b. Note that Docker Desktop must be opened from the Applications folder or the Spotlight search
    2. Clone the project where the application is wanting to run:
        a. Open a terminal on VS code (or where you will run the project) and type the following commands in:
                cd ~
                git clone https://github.com/tyymr23/DiscoveryPortal.git
                cd DiscoveryPortal
    3. Add necessary .env file
        a. Run the following command to reach the backend folder:
                cd backend
        b. Then run nano .env and enter the following:
                TOKEN_KEY=admin
                MYSQL_HOST=localhost
                MYSQL_USER=root
                MYSQL_PASSWORD=admin
                MYSQL_DB=portal
                MYSQL_PORT=3306
                PORT=3001
                # Admin Username and Password
                # Username: VT_ADMIN
                # Password: C$-P0rt@l_ADMIN-passWrd
        c. After adding these lines, save the changes and the file can be closed
    4. Build the Docker image
        a. Return to the main project directory using:
                cd ..
        b. Run the following command to build the Docker image (do not forget the period):
                docker build -t library .
        c. If you receive an error such as the one below, consider closing Docker Desktop and reopening it to assure all changes are
           synced. After reopening, return to step 4b.
                Cannot connect to the Docker daemon at unix:///Users/josh/.docker/run/docker.sock.
    5. Run the container
        a. Run the followings command to run the container (this is one single command):
                docker run -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock library
    6. The project is now running on http://localhost:80/





