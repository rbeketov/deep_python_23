Запуск тестов:
```
./run_tests.sh
```
или (из корневой директории):
```
python3 -m unittest tests/parse_json_test.py tests/mean_k_calls_test.py
```

Запуск линетров:
```
./linters.sh
```

Coverage report:
```
Name                         Stmts   Miss  Cover
------------------------------------------------
src/mean_k_calls.py             21      0   100%
src/parse_json.py               11      0   100%
tests/json_generator.py         34      0   100%
tests/mean_k_calls_test.py      72      8    89%
tests/parse_json_test.py        75      1    99%
------------------------------------------------
TOTAL                          213      9    96%
```