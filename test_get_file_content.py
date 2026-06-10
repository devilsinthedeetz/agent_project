from functions.get_file_content import get_file_content

lorem_files: list[str] = ["lorem.txt", "lorem_9999.txt", "lorem_10000.txt"]
small_files: list[str] = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]

for file in lorem_files:
    result = get_file_content("calculator", file)
    print(f"{file} length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

for file in small_files:
    result = get_file_content("calculator", file)
    print(f"""
Now reading {file} ...
Contents:
{result}
          """)
