import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QTreeView, QListWidget,
                            QFileDialog)
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QFileSystemModel, QClipboard
from PyQt6.QtGui import QFileSystemModel
from filepicker.file_list_widget import FileListWidget

class FileManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create file system model and tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.Filter.AllEntries | QDir.Filter.Hidden | QDir.Filter.Dirs)
        
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree_view.setColumnWidth(0, 200)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setWindowTitle("Dir View")
        
        # Hide unnecessary columns
        for i in range(1, self.model.columnCount()):
            self.tree_view.hideColumn(i)
            
        # Create buttons
        button_layout = QVBoxLayout()
        self.browse_btn = QPushButton("...")
        self.right_arrow_btn = QPushButton("→")
        self.left_arrow_btn = QPushButton("←")
        self.copy_btn = QPushButton("Copy")
        button_layout.addWidget(self.browse_btn)
        button_layout.addWidget(self.right_arrow_btn)
        button_layout.addWidget(self.left_arrow_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addStretch()  # This pushes all buttons to the top
        
        # Create file list
        file_list_container = QWidget()
        file_list_layout = QVBoxLayout(file_list_container)
        self.file_list = FileListWidget()
        file_list_layout.addWidget(self.file_list)
        
        # Add widgets to layout
        layout.addWidget(self.tree_view)
        layout.addLayout(button_layout)
        layout.addWidget(file_list_container)
        
        # Configure tree view to show ".."
        self.tree_view.setRootIsDecorated(True)
        self.model.setReadOnly(True)
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        
        # Connect signals
        self.right_arrow_btn.clicked.connect(self.add_file)
        self.left_arrow_btn.clicked.connect(self.remove_file)
        self.browse_btn.clicked.connect(self.browse_directory)
        self.copy_btn.clicked.connect(self.copy_files_to_clipboard)
        self.tree_view.doubleClicked.connect(self.handle_tree_double_click)
        
    def add_file(self):
        indexes = self.tree_view.selectedIndexes()
        if indexes:
            file_path = self.model.filePath(indexes[0])
            self.file_list.add_file(file_path)
            
    def remove_file(self):
        self.file_list.remove_selected_file()
        
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.tree_view.setRootIndex(self.model.index(directory))
            
    def handle_tree_double_click(self, index):
        file_name = self.model.fileName(index)
        if file_name == "..":
            current_index = self.tree_view.rootIndex()
            parent_index = current_index.parent()
            if parent_index.isValid():
                self.tree_view.setRootIndex(parent_index)
        elif self.model.isDir(index):
            self.tree_view.setRootIndex(index)
        else:
            # If it's a file, add it to the file list
            file_path = self.model.filePath(index)
            self.file_list.add_file(file_path)
            
    def copy_files_to_clipboard(self):
        if not self.file_list.file_paths:
            return
            
        # Get current working directory for relative paths
        cwd = os.getcwd()
        
        # Build the combined content
        combined_text = []
        for file_path in self.file_list.file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Convert to relative path
                    rel_path = os.path.relpath(file_path, cwd)
                    combined_text.append(rel_path)
                    combined_text.append("")
                    combined_text.append(content)
                    combined_text.append("\n")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
        # Join with newlines and copy to clipboard
        if combined_text:
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(combined_text))

def main():
    app = QApplication(sys.argv)
    window = FileManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
