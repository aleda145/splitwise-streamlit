#!/bin/bash

docker build -f Dockerfile . -t streamlit
docker run -v $(pwd)/splitwise.csv:/app/splitwise.csv --publish 8501:8501 streamlit