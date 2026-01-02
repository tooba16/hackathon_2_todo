#!/usr/bin/env python3
"""
TaskManagerAgent - Main agent for the console todo application
This agent controls the entire console todo application, shows the menu,
takes user input, and delegates work to sub-agents.
"""

from typing import List, Dict
from abc import ABC, abstractmethod


class Task:
    """Represents a single task in the todo list"""
    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} [{self.id}] {self.title}"


class SubAgent(ABC):
    """Abstract base class for all sub-agents"""
    def __init__(self, task_manager):
        self.task_manager = task_manager

    @abstractmethod
    def execute(self):
        pass


class AddTaskAgent(SubAgent):
    """Sub-agent responsible for creating new todo tasks"""
    
    def execute(self):
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        
        if not title:
            print("Task title cannot be empty!")
            return
        
        description = input("Enter task description (optional): ").strip()
        
        # Create and add the new task
        new_task = Task(
            task_id=self.task_manager.get_next_task_id(),
            title=title,
            description=description
        )
        
        self.task_manager.tasks.append(new_task)
        print(f"Task '{title}' added successfully!")


class DeleteTaskAgent(SubAgent):
    """Sub-agent responsible for removing tasks from the todo list"""
    
    def execute(self):
        print("\n--- Delete Task ---")
        
        if not self.task_manager.tasks:
            print("No tasks to delete!")
            return
        
        self.task_manager.view_tasks()
        
        try:
            task_id = int(input("\nEnter the task number to delete: "))
            task = self.task_manager.get_task_by_id(task_id)
            
            if task:
                self.task_manager.tasks.remove(task)
                print(f"Task '{task.title}' deleted successfully!")
            else:
                print("Task not found!")
        except ValueError:
            print("Please enter a valid number!")


class UpdateTaskAgent(SubAgent):
    """Sub-agent responsible for modifying existing tasks"""
    
    def execute(self):
        print("\n--- Update Task ---")
        
        if not self.task_manager.tasks:
            print("No tasks to update!")
            return
        
        self.task_manager.view_tasks()
        
        try:
            task_id = int(input("\nEnter the task number to update: "))
            task = self.task_manager.get_task_by_id(task_id)
            
            if task:
                print(f"Current title: {task.title}")
                new_title = input("Enter new title (or press Enter to keep current): ").strip()
                
                print(f"Current description: {task.description}")
                new_description = input("Enter new description (or press Enter to keep current): ").strip()
                
                if new_title:
                    task.title = new_title
                if new_description:
                    task.description = new_description
                
                print(f"Task updated successfully!")
            else:
                print("Task not found!")
        except ValueError:
            print("Please enter a valid number!")


class ViewTaskListAgent(SubAgent):
    """Sub-agent responsible for displaying all tasks"""
    
    def execute(self):
        print("\n--- Task List ---")
        self.task_manager.view_tasks()


class MarkCompleteAgent(SubAgent):
    """Sub-agent responsible for toggling task completion status"""
    
    def execute(self):
        print("\n--- Mark Task Complete/Incomplete ---")
        
        if not self.task_manager.tasks:
            print("No tasks to mark!")
            return
        
        self.task_manager.view_tasks()
        
        try:
            task_id = int(input("\nEnter the task number to toggle: "))
            task = self.task_manager.get_task_by_id(task_id)
            
            if task:
                task.completed = not task.completed
                status = "completed" if task.completed else "incomplete"
                print(f"Task '{task.title}' marked as {status}!")
            else:
                print("Task not found!")
        except ValueError:
            print("Please enter a valid number!")


class TaskManagerAgent:
    """Main agent that controls the entire console todo application"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
        
        # Initialize sub-agents
        self.add_task_agent = AddTaskAgent(self)
        self.delete_task_agent = DeleteTaskAgent(self)
        self.update_task_agent = UpdateTaskAgent(self)
        self.view_task_agent = ViewTaskListAgent(self)
        self.mark_complete_agent = MarkCompleteAgent(self)
    
    def get_next_task_id(self) -> int:
        """Get the next available task ID"""
        task_id = self.next_id
        self.next_id += 1
        return task_id
    
    def get_task_by_id(self, task_id: int) -> Task:
        """Find a task by its ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def view_tasks(self):
        """Display all tasks in a clean format"""
        if not self.tasks:
            print("No tasks in the list!")
            return
        
        # Sort tasks by ID to ensure consistent ordering
        sorted_tasks = sorted(self.tasks, key=lambda t: t.id)
        
        for task in sorted_tasks:
            print(task)
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*40)
        print("TASK MANAGER - CONSOLE TODO APP")
        print("="*40)
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View Task List")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("-"*40)
    
    def run(self):
        """Main application loop"""
        print("Welcome to the Task Manager Console App!")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Select an option (1-6): ").strip()
                
                if choice == "1":
                    self.add_task_agent.execute()
                elif choice == "2":
                    self.delete_task_agent.execute()
                elif choice == "3":
                    self.update_task_agent.execute()
                elif choice == "4":
                    self.view_task_agent.execute()
                elif choice == "5":
                    self.mark_complete_agent.execute()
                elif choice == "6":
                    print("\nThank you for using Task Manager. Goodbye!")
                    break
                else:
                    print("\nInvalid option! Please select a number between 1-6.")
            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    # Initialize and run the main agent
    agent = TaskManagerAgent()
    agent.run()