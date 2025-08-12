import time
import random
import os

file_path = "/workspaces/Mohammed-Nasser-Academy/src/pages/x.tsx"

def random_line():
    templates = [
        "const var{n} = {num};",
        "function func{n}() {{ return {num}; }}",
        "console.log('Debug {n}:', {num});",
        "let arr{n} = [{num}, {num2}, {num3}];",
        "export const value{n} = '{str}';",
    ]
    template = random.choice(templates)
    return template.format(
        n=random.randint(1, 1000),
        num=random.randint(0, 100),
        num2=random.randint(0, 100),
        num3=random.randint(0, 100),
        str=''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6))
    )

while True:
    line = random_line()
    with open(file_path, "a") as f:  # "a" means append
        f.write(line + "\n")
    print("Added:", line)
    time.sleep(1)  # Wait 1 second before writing again
