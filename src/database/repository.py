import re

from sqlalchemy.orm import Session


def add_one(model: type, session: Session, **args):
  instance = model(**args)
  session.add(instance)
  session.flush()

  return instance

def add_many(model: type, session: Session, args_list: list[dict]):
  instances = [model(**args) for args in args_list]
  session.add_all(instances)
  session.flush()

  return instances

def get_all(model: type, session: Session):
  return session.query(model).all()

def update(model: type, session: Session, instance_id: any, **args):
  instance = session.get(model, instance_id)
  if not instance:
    raise ValueError(f"{model.__name__} with id {instance_id} not found.")

  for key, value in args.items():
    setattr(instance, key, value)

  session.flush()
  return instance

def delete(model: type, session: Session, instance_id: any):
  instance = session.get(model, instance_id)
  if not instance:
    raise ValueError(f"{model.__name__} with id {instance_id} not found.")

  session.delete(instance)
  session.flush()