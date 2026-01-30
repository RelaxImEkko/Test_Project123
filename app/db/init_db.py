from sqlalchemy.orm import Session

from app.models.building import Building
from app.models.activity import Activity
from app.models.organization import Organization, OrganizationPhone


def init_db(db: Session) -> None:
    # если уже есть данные – не дублируем
    if db.query(Organization).first():
        return

    # ==== Здания (10 штук) ====
    buildings: list[Building] = []
    base_lat = 55.75
    base_lon = 37.60

    for i in range(10):
        b = Building(
            address=f"г. Москва, ул. Ленина {i + 1}, офис {i + 10}",
            latitude=base_lat + i * 0.01,
            longitude=base_lon + i * 0.01,
        )
        db.add(b)
        buildings.append(b)

    db.flush()

    # ==== Деятельности (дерево, >10 штук) ====
    # 1-й уровень
    food = Activity(name="Еда", parent_id=None)
    auto = Activity(name="Автомобили", parent_id=None)
    db.add_all([food, auto])
    db.flush()

    # 2-й уровень под Еда
    meat = Activity(name="Мясная продукция", parent_id=food.id)
    milk = Activity(name="Молочная продукция", parent_id=food.id)

    # 2-й уровень под Автомобили
    trucks = Activity(name="Грузовые", parent_id=auto.id)
    cars = Activity(name="Легковые", parent_id=auto.id)
    db.add_all([meat, milk, trucks, cars])
    db.flush()

    # 3-й уровень под Легковые
    parts = Activity(name="Запчасти", parent_id=cars.id)
    accessories = Activity(name="Аксессуары", parent_id=cars.id)
    tuning = Activity(name="Тюнинг", parent_id=cars.id)
    db.add_all([parts, accessories, tuning])
    db.flush()

    activities = [food, meat, milk, auto, trucks, cars, parts, accessories, tuning]

    # ==== Организации (10 штук) ====
    orgs: list[Organization] = []
    names = [
        'ООО "Рога и Копыта"',
        'ООО "Мясной двор"',
        'ООО "Молочные реки"',
        'ООО "АвтоГруз"',
        'ООО "Легковичок"',
        'ООО "Запчасть-Сервис"',
        'ООО "Автоакс"',
        'ООО "Тюнинг-Профи"',
        'ООО "Фермерская лавка"',
        'ООО "Городская еда"',
    ]

    for i in range(10):
        org = Organization(
            name=names[i],
            building_id=buildings[i].id,
        )
        db.add(org)
        orgs.append(org)

    db.flush()

    # ==== Телефоны (по 2–3 номера на каждую) ====
    phone_templates = [
        "2-222-22{}",
        "3-333-33{}",
        "8-923-666-1{}-{}",
    ]

    for idx, org in enumerate(orgs, start=1):
        phones = [
            OrganizationPhone(
                organization_id=org.id,
                phone=phone_templates[0].format(idx),
            ),
            OrganizationPhone(
                organization_id=org.id,
                phone=phone_templates[1].format(idx),
            ),
            OrganizationPhone(
                organization_id=org.id,
                phone=phone_templates[2].format(idx, idx),
            ),
        ]
        db.add_all(phones)

    # ==== Привязка организаций к видам деятельности ====
    # немного рандомной логики по индексам
    for i, org in enumerate(orgs):
        if i == 0:
            org.activities.extend([food, meat, milk])
        elif i == 1:
            org.activities.append(meat)
        elif i == 2:
            org.activities.append(milk)
        elif i == 3:
            org.activities.append(trucks)
        elif i == 4:
            org.activities.append(cars)
        elif i == 5:
            org.activities.extend([cars, parts])
        elif i == 6:
            org.activities.extend([cars, accessories])
        elif i == 7:
            org.activities.extend([cars, tuning])
        elif i == 8:
            org.activities.extend([food, meat])
        elif i == 9:
            org.activities.extend([food, milk])

    db.commit()
