from app.data import EQUIPMENT


def list_equipment():
    return list(EQUIPMENT.values())


def check_availability(equipment_id: int, quantity: int, department: str | None = None):
    equipment = EQUIPMENT.get(equipment_id)
    if equipment is None:
        return None
    available = equipment["available_quantity"]
    # 일반 부서는 지급 후 최소 1대를 남겨야 한다. IT 부서·부서 생략은 남은 수량까지 가능.
    reserve = 1 if department == "general" else 0
    can_allocate = quantity <= available - reserve
    return {
        "equipment_id": equipment_id,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_allocate": can_allocate,
    }
