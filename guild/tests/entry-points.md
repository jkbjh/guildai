# Entry points

Various Guild "objects" (internal code resources) are discoverable
using `importlib.metadata`. For details on this module, see the
official Python documentation.

    >>> from importlib.metadata import entry_points

For the tests below we're only interested in resources provided by
Guild itself and not other packages that may be installed on the
system.

Here's a function that returns a sorted list of Guild entry points.

    >>> def guild_entry_points(group, name=None):
    ...   eps = entry_points()
    ...   try:
    ...     group_eps = eps.select(group=group)
    ...   except AttributeError:  # Python <3.10 compatibility
    ...     group_eps = eps.get(group, [])
    ...   return sorted(
    ...     [ep for ep in group_eps
    ...      if (name is None or ep.name == name)
    ...      and ep.dist.name == "guildai"],
    ...     key=lambda ep: ep.name)

Guild uses entry points to discover various resources including
plugins, namespaces, and models. Guid defines its built-in resources
in `PKG_INFO/entry_points.txt` where `PKG_INFO` is the location of the
`guild` package. Other packages can advertise Guild entry points in
their own distributions in the same way.

    >>> pprint(guild_entry_points("guild.plugins"))  # doctest: +REPORT_UDIFF
    [EntryPoint(name='config_flags', value='guild.plugins.config_flags:ConfigFlagsPlugin'...),
     EntryPoint(name='cpu', value='guild.plugins.cpu:CPUPlugin'...),
     EntryPoint(name='dask', value='guild.plugins.dask:DaskPlugin'...),
     EntryPoint(name='disk', value='guild.plugins.disk:DiskPlugin'...),
     EntryPoint(name='dvc', value='guild.plugins.dvc:DvcPlugin'...),
     EntryPoint(name='exec_script', value='guild.plugins.exec_script:ExecScriptPlugin'...),
     EntryPoint(name='gpu', value='guild.plugins.gpu:GPUPlugin'...),
     EntryPoint(name='ipynb', value='guild.plugins.ipynb:NotebookPlugin'...),
     EntryPoint(name='memory', value='guild.plugins.memory:MemoryPlugin'...),
     EntryPoint(name='perf', value='guild.plugins.perf:PerfPlugin'...),
     EntryPoint(name='python_frameworks', value='guild.plugins.python_frameworks:PythonFrameworksPlugin'...),
     EntryPoint(name='python_script', value='guild.plugins.python_script:PythonScriptPlugin'...),
     EntryPoint(name='quarto_document', value='guild.plugins.quarto_document:QuartoDocumentPlugin'...),
     EntryPoint(name='queue', value='guild.plugins.queue:QueuePlugin'...),
     EntryPoint(name='r_script', value='guild.plugins.r_script:RScriptPlugin'...),
     EntryPoint(name='resource_flags', value='guild.plugins.resource_flags:ResourceFlagsPlugin'...),
     EntryPoint(name='skopt', value='guild.plugins.skopt:SkoptPlugin'...)]
