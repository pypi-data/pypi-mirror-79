from . import builtin
from .. import versioning as v
from ..build_inputs import build_input
from ..objutils import objectify

build_input('required_version')(
    lambda build_inputs, env: v.PythonSpecifierSet('')
)


@builtin.function(context='*')
def bfg9000_required_version(context, version=None, python_version=None):
    version = objectify(version or '', v.PythonSpecifierSet, prereleases=True)
    python_version = objectify(python_version or '', v.PythonSpecifierSet,
                               prereleases=True)

    v.check_version(v.bfg_version, version, kind='bfg9000')
    v.check_version(v.python_version, python_version, kind='python')
    context.build['required_version'] &= version


@builtin.getter(context='*')
def bfg9000_version(context):
    return v.bfg_version
