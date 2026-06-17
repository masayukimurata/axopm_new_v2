import os

# 出力対象外にするディレクトリ
EXCLUDE_DIRS = {'.git', '.venv', '__pycache__', '.vscode', 'assets'}
# 出力するファイル拡張子
INCLUDE_EXT = {'.py'}

def dump_project():
    output_file = "all_project_code.txt"
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk("."):
            # 除外ディレクトリの処理
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if any(file.endswith(ext) for ext in INCLUDE_EXT):
                    file_path = os.path.join(root, file)
                    outfile.write(f"\n{'='*20}\n")
                    outfile.write(f"FILE: {file_path}\n")
                    outfile.write(f"{'='*20}\n")

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            outfile.write(f.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}")
                    outfile.write("\n")
    print(f"全コードを {output_file} に書き出しました。")

if __name__ == "__main__":
    dump_project()
