from pathlib import Path

# Get the current working directory
current_dir = Path.cwd()

# Skip checking for current file since __file__ doesn't exist in Jupyter notebooks
print(f"Files in {current_dir}:")
for filepath in current_dir.iterdir():
    print(f" - {filepath.name}")
    # Only try to read text files to avoid binary file errors
    if filepath.is_file() and filepath.suffix in ['.txt', '.py', '.md', '.csv', '.json']:
        try:
            # Use encoding and limit content length to avoid large outputs
            content = filepath.read_text(encoding='utf-8')[:100] + '...' if len(filepath.read_text(encoding='utf-8')) > 100 else filepath.read_text(encoding='utf-8')
            print(f"   Content: {content}")
        except Exception as e:
            print(f"   Could not read file: {e}")