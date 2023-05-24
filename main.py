import uvicorn


from api.api import create_app

app = create_app()


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)


if __name__ == "__main__":
    main()
