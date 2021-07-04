# LOG ANALYZER
> Homework-1 for the `Python Developer. Professional` course

## Getting started

- Go to the project root
```shell
cd log_analyzer
```

- Run analyzer
```shell
python3 main.py
```

- If you have your own config, provide it as an argument
```shell
python3 main.py --config /pah/to/config.json
```

## Monitor script performance

Log on script actions -monitoring.txt- is stored in project root

## Provide logs for analysis 

By default the logs are expected to be in ./log directory, it can be redefined via config

## Enjoy the report

By default the report.html is stored in ./reports directory, it can be redefined via config

### Testing
Staying in the project root run
```shell
python3 -m unittest
```
