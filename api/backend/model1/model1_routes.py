from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)
import json
import pandas as pd
import numpy as np
from backend.db_connection import db
from backend.ml_models import model01

# This blueprint handles some basic routes that you can use for testing
model1_routes = Blueprint("model1_routes", __name__)