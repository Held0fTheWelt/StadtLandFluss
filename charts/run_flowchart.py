import webbrowser
import os

# Pfad relativ zu diesem Script
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(script_dir, 'flowchart.html')

webbrowser.open('file://' + html_file)