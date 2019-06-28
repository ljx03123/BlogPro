import datetime
import time
from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for, session
from App.models import *

blue = Blueprint('blog', __name__)

# 博客首页
@blue.route('/')
def index():
    cats = Category.query.all()
    return render_template('home/index.html', cats=cats)


# 博客首页栏目跳转
@blue.route('/categroy-list/<int:cid>')
def category_list(cid):
    cats = Category.query.all()
    for cat in cats:
        cat.count = Article.query.filter_by(categoryid=cat.id).count()
        db.session.commit()
    arts = Article.query.filter_by(categoryid=cid)
    return render_template('home/category_list.html', cats=cats, arts=arts)


# 博客文章内容跳转
@blue.route('/article_detail/<int:aid>')
def article_detail(aid):
    cats = Category.query.all()
    arts = Article.query.filter_by(id=aid)
    return render_template('home/category_list.html', cats=cats, arts=arts)


# 后台首页
@blue.route("/admin/", methods=['GET', 'POST'])
def admin():
    times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # 获取当前时间
    if not session.get('username'):    # 判断是否已经登录
        return redirect(url_for('blog.admin_login'))
    counts = len(Article.query.all())
    username = session.get('username', "未登录")       # 获取登录状态
    user = User.query.filter_by(username=username).first()
    return render_template('admin/index.html', counts=counts, username=username, user=user, times=times)


# 后台登录
@blue.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.pop('username', '')     # 退出登录后，在再次登录前删除sessiong
    user = User.query.first()
    user.logindate = user.date         # 在登录前将记录的上次登录时间date传递给上一次登录时间logindate
    db.session.commit()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('userpwd')
        users = User.query.filter_by(username=username, password=password)
        if users.count() > 0:     # 判断用户名及密码是否存在
            session['username'] = username
            user.counts += 1    # 统计登陆的总次数
            user.date = times    # 记录本次登录的时间
            db.session.commit()
            return redirect(url_for('blog.admin'))
        time.sleep(0.5)
        return redirect(url_for('blog.admin_login'))
    return render_template('admin/login.html', user=user)


# 显示栏目内容（类名）
@blue.route('/update-category/<int:catid>', methods=['POST', "GET"])
def update_category(catid):
    cats = Category.query.all()
    cat = Category.query.filter_by(id=catid).first()
    return render_template('admin/update-category.html', cats=cats, cat=cat, catid=catid)


# 后台增加栏目功能
@blue.route('/category/', methods=['POST', 'GET'])
def category():
    cats = Category.query.all()
    counts = len(cats)
    if request.method == "POST":
        name = request.form.get('name')
        asname = request.form.get('alias')
        fatherid = request.form.get('fid')
        keyword = request.form.get('keywords')
        descript = request.form.get('describe')
        c = Category()
        c.name = name
        c.asname = asname
        c.keyword = keyword
        c.fatherid = fatherid
        c.descript = descript
        try:
            db.session.add(c)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        return redirect(url_for('blog.category'))
    return render_template('admin/category.html', cats=cats, counts=counts)


# 删除栏目
@blue.route('/delete_category/<int:caid>')
def delete_category(caid):
    cats = Category.query.all()
    c = Category.query.filter_by(id=caid).first()
    if request.method == 'GET':
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for('blog.category'))
    return render_template('admin/category.html', cats=cats)


# 修改栏目
@blue.route('/update_content/<int:caid>', methods=['POST', "GET"])
def update_content(caid):
    cats = Category.query.all()
    cat = Category.query.filter_by(id=caid).first()
    if request.method == "POST":
        name = request.form.get('name')
        asname = request.form.get('alias')
        fatherid = request.form.get('fid')
        keyword = request.form.get('keywords')
        descript = request.form.get('describe')
        cat.name = name
        cat.asname = asname
        cat.keyword = keyword
        cat.fatherid = fatherid
        cat.descript = descript
        db.session.commit()
        return redirect(url_for('blog.category'))
    return render_template('admin/category.html')


# 后台文章管理、分页功能
@blue.route('/article/')
def article():
    counts = Article.query.count()
    per_page = 5       # 每页显示文章的篇数为5篇
    pages = ceil(counts/5)      # 获取分页的总页数
    page = request.args.get('page')   # 获取当前页码
    if not page:           # 跳转到文章首页时，默认分页在第一页
        page = 1
    arts = Article.query.order_by(Article.date).paginate(int(page), 5, False).items
    return render_template('admin/article.html', arts=arts, counts=counts, pages=pages, pag=int(page))


# 删除文章
@blue.route('/delete_article/<int:aid>')
def delete_article(aid):
    a = Article.query.filter_by(id=aid).first()
    if request.method == 'GET':
        db.session.delete(a)
        db.session.commit()
        return redirect(url_for('blog.article'))
    return render_template('admin/article.html')


# 后台增加文章
@blue.route('/add-article/', methods=['POST', "GET"])
def add_article():
    times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cats = Category.query.all()
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('content').split('>')[1].split('<')[0]     # 字符串的切片处理
        keyword = request.form.get('keywords')
        descript = request.form.get('describe')
        categoryid = request.form.get('category')
        date = request.form.get('time')
        a = Article()
        print(text)
        a.title = title
        a.text = text
        a.keyword = keyword
        a.descript = descript
        a.categoryid = categoryid
        a.date = date
        try:
            db.session.add(a)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        return redirect(url_for('blog.article'))
    return render_template('admin/add-article.html', cats=cats, times=times)


# 后台修改文章
@blue.route('/update-article/<int:aid>', methods=["GET", "POST"])
def update_article(aid):
    times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arts = Article.query.all()
    cats = Category.query.all()
    art = Article.query.get(aid)
    cat = Category.query.get(art.categoryid)
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('content').split('>')[1].split('<')[0]
        keyword = request.form.get('keywords')
        descript = request.form.get('describe')
        categoryid = request.form.get('category')
        art.title = title
        art.text = text
        art.keyword = keyword
        art.descript = descript
        art.categoryid = categoryid
        db.session.commit()
        return redirect(url_for('blog.article'))
    return render_template('admin/update-article.html', cats=cats, arts=arts, art=art, cat=cat, times=times)
