set -e
cd /workspace/il-resources
args=""
for m in letters/clerk/md/*.md; do b=$(basename $m .md); args="$args $m::letters/clerk/Word/$b.docx"; done
python3 build/md2docx.py letters/ag/Illinois_Attorney_General_Letter.md::letters/ag/Illinois_Attorney_General_Letter.docx $args
soffice --headless --convert-to pdf --outdir letters/ag letters/ag/Illinois_Attorney_General_Letter.docx >/dev/null 2>&1
soffice --headless --convert-to pdf --outdir letters/clerk/PDF letters/clerk/Word/*.docx >/dev/null 2>&1
ls letters/clerk/PDF | wc -l
