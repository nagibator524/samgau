from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///election_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели данных
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Админ логин (в реальном проекте используйте хеширование паролей)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route('/')
def index():
    news = News.query.order_by(News.created_at.desc()).limit(3).all()
    about = About.query.first()
    team = Team.query.all()
    return render_template('index.html', news=news, about=about, team=team)

@app.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    news_list = News.query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('news.html', news=news_list.items)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    article = News.query.get_or_404(news_id)
    all_news = News.query.order_by(News.created_at.desc()).limit(10).all()
    return render_template('news_detail.html', article=article, news=all_news)

@app.route('/about')
def about():
    about_content = About.query.first()
    return render_template('about.html', about=about_content)

@app.route('/team')
def team():
    team_members = Team.query.all()
    return render_template('team.html', team=team_members)

# Админ панель
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Неверные учетные данные!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    news_count = News.query.count()
    team_count = Team.query.count()
    return render_template('admin/dashboard.html', news_count=news_count, team_count=team_count)

# Управление новостями
@app.route('/admin/news')
def admin_news():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/news.html', news=news_list)

@app.route('/admin/news/create', methods=['GET', 'POST'])
def create_news():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = request.form['image_url']
        
        news = News(title=title, content=content, image_url=image_url)
        db.session.add(news)
        db.session.commit()
        
        flash('Новость успешно создана!', 'success')
        return redirect(url_for('admin_news'))
    
    return render_template('admin/create_news.html')

@app.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
def edit_news(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    news = News.query.get_or_404(id)
    
    if request.method == 'POST':
        news.title = request.form['title']
        news.content = request.form['content']
        news.image_url = request.form['image_url']
        news.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Новость успешно обновлена!', 'success')
        return redirect(url_for('admin_news'))
    
    return render_template('admin/edit_news.html', news=news)

@app.route('/admin/news/delete/<int:id>')
def delete_news(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    
    flash('Новость успешно удалена!', 'success')
    return redirect(url_for('admin_news'))

# Управление командой
@app.route('/admin/team')
def admin_team():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    team_list = Team.query.all()
    return render_template('admin/team.html', team=team_list)

@app.route('/admin/team/create', methods=['GET', 'POST'])
def create_team_member():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        description = request.form['description']
        image_url = request.form['image_url']
        
        member = Team(name=name, position=position, description=description, image_url=image_url)
        db.session.add(member)
        db.session.commit()
        
        flash('Член команды успешно добавлен!', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/create_team.html')

@app.route('/admin/team/edit/<int:id>', methods=['GET', 'POST'])
def edit_team_member(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    member = Team.query.get_or_404(id)
    
    if request.method == 'POST':
        member.name = request.form['name']
        member.position = request.form['position']
        member.description = request.form['description']
        member.image_url = request.form['image_url']
        
        db.session.commit()
        flash('Член команды успешно обновлен!', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/edit_team.html', member=member)

@app.route('/admin/team/delete/<int:id>')
def delete_team_member(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    member = Team.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    
    flash('Член команды успешно удален!', 'success')
    return redirect(url_for('admin_team'))

# Управление страницей "О нас"
@app.route('/admin/about', methods=['GET', 'POST'])
def admin_about():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    about_content = About.query.first()
    
    if request.method == 'POST':
        if about_content:
            about_content.title = request.form['title']
            about_content.content = request.form['content']
            about_content.updated_at = datetime.utcnow()
        else:
            about_content = About(
                title=request.form['title'],
                content=request.form['content']
            )
            db.session.add(about_content)
        
        db.session.commit()
        flash('Страница "О нас" успешно обновлена!', 'success')
        return redirect(url_for('admin_about'))
    
    return render_template('admin/about.html', about=about_content)

# Инициализация базы данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)