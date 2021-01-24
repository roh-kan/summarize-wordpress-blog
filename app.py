from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import URLField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import html5 as h5widgets
from utils import fetch, get_query_url

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = '7uPedwa3mOMgs0I8bqIjusQXGpdYFfqx'

# Flask-Bootstrap requires this line
Bootstrap(app)
DEFAULT_MAX_PAGE = 10


@app.route('/', methods=['GET', 'POST'])
def home():
    header = "Summarize WordPress Blog"
    form = NameForm()
    site_url = request.args.get('url')
    base_url = request.base_url

    if request.method == 'GET' and site_url != None:
        number_of_pages = request.args.get('pages')
        if number_of_pages != None:
            try:
                number_of_pages = int(number_of_pages)
            except:
                number_of_pages = 1
            form.number_of_pages.data = number_of_pages
        form.name.data = site_url
        lines = fetch(site_url, number_of_pages)
        query_url = get_query_url(base_url, site_url, number_of_pages)
        return render_template('search.html', pairs=lines, the_title=header, form=form, query_url=query_url)

    elif request.method == 'POST' and form.validate_on_submit():
        site_url = form.name.data
        number_of_pages = form.number_of_pages.data
        if number_of_pages is None:
            number_of_pages = DEFAULT_MAX_PAGE
        lines = fetch(site_url, number_of_pages)
        query_url = get_query_url(base_url, site_url, number_of_pages)
        return render_template('search.html', pairs=lines, the_title=header, form=form, query_url=query_url)

    return render_template('search.html', the_title=header, form=form)


class NameForm(FlaskForm):
    name = URLField('Enter a url for wordpress blog',
                    validators=[DataRequired()], description="e.g. https://www.xyz.com/articles or https://www.xyz.com/blogs")
    number_of_pages = IntegerField('Enter number of pages you want to see',
                                   widget=h5widgets.NumberInput(
                                       min=1, max=100),
                                   validators=[Optional()])

    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run()
