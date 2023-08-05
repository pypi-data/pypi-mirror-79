from beam import Site

import logging
import click
import yaml
import os

logger = logging.getLogger(__name__)

@click.command("build")
@click.option("--site", default="site.yml")
def build(site):
    if not os.path.exists(site):
        logger.error("Site {} not found!".format(site))
        return -1
    with open(site) as input_file:
        config = yaml.load(input_file.read())

    site = Site(config)

#    loader = FileLoader(paths=templates+('',))
#    env = Environment(loader)  
#    heresy_context = RenderContext(context)
#    heresy_tmpl = env.get_template(filename)
#    heresy_tmpl.compile()
#    res = heresy_tmpl.render(heresy_context)
