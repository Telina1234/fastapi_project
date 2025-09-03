from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Characteristics(BaseModel):
        max_speed: float
        max_fuel_capacity: float

class Car(BaseModel):
        identifier: str
        brand: str
        model: str
        characteristics: Characteristics

cars: List[Car] = []

@app.get("/ping")
def ping():
        return "pong"

def convert_car_to_dict(car: Car):
        return {
                "identifier": car.identifier,
                "brand": car.brand,
                "model": car.model,
                "characteristics": {
                        "max_speed": car.characteristics.max_speed,
                        "max_fuel_capacity": car.characteristics.max_fuel_capacity
                }
        }

@app.post("/cars", status_code=201)
def create_cars(new_cars: List[Car]):
        for car in new_cars:
                cars.append(car)
        result = []
        for car in cars:
                result.append(convert_car_to_dict(car))
        return {"cars": result}

@app.get("/cars")
def list_cars():
        result = []
        for car in cars:
                result.append(convert_car_to_dict(car))
        return {"cars": result}

@app.get("/cars/{car_id}")
def get_car(car_id: str):
        for car in cars:
                if car.identifier == car_id:
                        return {"car": convert_car_to_dict(car)}
        return {"message": f"Car with id '{car_id}' not found"}, 404

@app.put("/cars/{car_id}/characteristics")
def update_characteristics(car_id: str, new_chars: Characteristics):
        for car in cars:
                if car.identifier == car_id:
                        car.characteristics.max_speed = new_chars.max_speed
                        car.characteristics.max_fuel_capacity = new_chars.max_fuel_capacity
                        return {"car": convert_car_to_dict(car)}
        return {"message": f"Car with id '{car_id}' not found"}, 404
