import unittest
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes, markdown_to_html_node
from textnode import TextNode, TextType
from blocktypes import block_to_block_type

markdown_test_text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

```
This is a code block
with _formatting_ that should be **preserved**
```
"""

def debug_markdown_to_html(markdown, blocks):
    print(f"Input Markdown:\n{markdown}")
    
    # Call the function and capture the output
    result = markdown_to_html_node(markdown)

    # Print the result object itself (if readable)
    print(f"Output HTMLNode Object:\n{result}")

    for block in blocks:
        print(f"Block: {repr(block)}")
        block_type = block_to_block_type(block)
        print(f"Block type: {block_type}")

    # If your HTMLNode has children, print them too for inspection
    if hasattr(result, 'children'):
        def print_html_node(node, depth=0):
            indent = "  " * depth
            print(f"{indent}Tag: {node.tag}, Text: {node.value}, Attributes: {node.props}")
            for child in node.children:
                print_html_node(child, depth + 1)

        print("HTMLNode Hierarchy:")
        print_html_node(result)

    return result

debug_markdown_to_html("### Header 3... \n\n > quote", ["# Heading\n\n> Blockquote\n\n```\ncode block\n```", ">Blockquote\n>code block"])

result = markdown_to_html_node(markdown_test_text)

print(f"Result: {result}")
if hasattr(result, 'to_html'):
    print(f"HTML: {result.to_html()}")