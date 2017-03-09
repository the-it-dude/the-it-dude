import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

CONFIG_FILE = 'blog.yml'


class Blog(object):
    def __init__(self, config):
        self.env = Environment(
            loader=FileSystemLoader('./src'),
            autoescape=select_autoescape(['html'])
        )
        self.config = config

    def render(self, source, destination, context=None):
        """
        Simply glue files together.
        """
        full_context = config.get('context', {})

        if context is not None:
            full_context.update(context)

        logger.info("Rendering file: {} > {}".format(source, destination))
        logger.debug(" Context: {}".format(repr(context)))
        template = self.env.get_template(source)
        template.stream(**full_context).dump(destination)

    def render_all(self):
        for file_config in self.config['files']:
            self.render(
                source=file_config['source'],
                destination=file_config['destination'],
                context=file_config.get('context', None)
            )


if __name__ == '__main__':
    with open(CONFIG_FILE, 'r') as config_file:
        config = yaml.load(config_file)

    logger.debug("Config: {}".format(repr(config)))
    blog = Blog(config)
    blog.render_all()
