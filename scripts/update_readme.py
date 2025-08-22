import json, re, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
readme = root / "README.md"
data = json.loads((root / "data" / "now.json").read_text())

block = (
    "- **Now:** " + data["now"] + "\n"
    "- **Next:** " + data["next"] + "\n"
    "- **Exploring:** " + data["exploring"]
)

txt = readme.read_text()
pattern = r"(<!-- NOW_NEXT:START -->)(.*?)(<!-- NOW_NEXT:END -->)"
new = re.sub(pattern, r"\1\n" + block + r"\n\3", txt, flags=re.S)
readme.write_text(new)
print("Updated Now/Next/Exploring.")
