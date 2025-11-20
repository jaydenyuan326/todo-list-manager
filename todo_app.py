#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Todo List Manager
--------------------------
A portfolio-ready Data Structures project featuring:
1. Doubly Linked List (Custom Implementation)
2. Merge Sort Algorithm (O(n log n))
3. Stack-based Undo/Redo (Command Pattern)
4. JSON Persistence
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any

# ==========================================
# 1. DATA STRUCTURES: Doubly Linked List
# ==========================================

class TaskNode:
    """
    Doubly Linked List Node.
    Contains pointers to both next and previous nodes.
    """
    def __init__(self, description: str):
        self.description = description
        self.is_done = False
        self.priority = "medium"  # low, medium, high
        self.due_date: Optional[str] = None
        self.tags: List[str] = []
        
        # Pointers
        self.next: Optional['TaskNode'] = None
        self.prev: Optional['TaskNode'] = None

class TaskList:
    """
    Doubly Linked List implementation with Merge Sort.
    """
    def __init__(self):
        self.head: Optional[TaskNode] = None
        self.count = 0  # Optimization: Track size for O(1) access
    
    def add_task(self, description: str, priority="medium", due_date=None, tags=None) -> TaskNode:
        """Appends task to the end of the list (O(n))."""
        new_task = TaskNode(description)
        new_task.priority = priority
        new_task.due_date = due_date
        new_task.tags = tags if tags else []
        
        if self.head is None:
            self.head = new_task
        else:
            # Traverse to the end
            current = self.head
            while current.next:
                current = current.next
            
            # DLL Linkage
            current.next = new_task
            new_task.prev = current
        
        self.count += 1
        print(f"✅ Added: {description}")
        return new_task
    
    def delete_task_by_index(self, index: int) -> Optional[str]:
        """Deletes node by 1-based index using DLL logic."""
        if self.head is None or index < 1:
            return None
        
        current = self.head
        curr_idx = 1
        
        # Find the node
        while current and curr_idx < index:
            current = current.next
            curr_idx += 1
        
        if not current:
            return None # Index out of bounds
            
        deleted_desc = current.description
        
        # DLL Unlinking Logic
        if current == self.head:
            # Deleting head
            self.head = current.next
            if self.head:
                self.head.prev = None
        else:
            # Deleting middle or tail
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
                
        self.count -= 1
        print(f"🗑️  Deleted: {deleted_desc}")
        return deleted_desc

    # --- Merge Sort Implementation (O(n log n)) ---

    def sort_tasks(self, sort_by="priority"):
        """
        Entry point for Merge Sort.
        Sorts the list and rebuilds 'prev' pointers to maintain DLL integrity.
        """
        if self.head is None or self.head.next is None:
            return

        # Perform recursive merge sort (returns a sorted list with valid .next pointers)
        self.head = self._merge_sort(self.head, sort_by)
        
        # Repair 'prev' pointers after sort (Merge sort logic usually handles next only)
        current = self.head
        current.prev = None # Head has no prev
        while current.next:
            current.next.prev = current
            current = current.next

    def _merge_sort(self, head: TaskNode, sort_by: str) -> TaskNode:
        # Base case: if head is None or there is only one element
        if head is None or head.next is None:
            return head

        # 1. Split head into 'left' and 'right' sublists
        middle = self._get_middle(head)
        next_to_middle = middle.next
        middle.next = None # Break the link

        # 2. Recursively sort the sublists
        left = self._merge_sort(head, sort_by)
        right = self._merge_sort(next_to_middle, sort_by)

        # 3. Merge the sorted sublists
        sorted_list = self._sorted_merge(left, right, sort_by)
        return sorted_list

    def _sorted_merge(self, a: TaskNode, b: TaskNode, sort_by: str) -> TaskNode:
        if a is None: return b
        if b is None: return a

        # Comparison Logic
        val_a = self._get_sort_val(a, sort_by)
        val_b = self._get_sort_val(b, sort_by)
        
        result = None
        
        # Priority: Lower value = Higher priority (0 is High)
        # Dates/Strings: Standard comparison
        if val_a <= val_b:
            result = a
            result.next = self._sorted_merge(a.next, b, sort_by)
        else:
            result = b
            result.next = self._sorted_merge(a, b.next, sort_by)
        
        return result

    def _get_middle(self, head: TaskNode) -> TaskNode:
        # Slow/Fast pointer technique
        if head is None: return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def _get_sort_val(self, node: TaskNode, sort_by: str):
        if sort_by == "priority": 
            # Mapping: High=0 (First), Medium=1, Low=2
            return {"high": 0, "medium": 1, "low": 2}.get(node.priority, 3)
        if sort_by == "due_date": 
            return node.due_date if node.due_date else "9999-99-99"
        return node.description.lower()

    # --- Helper Methods for Undo/Redo ---

    def remove_last_node(self):
        """Removes the tail node (Undo Add)."""
        if self.head is None: return
        
        if self.head.next is None:
            self.head = None
        else:
            current = self.head
            while current.next:
                current = current.next
            # current is now tail
            if current.prev:
                current.prev.next = None
        self.count -= 1

    def delete_by_desc(self, description: str):
        """Deletes first occurrence by description (Redo Delete)."""
        current = self.head
        while current:
            if current.description == description:
                # Unlink
                if current == self.head:
                    self.head = current.next
                    if self.head: self.head.prev = None
                else:
                    if current.prev: current.prev.next = current.next
                    if current.next: current.next.prev = current.prev
                self.count -= 1
                return
            current = current.next

    def set_status_by_desc(self, description: str, status: bool):
        """Toggles completion status."""
        current = self.head
        while current:
            if current.description == description:
                current.is_done = status
                return
            current = current.next

    # --- Display & Utilities ---

    def show_tasks(self, filter_by=None, search_term=None):
        if self.head is None:
            print("\n📭 No tasks found.")
            return
        
        print("\n" + "─"*75)
        print(f"{'#':<4} {'Done':<6} {'Pri':<8} {'Due':<12} {'Task & Tags'}")
        print("─"*75)
        
        current = self.head
        index = 1
        
        while current:
            show = True
            # Filter Logic
            if filter_by == "done" and not current.is_done: show = False
            elif filter_by == "pending" and current.is_done: show = False
            elif filter_by == "high" and current.priority != "high": show = False
            if search_term and search_term.lower() not in current.description.lower(): show = False
            
            if show:
                status = "✓" if current.is_done else " "
                p_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                p_icon = p_map.get(current.priority, "⚪")
                tags = f"[{', '.join(current.tags)}]" if current.tags else ""
                due = current.due_date if current.due_date else "-"
                
                print(f"{index:<4} [{status:<1}]   {p_icon:<8} {due:<12} {current.description} {tags}")
            
            current = current.next
            index += 1
        print("─"*75)

    def mark_done_by_index(self, index: int) -> Optional[str]:
        current = self.head
        curr_idx = 1
        while current and curr_idx < index:
            current = current.next
            curr_idx += 1
        
        if current:
            current.is_done = True
            print(f"🎉 Completed: {current.description}")
            return current.description
        return None

    def get_stats(self):
        done = 0
        overdue = 0
        today = datetime.now().strftime("%Y-%m-%d")
        current = self.head
        while current:
            if current.is_done: done += 1
            if current.due_date and current.due_date < today and not current.is_done:
                overdue += 1
            current = current.next
        return done, self.count, overdue

# ==========================================
# 2. STACK: Command Pattern Undo/Redo
# ==========================================

class EnhancedUndoStack:
    def __init__(self):
        self.undo_stack: List[Dict] = []
        self.redo_stack: List[Dict] = []
        self.max_size = 15
    
    def push_action(self, action_type: str, desc: str, data: Any = None):
        action = {
            'type': action_type,
            'desc': desc,
            'data': data,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        self.undo_stack.append(action)
        self.redo_stack.clear()
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)
            
    def pop_undo(self) -> Optional[Dict]:
        if not self.undo_stack: return None
        action = self.undo_stack.pop()
        self.redo_stack.append(action)
        return action
        
    def pop_redo(self) -> Optional[Dict]:
        if not self.redo_stack: return None
        action = self.redo_stack.pop()
        self.undo_stack.append(action)
        return action

# ==========================================
# 3. DATA PERSISTENCE & PROJECT MGT
# ==========================================

class ProjectManager:
    def __init__(self):
        self.projects = {"Main": TaskList()}
        self.current_name = "Main"
    
    def get_current_list(self) -> TaskList:
        return self.projects[self.current_name]
    
    def create_project(self, name: str):
        if name and name not in self.projects:
            self.projects[name] = TaskList()
            print(f"Project '{name}' created.")
    
    def switch_project(self, name: str):
        if name in self.projects:
            self.current_name = name
            print(f"Switched to '{name}'.")

class DataManager:
    FILE_NAME = "todo_data.json"

    @staticmethod
    def save(pm: ProjectManager, stack: EnhancedUndoStack):
        data = {
            "projects": {},
            "current_project": pm.current_name,
            "undo_history": stack.undo_stack
        }
        
        for name, task_list in pm.projects.items():
            tasks = []
            curr = task_list.head
            while curr:
                tasks.append({
                    "desc": curr.description,
                    "done": curr.is_done,
                    "pri": curr.priority,
                    "due": curr.due_date,
                    "tags": curr.tags
                })
                curr = curr.next
            data["projects"][name] = tasks
            
        try:
            with open(DataManager.FILE_NAME, 'w') as f:
                json.dump(data, f, indent=2)
            print("\n💾 Data saved successfully.")
        except Exception as e:
            print(f"Error saving: {e}")

    @staticmethod
    def load(pm: ProjectManager, stack: EnhancedUndoStack):
        if not os.path.exists(DataManager.FILE_NAME): return
        
        try:
            with open(DataManager.FILE_NAME, 'r') as f:
                data = json.load(f)
                
            pm.projects.clear()
            for name, tasks in data["projects"].items():
                new_list = TaskList()
                for t in tasks:
                    node = new_list.add_task(t["desc"], t["pri"], t["due"], t["tags"])
                    node.is_done = t["done"]
                pm.projects[name] = new_list
                
            pm.current_name = data.get("current_project", "Main")
            stack.undo_stack = data.get("undo_history", [])
            print("📂 Previous session loaded.")
        except Exception as e:
            print(f"Error loading: {e}")

# ==========================================
# 4. MAIN APPLICATION CONTROLLER
# ==========================================

class TodoApp:
    def __init__(self):
        self.pm = ProjectManager()
        self.stack = EnhancedUndoStack()
        
    def start(self):
        print("\n" + "="*45)
        print("   🚀 ADVANCED TODO LIST MANAGER")
        print("   (DLL | Merge Sort | Stack | JSON)")
        print("="*45)
        
        DataManager.load(self.pm, self.stack)
        
        while True:
            self._print_menu()
            choice = input("👉 Select option: ").strip()
            
            if choice == '1': self._add_task()
            elif choice == '2': self.pm.get_current_list().show_tasks()
            elif choice == '3': self._complete_task()
            elif choice == '4': self._delete_task()
            elif choice == '5': self._handle_undo()
            elif choice == '6': self._handle_redo()
            elif choice == '7': self._show_dashboard()
            elif choice == '8': 
                print("\nSorting using Merge Sort (O(n log n))...")
                self.pm.get_current_list().sort_tasks("priority")
                self.pm.get_current_list().show_tasks()
            elif choice == '9': self._manage_projects()
            elif choice == '0': 
                DataManager.save(self.pm, self.stack)
                print("Goodbye! 👋")
                break
            else:
                print("Invalid option.")

    def _print_menu(self):
        proj = self.pm.current_name
        count = self.pm.get_current_list().count
        print(f"\n[ Project: {proj} | Tasks: {count} ]")
        print("1. Add Task      2. List Tasks    3. Complete Task")
        print("4. Delete Task   5. Undo          6. Redo")
        print("7. Dashboard     8. Sort (Merge)  9. Projects")
        print("0. Save & Exit")

    def _add_task(self):
        desc = input("Task: ").strip()
        if not desc: return
        
        pri = input("Priority (h/m/l): ").strip().lower()
        pri_map = {'h': 'high', 'm': 'medium', 'l': 'low'}
        
        due = input("Due (YYYY-MM-DD): ").strip()
        tags = input("Tags (comma sep): ").strip().split(",") if input else []
        tags = [t.strip() for t in tags if t.strip()]
        
        task_data = {'desc': desc, 'pri': pri_map.get(pri, 'medium'), 'due': due, 'tags': tags}
        
        self.pm.get_current_list().add_task(task_data['desc'], task_data['pri'], task_data['due'], task_data['tags'])
        self.stack.push_action("ADD", desc, task_data)

    def _delete_task(self):
        self.pm.get_current_list().show_tasks()
        try:
            idx = int(input("Delete # "))
            # Find data first for Undo
            tasks = self.pm.get_current_list()
            curr = tasks.head
            c_idx = 1
            saved_data = None
            
            while curr:
                if c_idx == idx:
                    saved_data = {
                        'desc': curr.description,
                        'pri': curr.priority,
                        'due': curr.due_date,
                        'tags': curr.tags,
                        'done': curr.is_done
                    }
                    break
                curr = curr.next
                c_idx += 1
            
            deleted = tasks.delete_task_by_index(idx)
            if deleted and saved_data:
                self.stack.push_action("DELETE", deleted, saved_data)
        except ValueError:
            print("Invalid number.")

    def _complete_task(self):
        self.pm.get_current_list().show_tasks("pending")
        try:
            idx = int(input("Complete # "))
            desc = self.pm.get_current_list().mark_done_by_index(idx)
            if desc:
                self.stack.push_action("DONE", desc)
        except ValueError:
            pass

    def _handle_undo(self):
        action = self.stack.pop_undo()
        if not action: return print("Nothing to undo.")
        
        typ, desc, data = action['type'], action['desc'], action['data']
        tasks = self.pm.get_current_list()
        
        print(f"↩️  Undoing {typ}...")
        if typ == "ADD": tasks.remove_last_node()
        elif typ == "DELETE": 
            t = tasks.add_task(data['desc'], data['pri'], data['due'], data['tags'])
            t.is_done = data['done']
        elif typ == "DONE": tasks.set_status_by_desc(desc, False)

    def _handle_redo(self):
        action = self.stack.pop_redo()
        if not action: return print("Nothing to redo.")
        
        typ, desc, data = action['type'], action['desc'], action['data']
        tasks = self.pm.get_current_list()
        
        print(f"↪️  Redoing {typ}...")
        if typ == "ADD": tasks.add_task(data['desc'], data['pri'], data['due'], data['tags'])
        elif typ == "DELETE": tasks.delete_by_desc(desc)
        elif typ == "DONE": tasks.set_status_by_desc(desc, True)

    def _show_dashboard(self):
        done, total, overdue = self.pm.get_current_list().get_stats()
        rate = (done/total*100) if total > 0 else 0
        print(f"\n📊 STATISTICS")
        print(f"   Completion Rate: {rate:.1f}%")
        print(f"   Pending: {total - done} | Overdue: {overdue}")
        # Simple visual bar
        bar = "█" * int(rate/10) + "░" * (10 - int(rate/10))
        print(f"   Progress: [{bar}]")

    def _manage_projects(self):
        print(f"\nCurrent: {self.pm.current_name}")
        print("Available:", ", ".join(self.pm.projects.keys()))
        opt = input("1. Switch  2. Create  \nChoice: ")
        if opt == '1': self.pm.switch_project(input("Name: "))
        elif opt == '2': self.pm.create_project(input("New Name: "))

if __name__ == "__main__":
    app = TodoApp()
    app.start()