from flask import Flask, render_template, flash, request
from bs4 import BeautifulSoup
import requests
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Optional

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = '7uPedwa3mOMgs0I8bqIjusQXGpdYFfqx'

# Flask-Bootstrap requires this line
Bootstrap(app)
DEFAULT_MAX_PAGE = 10


@app.route('/', methods=['GET', 'POST'])
def home():
    header = "Summarize Wordpress Blog"
    form = NameForm()
    if form.validate_on_submit():
        siteurl = form.name.data
        noOfPages = form.noOfPages.data
        if noOfPages is None:
            noOfPages = DEFAULT_MAX_PAGE
        lines = fetch(siteurl, noOfPages)

        return render_template('search.html', pairs=lines, the_title=header, form=form)
    return render_template('search.html', the_title=header, form=form)


def fetch(url, noOfPages):
    lines = []
    try:
        for i in range(1, noOfPages + 1):
            r = requests.get(str(url) + '/page/'+str(i))
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.content, 'html.parser')

            articles = soup.findAll("article")  # class_="entry-title")
            for article in articles:
                childHead = article.find(class_="entry-title").contents[0]
                childBody = article.find(class_="entry-content").p
                row = {"link": childHead.get(
                    "href"), "title": childHead.get_text(), "summary": childBody.get_text()}
                lines.append(row)
    except:
        lines = None

    return lines


class NameForm(FlaskForm):
    name = URLField('Enter a url for wordpress blog',
                    validators=[DataRequired()], description="https://www.xyz.com/articles or https://www.xyz.com/blogs")
    noOfPages = IntegerField(
        'Enter number of pages you want to see', validators=[Optional()])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run()
