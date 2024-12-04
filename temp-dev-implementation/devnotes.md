Lab notes.
### Inicializacija raznih reči
##### pip
`python.exe -m pip install --upgrade pip`
##### FastAPI in Uvicorn
`pip install fastapi[standard] uvicorn[standard]`

https://fastapi.tiangolo.com/tutorial/first-steps/

https://fastapi.tiangolo.com/tutorial/bigger-applications/#import-apirouter
##### Kako izklopiti spellcheck v PyCharm zaradi slovenščine
Pojdi v `File -> Settings -> Editor -> Inspections -> Proofreading -> Typo` in uncheckaj Typo.
### Testiranje FastAPI
`fastapi dev tests\hello\fastapi_test.py` servira test na `http://127.0.0.1:8000`.
Poglej `/docs` za avtomatsko ustvarjeno Swagger dokumentacijo.

`fastapi dev tests\multifile\app\main.py` testira zahtevnejši primer.