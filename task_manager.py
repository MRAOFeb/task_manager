import json
import os

# Класс задач
class Task:  
    def __init__(self, title, description, 
                category, due_date, priority):
        self.id = None,
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.completed = False

    def to_dict(self):
        return {
            "id": self.id,
            "title" : self.title,
            "description" : self.description,
            "category" : self.category,
            "due_date" : self.due_date,
            "priority" : self.priority,
            "completed" : self.completed
        }

# Класс менеджера задач
class TaskManager: 
    task_file = 'tasks.json'

    def __init__(self):
        self.tasks = self.load_tasks()
        
    # Загрузка задач из файла
    def load_tasks(self):
        tasks = []
        if os.path.exists(self.task_file):
            with open(self.task_file, 'r', encoding='utf-8') as file:
                for _task in json.load(file):
                    task = Task(
                        title = _task["title"],
                        description = _task["description"],
                        category = _task["category"],
                        due_date = _task["due_date"],
                        priority = _task["priority"],
                    )
                    task.id = _task["id"]
                    task.completed = _task["completed"]
                    tasks.append(task)

                
        return tasks

    # Генератор id
    def gen_id(self):
        if len(self.tasks) > 0:
            new_id = self.tasks[-1].id + 1
        else:
            new_id = 1

        return new_id

    # Очистка задач (удаление файла с задачами)
    def clean_tasks(self):
        if os.path.exists(self.task_file):
            os.remove(self.task_file)
        
        print("Все задачи удалены")

    # Сохранение задач
    def save_tasks(self):
        with open(self.task_file, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False)
            

    # Добавление задачи
    def add_task(self, title, description, 
            category, due_date, priority):

        new_task = Task(title, description, category, due_date, priority)
        new_task.id = self.gen_id()

        self.tasks.append(new_task)
        self.save_tasks()

        print(f"Задача '{title}' добавлена.")

    # Вывод задач в консоль
    def view_tasks(self, tasks = None):
        if tasks is None:
            tasks = self.tasks
            
        for task in tasks:
            status = "Выполнена" if task.completed else "Не выполнена"
            print(f"id {task.id}: {task.title} - {status} (Описание: {task.description} Категория: {task.category}, Срок: {task.due_date}, Приоритет: {task.priority})")


    # Изменение задачи
    def edit_task(self, task_id, 
            title = '-', description = '-', 
            category = '-', due_date = '-', 
            priority = '-'):

        for task in self.tasks:
            if task.id == task_id:
                if "-" not in title:
                    task.title = title
                if "-" not in description:
                    task.description = description
                if "-" not in category:
                    task.category = category
                if "-" not in due_date:
                    task.due_date = due_date
                if "-" not in priority:
                    task.priority = priority
                
                self.save_tasks()
                print(f"Задача [{task_id}] изменена")
                return

        print("Задача не найдена")

    # Сохранение задач выполнена/невыполнена
    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                print(f"Задача [{task_id}] отмечена как выполненная")
                return

        print("Задача не найдена")

    # Удаление задачи
    def delete_task(self, task_id):        
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

        print(f"Задача [{task_id}] удалена")

    # Поиск задач
    def search_tasks(self, keyword):
        results = []
        for task in self.tasks:
            if keyword.isdigit():
                if int(keyword) == task.id:
                    results.append(task)
                    continue
            if (keyword.lower() in task.title.lower() 
                    or keyword.lower() in task.description.lower() 
                    or keyword.lower() in task.category.lower() 
                    or keyword.lower() in task.priority.lower()):
                results.append(task)
                continue
            if keyword == task.completed:
                results.append(task)
                continue
            

        return results

# Команды управления
commands = """-----
Команды: 
1 - просмотр всех задач, 
2 - добавить новую задачу,
3 - изменить задачу,
4 - удалить задачу,
5 - найти задачу,
6 - удалить все задачи,
7 - отметь задачу выполненной,
0 - выход из программы
-----"""


if __name__ == "__main__":
    mannager = TaskManager()
    # Обработчик команд
    while(True):
        print(commands)
        command = input()

        if command.isdigit():
            command = int(command)

        else:
            print("Введите номер команды")
            continue
        
        if (command == 0):
            break

        if (command == 1):
            mannager.view_tasks()
            
        elif (command == 2):
            print("Введите через запятую: Название, описание, категорию, срок, приоритет")
            title, description, category, due_date, priority = input().split(',')
            mannager.add_task(title = title, 
                        description = description, due_date = due_date, 
                        category = category, priority = priority)

        elif (command == 3):
            print("Введите id или категорию, ключевые слова, приоритет задачи:")
            keyword = input()
            tasks = mannager.search_tasks(keyword)
            mannager.view_tasks(tasks)

            if len(tasks) > 1:
                flag = True
                while (flag):
                    print("Введите id задачи, которую хотите изменить:")
                    keyword = input()
                    if keyword.isdigit():
                        keyword = int(keyword)
                        for task in tasks:
                            if task.id == keyword:
                                flag = False
                                break
                                
                        else:
                            print(f'Нет задачи с id {keyword}')
                
            elif len(tasks) == 1:
                task = tasks[0]
            
            else:
                continue

            print("Введите через запятую (-, чтобы не менять): Название, описание, категорию, срок, приоритет")
            title, description, category, due_date, priority = input().split(',')
            mannager.edit_task(task.id, title = title, 
                            description = description, due_date = due_date, 
                            category = category, priority = priority)
        
        elif (command == 4):
            print("Введите id или категорию, ключевые слова, приоритет задачи:")
            keyword = input()
            tasks = mannager.search_tasks(keyword)
            mannager.view_tasks(tasks)

            if len(tasks) > 1:
                flag = True
                while (flag):
                    print("Введите id задачи, которую выполнили:")
                    keyword = input()
                    if keyword.isdigit():
                        keyword = int(keyword)
                        for task in tasks:
                            if task.id == keyword:
                                flag = False
                                break
                                
                        else:
                            print(f'Нет задачи с id {keyword}')
                
            elif len(tasks) == 1:
                task = tasks[0]
            
            else:
                continue

            
            mannager.delete_task(task.id)
        
        elif (command == 5):
            print("Введите id или категорию, ключевые слова, приоритет задачи:")
            keyword = input()
            mannager.view_tasks(mannager.search_tasks(keyword))
        
        elif (command == 6):
            print("Точно удалить все задачи? y/n")
            keyword = input()
            if keyword == y:
                mannager.clean_tasks()
            else:
                print("Удаление всех задач отменено")

        elif (command == 7):
            print("Введите id или категорию, ключевые слова, приоритет задачи:")
            keyword = input()
            tasks = mannager.search_tasks(keyword)
            mannager.view_tasks(tasks)

            if len(tasks) > 1:
                flag = True
                while (flag):
                    print("Введите id задачи, которую хотите изменить:")
                    keyword = input()
                    if keyword.isdigit():
                        keyword = int(keyword)
                        for task in tasks:
                            if task.id == keyword:
                                flag = False
                                break
                                
                        else:
                            print(f'Нет задачи с id {keyword}')
                
            elif len(tasks) == 1:
                task = tasks[0]
            
            else:
                continue

            mannager.complete_task(task.id)
    
        else:
            print("Нет такой команды")
        