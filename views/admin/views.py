import base64
import config
from flask import redirect, render_template, request, session, url_for, flash,g
import mysql
import mysql.connector
from . import admin_blu