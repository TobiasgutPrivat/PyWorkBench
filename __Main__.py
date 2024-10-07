import ttkbootstrap as ttk
import importlib
import sys
import inspect
import types
from tkinter import StringVar, messagebox


class PythonWorkbenchApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Python Workbench")
        self.geometry("800x600")

        # Package Loading Frame
        self.package_frame = ttk.Frame(self)
        self.package_frame.pack(fill=X, padx=10, pady=10)

        # Package Input
        self.package_var = StringVar()
        self.package_entry = ttk.Entry(self.package_frame, textvariable=self.package_var)
        self.package_entry.pack(side=LEFT, expand=True, fill=X, padx=5)

        # Load Button
        self.load_button = ttk.Button(self.package_frame, text="Load Package", command=self.load_package)
        self.load_button.pack(side=LEFT, padx=5)

        # Loaded Modules Treeview
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Type"), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.column("Type", width=150, anchor=CENTER)
        self.tree.pack(fill=BOTH, expand=True)

        # Information Area
        self.info_frame = ttk.LabelFrame(self, text="Details", padding=10)
        self.info_frame.pack(fill=X, padx=10, pady=5)
        self.info_label = ttk.Label(self.info_frame, text="", anchor=W, justify=LEFT)
        self.info_label.pack(fill=X)

        # Load initial built-in modules
        self.load_modules(sys.modules)

    def load_modules(self, modules):
        """
        Populate the tree with the current loaded modules and their functions, classes, and variables.
        """
        self.tree.delete(*self.tree.get_children())  # Clear existing tree items

        for module_name, module in modules.items():
            # Only display loaded modules
            if module and isinstance(module, types.ModuleType):
                module_node = self.tree.insert("", "end", text=module_name, values=("Module",))

                # Get classes, functions, and variables in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        self.tree.insert(module_node, "end", text=name, values=("Class",))
                    elif inspect.isfunction(obj):
                        self.tree.insert(module_node, "end", text=name, values=("Function",))
                    elif not name.startswith("_"):
                        self.tree.insert(module_node, "end", text=name, values=("Variable",))

                self.tree.item(module_node, open=True)

    def load_package(self):
        """
        Load a package dynamically and refresh the module list.
        """
        package_name = self.package_var.get().strip()

        if not package_name:
            messagebox.showwarning("Warning", "Please enter a valid package name")
            return

        try:
            importlib.import_module(package_name)
            self.load_modules(sys.modules)  # Refresh the module list
            messagebox.showinfo("Success", f"Successfully loaded package '{package_name}'")
        except ImportError as e:
            messagebox.showerror("Error", f"Failed to load package '{package_name}': {e}")


if __name__ == "__main__":
    app = PythonWorkbenchApp()
    app.mainloop()