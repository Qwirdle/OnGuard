from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *

from __main__ import app

# For next button, to detect going to the next chapter
articlesPerChapter = [3, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3]

@app.route('/articles/<int:chapter>/<int:article>')
@login_required
def viewArticle(chapter, article):
    # Check if next is going to next chapter, and if so increment
    if articlesPerChapter[chapter - 1] < article:
        article = 1
        chapter +=1
    try: # Try in order to handle accessing false articles (especially over URLs)
        if articlesPerChapter[chapter-1] < article:
            return render_template(f'articles/{chapter}/{article}.html', article=article+1, chapter=1)
        else:
            return render_template(f'articles/{chapter}/{article}.html', article=article, chapter=chapter)
    except:
        return render_template('error.html', message="Oops! Article not found."), 404