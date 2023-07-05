# Social Network App

This is a small social network app built with FastAPI. It provides API endpoints for managing posts and likes. 

## Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/social-network-app.git

2. Edit docker-compose.yml file to add API keys for HUNTER_API_KEY and ENRICHMENT_API_KEY. The app will work without said keys but it will not use these services.

3. Start the app using the following command:
    ```bash
    docker-compose up --build

4. The API will be accessable at http://0.0.0.0:8000

5. To run the tests, use the following command:
    ```bash
    docker-compose exec social_network pytest social_network/

6. Swagger documentation for the API endpoints is available at http://localhost:8000/docs when the project is started.
