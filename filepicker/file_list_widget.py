from PyQt6.QtWidgets import QListWidget
import os

class FileListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.itemDoubleClicked.connect(self.handle_double_click)
        
    def add_file(self, file_path):
        if file_path not in self.file_paths:
            self.file_paths.append(file_path)
            self._update_display()
            
    def remove_selected_file(self):
        current_row = self.currentRow()
        if current_row >= 0:
            self.file_paths.pop(current_row)
            self._update_display()
            
    def _update_display(self):
        self.clear()
        if not self.file_paths:
            return
            
        # Find common prefix path
        if len(self.file_paths) == 1:
            # For single file, just show filename
            self.addItem(os.path.basename(self.file_paths[0]))
            return
            
        # Get the current working directory
        cwd = os.getcwd()
        
        # For files in different directories, show paths relative to current working directory
        for path in self.file_paths:
            # Convert absolute path to relative path from current directory
            try:
                rel_path = os.path.relpath(path, cwd)
                self.addItem(rel_path)
            except ValueError:
                # If paths are on different drives, show full path
                self.addItem(path)
            
    def handle_double_click(self, item):
        current_row = self.row(item)
        if current_row >= 0:
            self.file_paths.pop(current_row)
            self._update_display()
