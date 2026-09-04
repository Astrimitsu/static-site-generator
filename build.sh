python3 src/main.py --basepath static-site-generator --build
cd docs && python3 -m http.server 8888
cd ..