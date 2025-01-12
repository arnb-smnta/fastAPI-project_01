from fastapi import APIRouter
from models.notes_model import Note
from config.db import conn
from schemas.notes_schema import notesEntity

note=APIRouter()