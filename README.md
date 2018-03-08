# wikidata-external-id-distribution

Tool to calculate the external-id distribution on Wikidata. Result is a pdf bar chart and a csv file including the top 50 external-ids.

## Installation

```
$ git clone https://github.com/marisanest/wikidata-external-id-distribution.git
```

## Usage

The calling syntax is

```
$ python src/main.py
```

You can than find the plot as pdf file in

```
$ cd plots/
```

and the distribution as csv in

```
$ cd csv/
```

## License

The source code is licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3.

## Requirements
* requests
* matplotlib
* pandas
* os

