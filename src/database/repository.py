from sqlalchemy.orm import Session
from src.database.models import Base


def add_one[Model: Base](model: type[Model], session: Session, **args) -> Model:
  instance = model(**args)
  session.add(instance)
  session.flush()

  return instance

def add_many[Model: Base](model: type[Model], session: Session, args_list: list[dict]) -> list[Model]:
  instances = [model(**args) for args in args_list]
  session.add_all(instances)
  session.flush()

  return instances

def get_all[Model: Base](model: type[Model], session: Session) -> list[Model]:
  return session.query(model).all()

def update[Model: Base](model: type[Model], session: Session, instance_id: any, **args) -> Model:
  instance = session.get(model, instance_id)
  if not instance:
    raise ValueError(f"{model.__name__} with id {instance_id} not found.")

  for key, value in args.items():
    setattr(instance, key, value)

  session.flush()
  return instance

def delete[Model: Base](model: type[Model], session: Session, instance_id: any):
  instance = session.get(model, instance_id)
  if not instance:
    raise ValueError(f"{model.__name__} with id {instance_id} not found.")

  session.delete(instance)
  session.flush()