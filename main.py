import pandas as pd
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn

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
    
    if not food_list.empty:
        return food_list
    else:
        raise HTTPException(status_code=404, detail="입력한 재료가 들어간 음식 레시피가 없습니다")


# 카테고리를 기반으로 레시피들을 조회
@app.get('/recipe/category')
async def food_category(category: str):
    food_list = df[df.eq(category).any(axis=1)]
    
    if not food_list.empty:
        return food_list
    else:
        raise HTTPException(status_code=404, detail="잘못된 카테고리입니다.")


# 오늘의 추천 레시피
@app.get('/recipe/today')
async def today_recipe():
    a = random.randint(0, 281)
    food_list = df.iloc[a]
    return food_list


# 음식 아이디를 받으면 대표 이미지 리턴
@app.get('/recipe/{image_id}')
async def food_image(image_id: int):
    name = df.loc[image_id, 'name']
    return FileResponse(f'data/{name}/main.jpeg')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)