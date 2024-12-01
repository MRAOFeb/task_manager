import os
import pytest
from task_manager import Task, TaskManager


@pytest.fixture
def task_manager():
    if os.path.exists(TaskManager.task_file):
        os.remove(TaskManager.task_file)
    manager = TaskManager()
    return manager

# Тест на добавление
def test_add_task(task_manager):
    task_manager.add_task("Тестовая задача", "Описание задачи", 
                        "Работа", "2024-01-30", "Высокий")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Тестовая задача"

# Тест на изменение
def test_edit_task(task_manager):
    task_manager.add_task("Редактируемая задача", "Описание", 
                        "Категория", "Время", "Средний")
    task_id = task_manager.tasks[0].id
    
    task_manager.edit_task(task_id, title="Измененная задача")
    
    assert task_manager.tasks[0].title == "Измененная задача"

# Тест на изменение выполнена/невыполнена
def test_complete_task(task_manager):
    task_manager.add_task("Задача для выполнения", "Описание", 
                        "Категория", "Время", "Высокий")
    task_id = task_manager.tasks[0].id
    
    task_manager.complete_task(task_id)
    
    assert task_manager.tasks[0].completed is True

# Тест на удаление
def test_delete_task(task_manager):
    task_manager.add_task("Задача для удаления", "Описание", 
                        "Категория", "Время", "Низкий")
    task_manager.add_task("Задача для заполнения", "Описание", 
                        "Категория", "Время", "Низкий")
    task_id = task_manager.tasks[0].id
    
    task_manager.delete_task(task_id)
    
    assert len(task_manager.tasks) == 1

# Тест на поиск
def test_search_tasks(task_manager):
    task_manager.add_task("Первая задача", "Описание 1", "Категория", "", "Низкий")
    task_manager.add_task("Вторая задача", "Описание 2", "Категория", "", "Средний")
    
    found_tasks = task_manager.search_tasks(keyword="Первая")
    
    assert len(found_tasks) == 1
    assert found_tasks[0].title == "Первая задача"