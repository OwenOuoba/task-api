from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

# Créer les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Une API simple pour gérer des tâches",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Bienvenue sur Task Manager API! Visite /docs pour la documentation"}

# CREATE - Créer une tâche
@app.post("/tasks/", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# READ - Lire toutes les tâches
@app.get("/tasks/", response_model=List[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

# READ - Lire une tâche spécifique
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

# UPDATE - Mettre à jour une tâche
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    # Mise à jour uniquement des champs fournis
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# DELETE - Supprimer une tâche
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    db.delete(db_task)
    db.commit()
    return None