from soup import get_reviews
from make_csv import save_to_file

reviews = get_reviews()
save_to_file(reviews)