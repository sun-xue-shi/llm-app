import uuid
from dataclasses import dataclass

from injector import inject

from internal.model import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        # 使用数据库的自动提交功能
        with self.db.auto_commit():
            # 创建一个App对象，参数为name、icon、description和account_id
            app = App(name="test", icon="", description="test_desc", account_id=uuid.uuid4())
            # 将App对象添加到数据库会话中
            self.db.session.add(app)
        # 返回创建的App对象
        return app

    # 定义一个函数，用于获取指定id的应用
    def get_app(self, id: uuid.uuid4()) -> App:
        # 从数据库会话中查询指定id的应用
        return self.db.session.query(App).get(id)

    def del_app(self, id: uuid.uuid4()) -> App:
        # 使用with语句自动提交数据库事务
        with self.db.auto_commit():
            # 获取要删除的应用
            app = self.get_app(id)
            # 删除应用
            self.db.session.delete(app)
        # 返回删除的应用
        return app

    def update_app(self, id: uuid.uuid4()) -> App:
        # 使用with语句自动提交数据库事务
        with self.db.auto_commit():
            # 根据id获取app对象
            app = self.get_app(id)
            # 修改app对象的name属性
            app.name = "test_update"
        # 返回修改后的app对象
        return app
