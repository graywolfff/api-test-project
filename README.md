### TRAVEL RECOMMENDATION SYSTEM

This repository have use **OpenAI** to recommend some place to visit in a country on a season.  
For example you want to go to Vietman in summer but not know what **attivities** you should do.  
This repository will help you.  

---  

### How to setup and run  

**TO RUN THIS REPO, YOU NEED DOCKER ON YOUR MACHINE**

#### 1. Modify `.env` file. 

This file contain environment variable to run this system.  Rename or make a copy of `.env.expample` file to `.env` in case this file doesn't exist.  
Please enter your **OPENAI_API_KEY**  (**important**)
Modify another variables in case you need.  

---

#### 2. Build Docker images and run application

In the root of repository (where you can find `docker-compose.yml` file)  
Run `docker-compose build` command to build images  
After building process is complete, just run all servies that definded on `docker-compose.yml` file.  
Run command `docker-compose up -d` to do that.   

---
#### 3. Call first API endpoint to see the result  
On the browser, navigate to `/docs` or  `/redoc` to read and make your requests  
If in `.env` file, `API_SERVER_PORT` set to 3000, the url will be `http://your-host:3000/docs`  

Make request to get recommendation  
<img src="./make_recommendation_request.png" alt="make_recommendation_request">  
After you have uid of your request, you can retreive the answer after that.  
<img src="./retrieve_recommendation_result.png" alt="retrieve_recommendation_result">  
