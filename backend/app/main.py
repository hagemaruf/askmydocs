from fastapi import FastAPI

app = FastAPI(
    title="AskMyDocs API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AskMyDocs API is running"
    }