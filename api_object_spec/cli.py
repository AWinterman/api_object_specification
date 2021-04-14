import click
import os
import json

from api_object_spec.compile import ApiSpecification


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

    if not spec_file:
        raise click.ClickException("No JSL spec specified:w")

    with open(spec_file[0], 'r') as f:
        spec = ApiSpecification(f.read())
        ctx.obj['spec'] = spec


@click.command()
@click.option('--name', help="the name of the rule you wish to validate against")
@click.argument('file', nargs=1)
@click.pass_context
def validate(ctx, file, name=None):
    with open(file, 'r') as f:
        text = f.read()

    data = json.loads(text)

    spec = ctx.obj['spec']

    results = []

    if name is not None:
        result = spec.validate(name, data)
        results.append((result, name, spec.definitions[name]))
    else:
        for n in spec.definitions:
            result = spec.validate(n, data)
            results.append((result, n, spec.definitions[n],))

    matches = [(name, definitions) for match, name, definitions in results if match]

    if matches:
        click.echo('matches definitions:')

    for name, definitions in matches:
        click.echo('    ' + name)

    if not matches:
        raise click.ClickException(
            'no matches found, tried the following definition names:\n    {}'.format('\n    '.join(n for _, n, _ in results))
        )


@click.command()
def generate(*args, **kwargs):
    pass


cli.add_command(validate)
cli.add_command(generate)

if __name__ == '__main__':
    cli(obj={})

