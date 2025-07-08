from textnode import TextNode, TextType
from blocktypes import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        current_text = node.text
        
        # Continue processing until no more delimiter pairs are found
        while delimiter in current_text:
            # Find the first delimiter
            start_idx = current_text.find(delimiter)
            
            # Find the next delimiter after the first one
            end_idx = current_text.find(delimiter, start_idx + len(delimiter))
            
            # If no paired delimiter, that's an error
            if end_idx == -1:
                raise Exception(f"No closing delimiter found for '{delimiter}'")
                
            # Add text before the first delimiter
            if start_idx > 0:
                new_nodes.append(TextNode(current_text[:start_idx], TextType.TEXT))
                
            # Add the delimited text (without the delimiters)
            delimited_text = current_text[start_idx + len(delimiter):end_idx]
            new_nodes.append(TextNode(delimited_text, text_type))
            
            # Update current_text to be everything after the second delimiter
            current_text = current_text[end_idx + len(delimiter):]
        
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        if "![" not in  current_text:
            new_nodes.append(node)
            continue
        else:
            images = extract_markdown_images(current_text)
            if not images:
                new_nodes.append(node)
                continue
        
        remaining_text = current_text
        for alt_text, url in images:
            image_text = f"![{alt_text}]({url})"

            parts = remaining_text.split(image_text, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(current_text)
        if not links:
            new_nodes.append(node)
            continue
        
        remaining_text = current_text
        for alt_text, url in links:
            link_text = f"[{alt_text}]({url})"

            parts = remaining_text.split(link_text, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    return nodes

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return HTMLNode(None, text_node.text, [])
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode("b", None, [HTMLNode(None, text_node.text, [])])
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode("i", None, [HTMLNode(None, text_node.text, [])])
    elif text_node.text_type == TextType.CODE:
        return HTMLNode("code", None, [HTMLNode(None, text_node.text, [])])
    elif text_node.text_type == TextType.LINK:
        return HTMLNode("a", {"href": text_node.url}, [HTMLNode(None, text_node.text, [])])
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode("img", {"src": text_node.url, "alt": text_node.text}, [])
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    
def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    result = []
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        result.append(block)
    return result

def markdown_to_html_node(markdown):
    parent_node = HTMLNode('div', None, [])
    blocks = markdown_to_blocks(markdown)
    print(f"Blocks: {blocks}")  # Debug print
    
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Block: {block}, Type: {block_type}")
        
        if block_type == BlockType.PARAGRAPH:
            # Process paragraph blocks
            blocklines = block.split("\n")
            html_nodes = []
            for idx, line in enumerate(blocklines):
                text_nodes = text_to_textnodes(line)
                html_nodes.extend([text_node_to_html_node(node) for node in text_nodes])
                if idx < len(blocklines) - 1:
                    html_nodes.append(HTMLNode("br", None, []))
            paragraph_node = HTMLNode("p", None, html_nodes)
            parent_node.children.append(paragraph_node)
            
        elif block_type == BlockType.HEADING:
            # Process heading blocks
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            content = block[level:].strip()
            
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            heading_node = HTMLNode(f"h{level}", None, html_nodes)
            parent_node.children.append(heading_node)
            
        # Process code blocks
        elif block_type == BlockType.CODE:
            # Split the block into lines
            lines = block.split("\n")
            # Remove the first and last lines (which contain ```)
            code_content = "\n".join(lines[1:-1])
            # Create a text node with no inline parsing
            text_node = TextNode(code_content, TextType.TEXT)
            code_node = text_node_to_html_node(text_node)
            # Wrap in pre and code tags
            pre_node = HTMLNode("pre", None, [HTMLNode("code", None, [code_node])])
            parent_node.children.append(pre_node)
            
        elif block_type == BlockType.QUOTE:
            # Process quote blocks
            # Remove the > marker from each line
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith(">"):
                    new_lines.append(line[1:].lstrip())
            content = "\n".join(new_lines)
            
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            quote_node = HTMLNode("blockquote", None, html_nodes)
            parent_node.children.append(quote_node)

        elif block_type == BlockType.UNORDERED_LIST:
            list_node = HTMLNode('ul', None, [])
            lines = block.split("\n")
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Remove the list marker (* or - or +) and leading/trailing whitespace
                # Find the first occurrence of a list marker
                for i, char in enumerate(line):
                    if char in "*-+":
                        # Remove the marker and any surrounding whitespace
                        line_content = line[i+1:].strip()
                        break
                
                # Process inline markdown in the list item
                text_nodes = text_to_textnodes(line_content)
                html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                
                # Create list item node and add it to the list
                li_node = HTMLNode("li", None, html_nodes)
                list_node.children.append(li_node)
            
            parent_node.children.append(list_node)

        elif block_type == BlockType.ORDERED_LIST:
            list_node = HTMLNode('ol', None, [])
            lines = block.split("\n")
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # For ordered lists, find where the number and period end
                marker_end = -1
                for i, char in enumerate(line):
                    if char == '.' and i > 0 and line[:i].strip().isdigit():
                        marker_end = i
                        break
                
                if marker_end >= 0:
                    # Remove the marker and any surrounding whitespace
                    line_content = line[marker_end+1:].strip()
                    
                    # Process inline markdown in the list item
                    text_nodes = text_to_textnodes(line_content)
                    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                    
                    # Create list item node and add it to the list
                    li_node = HTMLNode("li", None, html_nodes)
                    list_node.children.append(li_node)
            
            parent_node.children.append(list_node)
                    
    return parent_node