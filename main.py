from fastapi import FastAPI, Request
from App import models
from App.database import engine
from App.routers import trainings, users, login, predict
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import logging as lg
import uvicorn
import os

app = FastAPI(
    title="Featness API",
    description="Track your trainings on our app",
    terms_of_service="www.google.com",
    contact={
        "Team Developer": "Gideon, Guillaume and Sofiane",
        "Website": "www.google.com",
        "email": "sss@gmail.com",
    },
    license_info={
        "name": "Open Simplon"
    }
)

templates = Jinja2Templates(directory="App/templates")


@app.get('/', response_class=HTMLResponse)
async def depart(request: Request):
    """_summary_
       Get a json with all users 
    """
    return templates.TemplateResponse("index.html", {'some_object': "some_object", 'request': request})

app.include_router(trainings.router)
app.include_router(users.router)
app.include_router(login.router)
# app.include_router(predict.router)


lg.info('Database destroy')
models.Base.metadata.drop_all(engine)
lg.info('Database start to create!')
models.Base.metadata.create_all(engine)
lg.info('Database created')

# lg.info('Database import bird')
# data = pd.read_csv ('App/data/OiseauxFini.csv')
# df = pd.DataFrame(data)
# df.to_sql('birds', con = engine, if_exists='append', index=False)

lg.info('Database import users!')

lg.info('Database initialized!')

if __name__ == "__main__":
    uvicorn.run("main:app")
