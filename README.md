# sphinx-grammar

Generate examples from, or ensure that an expression is a member of a context
free grammar defined in a sphinx document.

sphinx-grammar does the following:

- Parses context free grammars written in a
  [sphinx](http://sphinx-doc.org/markup/para.html#grammar-production-displays)
  project.
- Generates library code from the context free grammar which:
  - Can validate that instances are a member of the grammar. 
  - Can randomly generate member instances for fuzzing or testing.

## How does it work?

It simply translates from the format supported by sphinx to the format input to
[gnu-bison][bison]. Then you can use bison to generate C-Lang or Java code, or
[jison][jison] to generate JavaScript.

[bison]: https://www.gnu.org/software/bison/manual/bison.html
[jison]: https://zaach.github.io/jison/
