# minesweeper
A React frontend (with NextJS) + Django backened minesweeper app

# Local Dev
## Start the server
1. Ensure you have latest python3, django and pip setup
2. In `./api` directory, start the python virtual environment
```bash
source bin/activate
```
3. Run migrations to set up the built-in database in Django
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Start the server
```
python manage.py runserver
```
The server should be now available on `localhost:8000`.

## Start the client
Follow client's README.md instructions using `npm run dev`. The client should be available at `localhost:3000`. This is where the game UI resides.
To play the game you must have the server running on your local machine as well.

