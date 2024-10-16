# 🎬 IMDB App

This project is part of an assignment by DailyRounds. It provides a RESTful API for uploading and fetching movie data stored in a MongoDB database. The application supports CSV file uploads and offers pagination, filtering, and sorting options for retrieving movie records.

## 📖 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup and Usage](#setup-and-usage)
- [API Endpoints](#api-endpoints)
- [Test Cases and Code Coverage](#testcases-and-code-coverage)
- [Contributions](#contributions)

## Features

- **Upload Movies via CSV**: Upload movie data using a CSV file to populate the database.
- **Fetch Movies with Pagination**: Retrieve movie records with pagination, filtering, and sorting support.
- **Data Validation**: Validates the input data for consistency and correctness during uploads.
- **Error Handling & Logging**: Provides robust error handling with detailed logging for troubleshooting.

## Requirements

- Python 3.x
- chalice (a Python framework by AWS based on Flask)
- pandas
- pymongo
- MongoDB (local setup for development). Refer to the [official MongoDB documentation](https://www.mongodb.com/docs/manual/administration/install-community/) to install the MongoDB community version.

## Installation

Install the required Python packages using `pip` and the [requirements.txt](./requirements.txt) file:

```bash
pip install -r requirements.txt
```

## Setup and Usage

After installing the required Python packages, navigate to the `imdb-app` directory in your terminal:
```bash
cd imdb-app
```

Update the environment variables in the [.chalice/config.json](./.chalice/config.json) file as needed. To run the service on your local machine, use the Chalice local command:

```bash
chalice local
```

This will start the service on `localhost` with the default port `8000`. To run the service on a specific port, use:

```bash
chalice local --port <PORT_NUMBER>
```

To verify that the service is running, use the following cURL command on terminal, Postman, or hit the endpoint on your browser:

```bash
curl --location 'http://127.0.0.1:8000/api/health_check'
```

A status message indicating "Running" should be displayed. Use the remaining API endpoints via Postman or your preferred method.

To test the APIs directly, you can import the existing [Postman collection](./postman_collection) and hit the endpoints on the Postman app.


## API Endpoints

- Healthcheck API
Check if the service is running:
<img width="532" alt="image" src="https://github.com/user-attachments/assets/d1f08135-9b55-4ef3-9c72-283b6d9c4e27">

- Upload File API
Upload a CSV file to add movie data:
<img width="608" alt="image" src="https://github.com/user-attachments/assets/ff688727-d658-477b-9b3f-d4415bf70bf7">

- Fetch Data API
Retrieve movie records with pagination, filtering, and sorting options:
<img width="581" alt="image" src="https://github.com/user-attachments/assets/e9875478-ad9d-41b5-baf4-80323d801072">


## Testcases and Code Coverage

To view the test cases for the API endpoints, explore the tests/ folder. To run the test cases and generate a code coverage report, navigate to the imdb-app directory in your terminal:

```bash
cd imdb-app
```

Then, execute the generate_coverage.sh script:

```bash
./generate_coverage.sh 
```

This will generate code coverage reports (.coverage and coverage.xml) and help you ensure the application's reliability and quality.

## Contributions

Contributions are welcome! Feel free to submit a pull request or open an issue for discussion. Thank you for your interest!
