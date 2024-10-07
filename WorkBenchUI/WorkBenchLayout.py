import flet as ft # type: ignore
import random

# Create a class to encapsulate the UI and its logic
class WorkBenchLayout(ft.View):
    def __init__(self):
        super().__init__()

    def build(self):
        # Base layout
        self.title = ft.Text("Dynamic Layout Example", size=30)

        # Container for the dynamic part of the layout
        self.dynamic_content = ft.Column()

        # Button to regenerate content
        self.regenerate_button = ft.ElevatedButton("Regenerate Content", on_click=self.regenerate_content)

        # Initialize content
        self.regenerate_content(None)

        # Return the complete layout
        return ft.Column(
            controls=[
                self.title,
                self.regenerate_button,
                self.dynamic_content
            ]
        )

    # Function to regenerate dynamic content
    def regenerate_content(self, e):
        # Clear existing content
        self.dynamic_content.controls.clear()

        # Generate new content
        new_data = random.randint(1, 100)
        self.dynamic_content.controls.append(ft.Text(f"New data: {new_data}"))

        # Reflect the changes in the UI
        self.update()

# Main function to run the app
def main(page: ft.Page):
    # Create an instance of the class
    workbench = WorkBenchLayout()
    
    # Add the layout to the page
    page.add(workbench)