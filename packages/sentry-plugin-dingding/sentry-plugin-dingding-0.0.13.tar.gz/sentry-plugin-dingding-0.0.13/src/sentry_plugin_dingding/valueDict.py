# coding: utf-8
import re

rule = r'\{\{.+\}\}'
markdownMap = {
    u"PROJECT_NAME": u'',
    u"TITLE": u"title",
    u"MESSAGE": u"message",
    u"ENV": u"env",
    u"PLATFORM": u"platform",
    u"DATETIME": u"datetime",
		u"LEVEL": u'level',
		u"RELEASE": u'release'
}

defaultMarkdown = u'''
### {PROJECT_NAME}
#### {TITLE}
{MESSAGE}
[查看详情]({URL})
'''


def formatTemplate(detail, template=defaultMarkdown):
	template = template.format(
		PROJECT_NAME=detail.PROJECT_NAME,
		TITLE=detail.get('title'),
		MESSAGE=detail.get('message').get('formatted'),
		URL=detail.URL,
		ENV=detail.get('environment'),
		PLATFORM=detail.get('platform'),
		DATETIME=detail.get('datetime'),
		RELEASE=detail.get('release'),
	)
	return template
