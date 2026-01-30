from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    def get_with_children_ids(self, db: Session, activity_id: int) -> list[int]:
        # рекурсивно собираем id всех потомков
        result: list[int] = []

        def collect_ids(act: Activity):
            result.append(act.id)
            for child in act.children:
                collect_ids(child)

        root = db.query(Activity).filter(Activity.id == activity_id).first()
        if root:
            collect_ids(root)
        return result

    def can_create_with_parent(self, db: Session, parent_id: int | None) -> bool:
        if parent_id is None:
            return True
        parent = db.query(Activity).filter(Activity.id == parent_id).first()
        if not parent:
            return False

        level = 1
        current = parent
        while current.parent is not None:
            level += 1
            current = current.parent
        # разрешаем максимум 3 уровня
        return level < 3


activity = CRUDActivity(Activity)
