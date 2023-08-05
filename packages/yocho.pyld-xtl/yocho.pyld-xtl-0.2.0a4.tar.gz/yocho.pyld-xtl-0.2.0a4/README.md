# Extra command line tools for pyld

TODO

Usage examples:

```bash
# Install pipx
pip3 install --user --upgrade pipx

# (optionally) clear pipx cache if you want the latest version ...
\rm -vr ~/.local/pipx/.cache/

# check version
pipx run --spec yocho.pyld-xtl pyld-xtl --version

# url resolving
pipx run --spec yocho.pyld-xtl pyld-xtl compact --url https://raw.githubusercontent.com/json-ld/json-ld.org/master/examples/syntax/example-061-Aliasing-keywords.json

# input file handling
curl --silent https://raw.githubusercontent.com/json-ld/json-ld.org/master/examples/syntax/example-061-Aliasing-keywords.json | pipx run --spec yocho.pyld-xtl pyld-xtl compact -
curl --silent https://raw.githubusercontent.com/json-ld/json-ld.org/master/examples/syntax/example-061-Aliasing-keywords.json | pipx run --spec yocho.pyld-xtl pyld-xtl compact /dev/stdin
pipx run --spec yocho.pyld-xtl pyld-xtl compact <(curl --silent https://raw.githubusercontent.com/json-ld/json-ld.org/master/examples/syntax/example-061-Aliasing-keywords.json)
```
