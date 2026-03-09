import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from services.set_services import SetService
from services.exceptions import badRequestError
from models.game_cards_model import CardLocation

# --- MOCKS DE MODELOS ---

class MockCard:
    def __init__(self, image: str):
        self.image = image

class MockGameCards:
    def __init__(self, id: int, owner_id: int, location: CardLocation, image_prefix: str):
        self.id = id
        self.owner_id = owner_id
        self.location = location
        self.card = MockCard(f"{image_prefix}-detective.png")
        self.set_id = None

class MockSetPlay:
    def __init__(self, id: int, game_id: int, owner_id: int):
        self.id = id
        self.game_id = game_id
        self.owner_id = owner_id
        self.cards = []

# --- CONSTANTES ---
GAME_ID = 1
PLAYER_ID = 10
SET_ID = 100
DETECTIVE_CARD_ID = 200
POIROT_PREFIX = "07"
MARPLE_PREFIX = "08"

# --- FIXTURE PARA EL SERVICIO (Unit Test Setup) ---
@pytest.fixture
def mock_set_service(mock_db_session: Session):
    """
    Fixture que devuelve un SetService con sus repositorios mockeados.
    Se usa MagicMock para add_detective para evitar RuntimeWarning.
    """
    service = SetService(mock_db_session)
    
    # Mockear las funciones asíncronas de eventos
    with patch('services.set_services.emit_player_sets', new=AsyncMock()), \
         patch('services.set_services.emit_player_hand', new=AsyncMock()), \
         patch('services.set_services.emit_all_sets', new=AsyncMock()):
        
        service.repo = MagicMock()
        service.repo_game_cards = MagicMock()
        service.repo.add_detective = MagicMock(return_value=True) 
        
        yield service

# ==============================================================================
# PRUEBAS DE UNIDAD (SetService.join_detective_to_set)
# ==============================================================================

class TestSetServiceJoinDetective:
    
    # 1. Éxito: Detective tipo 07 a un Set tipo 07
    @pytest.mark.asyncio
    async def test_success_join_matching_detective(self, mock_set_service: SetService, mock_db_session: MagicMock):
        # Configuración
        target_set = MockSetPlay(SET_ID, GAME_ID, PLAYER_ID)
        detective_card = MockGameCards(DETECTIVE_CARD_ID, PLAYER_ID, CardLocation.HAND, POIROT_PREFIX)
        set_cards = [MockGameCards(301, PLAYER_ID, CardLocation.SET, POIROT_PREFIX)]
        
        mock_set_service.repo.get_by_id.return_value = target_set
        mock_set_service.repo_game_cards.get_by_id.side_effect = [detective_card, detective_card]
        mock_set_service.repo_game_cards.get_cards_in_set.return_value = set_cards
        
        # Ejecución
        result = await mock_set_service.join_detective_to_set(
            GAME_ID, DETECTIVE_CARD_ID, SET_ID, PLAYER_ID
        )
        
        # Verificación
        assert result is target_set
        mock_set_service.repo.add_detective.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(target_set)

    # 2. Fallo Lógica: Mismatch de tipo (07 Set + 08 Detective)
    @pytest.mark.asyncio
    async def test_failure_mismatch_set_type(self, mock_set_service: SetService):
        # Configuración
        target_set = MockSetPlay(SET_ID, GAME_ID, PLAYER_ID)
        detective_card = MockGameCards(DETECTIVE_CARD_ID, PLAYER_ID, CardLocation.HAND, MARPLE_PREFIX)
        set_cards = [MockGameCards(301, PLAYER_ID, CardLocation.SET, POIROT_PREFIX)]
        
        mock_set_service.repo.get_by_id.return_value = target_set
        mock_set_service.repo_game_cards.get_by_id.return_value = detective_card
        mock_set_service.repo_game_cards.get_cards_in_set.return_value = set_cards
        
        # Ejecución y Verificación (Espera HTTPException 400 por la conversión de badRequestError)
        with pytest.raises(HTTPException) as excinfo:
            await mock_set_service.join_detective_to_set(
                GAME_ID, DETECTIVE_CARD_ID, SET_ID, PLAYER_ID
            )
        assert excinfo.value.status_code == 400
        assert "Detective card does not match the set type" in excinfo.value.detail

    # 3. Fallo de Validación: Carta detective no está en la mano
    @pytest.mark.asyncio
    async def test_failure_card_not_in_hand(self, mock_set_service: SetService):
        # Configuración
        target_set = MockSetPlay(SET_ID, GAME_ID, PLAYER_ID)
        detective_card = MockGameCards(DETECTIVE_CARD_ID, PLAYER_ID, CardLocation.DISCARD, POIROT_PREFIX) 
        
        mock_set_service.repo.get_by_id.return_value = target_set
        mock_set_service.repo_game_cards.get_by_id.return_value = detective_card
        
        # Ejecución y Verificación (Espera HTTPException 400)
        with pytest.raises(HTTPException) as excinfo:
            await mock_set_service.join_detective_to_set(
                GAME_ID, DETECTIVE_CARD_ID, SET_ID, PLAYER_ID
            )
        assert excinfo.value.status_code == 400
        assert "Card does not belong to player or is not in their hand" in excinfo.value.detail


# ==============================================================================
# PRUEBAS DE INTEGRACIÓN (game_routers.py) - CORREGIDAS
# ==============================================================================
@pytest.mark.asyncio
@patch('routers.game_routers.SetService') 
async def test_router_success(MockSetService, test_client: TestClient):
    """Verifica que el endpoint llame al servicio correctamente y devuelva 200."""
    # 1. Configuración de Mocks
    mock_set_play_result = MockSetPlay(SET_ID, GAME_ID, PLAYER_ID)
    
    mock_set_service_instance = MockSetService.return_value
    mock_set_service_instance.join_detective_to_set = AsyncMock(return_value=mock_set_play_result)
    
    # CORRECCIÓN 1: El payload debe coincidir con DetectiveJoinRequest
    payload = {
        "detective_card_id": DETECTIVE_CARD_ID, 
        "player_id": PLAYER_ID,
        "target_set_id": SET_ID  # <-- Este campo faltaba (Causa del 422)
    }
    
    # 2. Ejecución
    # CORRECCIÓN 2: El método del router es .post(), no .patch()
    response = test_client.post(
        f"/games/{GAME_ID}/set/{SET_ID}/detectives",
        json=payload
    )
    
    # 3. Verificación
    mock_set_service_instance.join_detective_to_set.assert_called_once_with(
        game_id=GAME_ID,
        detective_card_id=DETECTIVE_CARD_ID,
        target_set_id=SET_ID,
        player_id=PLAYER_ID,
    )
    assert response.status_code == status.HTTP_200_OK
    # Asumo que tu objeto MockSetPlay se serializa a un JSON con 'id'
    assert response.json()["id"] == SET_ID


@pytest.mark.asyncio
@patch('routers.game_routers.SetService') 
async def test_router_logic_error_400(MockSetService, test_client: TestClient):
    """Verifica que el endpoint maneje correctamente los errores 400."""
    # 1. Configuración de Mocks
    error_detail = "Detective card does not match the set type"
    
    mock_set_service_instance = MockSetService.return_value
    mock_set_service_instance.join_detective_to_set = AsyncMock(side_effect=badRequestError(error_detail))
    
    # CORRECCIÓN 1: El payload debe coincidir con DetectiveJoinRequest
    payload = {
        "detective_card_id": DETECTIVE_CARD_ID, 
        "player_id": PLAYER_ID,
        "target_set_id": SET_ID  # <-- Este campo faltaba (Causa del 422)
    }
    
    # 2. Ejecución 
    # CORRECCIÓN 2: El método del router es .post(), no .patch()
    response = test_client.post(
        f"/games/{GAME_ID}/set/{SET_ID}/detectives",
        json=payload
    )
            
    # 3. Verificación
    # Asumiendo que tu excepción 'badRequestError' se maneja correctamente
    # y se convierte en un error 400 por FastAPI
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == error_detail