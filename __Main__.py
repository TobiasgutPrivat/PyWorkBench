from WorkBenchUI.WorkBenchLayout import main
from typing import Callable
import flet as ft # type: ignore

# Run the app
target: Callable = main
ft.app(target)