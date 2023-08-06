from ..backends.make import writer as make
from ..backends.ninja import writer as ninja
from ..build_inputs import build_input
from ..iterutils import listify
from ..path import Path


@build_input('regenerate')
class Regenerate:
    def __init__(self, build_inputs, env):
        self.outputs = []
        self.depfile = None


@make.post_rule
def make_regenerate_rule(build_inputs, buildfile, env):
    bfg9000 = env.tool('bfg9000')

    make.multitarget_rule(
        build_inputs, buildfile,
        targets=[Path('Makefile')] + build_inputs['regenerate'].outputs,
        deps=build_inputs.bootstrap_paths + listify(env.toolchain.path),
        recipe=[bfg9000(Path('.'))],
        clean_stamp=False
    )


@ninja.post_rule
def ninja_regenerate_rule(build_inputs, buildfile, env):
    bfg9000 = env.tool('bfg9000')

    rule_kwargs = {}
    if ninja.features.supported('console', env.backend_version):
        rule_kwargs['pool'] = 'console'
    buildfile.rule(
        name='regenerate',
        command=bfg9000(Path('.')),
        generator=True,
        depfile=build_inputs['regenerate'].depfile,
        **rule_kwargs
    )
    buildfile.build(
        output=[Path('build.ninja')] + build_inputs['regenerate'].outputs,
        rule='regenerate',
        implicit=build_inputs.bootstrap_paths + listify(env.toolchain.path)
    )
