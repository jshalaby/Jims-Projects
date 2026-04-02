import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path

class FolderExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Explorer")
        self.root.geometry("900x600")
        
        # Start from home directory instead of Documents (has more content)
        self.home_path = Path.home()
        self.documents_path = self.home_path / "Documents"
        self.current_path = self.home_path
        self.folder_map = {}  # Maps tree item IDs to folder paths
        self.path_map = {}    # Maps folder paths to tree item IDs (reverse lookup)
        
        # Create top frame for navigation
        top_frame = ttk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Home button
        self.home_button = ttk.Button(top_frame, text="🏠 Home", command=self.go_home)
        self.home_button.pack(side=tk.LEFT, padx=5)
        
        # Create main content frame with paned window
        content_frame = ttk.Frame(root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Paned window to split left and right panels
        paned = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Folder tree view
        left_frame = ttk.LabelFrame(paned, text="Folder Hierarchy", padding=5)
        paned.add(left_frame, weight=1)
        
        # Treeview for folders
        tree_scroll = ttk.Scrollbar(left_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(left_frame, yscrollcommand=tree_scroll.set, height=20)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)
        
        # Bind tree selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<<TreeviewOpen>>", self.on_expand)
        
        # Right panel - File details
        right_frame = ttk.LabelFrame(paned, text="Contents", padding=5)
        paned.add(right_frame, weight=1)
        
        # Current path label - use Entry widget for selectability
        path_frame = ttk.Frame(right_frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        path_label_text = ttk.Label(path_frame, text="Path:", font=("Arial", 9))
        path_label_text.pack(side=tk.LEFT, padx=5)
        
        self.path_label = tk.Entry(path_frame, font=("Arial", 9), state='readonly')
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Treeview detail view for files
        detail_scroll = ttk.Scrollbar(right_frame)
        detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.detail_tree = ttk.Treeview(
            right_frame, 
            columns=("type", "size"), 
            yscrollcommand=detail_scroll.set,
            height=20
        )
        self.detail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        detail_scroll.config(command=self.detail_tree.yview)
        
        # Configure detail tree columns
        self.detail_tree.column("#0", width=200)
        self.detail_tree.column("type", width=100)
        self.detail_tree.column("size", width=100)
        self.detail_tree.heading("#0", text="Name")
        self.detail_tree.heading("type", text="Type")
        self.detail_tree.heading("size", text="Size")
        
        # Bind double-click on right panel to open folders
        self.detail_tree.bind("<Double-Button-1>", self.on_detail_double_click)
        
        # Initialize tree with Documents folder
        self.load_full_tree()
    
    def load_full_tree(self):
        """Recursively load the entire folder tree from home directory"""
        self.tree.delete(*self.tree.get_children())
        self.folder_map.clear()
        self.path_map.clear()
        
        # Add home directory as root
        home_name = self.home_path.name if self.home_path.name else str(self.home_path)
        root_id = self.tree.insert("", "end", text=f"📁 {home_name}", open=True)
        self.folder_map[root_id] = self.home_path
        self.path_map[str(self.home_path)] = root_id
        
        # Recursively populate with all folders
        self.populate_tree_recursive(root_id, self.home_path)
        
        # Select root and show its contents
        self.tree.selection_set(root_id)
        self.on_tree_select(None)
    
    def populate_tree_recursive(self, parent_id, folder_path, depth=0):
        """Recursively populate tree with all folders (limited depth to avoid too many items)"""
        if depth > 3:  # Limit depth to avoid infinite recursion and performance issues
            return
        
        try:
            items = sorted(os.listdir(folder_path))
            folder_list = []
            
            for item in items:
                item_path = folder_path / item
                
                # Only show directories that actually exist
                try:
                    if os.path.isdir(item_path) and item_path.exists():
                        folder_list.append((item, item_path))
                except (PermissionError, OSError):
                    pass
            
            # Add folders to tree
            for item_name, item_path in folder_list:
                node_id = self.tree.insert(parent_id, "end", text=f"📁 {item_name}")
                self.folder_map[node_id] = item_path
                self.path_map[str(item_path)] = node_id
                
                # Recursively populate subfolders
                self.populate_tree_recursive(node_id, item_path, depth + 1)
        
        except PermissionError:
            pass
    
    def on_tree_select(self, event):
        """Handle tree selection to show files and folders"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            if item in self.folder_map:
                folder_path = self.folder_map[item]
                self.current_path = folder_path
                self.update_file_panel(folder_path)
    
    def on_expand(self, event):
        """Handle tree expansion (lazy loading not needed since we load full tree)"""
        pass
    
    def update_file_panel(self, folder_path):
        """Update the right panel with files and folders from selected folder"""
        # Clear detail tree
        self.detail_tree.delete(*self.detail_tree.get_children())
        
        # Update path label - need to temporarily enable Entry to update it
        self.path_label.config(state='normal')
        self.path_label.delete(0, tk.END)
        self.path_label.insert(0, str(folder_path))
        self.path_label.config(state='readonly')
        
        try:
            items = sorted(os.listdir(folder_path))
            
            for item in items:
                item_path = folder_path / item
                
                # Skip items that don't exist (broken links, etc.)
                try:
                    if not item_path.exists():
                        continue
                except (OSError, PermissionError):
                    continue
                
                # Get file info
                if os.path.isdir(item_path):
                    file_type = "Folder"
                    size = ""
                else:
                    file_type = "File"
                    try:
                        size = f"{item_path.stat().st_size:,} bytes"
                    except:
                        size = "N/A"
                
                # Add to detail tree
                self.detail_tree.insert("", "end", text=item, values=(file_type, size))
        
        except PermissionError:
            self.detail_tree.insert("", "end", text="Permission denied", values=("", ""))
    
    def on_detail_double_click(self, event):
        """Handle double-click on right panel to open folders"""
        item = self.detail_tree.selection()
        if item:
            item_id = item[0]
            item_name = self.detail_tree.item(item_id, "text")
            item_path = self.current_path / item_name
            
            # Check if it exists and is a folder
            try:
                if item_path.exists() and os.path.isdir(item_path):
                    # Update current path
                    self.current_path = item_path
                    
                    # Find or select the folder in the tree
                    path_str = str(item_path)
                    if path_str in self.path_map:
                        tree_id = self.path_map[path_str]
                        self.tree.selection_set(tree_id)
                        self.tree.see(tree_id)  # Scroll to make it visible
                        self.on_tree_select(None)
            except (OSError, PermissionError):
                pass
    
    def go_home(self):
        """Go to home directory"""
        self.current_path = self.home_path
        root_children = self.tree.get_children()
        if root_children:
            self.tree.selection_set(root_children[0])
            self.on_tree_select(None)

def main():
    root = tk.Tk()
    app = FolderExplorer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
