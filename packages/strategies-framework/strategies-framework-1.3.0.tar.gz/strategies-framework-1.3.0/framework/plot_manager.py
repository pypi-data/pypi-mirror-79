import os

from flask import Flask, render_template


class PlotManager:
    """
    绘图工具
    """

    def __init__(self):
        # 寻求路径
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.BASE_DIR, 'templates')
        self.static_dir = os.path.join(self.BASE_DIR, 'static')

    def plot_show(self):
        # 指定 templates 和 static
        _app = Flask(__name__, template_folder=self.templates_dir, static_folder=self.static_dir)

        def plot():
            strategies = []
            return render_template('k-line.html', strategies=strategies)

        _app.add_url_rule('/', view_func=plot)
        _app.run(host='127.0.0.1', port=9999)
        return _app


if __name__ == '__main__':
    plot = PlotManager()
    plot.plot_show()
