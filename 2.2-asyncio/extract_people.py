import asyncio, aiohttp
from pprint import pprint
from models import engine, Base, Session, SwapiPeople
from more_itertools import chunked

async def get_person_count():
    session = aiohttp.ClientSession()
    response = await session.get(f'https://swapi.dev/api/people/')
    json_data = await response.json()
    await session.close()
    return json_data['count']


async def get_person_list_params(param=None, path=None):
    session = aiohttp.ClientSession()
    response = await session.get(path)
    json_data = await response.json()
    await session.close()
    if param == 'film':
        return json_data['title']
    else:
        return json_data['name']


async def get_person(person_id):
    try:
        session = aiohttp.ClientSession()
        response = await session.get(f'https://swapi.dev/api/people/{person_id}/')
       
        json_data = await response.json(content_type='application/json')
    except:
        get_person(person_id)
    await session.close()
    return json_data


async def add_to_db(objects):
    async with Session() as session:
        orm_objects = []
        for obj in objects:
            orm_object = SwapiPeople(
                birth_year = obj['birth_year'],
                eye_color = obj['eye_color'],
                films = ', '.join(obj['films']),
                gender = obj['gender'],
                hair_color = obj['hair_color'],
                height = obj['height'],
                homeworld = obj['homeworld'],
                mass = obj['mass'],
                name = obj['name'],
                skin_color = obj['skin_color'],
                species = ', '.join(obj['species']),
                starships = ', '.join(obj['starships']),
                vehicles = ', '.join(obj['vehicles']),
            )
            orm_objects.append(orm_object)
        session.add_all(orm_objects)
        await session.commit()


async def main():
    
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    
    person_count = await get_person_count()
    person_coros = (get_person(i) for i in range(1, person_count + 2))
    persons = await asyncio.gather(*person_coros)
    
    for person in persons:
        if person.get('detail') == 'Not found':
            persons.remove(person)
            continue
        
        person_films_coros = (get_person_list_params(param='film', path=film) for film in person.get('films') if person.get('films') is not None)
        person_species_coros = (get_person_list_params(path=spec) for spec in person.get('species') if person.get('species') is not None)
        person_starships_coros = (get_person_list_params(path=starship) for starship in person.get('starships') if person.get('starships') is not None)
        person_vehicles_coros = (get_person_list_params(path=vehicle) for vehicle in person.get('vehicles') if person.get('vehicles') is not None)
        
        person['films'] = await asyncio.gather(*person_films_coros)
        person['species'] = await asyncio.gather(*person_species_coros)
        person['starships'] = await asyncio.gather(*person_starships_coros)
        person['vehicles'] = await asyncio.gather(*person_vehicles_coros)
    
    task = asyncio.create_task(add_to_db(persons))
    await task



if __name__ == '__main__':
    asyncio.run(main())