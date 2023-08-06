date
aws s3 cp docs/_build/html/ s3://jupyxml-documentation/ --acl public-read --recursive --region "ap-southeast-2" $@
aws cloudfront create-invalidation --distribution-id ELV4WPM59AATK --paths "/*" $@
date
