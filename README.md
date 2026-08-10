# fn64.github.io

The public website for [fn64](https://github.com/fn64/fn64), a clean-room Rust
foundation for Nintendo 64 static recompilation projects and native ports.

The site is dependency-free HTML and CSS. To preview it locally:

```sh
python3 -m http.server 4173
```

Then open <http://localhost:4173/>.

Validate local links, document structure, and CSS before publishing:

```sh
python3 scripts/lint-site.py
```

Technical claims should link to the authoritative documentation in the main
fn64 repository rather than duplicating its implementation status here.

## License

MIT
