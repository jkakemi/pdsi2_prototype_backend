import src.app.classes as classes
import src.app.model as model
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import FastAPI, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from src.app.database import engine, get_db
from sqlalchemy.orm import Session
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
   'http://localhost:3000'
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=['*'],
   allow_headers=['*']
)
# Se tiver uma pasta dentro, tem que
# colocar pasta.main:app exemplo
@app.get("/")
def read_root():
    return {"Hello": "lala"}   

@app.post("/criar")
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    #mensagem_criada = model.Model_Mensagem(titulo=nova_mensagem.titulo, conteudo=nova_mensagem.conteudo, publicada=nova_mensagem.publicada)
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/quadrado/{num}")
def square(num: int):
    return num**2

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int=100):
 mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
 return mensagens

# @app.post("/criar")
# def criar_valores(res: dict = Body(...)):
#     print(res)
#     return {"Mensagem": "Criado com Sucesso!"}

# @app.post("/criar")
# def criar_valores(res: dict = Body(...)):
#     print(res)
#     return {"Mensagem": f"lala: {res['lala']} lele: {res['lele']}"}

# @app.post("/criar")
# def criar_valores(nova_mensagem: classes.Mensagem):
#     print(nova_mensagem)
#     return {"Mensagem": f"Titulo: {nova_mensagem.titulo} Mensagem: {nova_mensagem.conteudo} Publicada: {nova_mensagem.publicada}"}