# Documents

For Word, PDF, presentation, and spreadsheet work, load the matching installed
`docx`, `pdf`, `pptx`, or `xlsx` skill. Use `anydoc` to extract an existing document
instead of guessing its contents. Keep confidential documents local unless the
user explicitly asks for a hosted conversion.

`doc-python` runs the dedicated document environment at
`~/.local/share/dotfiles/documents`. It includes python-docx, python-pptx, openpyxl,
pypdf, ReportLab, Pillow, and pypandoc with its bundled Pandoc binary. Use this
environment instead of installing libraries into Arch's system Python.

Check the actual exported artifact: text, page or sheet structure, formulas, and
rendered layout where tooling supports it. Opening a document with a library does
not prove the visual layout. State missing rendering tools when they affect the
result; do not describe an unrendered document as visually verified.
