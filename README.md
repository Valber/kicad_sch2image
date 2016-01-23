# kicad_sch2image

Конвертим kicad *.sch в изображения.

## Usage

```
kicad_sch2image.py [-h] [-v] [-o OUTPUT] [-T {png,svg,ps}] [-L lib]
                          target

kicad_sch2image - convert sch file to image

positional arguments:
  target                target *.sch file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -o OUTPUT, --output OUTPUT
                        output dir or file
  -T {png,svg,ps}, --type {png,svg,ps}
                        type output file
  -L lib, --library lib
                        cashe lib file or dir with it

Example:
	kicad_sch2image.py test.sch -o test_image.png -L ~/test_prj/
```

## Requirements

* python3
* pycairo

## License

GPLv2
