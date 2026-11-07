# Shape Guesser

'Native' python program that scores the 'rectangle-ness' of the shape you draw

## Installation / Usage

requires the uv package manager

```sh
git clone git@github.com:DigitalHungerTM/shape-guesser.git
cd shape-guesser
uvx briefcase dev
```

First time start may take a while because the `largestinteriorrectangle` package gets JIT compiled. Consequent runs should start instantly.

`uvx briefcase run` doesn't work for some reason and I can't be arsed to find out why.

## Screenshots

![Drawing that looks square and has high score](docs/screenshot-01.png)

![Drawing that looks round and has low score](docs/screenshot-02.png)
