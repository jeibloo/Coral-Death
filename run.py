# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import index, process

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar

NavbarSimple consists of a 'brand' on the left, to which you can attach a link
with brand_href, and a number nav items as its children. NavbarSimple will
collapse on smaller screens, and add a toggle for revealing navigation items.

brand (string, optional): Brand text, to go top left of the navbar.
brand_href (string, optional): Link to attach to brand.
children (a list of or a singular dash component, string or number, optional): The children of this component
color (string, optional): Sets the color of the NavbarSimple. Main options are primary, light and dark, default light. You can also choose one of the other contextual classes provided by Bootstrap (secondary, success, warning, danger, info, white) or any valid CSS color of your choice (e.g. a hex code, a decimal code or a CSS color name)
dark (boolean, optional): Applies the `navbar-dark` class to the NavbarSimple, causing text in the children of the Navbar to use light colors for contrast / visibility.
light (boolean, optional): Applies the `navbar-light` class to the NavbarSimple, causing text in the children of the Navbar to use dark colors for contrast / visibility.
sticky (string, optional): Stick the navbar to the top or the bottom of the viewport, options: top, bottom. With `sticky`, the navbar remains in the viewport when you scroll. By contrast, with `fixed`, the navbar will remain at the top or bottom of the page.
"""

navbar = dbc.NavbarSimple(
    brand='Coral Death',
    brand_href='/',
    children=[
        dbc.NavItem(dcc.Link('Process', href='/process', className='nav-link')),
    ],
    color=None,
    light=True, #This is for the text
    dark=False
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Jason Nova', className='mr-4 name'),
                    html.A(html.I(className='fas fa-envelope-square mr-3'), href='mailto:jasonnova@protonmail.com'),
                    html.A(html.I(className='fab fa-github-square mr-3'), href='https://github.com/jeibloo/coral-death'),
                    html.A(html.I(className='fab fa-linkedin mr-3'), href='https://www.linkedin.com/in/jason-nova/'),
                    html.A(html.I(className='fab fa-twitter-square mr-3'), href='https://twitter.com/jsn404'),
                    html.A(html.I(className='fas fa-paw mr-3'), href='https://www.worldwildlife.org/initiatives/oceans'),
                ],
                className='lead',
            )
        ),
        align='end'
    ),
    className='footer'
)

# For more explanation, see:
# Plotly Dash User Guide, URL Routing and Multiple Apps
# https://dash.plot.ly/urls

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className='mt-6'),
    footer
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/process':
        return process.layout
    else:
        return dcc.Markdown('## Page not found')

if __name__ == '__main__':
    app.run_server(debug=True)
