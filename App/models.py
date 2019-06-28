from App.exts import db

# 分类
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    asname = db.Column(db.String(100), unique=True)
    keyword = db.Column(db.String(100))
    descript = db.Column(db.Text(500))
    fatherid = db.Column(db.String(50), default="无")
    # 添加关联
    atricles = db.relationship('Article', backref='categorys', lazy=True)

# 文章
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text(5000))
    date = db.Column(db.Date)
    keyword = db.Column(db.String(100), default='无')
    descript = db.Column(db.Text(500), default='无')
    categoryid = db.Column(db.Integer, db.ForeignKey(Category.id))

    def __str__(self):
        return self.title + str(self.date)

# 用户
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    tel = db.Column(db.String(50))
    counts = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    logindate = db.Column(db.DateTime)


