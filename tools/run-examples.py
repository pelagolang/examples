#!/usr/bin/env python3
"""Check and run every example in this repository with the real `pelago` tool.

Each example is a single `.pel` file with a header comment. The expected output is the block of lines that
start with `/// |` (the text after the bar is one line of output). For every example this script runs:

  1. pelago check   FILE          (parse, resolve names, check types)
  2. pelago run     FILE          (native code, the default) and compares stdout with the header
  3. pelago run --interp FILE     (the IR interpreter) and compares again, unless the header says `/// Interp: no`

Usage:
  python3 tools/run-examples.py [--pelago PATH] [--bless] [--quick] [name-or-folder ...]

  --bless   rewrite the `/// |` block of each example from what the native run prints (review the diff!)
  --quick   native run only (skip `check` and `--interp`)
"""
import os, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "tools", "projects", "node_modules"}


def find_examples(filters):
    found = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        rel = os.path.relpath(base, ROOT)
        if rel == ".":
            continue
        if "main.pel" in files:
            # A directory with a `main.pel` is one multi-file example: run the directory.
            path = rel.replace(os.sep, "/")
            if not filters or any(path.startswith(x.rstrip("/")) or x in path for x in filters):
                found.append(path)
            dirs[:] = []
            continue
        for f in sorted(files):
            if f.endswith(".pel"):
                path = os.path.join(rel, f).replace(os.sep, "/")
                if not filters or any(path.startswith(x.rstrip("/")) or x in path for x in filters):
                    found.append(path)
    return sorted(found)


def expected_of(lines):
    out, started = [], False
    for line in lines:
        s = line.rstrip("\n")
        if s == "/// |" or s.startswith("/// | "):
            started = True
            out.append(s[6:])
        elif started:
            break
    return out


def header_flag(lines, key):
    for line in lines[:80]:
        if line.startswith("/// " + key + ":"):
            return line.split(":", 1)[1].strip()
    return None


def bless(path, lines, actual):
    new, i, done = [], 0, False
    while i < len(lines):
        line = lines[i]
        new.append(line)
        i += 1
        if not done and line.startswith("/// Output:"):
            while i < len(lines) and lines[i].startswith("/// |"):
                i += 1
            for a in actual:
                new.append(("/// | " + a).rstrip() if a else "/// |")
            done = True
    with open(path, "w", newline="\n") as f:
        f.writelines(l if l.endswith("\n") else l + "\n" for l in new)


def run(cmd, cwd, timeout=300):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    return p.returncode, p.stdout, p.stderr


def main():
    args = sys.argv[1:]
    pel = os.environ.get("PELAGO", "pelago")
    do_bless = quick = False
    filters = []
    while args:
        a = args.pop(0)
        if a == "--pelago":
            pel = os.path.abspath(args.pop(0))
        elif a == "--bless":
            do_bless = True
        elif a == "--quick":
            quick = True
        else:
            filters.append(a)
    examples = find_examples(filters)
    if not examples:
        print("no examples found")
        return 1
    failed = []
    for rel in examples:
        full = os.path.join(ROOT, rel)
        header = os.path.join(full, "main.pel") if os.path.isdir(full) else full
        with open(header, encoding="utf-8") as f:
            lines = f.read().split("\n")
        want = expected_of(lines)
        problems = []
        work = tempfile.mkdtemp(prefix="pelago-example-")
        try:
            if not quick:
                code, out, err = run([pel, "check", full], work)
                if code != 0 or " 0 errors" not in out + err:
                    problems.append("check failed:\n" + (out + err).strip())
            code, out, err = run([pel, "run", full], work)
            got = out.split("\n")
            if got and got[-1] == "":
                got.pop()
            if code != 0:
                problems.append("run exited with %d:\n%s" % (code, err.strip()))
            if do_bless and code == 0:
                bless(header, lines, got)
                want = got
            elif got != want:
                problems.append("native output differs\n--- expected\n%s\n--- got\n%s" % ("\n".join(want), "\n".join(got)))
            if not quick and header_flag(lines, "Interp") != "no":
                code, out, err = run([pel, "run", "--interp", full], work)
                got2 = out.split("\n")
                if got2 and got2[-1] == "":
                    got2.pop()
                if code != 0:
                    problems.append("interp exited with %d:\n%s" % (code, err.strip()))
                elif got2 != want:
                    problems.append("interpreter output differs\n--- expected\n%s\n--- got\n%s" % ("\n".join(want), "\n".join(got2)))
        except subprocess.TimeoutExpired:
            problems.append("timed out")
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if problems:
            failed.append(rel)
            print("FAIL " + rel)
            for p in problems:
                print("    " + p.replace("\n", "\n    "))
        else:
            print("ok   " + rel)
    if not filters:
        readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
        for rel in examples:
            want_link = "(" + rel.rstrip("/") + ("/)" if os.path.isdir(os.path.join(ROOT, rel)) else ")")
            if want_link not in readme:
                failed.append(rel)
                print("FAIL %s: not listed in README.md" % rel)
    print("\n%d examples, %d failed" % (len(examples), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
