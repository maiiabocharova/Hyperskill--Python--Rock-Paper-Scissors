from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_restful import reqparse, inputs
from flask_marshmallow import Marshmallow
import sys
import datetime
from flask_restful import fields, marshal_with
resource_fields = {
    'id':   fields.Integer,
    'event':    fields.String,
    'date': fields.String
}
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
class Event(db.Model):
    __tablename__ = 'event_name'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
db.create_all()


class EventSchema(ma.Schema):
    class Meta:
        fields = ("id", "event", "date")
events_schema = EventSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)
parser2 = reqparse.RequestParser()
parser2.add_argument(
    'start_time',
    type=inputs.date,
    required=False
)
parser2.add_argument(
    'end_time',
    type=inputs.date,
    required=False
)

class Events(Resource):
    def get(self):
        try:
            args = parser2.parse_args()
            print(args)
            start_time = args['start_time']
            end_time = args['end_time']
            events = Event.query.filter((Event.date >= start_time) & (Event.date <= end_time))
            if events is None:
                abort(404, "The event doesn't exist!")
            print(len(events_schema.dump(events)))
            return events_schema.dump(events)
        except:
            events = Event.query.all()
            return events_schema.dump(events)

    def post(self):
        args = parser.parse_args()
        new_event = Event(event=args['event'], date=args['date'])
        db.session.add(new_event)
        db.session.commit()
        return {
    "message": "The event has been added!",
    "event": args['event'],
    "date": str(args['date'].date())
}

class EventByID(Resource):
    def get(self, event_id):
        print(f'select event_id: {event_id}')
        event = Event.query.get(event_id)
        if event:
            event = Event.query.filter(Event.id==event_id).all()
            return events_schema.dump(event)[0]
        else:
            abort(404, "The event doesn't exist!")

    def delete(self, event_id):
        print(f'delete event_id: {event_id}')
        event = Event.query.get(event_id)
        print(event)
        if event:
            db.session.delete(event)
            db.session.commit()
            return {"message": "The event has been deleted!"}
        else:
            abort(404, "The event doesn't exist!")

class EventsToday(Resource):
    def get(self):
        event = Event.query.filter(Event.date==datetime.date.today()).all()
        if event is None:
            #return {"message": "The event doesn't exist!"}
            abort(404, "The event doesn't exist!")
        return events_schema.dump(event)

api.add_resource(EventByID, '/event/<int:event_id>')
api.add_resource(Events, '/event')
api.add_resource(EventsToday, '/event/today')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
