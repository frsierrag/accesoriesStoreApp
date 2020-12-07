from flask import Flask, render_template, redirect, url_for
from app.settings.config import Ajustes
app = Flask(__name__)
app.config.from_object(Ajustes)
from app import rutas