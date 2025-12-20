import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import book_client
from ..forms import BookReviewForm, SearchForm, SaveBookForm, RemoveSavedBookForm
from ..models import User, Review, SavedBook
from ..utils import current_time
from flask_login import current_user

books = Blueprint("books", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@books.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("books.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@books.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = book_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@books.route("/books/<book_id>", methods=["GET", "POST"])
def book_detail(book_id):
    try:
        result = book_client.retrieve_book_by_id(book_id)
    except ValueError as e:
        return render_template("book_detail.html", error_msg=str(e))

    form = BookReviewForm()
    save_form = SaveBookForm()
    remove_form = RemoveSavedBookForm()
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for("users.login"))
        
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            book_id=book_id,
            book_title=result.title,
        )

        review.save()

        return redirect(request.path)
    
    if save_form.save_book.data and save_form.validate():
        if current_user.is_authenticated:
            saved_book = SavedBook(
                user=current_user._get_current_object(),
                book_id=book_id,
                book_title=result.title,
                book_image=result.imageLink
            )
            saved_book.save()
            return redirect(request.path)
    
    if remove_form.remove_book.data and remove_form.validate():
        if current_user.is_authenticated:
            SavedBook.objects(user=current_user._get_current_object(), book_id=book_id).delete()
            return redirect(request.path)

    reviews = Review.objects(book_id=book_id)
    
    reviews_with_images = []
    for review in reviews:
        review_with_image = {
            'commenter': review.commenter,
            'content': review.content,
            'date': review.date,
            'image': get_b64_img(review.commenter.username) if review.commenter.profile_pic and review.commenter.profile_pic.get() else None
        }
        reviews_with_images.append(review_with_image)

    is_saved = False
    if current_user.is_authenticated:
        saved_book = SavedBook.objects(user=current_user._get_current_object(), book_id=book_id).first()
        is_saved = saved_book is not None

    return render_template("book_detail.html", form=form, book=result, reviews=reviews_with_images, is_saved=is_saved, save_form=save_form, remove_form=remove_form)


@books.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    
    if user is None:
        return render_template("user_detail.html", error="User not found")
    
    image = get_b64_img(username) if user.profile_pic and user.profile_pic.get() else None
    
    reviews = Review.objects(commenter=user)
    
    return render_template("user_detail.html", error=None, image=image, reviews=reviews, user=user)
