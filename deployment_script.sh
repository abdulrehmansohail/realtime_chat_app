
# Setup postgresql database on server
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER test WITH PASSWORD 'admin@1234';"
sudo -u postgres psql -c "CREATE DATABASE test_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE test_db TO test;"

# Exit the PostgreSQL shell
sudo -u postgres psql -c "\q"

# Step 3: Install python specified version
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt install python3.8 -y
python3.8 --version

# Change to the project directory
cd /home/ubuntu/realtime_chat_app/

# Install python virtual environment
sudo apt-get install python3.8-venv -y
python3.8 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip3 install -r requirements.txt

# Run django migrations
python3 manage.py migrate

# Run the Django development server
python3 manage.py runserver 0.0.0.0:8000
