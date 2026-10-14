#!/usr/bin/env python3
"""Confere as referencias `caminho:linha` de um flow.md contra o codigo.

Uso: python3 -I check_refs.py <flow.md> <raiz-do-repo>

Aceita `caminho/arquivo.py:12` e `caminho/arquivo.py:12-30` (entre crases).
Falha (exit 1) se algum arquivo nao existir ou a linha passar do fim do arquivo.
Isso garante a regra "nada de fluxo inventado": todo passo aponta para codigo real.
"""
import re
import sys
from pathlib import Path

REF = re.compile(r"`([\w./\-]+\.\w+):(\d+)(?:-(\d+))?`")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    flow_path, root = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
    text = flow_path.read_text(encoding="utf-8")
    refs = REF.findall(text)
    if not refs:
        print("Nenhuma referencia caminho:linha encontrada.")
        return 1

    line_counts: dict[Path, int] = {}
    problems: list[str] = []
    seen = set()

    for rel, start, end in refs:
        key = (rel, start, end)
        if key in seen:
            continue
        seen.add(key)

        target = (root / rel).resolve()
        if root not in target.parents and target != root:
            problems.append(f"{rel}:{start} aponta para fora do repo")
            continue
        if not target.is_file():
            problems.append(f"{rel}:{start} arquivo nao existe")
            continue
        if target not in line_counts:
            with target.open(encoding="utf-8", errors="replace") as fh:
                line_counts[target] = sum(1 for _ in fh)

        first = int(start)
        last = int(end) if end else first
        if first < 1 or last < first:
            problems.append(f"{rel}:{start}-{end} intervalo invalido")
        elif last > line_counts[target]:
            problems.append(f"{rel}:{start}-{end or start} passa do fim ({line_counts[target]} linhas)")

    total = len(seen)
    if problems:
        print(f"{len(problems)} problema(s) em {total} referencias unicas:")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"OK: {total} referencias unicas conferem com o codigo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
