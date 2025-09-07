from textnode import TextNode, TextType
import os, shutil

def generate_static():
    current_dir = os.path.dirname(__file__)
    if os.path.isdir(os.path.join(current_dir, "..", "public")):
        pass
        
        



def main():
    print(TextNode("Hello, World!", TextType.BOLD, "https://www.example.com"))

main()