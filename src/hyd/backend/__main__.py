import uvicorn

uvicorn.run("hyd.backend.main:app", host="0.0.0.0", port=8000, reload=True)
