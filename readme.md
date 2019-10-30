[![PyPI pyversions](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360)

# Installation of development environment

### Dependencies

```sh
# Create virtual environment
python3.7 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Install python dependencies
pip install -r requirements.txt
pip install -r api/requirements.txt
pip install -r miner/requirements.txt
# Create data folders and .env file with PYTHONPATHs
./run.sh prepare
# Run development docker stack
./run.sh dev
```

# Installation of production environment

### Dependencies

```sh
# Install system dependencies
sudo apt-get install git htop build-essential python-pip
# Install docker
# (Ubuntu)
https://docs.docker.com/install/linux/docker-ce/ubuntu/
# (Debian)
https://docs.docker.com/install/linux/docker-ce/debian/
# Install Docker-compose
https://docs.docker.com/compose/install/
# Clone Git repo
git clone https://github.com/Outbooker/Outbookers.git outbookers
# Share prod config with remote server
scp ./configs/.prod.env root@95.216.199.197:/root/projects/outbookers/configs/

# Configure Database according to instructions below (don't forget to replace password with prod password)

./run.sh prepare
# Run development docker stack
./run.sh prod
```

### Database

Initial setup:

```sh
# Connect to PostgreSQL container
./run.sh postgres
# Run PostgreSQL shell
psql --user outbookers
# Create database outbookers
CREATE DATABASE outbookers;
CREATE DATABASE outbookers_test;
# Create user outbookers
CREATE USER outbookers WITH ENCRYPTED PASSWORD 'outbookers';
# Give permissions to user outbookers on database outbookers
GRANT ALL PRIVILEGES ON DATABASE outbookers TO outbookers;
GRANT ALL PRIVILEGES ON DATABASE outbookers_test TO outbookers;

# Create tables
docker exec -it outbookers_api python -m shared.database.db_utils -t init_db
# Connect to PostgreSQL again and add new user with password 'admin'
INSERT INTO users (id, username, password, allowed_scrapers, is_admin) VALUES ('7edb2f05-b532-4a1d-89a5-689a5fb26da4', 'admin', 'pbkdf2:sha256:150000$8JaWXOKX$4ea771d57d0c45afa9c2bf928e9e3fb39389836064986bd9f231637d11e770a0', '{}', TRUE);
```

# Testing

```sh
# Activate virtual environment
source venv/bin/activate
# Run all tests
./run.sh test
```

# Other

Run scraper manually:

```sh
./run.sh miner
cd src/betsscrapers
scrapy crawl surebet -a website="surebet" -a username="10beteb@mail.ru" -a password=Surebet -a id="9cf1e945-3618-4833-8bd4-843d92392df9" -a main_book="10bet" -a scanned_book="Winline, Betcity" -a proxy_address="91.203.232.2:8000" -a proxy_username="1rKCnL" -a proxy_password="pgjMDC"
```
