import pandas as pd
import random
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json

df = pd.read_csv('Menu_List.csv')
df = df.fillna('')
app = FastAPI()


@app.get('/')
async def hello_world():
    return {"status": "서버켜짐"}


# 입력한 재료를 기반으로 레시피들을 조회
@app.get('/recipe/material')
async def food_material(material: str):
    food_list = df[df.eq(material).any(axis=1)]
    food_list = food_list.to_json(orient='records', force_ascii=False).replace("\\/", "/")
    
    if food_list:
        return json.loads(food_list)
    else:
        return {"status": 400}


# 카테고리를 기반으로 레시피들을 조회
@app.get('/recipe/category')
async def food_category(category: str):
    food_list = df[df.eq(category).any(axis=1)]
    food_list = food_list.to_json(orient='records', force_ascii=False).replace("\\/", "/")
    
    if food_list:
        return json.loads(food_list)
    else:
        return {"status": 400}


# 오늘의 추천 레시피
@app.get('/recipe/today')
async def today_recipe():
    a = random.sample(range(0, 281), 12)

    food_list = [df.iloc[i].to_dict() for i in a]
        
    food_list = pd.Series(food_list).to_json(orient='records', force_ascii=False).replace("\\/", "/")
    
    if food_list:
        return json.loads(food_list)
    else:
        return {"status": 400}


# 음식 아이디를 받으면 대표 이미지 리턴
@app.get('/recipe/{image_id}')
async def food_image(image_id: int):
    name = df.loc[image_id, 'name']
    return FileResponse(f'data/{name}/main.jpeg')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
