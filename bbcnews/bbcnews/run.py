from scrapy import cmdline


name = 'bbc'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())