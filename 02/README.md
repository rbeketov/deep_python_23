Запуск тестов:
```
./run_tests.sh
```
или:
```
python3 -m unittest test_parse_json.py test_mean_k_calls.py
```

Запуск линетров:
```
./linters.sh
```

Coverage report:
```
Name                   Stmts   Miss  Cover
------------------------------------------
json_generator.py         34      0   100%
mean_k_calls.py           21      0   100%
parse_json.py             11      0   100%
test_mean_k_calls.py      72      8    89%
test_parse_json.py       112      1    99%
------------------------------------------
TOTAL                    250      9    96%

```