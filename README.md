# x86 Disassembler

This project is an x86 instruction disassembler. It recognizes only a subset of x86 instructions, those of which are specified in this projects [assignment document](docs/ProgrammingAssignment1.pdf).

This was written as part of the Reverse Engineering and Vulnerability Analysis course at John's Hopkins University .

## Usage

This project has no dependencies and therefore has no installation or setup instructions. The only requirement is that the user has `python` version >= 3.7.

To run the disassembler, use the following format:

```bash
$ python main.py -i <input_file>
```

Where `input_file` is any valid assembled binary file.

Example:

```bash
$ 
```

> Note: a collection of example binary files (in addition to their pre-assembled files) are inside of this repo's `examples/` directory.

## Running Tests

This project was set up with [`pipenv`](https://pipenv.pypa.io/en/latest/) - python's packaging/scripting tool. It's intended to merge together the nice features of `pip` and `venv`. To install it, run:

```bash
$ pip insall --user pipenv
```

Then, you can install this project's testing/development dependencies via:

```bash
$ pipenv sync --dev
```

Now that you have the dependencies installed required for testing, you can execute the tests via:

```bash
$ pipenv run test
```
