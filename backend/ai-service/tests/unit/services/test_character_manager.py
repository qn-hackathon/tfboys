"""
测试角色管理服务
"""
import pytest
from unittest.mock import patch, AsyncMock
from app.services.character_manager import CharacterManager
from shared.models.scene import Scene, Character


@pytest.mark.unit
class TestCharacterManager:
    @pytest.fixture
    def character_manager(self):
        """创建CharacterManager实例"""
        return CharacterManager()
    
    @pytest.mark.asyncio
    async def test_process_characters_new_characters(
        self, character_manager, mock_redis_client, mock_local_storage_client, mock_openai_client, mock_httpx_client
    ):
        """测试处理新角色"""
        scenes = [
            Scene(
                scene_id="scene_001",
                scene_index=0,
                description="测试场景",
                narration="测试旁白",
                characters=[
                    Character(
                        character_id="temp_1",
                        name="小明",
                        description="黑发少年"
                    ),
                    Character(
                        character_id="temp_2",
                        name="小红",
                        description="红发少女"
                    )
                ]
            ),
            Scene(
                scene_id="scene_002",
                scene_index=1,
                description="测试场景2",
                narration="测试旁白2",
                characters=[
                    Character(
                        character_id="temp_1",
                        name="小明",
                        description="黑发少年"
                    )
                ]
            )
        ]
        
        with patch('shared.clients.redis_client', mock_redis_client), \
             patch('shared.clients.local_storage_client', mock_local_storage_client), \
             patch('app.services.image_generator.AsyncOpenAI', return_value=mock_openai_client), \
             patch('httpx.AsyncClient') as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = mock_httpx_client
            
            characters = await character_manager.process_characters("test_task", scenes)
        
        assert len(characters) == 2
        assert "小明" in characters
        assert "小红" in characters
        assert mock_redis_client.save_character.call_count == 2
        assert mock_redis_client.add_task_character.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_or_create_character_existing(
        self, character_manager, mock_redis_client, sample_character_data
    ):
        """测试获取已存在的角色"""
        mock_redis_client.get_character = AsyncMock(return_value=sample_character_data)
        
        with patch('shared.clients.redis_client', mock_redis_client):
            character = await character_manager.get_or_create_character(
                character_name="小明",
                character_desc="黑发少年",
                task_id="test_task"
            )
        
        assert character.name == "小明"
        assert character.description == sample_character_data["description"]
        mock_redis_client.save_character.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_or_create_character_new(
        self, character_manager, mock_redis_client, mock_local_storage_client, mock_openai_client, mock_httpx_client
    ):
        """测试创建新角色"""
        mock_redis_client.get_character = AsyncMock(return_value=None)
        
        with patch('shared.clients.redis_client', mock_redis_client), \
             patch('shared.clients.local_storage_client', mock_local_storage_client), \
             patch('app.services.image_generator.AsyncOpenAI', return_value=mock_openai_client), \
             patch('httpx.AsyncClient') as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = mock_httpx_client
            
            character = await character_manager.get_or_create_character(
                character_name="新角色",
                character_desc="新角色描述",
                task_id="test_task"
            )
        
        assert character.name == "新角色"
        assert character.description == "新角色描述"
        mock_redis_client.save_character.assert_called_once()
        mock_redis_client.add_task_character.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_character_references(self, character_manager, mock_redis_client, sample_character_data):
        """测试批量获取角色引用"""
        mock_redis_client.get_character = AsyncMock(return_value=sample_character_data)
        
        with patch('shared.clients.redis_client', mock_redis_client):
            references = await character_manager.get_character_references(["小明", "小红"])
        
        assert len(references) == 2
        assert "小明" in references
    
    @pytest.mark.asyncio
    async def test_get_character_references_empty(self, character_manager):
        """测试空角色列表"""
        references = await character_manager.get_character_references([])
        
        assert references == {}
    
    def test_generate_character_id(self, character_manager):
        """测试角色ID生成"""
        char_id_1 = character_manager.generate_character_id("小明")
        char_id_2 = character_manager.generate_character_id("小明")
        char_id_3 = character_manager.generate_character_id("小红")
        
        assert char_id_1 == char_id_2
        assert char_id_1 != char_id_3
        assert char_id_1.startswith("char_")
    
    @pytest.mark.asyncio
    async def test_get_character_by_name(self, character_manager, mock_redis_client, sample_character_data):
        """测试根据名称获取角色"""
        mock_redis_client.get_character = AsyncMock(return_value=sample_character_data)
        
        with patch('shared.clients.redis_client', mock_redis_client):
            character = await character_manager.get_character_by_name("小明")
        
        assert character is not None
        assert character.name == "小明"
    
    @pytest.mark.asyncio
    async def test_get_character_by_name_not_found(self, character_manager, mock_redis_client):
        """测试获取不存在的角色"""
        mock_redis_client.get_character = AsyncMock(return_value=None)
        
        with patch('shared.clients.redis_client', mock_redis_client):
            character = await character_manager.get_character_by_name("不存在")
        
        assert character is None
    
    @pytest.mark.asyncio
    async def test_list_task_characters(self, character_manager, mock_redis_client, sample_character_data):
        """测试获取任务的所有角色"""
        mock_redis_client.list_task_characters = AsyncMock(return_value=["char_1", "char_2"])
        mock_redis_client.get_character = AsyncMock(return_value=sample_character_data)
        
        with patch('shared.clients.redis_client', mock_redis_client):
            characters = await character_manager.list_task_characters("test_task")
        
        assert len(characters) == 2
        assert all(isinstance(c, Character) for c in characters)
