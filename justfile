set dotenv-load

@serve:
    npx parcel frontend/index.html

@deploy:
    rm -rf .parcel-cache
    rm -rf dist
    npx parcel build frontend/index.html
    aws s3 rm s3://crpts --recursive --include "*" --exclude "epubs/*"
    aws s3 cp dist s3://crpts/ --recursive
    rm -rf dist
    aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_DISTRIBUTION --paths "/*"

@update:
    python src/get_reports.py
