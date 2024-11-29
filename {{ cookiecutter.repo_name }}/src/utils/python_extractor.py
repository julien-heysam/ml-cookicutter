from pathlib import Path

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


def walk_directory(directory: Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    paths = sorted(
        Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            if path.name == "__pycache__":
                continue
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            icon = "🐍 " if path.suffix == ".py" else "📄 "
            tree.add(Text(icon) + text_filename)


def extract_code(file_path: Path) -> str:
    """Extract functions and classes from a Python file."""
    with open(file_path, "r") as f:
        code = f.read()
    return code


if __name__ == "__main__":
    directory = "src/"  # Replace with your directory
    output_file = "extracted_code.py"  # Replace with your desired output file

    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        guide_style="bold bright_blue",
    )
    walk_directory(Path(directory), tree)
    print(tree)

    with open(output_file, "w") as outfile:
        for path in Path(directory).rglob("*.py"):
            outfile.write(f"# --- {path} ---\n")
            outfile.write(extract_code(path))
            outfile.write("\n\n")

    print(f"Extracted code written to {output_file}")
