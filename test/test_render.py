from src.render import render_info, render_article
from src.render.plugins import All
from src.settings import DEFAULT_CORPUS

assert render_info("""---
title: YAML测试
date: 2018-09-15
update: 2018-09-15
tags: Markdown
corpus:
summary:
recommend: true
---
TEST
""") == ({'title': 'YAML测试', 'date': '2018-09-15', 'update': '2018-09-15', 'tags': ['Markdown'], 'corpus': DEFAULT_CORPUS, 'summary': '', "recommend": "true"}, '\nTEST\n')

assert render_info("""---
title: YAML测试
date: 2018-09-15
update: 2018-09-15
tags: 
corpus: 测试
summary:
---
TEST
""") == ({'title': 'YAML测试', 'date': '2018-09-15', 'update': '2018-09-15', 'tags': [], 'corpus': '测试', 'summary': ''}, '\nTEST\n')

assert render_info("""---
<title>XML测试</title>
<date>2018-09-15</date>
<update>2018-09-15</update>
<tags>Markdown</tags>
<corpus></corpus>
<permalink></permalink>
---

TEST
""") == ({'title': 'XML测试', 'date': '2018-09-15', 'update': '2018-09-15', 'tags': ['Markdown'], 'corpus': DEFAULT_CORPUS, 'permalink': ''}, '\n\nTEST\n')

assert render_info("""---
<title>XML测试</title>
<date>2018-09-15</date>
<update>2018-09-15</update>
<tags></tags>
<corpus>测试</corpus>
<permalink></permalink>
---

TEST
""") == ({'title': 'XML测试', 'date': '2018-09-15', 'update': '2018-09-15', 'tags': [], 'corpus': '测试', 'permalink': ''}, '\n\nTEST\n')
