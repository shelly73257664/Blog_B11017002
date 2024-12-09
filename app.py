from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定義 Article 模型
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# 創建資料庫
with app.app_context():
    db.create_all()

# 主頁，顯示文章列表
@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('home.html', articles=articles)

# 新增文章頁面
@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        new_article = Article(title=title, author=author, content=content)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_article.html')

# 顯示單篇文章
@app.route('/articles/<int:article_id>')
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)

# 編輯文章
@app.route('/articles/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.author = request.form['author']
        article.content = request.form['content']
        db.session.commit()
        return redirect(url_for('article_detail', article_id=article.id))
    return render_template('edit_article.html', article=article)

# 刪除文章
@app.route('/articles/delete/<int:article_id>')
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    
    
import os

port = int(os.getenv('PORT', 8080))  # 從環境變數獲取 PORT，如果未設置則預設為 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)  # 綁定所有網路介面，允許外部訪問
