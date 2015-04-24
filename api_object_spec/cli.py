import click
import os
import json

from compile import ApiSpecification

@click.group(name="json-spec")
@click.option('--spec-file', help="A file containing a JSL specification. Fallsback to ./jsl-spec and then ~/.jsl-spec if unspecified.")
@click.pass_context
def cli(ctx, spec_file=None):

    fallbacks = (
        spec_file,
        os.path.join(os.getcwd(), '.jsl-spec'),
        os.path.join(os.getenv('HOME'), '.jsl-spec'),
    )

    spec_file = [file_path for file_path in fallbacks if file_path is not None and os.path.isfile(file_path)]

    with open(spec_file[0], 'r') as f:
        spec = ApiSpecification(f.read())
        ctx.obj['spec'] = spec

@click.command()
@click.option('--name', help="the name of the rule you wish to validate against")
@click.option('--text', help="The text you would like to verify. Required")
@click.pass_context
def validate(text, name=None):

    spec = ctx.obj['spec']

    results = []

    if name is not None:
        result = spec.validate(name, text)
        results.append((result, name, spec.definitions[name]))
    else:
        for n in spec.definitions:
            result = spec.validate(n, text)
            results.append((result, n, spec.definitions[n],))

    matches = [(name, definitions) for match, name, definitions in results if match]

    if matches:
        click.echo('matches definitions:')

    for name, definitios in matches:
        click.echo('    ' + definitions.text)
    else:
        raise click.ClickException(
            'no matches found, tried the following definition names:\n    {}'.format('\n    '.join(n for _, n, _ in results))
        )


cli.add_command(validate)

if __name__ == '__main__':
    cli()








