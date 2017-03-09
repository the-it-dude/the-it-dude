import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class Blog(object):
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('./src'),
            autoescape=select_autoescape(['html'])
        )

    def render(self, source, destination, context):
        """
        Simply glue files together.
        """
        logger.info("Rendering file: {} > {}".format(source, destination))
        logger.debug(" Context: {}".format(repr(context)))
        template = self.env.get_template(source)
        template.stream(**context).dump(destination)

    def render_all(self, config):
        for file_config in config['files']:
            self.render(
                source=file_config['source'],
                destination=file_config['destination'],
                context={}
            )


if __name__ == '__main__':
    blog = Blog()
    blog.render_all(dict(
        files=[
            dict(source='index.html',
                 destination='index.html')
        ]
    ))
