def parse_file_generator(filepath):
    def parser(filepath: str) -> dict:
        import re
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = [line.rstrip() for line in file if line.strip()]

        root = {}
        stack = [(0, root)]
        i = 0

        while i < len(lines):
            line = lines[i]

            match = re.match(r'^(#+)\s*(.+?)(\s*#.*)?$', line)
            if match:
                hashes, title, _ = match.groups()
                level = len(hashes)

                while stack and stack[-1][0] >= level:
                    stack.pop()
                parent = stack[-1][1]

                answer_lines = []
                i += 1
                while i < len(lines) and not re.match(r'^\s*#+\s*\S+', lines[i]):
                    clean_line = lines[i].split('#')[0].rstrip()
                    if clean_line:
                        answer_lines.append(clean_line)
                    i += 1

                answer = "\n".join(answer_lines).strip()

                if answer:
                    node = {
                        "question": title.strip(),
                        "answer": answer
                    }
                    parent[title.strip()] = node
                    stack.append((level, node))
                else:
                    node = {}
                    parent[title.strip()] = node
                    stack.append((level, node))
            else:
                i += 1
        return root

    def walk_tree(tree, path=None):
        if path is None:
            path = []

        for key, value in tree.items():
            if isinstance(value, dict):
                new_path = path + [key]
                if 'question' in value and 'answer' in value:
                    hierarchy = " > ".join(path)
                    yield f"[DZIEDZINA] {hierarchy}\n[PYTANIE] {value['question']}\n[ODPOWIEDŹ] {value['answer']}"
                yield from walk_tree(value, new_path)

    tree = parser(filepath)
    yield from walk_tree(tree)