import os


def add_os_variables():
    os.environ["ENV"] = "local"
    os.environ["SERVICE_NAME"] = "imdb-app"
    os.environ["MONGO_CONNECTION_STRING"] = "mongodb:{password}//localhost:27017/"
    os.environ["MONGODB_PASSWORD"] = ""
    os.environ["MAX_CSV_FILE_SIZE_IN_MB"] = "100"
