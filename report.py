"""

author: nukestye
version: v0.1.0
description:  Generates a html report based on inputs given using template builder Jinja.

"""

import os   
import webbrowser

from jinja2 import (Environment, 
                    PackageLoader, 
                    select_autoescape, 
                    Template)


def make_env() -> Environment:
    """
    Generates the enviroment needed for Jinja

    ### Returns
        - Environment
            - Jinja environment variable

    """
    env = Environment(
        loader=PackageLoader("pcs-crawler"),
        autoescape=select_autoescape()
    )

    return env

def render_report(template: Template, **vars) -> None:
    """
    Renders the report.

    Report is rendered using variables that passed through a dictionary.
    Takes in a Template type that controls the rendering process.


    ### Arguments
        1. `template` Template: Template type variable that is used to render the html
        2. `**vars` dict: The variables used to render html file

    ### Returns
        Nothing

    """

    with open('out/output.html', 'w') as f:
        print(template.render(vars), file = f)


def make_report():
    """
    Generates the report based using Jinja.
    """
    
    # Grab the env for Jinja
    env = make_env();

    template = env.get_template('default.html')

    render_report(template, test=1)

    webbrowser.open_new_tab('file://' + os.path.realpath( './out/output.html'))
