from distutils.core import setup #如果没有需要先安装
setup(name='alsolib',  #打包后的包文件名
      version='1.1.20200918',  #版本
      description='爱搜库1.2.20200918，请使用python原版下载,火焰社区通已发布',
      author='asunc',
      author_email='asunc@asunc.cn',
      url='http://asunc.cn',
      py_modules=['alsolib\\alsoapi','alsolib\\alsolib','alsolib\\alsoxes','alsolib\\xespass'],  #与前面的新建文件名一致
)