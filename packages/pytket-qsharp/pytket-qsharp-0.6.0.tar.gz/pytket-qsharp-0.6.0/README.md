# pytket-qsharp

[Pytket](https://cqcl.github.io/pytket) is a Python module for interfacing
with CQC t|ket>, a set of quantum programming tools.

Microsoft's [QDK](https://docs.microsoft.com/en-us/quantum/install-guide) is a
language and associated toolkit for quantum programming.

`pytket-qsharp` is an extension to `pytket` that allows `pytket` circuits to be
executed on simulators and resource estimators from the Microsoft QDK.

## Getting started

`pytket-qsharp` is available for Python 3.6, 3.7 and 3.8, on Linux, MacOS and Windows. To
install, run:

```pip install pytket-qsharp```

In order to use `pytket-qsharp` you will first need to install the `dotnet` SDK
(3.1) and the `iqsharp` tool. On some Linux systems it is also necessary to
modify your `PATH`:

1. See [this page](https://dotnet.microsoft.com/download/dotnet-core/3.1) for
instructions on installing the SDK on your operating system.

2. On Linux, ensure that the `dotnet` tools directory is on your path. Typically
this will be `~/.dotnet/tools`.

3. Run `dotnet tool install -g Microsoft.Quantum.IQSharp`.

4. Run `dotnet iqsharp install --user`.

## Backends provided in this module

This module provides three
[backends](https://cqcl.github.io/pytket/build/html/backends.html), all deriving
from the `pytket` `Backend` class:

* `QsharpSimulatorBackend`, for simulating a general pure-quantum circuit using
the QDK;

* `QsharpToffoliSimulatorBackend`, for simulating a Toffoli circuit using the
QDK;

* `QsharpEstimatorBackend`, for estimating various quantum resources of a
circuit using the QDK. This provides a `get_resources` method, which returns a
dictionary.

## LICENCE

Copyright 2020 Cambridge Quantum Computing

Pytket is licensed under a Non-Commercial Use Software Licence (the "Licence");
you may not use this product except in compliance with the Licence. You may view
the License [here](https://cqcl.github.io/pytket/build/html/licence.html).

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the Licence for the
specific language governing permissions and limitations under the Licence, but
note it is strictly for non-commercial use.
