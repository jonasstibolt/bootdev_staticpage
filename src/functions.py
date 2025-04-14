from textnode import TextNode, TextType
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

# def markdown_to_blocks(markdown):
#     lines = markdown.split("\n\n")
#     return lines