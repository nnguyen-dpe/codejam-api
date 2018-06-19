from flaskwsk import invoke
from app import app

def main(args):
    return invoke(app, args)