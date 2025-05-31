from typing import List
from apps.victims.dto.victim_dto import VictimCreateRequest, VictimCreateResponse, VictimResponse, VictimUpdateRequest
from apps.victims.service.victim_service import VictimService
from ninja import Router

router = Router(tags=["Vítimas"])

@router.post("/", response={200: VictimCreateResponse, 201: VictimCreateResponse, 400: dict, 403: dict})
def create_victim(victim: VictimCreateRequest):
    return VictimService().create_victim(victim)

@router.get("/", response={200: List[VictimResponse], 400: dict, 403: dict})
def list_victims():
    return VictimService().list_victims()

@router.get("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def get_victim(victim_id: int):
    return VictimService().get_victim(victim_id)

@router.put("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def update_victim(victim_id: int, victim: VictimUpdateRequest):
    return VictimService().update_victim(victim_id, victim)

@router.delete("/{victim_id}", response={200: dict, 400: dict, 403: dict})
def delete_victim(victim_id: int):
    return VictimService().delete_victim(victim_id)


