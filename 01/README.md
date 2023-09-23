Запуск тестов:
```
./run_tests.sh
```
или (из корневой директории):
```
python3 -m unittest tests/predict_mood_test.py tests/rf_gen_test.py
```

Запуск линетров:
```
./linters.sh
```

Coverage report:
```
Name                         Stmts   Miss  Cover
------------------------------------------------
src/__init__.py                  0      0   100%
src/model.py                     5      2    60%
src/predict_mood.py             14      0   100%
src/rf_gen.py                   16      0   100%
tests/__init__.py                0      0   100%
tests/predict_mood_test.py      55      1    98%
tests/rf_gen_test.py            76      1    99%
------------------------------------------------
TOTAL                          166      4    98%
```