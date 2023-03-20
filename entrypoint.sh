if [ "$API_DEBUG" = "True" ]; then
    echo "Running Development Server"
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
else
    echo "Running Production Server"
    uvicorn main:app --host 0.0.0.0 --port 8080
fi