# PyOpenADR

PyOpenADR is a Python 3 module that provides a convenient interface to OpenADR
systems. It contains an OpenADR Client that you can use to talk to other OpenADR
systems, and it contains an OpenADR Server (VTN) with convenient integration
possibilities.

## Documentation

You can find documentation here: https://finetuned.nl/pyopenadr

## Contributing

At this moment, we're finishing off a first usable version. After version 0.5.0,
new bug reports and pull requests are most welcome.

## Developing

```bash
git clone https://git.finetuned.nl/stan/pyopenadr
cd pyopenadr
python3 -m venv python_env
./python_env/bin/pip3 install -e .
```

## Running conformance tests

```bash
./python_env/bin/pip3 install pytest pytest-asyncio
./python_env/bin/python3 -m pytest test/conformance
```
