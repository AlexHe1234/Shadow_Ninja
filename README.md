# README

## Environment

1. Node.js
2. Npm
3. Python3
4. MySQL

## Organization
This repo is organized into 3 completely separate folders

1. Backend - entire backend using flask + alchemy
2. Database - a single sql creation file
3. Frontend - entire frontend using node.js and vue

## Run

1. Have mysql ready, change config inside `backend/config.py`, and execute the `database/create.sql` file
2. `cd backend`, then `python3 app.py`
3. `cd frontend`, then `npm install`. if you want to dev locally run  `npm run dev`. if you want to deploy then run `npm run build` and `npm run preview`.
