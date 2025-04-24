#!/usr/bin/env python3
import os
import sys
import shutil

def collect_files(input_dir, output_dir, max_depth=None):
    if not os.path.isdir(input_dir):
        print("Error: input_dir does not exist or is not a directory.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    name_counts = {}

    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    for root, dirs, files in os.walk(input_dir):
        rel_path = os.path.relpath(root, input_dir)
        rel_parts = [] if rel_path == '.' else rel_path.split(os.sep)

        # "Срезаем" глубину, если превышает max_depth
        if max_depth is not None and len(rel_parts) >= max_depth:
            new_rel_parts = rel_parts[-max_depth:]
        else:
            new_rel_parts = rel_parts

        target_root = os.path.join(output_dir, *new_rel_parts)
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(target_root, file)

            # Если файл уже существует, добавляем суффикс
            if os.path.exists(dst_path):
                base, ext = os.path.splitext(file)
                count = name_counts.get(file, 1)
                while True:
                    new_name = f"{base}_{count}{ext}"
                    new_path = os.path.join(target_root, new_name)
                    if not os.path.exists(new_path):
                        dst_path = new_path
                        name_counts[file] = count + 1
                        break
                    count += 1
            else:
                name_counts[file] = 1

            shutil.copyfile(src_path, dst_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: collect_files.py <input_dir> <output_dir> [--max_depth N]")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_depth = None

    if "--max_depth" in sys.argv:
        try:
            idx = sys.argv.index("--max_depth")
            max_depth = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("Error: Invalid --max_depth value")
            sys.exit(1)

    collect_files(input_dir, output_dir, max_depth)
