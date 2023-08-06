# coding: utf-8
import re

rule = r'\{\{.+\}\}'
markdownMap = {
    u"PROJECT_NAME": u'',
    u"TITLE": u"title",
    u"MESSAGE": u"message",
    u"ENV": u"env",
    u"PLATFORM": u"platform",
		u"LEVEL": u'level'
}

defaultMarkdown = u'''
### {PROJECT_NAME}
#### {TITLE}
{MESSAGE}
[查看详情]({URL})
'''


def formatTemplate(detail, template=defaultMarkdown):
	template = template.format(
		PROJECT_NAME=detail.get('PROJECT_NAME'),
		TITLE=detail.get('title'),
		MESSAGE=detail.get('logentry').formatted,
		URL=detail.get('URL'),
		ENV=detail.get('environment'),
		PLATFORM=detail.get('platform'))
	return template
