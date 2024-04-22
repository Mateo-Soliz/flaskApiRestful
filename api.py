from flask import Flask, render_template, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)

#base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    

parseador = reqparse.RequestParser()
parseador.add_argument('task', type=str)

class Todo(Resource):
    #get,post, put,delete
    def get(self, todo_id):
        todo = TodoModel.query.filter_by(id=todo_id).first()
        return {
            "task": todo.task
        }
    def post(self, todo_id):
        args = parseador.parse_args()
        print(args)
        todo = TodoModel(id=todo_id, task=args['task'])
        db.session.add(todo)
        db.session.commit()
        return {
            "task": todo.task
        }
    def put(self, todo_id):
        args = parseador.parse_args()
        todo = TodoModel.query.filter_by(id=todo_id).first()
        todo.task = args['task']
        db.session.commit()
        return {
            "task": todo.task
        }
    def delete(self, todo_id):
        todo = TodoModel.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        return {
            "task": "deleted"
        } 

api.add_resource(Todo, '/todo/<string:todo_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)