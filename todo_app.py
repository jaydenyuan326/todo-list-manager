# Enhanced Todo List Manager with Linked List and Stack
class TaskNode:
    """Linked list node for storing tasks"""
    def __init__(self, description):
        self.description = description
        self.is_done = False
        self.priority = "medium"
        self.due_date = None
        self.tags = []
        self.next = None

class TaskList:
    """Enhanced linked list implementation"""
    def __init__(self):
        self.head = None
    
    def add_task(self, description, priority="medium", due_date=None, tags=None):
        """Add task to linked list with enhanced features"""
        new_task = TaskNode(description)
        new_task.priority = priority
        new_task.due_date = due_date
        new_task.tags = tags if tags else []
        
        if self.head is None:
            self.head = new_task
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_task
        
        print(f"Added: {description} (Priority: {priority})")
        return new_task
    
    def show_tasks(self, filter_by=None, search_term=None):
        """Display all tasks with filtering and searching"""
        if self.head is None:
            print("No tasks")
            return
        
        current = self.head
        index = 1
        filtered_count = 0
        
        print("\n" + "="*60)
        print(f"{'No.':<3} {'Status':<6} {'Priority':<8} {'Due Date':<12} {'Description'}")
        print("="*60)
        
        while current:
            # Filter logic
            show_task = True
            if filter_by == "done" and not current.is_done:
                show_task = False
            elif filter_by == "pending" and current.is_done:
                show_task = False
            elif filter_by == "high" and current.priority != "high":
                show_task = False
                
            # Search logic
            if search_term and search_term.lower() not in current.description.lower():
                show_task = False
            
            if show_task:
                status = "✓" if current.is_done else "○"
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(current.priority, "⚪")
                due_display = current.due_date if current.due_date else "No date"
                tags_display = " ".join([f"[{tag}]" for tag in current.tags]) if current.tags else ""
                
                print(f"{index:<3} [{status}]   {priority_icon:<2} {due_display:<12} {current.description} {tags_display}")
                filtered_count += 1
            
            current = current.next
            index += 1
        
        if filtered_count == 0:
            print("No tasks match your criteria")
        else:
            print("="*60)
            print(f"Total: {filtered_count} task(s)")
    
    def mark_done(self, task_num):
        """Mark a task as completed"""
        current = self.head
        index = 1
        
        while current and index < task_num:
            current = current.next
            index += 1
        
        if current and not current.is_done:
            current.is_done = True
            print(f"Completed: {current.description}")
            return current.description
        elif current and current.is_done:
            print("Task already completed!")
        else:
            print("Task not found!")
        return None

    def delete_task(self, task_num):
        """Delete a task from linked list"""
        if self.head is None:
            print("No tasks to delete")
            return None
            
        try:
            if task_num == 1:
                deleted = self.head
                self.head = self.head.next
                print(f"Deleted: {deleted.description}")
                return deleted.description
            
            current = self.head
            index = 1
            while current and index < task_num - 1:
                current = current.next
                index += 1
            
            if current and current.next:
                deleted = current.next
                current.next = current.next.next
                print(f"Deleted: {deleted.description}")
                return deleted.description
            else:
                print("Task not found!")
                return None
                
        except:
            print("Please enter a valid number")
        return None
    
    def get_task_count(self):
        """Get total number of tasks"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def get_completed_count(self):
        """Get number of completed tasks"""
        count = 0
        current = self.head
        while current:
            if current.is_done:
                count += 1
            current = current.next
        return count
    
    def find_overdue_tasks(self):
        """Find overdue tasks"""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        overdue = []
        
        current = self.head
        while current:
            if current.due_date and current.due_date < today and not current.is_done:
                overdue.append(current.description)
            current = current.next
        
        return overdue

    def sort_tasks(self, sort_by="priority"):
        """Sort tasks in the linked list using bubble sort"""
        if self.head is None or self.head.next is None:
            return  # Empty list or single node doesn't need sorting
        
        # Define sort key function
        def get_sort_key(task):
            if sort_by == "priority":
                priority_weights = {"high": 3, "medium": 2, "low": 1}
                return priority_weights.get(task.priority, 0)
            elif sort_by == "due_date":
                return task.due_date if task.due_date else "9999-99-99"
            elif sort_by == "description":
                return task.description.lower()
            return 0
        
        # Bubble sort implementation
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current and current.next:
                current_key = get_sort_key(current)
                next_key = get_sort_key(current.next)
                
                # Sort in descending order for priority, ascending for others
                if sort_by == "priority":
                    if current_key < next_key:
                        self._swap_node_data(current, current.next)
                        swapped = True
                else:
                    if current_key > next_key:
                        self._swap_node_data(current, current.next)
                        swapped = True
            
                current = current.next

    def _swap_node_data(self, node1, node2):
        """Swap data between two nodes"""
        node1.description, node2.description = node2.description, node1.description
        node1.is_done, node2.is_done = node2.is_done, node1.is_done
        node1.priority, node2.priority = node2.priority, node1.priority
        node1.due_date, node2.due_date = node2.due_date, node1.due_date
        node1.tags, node2.tags = node2.tags, node1.tags

class EnhancedUndoStack:
    """Enhanced stack for undo/redo functionality"""
    def __init__(self):
        self.undo_actions = []
        self.redo_actions = []
        self.max_size = 10
    
    def save_action(self, action_type, task_desc, task_data=None):
        """Push action to stack with task data"""
        action = {
            'type': action_type,
            'description': task_desc,
            'data': task_data,
            'timestamp': self._get_timestamp()
        }
        
        self.undo_actions.append(action)
        self.redo_actions.clear()  # Clear redo stack on new action
        
        # Maintain stack size
        if len(self.undo_actions) > self.max_size:
            self.undo_actions.pop(0)
    
    def undo(self):
        """Pop last action from undo stack to redo stack"""
        if not self.undo_actions:
            print("Nothing to undo")
            return None
        
        action = self.undo_actions.pop()
        self.redo_actions.append(action)
        
        # Maintain redo stack size
        if len(self.redo_actions) > self.max_size:
            self.redo_actions.pop(0)
            
        return action
    
    def redo(self):
        """Pop last action from redo stack back to undo stack"""
        if not self.redo_actions:
            print("Nothing to redo")
            return None
        
        action = self.redo_actions.pop()
        self.undo_actions.append(action)
        return action
    
    def show_history(self):
        """Display undo history"""
        if not self.undo_actions:
            print("No actions in history")
            return
        
        print("\nUndo History:")
        for i, action in enumerate(reversed(self.undo_actions), 1):
            print(f"{i}. {action['type']} - {action['description']} ({action['timestamp']})")
    
    def show_redo_history(self):
        """Display redo history"""
        if not self.redo_actions:
            print("No actions to redo")
            return
        
        print("\nRedo History:")
        for i, action in enumerate(reversed(self.redo_actions), 1):
            print(f"{i}. {action['type']} - {action['description']}")

    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

class Project:
    """Project class for organizing tasks"""
    def __init__(self, name):
        self.name = name
        self.tasks = TaskList()

class ProjectManager:
    """Manager for multiple projects"""
    def __init__(self):
        self.projects = {}
        self.current_project = "default"
        self.projects["default"] = Project("default")
    
    def create_project(self, project_name):
        """Create a new project"""
        if project_name in self.projects:
            print(f"Project '{project_name}' already exists")
            return False
        
        self.projects[project_name] = Project(project_name)
        print(f"Project '{project_name}' created")
        return True
    
    def switch_project(self, project_name):
        """Switch to a different project"""
        if project_name not in self.projects:
            print(f"Project '{project_name}' not found")
            return False
        
        self.current_project = project_name
        print(f"Switched to project: {project_name}")
        return True
    
    def list_projects(self):
        """List all projects"""
        if not self.projects:
            print("No projects available")
            return
        
        print("\nProjects:")
        for i, project_name in enumerate(self.projects.keys(), 1):
            task_count = self.projects[project_name].tasks.get_task_count()
            current_indicator = " (current)" if project_name == self.current_project else ""
            print(f"{i}. {project_name} - {task_count} tasks{current_indicator}")
    
    def get_current_tasks(self):
        """Get task list of current project"""
        return self.projects[self.current_project].tasks
    
    def delete_project(self, project_name):
        """Delete a project"""
        if project_name not in self.projects:
            print(f"Project '{project_name}' not found")
            return False
        
        if project_name == "default":
            print("Cannot delete default project")
            return False
        
        if self.current_project == project_name:
            self.current_project = "default"
        
        del self.projects[project_name]
        print(f"Project '{project_name}' deleted")
        return True

import json
import os

class DataManager:
    """Manager for data persistence"""
    def __init__(self, project_manager, undo_stack):
        self.project_manager = project_manager
        self.undo_stack = undo_stack
        self.data_file = "todo_data.json"
    
    def save_to_file(self):
        """Save all data to JSON file"""
        data = {
            'projects': self._serialize_projects(),
            'current_project': self.project_manager.current_project,
            'undo_history': self.undo_stack.undo_actions,
            'redo_history': self.undo_stack.redo_actions
        }
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_from_file(self):
        """Load data from JSON file"""
        if not os.path.exists(self.data_file):
            print("No saved data found")
            return False
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Rebuild projects
            self.project_manager.projects.clear()
            for project_name, project_data in data.get('projects', {}).items():
                self.project_manager.projects[project_name] = Project(project_name)
                for task_data in project_data.get('tasks', []):
                    self.project_manager.projects[project_name].tasks.add_task(
                        task_data['description'],
                        task_data.get('priority', 'medium'),
                        task_data.get('due_date'),
                        task_data.get('tags', [])
                    )
                    # Restore completion status
                    if task_data.get('is_done', False):
                        current = self.project_manager.projects[project_name].tasks.head
                        while current and current.next:
                            current = current.next
                        if current:
                            current.is_done = True
            
            # Restore current project and history
            self.project_manager.current_project = data.get('current_project', 'default')
            self.undo_stack.undo_actions = data.get('undo_history', [])
            self.undo_stack.redo_actions = data.get('redo_history', [])
            
            print(f"Data loaded from {self.data_file}")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _serialize_projects(self):
        """Serialize all projects to dictionary"""
        projects_data = {}
        for project_name, project in self.project_manager.projects.items():
            tasks_data = []
            current = project.tasks.head
            while current:
                tasks_data.append({
                    'description': current.description,
                    'is_done': current.is_done,
                    'priority': current.priority,
                    'due_date': current.due_date,
                    'tags': current.tags
                })
                current = current.next
            projects_data[project_name] = {'tasks': tasks_data}
        return projects_data

class TodoApp:
    """Enhanced main application class"""
    def __init__(self):
        self.project_manager = ProjectManager()
        self.undo_stack = EnhancedUndoStack()
        self.data_manager = DataManager(self.project_manager, self.undo_stack)
    
    def get_current_tasks(self):
        """Get current project's task list"""
        return self.project_manager.get_current_tasks()
    
    def show_statistics(self):
        """Display task statistics"""
        tasks = self.get_current_tasks()
        total = tasks.get_task_count()
        completed = tasks.get_completed_count()
        pending = total - completed
        overdue = len(tasks.find_overdue_tasks())
        
        print("\n" + "="*40)
        print("TASK STATISTICS")
        print("="*40)
        print(f"Total Tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        print(f"Overdue: {overdue}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Completion Rate: {completion_rate:.1f}%")
        
        overdue_tasks = tasks.find_overdue_tasks()
        if overdue_tasks:
            print(f"\n🚨 Overdue Tasks: {len(overdue_tasks)}")
            for task in overdue_tasks:
                print(f"   - {task}")
    
    def add_task(self):
        """Add new task with enhanced features"""
        desc = input("Enter task: ").strip()
        if not desc:
            print("Task cannot be empty!")
            return
        
        print("\nPriority levels:")
        print("1. High 🔴")
        print("2. Medium 🟡") 
        print("3. Low 🟢")
        priority_choice = input("Choose priority (1-3, default 2): ").strip()
        priority_map = {"1": "high", "2": "medium", "3": "low"}
        priority = priority_map.get(priority_choice, "medium")
        
        due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
        if not due_date:
            due_date = None
        
        tags_input = input("Tags (comma separated, optional): ").strip()
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
        
        task_data = {
            'description': desc,
            'priority': priority,
            'due_date': due_date,
            'tags': tags
        }
        
        task = self.get_current_tasks().add_task(desc, priority, due_date, tags)
        self.undo_stack.save_action("ADD", desc, task_data)
    
    def show_tasks(self):
        """Display tasks with filtering options"""
        print("\nFilter options:")
        print("1. All tasks")
        print("2. Pending tasks") 
        print("3. Completed tasks")
        print("4. High priority tasks")
        print("5. Search tasks")
        
        choice = input("Choose filter (1-5): ").strip()
        
        filter_map = {
            "1": None,
            "2": "pending", 
            "3": "done",
            "4": "high"
        }
        
        search_term = None
        if choice == "5":
            search_term = input("Enter search term: ").strip()
            filter_by = None
        else:
            filter_by = filter_map.get(choice)
        
        self.get_current_tasks().show_tasks(filter_by, search_term)
    
    def mark_task_done(self):
        """Mark task as completed"""
        self.get_current_tasks().show_tasks("pending")
        try:
            num = int(input("Enter task number: "))
            task_desc = self.get_current_tasks().mark_done(num)
            if task_desc:
                self.undo_stack.save_action("DONE", task_desc)
        except ValueError:
            print("Please enter a valid number")
    
    def delete_task(self):
        """Delete a task"""
        self.get_current_tasks().show_tasks()
        try:
            num = int(input("Enter task number to delete: "))
            # Save task info first for potential recovery
            current = self.get_current_tasks().head
            index = 1
            task_data = None
            while current and index <= num:
                if index == num:
                    task_data = {
                        'description': current.description,
                        'priority': current.priority,
                        'due_date': current.due_date,
                        'tags': current.tags,
                        'is_done': current.is_done
                    }
                    break
                current = current.next
                index += 1
                
            task_desc = self.get_current_tasks().delete_task(num)
            if task_desc:
                self.undo_stack.save_action("DELETE", task_desc, task_data)
        except ValueError:
            print("Please enter a valid number")
    
    def undo_action(self):
        """Enhanced undo functionality"""
        action = self.undo_stack.undo()
        if action:
            action_type, task_desc = action['type'], action['description']
            print(f"Undid: {action_type} - {task_desc}")
            
            if action_type == "DELETE" and action['data']:
                print(f"Note: To fully restore '{task_desc}', use the add task function.")
    
    def redo_action(self):
        """Redo functionality"""
        action = self.undo_stack.redo()
        if action:
            action_type, task_desc = action['type'], action['description']
            print(f"Redid: {action_type} - {task_desc}")
            
            if action_type == "DELETE" and action['data']:
                print(f"Note: To fully restore '{task_desc}', use the add task function.")
    
    def show_kanban_view(self):
        """Simple kanban-style view using linked list"""
        tasks = self.get_current_tasks()
        if tasks.head is None:
            print("No tasks to display")
            return
        
        columns = {
            "TODO": [],
            "IN PROGRESS": [],
            "DONE": []
        }
        
        current = tasks.head
        while current:
            if current.is_done:
                columns["DONE"].append(current)
            elif current.priority == "high":
                columns["IN PROGRESS"].append(current)
            else:
                columns["TODO"].append(current)
            current = current.next
        
        print("\n" + "="*80)
        print("KANBAN VIEW")
        print("="*80)
        
        for column_name, tasks in columns.items():
            print(f"\n{column_name} ({len(tasks)} tasks)")
            print("-" * 40)
            
            for task in tasks:
                status = "✓" if task.is_done else "○"
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
                print(f" [{status}] {priority_icon} {task.description}")
    
    def sort_tasks(self):
        """Sort tasks in current project"""
        print("\nSort options:")
        print("1. By Priority (High to Low)")
        print("2. By Due Date (Earliest first)")
        print("3. By Description (A-Z)")
        
        choice = input("Choose sort method (1-3): ").strip()
        sort_methods = {"1": "priority", "2": "due_date", "3": "description"}
        
        if choice in sort_methods:
            self.get_current_tasks().sort_tasks(sort_methods[choice])
            print(f"Tasks sorted by {sort_methods[choice]}")
        else:
            print("Invalid choice!")
    
    def project_management(self):
        """Manage projects"""
        while True:
            print(f"\nCurrent Project: {self.project_manager.current_project}")
            print("1. List Projects")
            print("2. Create Project")
            print("3. Switch Project")
            print("4. Delete Project")
            print("5. Back to Main Menu")
            
            choice = input("Choose (1-5): ").strip()
            
            if choice == '1':
                self.project_manager.list_projects()
            elif choice == '2':
                project_name = input("Enter project name: ").strip()
                if project_name:
                    self.project_manager.create_project(project_name)
                else:
                    print("Project name cannot be empty")
            elif choice == '3':
                project_name = input("Enter project name to switch to: ").strip()
                if project_name:
                    self.project_manager.switch_project(project_name)
                else:
                    print("Project name cannot be empty")
            elif choice == '4':
                project_name = input("Enter project name to delete: ").strip()
                if project_name:
                    self.project_manager.delete_project(project_name)
                else:
                    print("Project name cannot be empty")
            elif choice == '5':
                break
            else:
                print("Invalid choice!")
    
    def run(self):
        """Enhanced main program loop"""
        print("=== Enhanced Todo App ===")
        print("Uses: Linked List + Stack + Enhanced Features")
        
        # Auto-load data on startup
        self.data_manager.load_from_file()
        
        while True:
            print(f"\nCurrent Project: {self.project_manager.current_project}")
            print("1. Add Task")
            print("2. Show Tasks")
            print("3. Mark Done") 
            print("4. Delete Task")
            print("5. Undo")
            print("6. Redo")
            print("7. Statistics")
            print("8. Kanban View")
            print("9. Sort Tasks")
            print("10. Project Management")
            print("11. Save Data")
            print("12. Undo History")
            print("13. Redo History")
            print("14. Exit")
            
            choice = input("Choose (1-14): ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.show_tasks()
            elif choice == '3':
                self.mark_task_done()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.undo_action()
            elif choice == '6':
                self.redo_action()
            elif choice == '7':
                self.show_statistics()
            elif choice == '8':
                self.show_kanban_view()
            elif choice == '9':
                self.sort_tasks()
            elif choice == '10':
                self.project_management()
            elif choice == '11':
                self.data_manager.save_to_file()
            elif choice == '12':
                self.undo_stack.show_history()
            elif choice == '13':
                self.undo_stack.show_redo_history()
            elif choice == '14':
                self.data_manager.save_to_file()  # Auto-save on exit
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1-14.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()