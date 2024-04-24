# AI Poker Bot & Product Recommender System

Welcome to my repository featuring an AI-powered Poker Bot, built on OpenAI's GPT-4, and a Product Recommender System utilizing a GANN Neural Network. This project includes a Vue.js frontend for interactive gameplay against the Poker Bot and for using the recommender system.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Node.js](https://nodejs.org/)
- Python (with an environment to run server scripts)

## Getting Started

Clone the repository to your local machine:

git clone https://your-repository-url.git
cd your-repository-directory

### Setting Up the AI Poker Bot

To set up and run the AI Poker Bot, follow these steps:

0. Obtain an Open Ai Api key, and insert this in the appsettings.py file. This may require a paid account. Read the server logs for debug information when running. 

2. Navigate to the AI Poker Bot directory:
   cd AI-Poker-Bot

3. Run the game server:
   python run GameServer.py

4. Install and run the frontend:
   npm install
   npm run serve

### Setting Up the Product Recommender

1. Navigate to the Recommender project directory:
   cd Recommender-Project
   
2. Run the server:
   python run server.py
   
3. Install and run the frontend:
   npm install
   npm run serve

## Usage

Once the servers are running, you can access the poker bot interface and the product recommender system UI through your browser by navigating to http://localhost:8080 or the port specified in your npm server output.

Also! There are many package dependancies in the projects, you must intall them all in an envioirnment, conda or pip. Reading the server logs will help identify which packages are missing when trying to run.

Enjoy playing against the AI Poker Bot or exploring product recommendations!

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

