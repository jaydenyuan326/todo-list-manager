# Todo List Manager with Linked List and Stack
class TaskNode:
    """Linked list node for storing tasks"""
    def __init__(self, description):
        self.description = description  # Store task description
        self.is_done = False   # Task completion status, initially False
        self.next = None

class TaskList:
    """Simple linked list implementation"""
    def __init__(self):
        self.head = None   # Head pointer of the linked list, initially None
    
    def add_task(self, description):
        """Add task to linked list"""
        new_task = TaskNode(description)   # Create new task node
        
        if self.head is None:          # If linked list is empty
            self.head = new_task       # New task becomes head node
        else:
            current = self.head        # Start from head node
            while current.next:        # Traverse to the last node
                current = current.next
            current.next = new_task    # Add new task at the end
        
        print(f"Added: {description}")
    
    def show_tasks(self):
        """Display all tasks by traversing linked list"""
        if self.head is None:                # Check if linked list is empty
            print("No tasks")            
            return
        
        current = self.head
        index = 1
        while current:                          # Traverse all nodes
            status = "✓" if current.is_done else "○"           # Choose symbol based on status
            print(f"{index}. [{status}] {current.description}")
            current = current.next               # Move to next node
            index += 1
    
    def mark_done(self, task_num):
        """Mark a task as completed"""
        current = self.head
        index = 1
        
        while current and index < task_num:      # Find node at specified position
            current = current.next
            index += 1
        
        if current and not current.is_done:           # If found and not done
            current.is_done = True                    # Mark as done
            print(f"Completed: {current.description}")
            return current.description              # Return description for undo
        elif current and current.is_done:
            print("Task already completed!")
        else:
            print("Task not found!")
        return None

    def delete_task(self, task_num):
        """Delete a task from linked list"""
        if self.head is None:                      # Check if linked list is empty
            print("No tasks to delete")
            return None
            
        try:
            if task_num == 1:                     # If deleting head node
                deleted = self.head
                self.head = self.head.next        # Head pointer points to next node
                print(f"Deleted: {deleted.description}")
                return deleted.description
            
            current = self.head
            index = 1
            while current and index < task_num - 1:
                current = current.next
                index += 1
            
            if current and current.next:          # If found the node to delete
                deleted = current.next
                current.next = current.next.next    # Bypass the deleted node
                print(f"Deleted: {deleted.description}")
                return deleted.description
            else:
                print("Task not found!")
                return None
                
        except:
            print("Please enter a valid number")
        return None

class UndoStack:
    """Simple stack for undo functionality"""
    def __init__(self):
        self.actions = []           # Use list as stack storage
    
    def save_action(self, action_type, task_desc):
        """Push action to stack"""
        self.actions.append((action_type, task_desc))  # Push operation
    
    def undo(self):
        """Pop last action from stack"""
        if not self.actions:      # Check if stack is empty
            print("Nothing to undo")
            return None
        return self.actions.pop()   # Pop operation

class TodoApp:
    """Main application class"""
    def __init__(self):
        self.tasks = TaskList()    # Create task linked list
        self.undo_stack = UndoStack() # Create undo stack
    
    def add_task(self):
        """Add new task"""
        desc = input("Enter task: ").strip()
        if desc:
            self.tasks.add_task(desc)     # Add to linked list
            self.undo_stack.save_action("ADD", desc) # Save to undo stack
        else:
            print("Task cannot be empty!")
    
    def show_tasks(self):
        """Display all tasks"""
        print("\nYour Tasks:")
        self.tasks.show_tasks()
    
    def mark_task_done(self):
        """Mark task as completed"""
        self.tasks.show_tasks()     # First display all tasks
        try:
            num = int(input("Enter task number: "))  # Get task number
            task_desc = self.tasks.mark_done(num)    # Mark as done
            if task_desc:
                self.undo_stack.save_action("DONE", task_desc)  # Save action
        except ValueError:
            print("Please enter a valid number")
    
    def delete_task(self):
        """Delete a task"""
        self.tasks.show_tasks()        # Display task list
        try:
            num = int(input("Enter task number to delete: "))
            task_desc = self.tasks.delete_task(num)   # Delete task
            if task_desc:
                self.undo_stack.save_action("DELETE", task_desc) # Save action
        except ValueError:
            print("Please enter a valid number")
    
    def undo_action(self):
        """Undo last action"""
        action = self.undo_stack.undo()        # Get last action from stack
        if action:
            action_type, task_desc = action
            print(f"Undid: {action_type} - {task_desc}")     # Display undo information
    
    def run(self):
        """Main program loop"""
        print("=== Todo App ===")
        print("Uses: Linked List + Stack")
        
        while True:
            print("\n1. Add Task")
            print("2. Show Tasks")
            print("3. Mark Done") 
            print("4. Delete Task")
            print("5. Undo")
            print("6. Exit")
            
            choice = input("Choose: ").strip()    # Get user choice
            
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
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1-6.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()