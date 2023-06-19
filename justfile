@serve:
    npx parcel frontend/index.html

@deploy:
    npx parcel build frontend/index.html
    aws s3 rm s3://crpts --recursive --include "*" --exclude "epubs/*"
    aws s3 cp dist s3://crpts/ --recursive
    rm -rf dist/

@update:
    python src/get_reports.py
