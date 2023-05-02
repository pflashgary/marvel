# Marvel character to comics count

Register for an API key-pair at: <https://developer.marvel.com/account> and then rename `.env.sample` to `.env` and put your key pair in there (alternatively `export MARVEL_API_PUBLIC_KEY=...` and `export MARVEL_API_PUBLIC_KEY=...`)

## How to use it

### Optional venv to keep app dependencies separate from system libraries

```sh
pip3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```sh
pip3 install -r requirements.txt
```

### Run it

```sh
./main.py
```
