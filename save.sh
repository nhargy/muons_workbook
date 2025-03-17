#! /bin/bash

echo "Saving and deploying..."

cd ~/Science/JBooks/muons_workbook
rm -rf docs
mkdir docs
touch docs/.nojekyll
jupyter-book build .
mv _build/html/* docs/

git add . .git
git commit -m "Sync"
git push origin main