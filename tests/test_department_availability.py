import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "department,equipment_id,quantity,available,expected",
    [
        ("it", 1, 3, 3, True),  # IT 최대 수량
        ("general", 1, 3, 3, False),  # 같은 입력에서 부서별 차이
        ("general", 1, 2, 3, True),  # 일반 부서 최대 수량
        (None, 1, 3, 3, True),  # 부서 생략 시 기존 동작 유지
        ("it", 1, 4, 3, False),  # 재고 초과
        ("general", 2, 1, 0, False),  # 재고 0
    ],
)
def test_department_availability(department, equipment_id, quantity, available, expected):
    params = {"quantity": quantity}
    if department is not None:
        params["department"] = department
    response = client.get(f"/equipment/{equipment_id}/availability", params=params)
    assert response.status_code == 200
    assert response.json() == {
        "equipment_id": equipment_id,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_allocate": expected,
    }


@pytest.mark.parametrize(
    "params",
    [
        {"department": "sales", "quantity": 1},  # 지원하지 않는 부서
        {"department": "it", "quantity": 0},  # 잘못된 수량
    ],
)
def test_invalid_input_is_rejected(params):
    response = client.get("/equipment/1/availability", params=params)
    assert response.status_code == 422


def test_unknown_equipment_with_department_returns_404():
    response = client.get(
        "/equipment/99/availability", params={"department": "it", "quantity": 1}
    )
    assert response.status_code == 404
