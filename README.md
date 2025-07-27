### Start app

 - create venv `python3 -m venv venv`
 - activate venv `source venv/bin/activate`
 - install requirements `pip install -r requirements.txt`
 - filling core/.env file
 - start docker compose `docker compose up`
 - start faust app `faust -A faust_main worker -l info`
 - check on ui result test data)