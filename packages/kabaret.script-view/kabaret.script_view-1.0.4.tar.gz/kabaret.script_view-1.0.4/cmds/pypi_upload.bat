
cd ..

rem C:\Python36\python.exe -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
C:\Python36\python.exe -m twine upload dist/* --skip-existing

pause