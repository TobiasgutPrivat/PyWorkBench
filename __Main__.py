import flet as ft

def main(page: ft.Page):
    # Navigation handler
    def go_to_page2(e):
        page.controls.clear()  # Clear the existing page content
        page.add(ft.Text("Welcome to Page 2!"))
        page.add(ft.ElevatedButton(text="Go to Page 1", on_click=go_to_page1))
        page.update()  # Refresh the UI
    
    def go_to_page1(e):
        page.controls.clear()  # Clear the existing page content
        page.add(ft.Text("Welcome to Page 1!"))
        page.add(ft.ElevatedButton(text="Go to Page 2", on_click=go_to_page2))
        page.update()  # Refresh the UI
    
    # Start with Page 1
    go_to_page1(None)

# Run the app
ft.app(target=main)
