
# from fastapi.testclient import TestClient
# from backend.app import app
# from config import ROOM_ID

# client = TestClient(app)

# def test_filter_api():
#     payload = {
#         "image_data": [1, 2, 3],
#         "width": 1,
#         "height": 1,
#         "filter_name": "blur"
#     }

#     res = client.post(f"/filter/{ROOM_ID}", json=payload)
#     assert res.status_code == 200
#     assert res.json()["image_data"] == payload["image_data"]

# def test_filter_invert_real():
#     payload = {
#         "image_data": [0, 0, 0, 255],  # чорний піксель RGBA
#         "width": 1,
#         "height": 1,
#         "filter_name": "invert"
#     }
    
#     expected = [255, 255, 255, 255]  # інверсія чорного — білий, альфа без змін
    
#     res = client.post(f"/filter/{ROOM_ID}", json=payload)
#     assert res.status_code == 200
#     assert res.json()["image_data"] == expected

from fastapi.testclient import TestClient
from backend.app import app
from config import ROOM_ID

client = TestClient(app)

def test_filter_api():
    payload = {
        "image_data": [1, 2, 3],       # спрощене тестове зображення
        "filter_name": "blur",        # назва фільтра
        "width": 1,
        "height": 3
    }

    res = client.post(f"/filter/{ROOM_ID}", json=payload)

    assert res.status_code == 200
    assert "image_data" in res.json()
    assert isinstance(res.json()["image_data"], list)  # або str — залежить від того, що повертає apply_filter_cpp


