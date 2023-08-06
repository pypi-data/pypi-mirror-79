<h1 align="center">agine <br>
  <a href="https://github.com/ZenithClown/agine/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ZenithClown/agine?style=plastic"></a>
  <a href="https://github.com/ZenithClown/agine/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ZenithClown/agine"></a>
  <br>
  <a href = "https://www.linkedin.com/in/dpramanik/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/linkedin.svg"/></a>
	<a href = "https://github.com/ZenithClown"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/github.svg"/></a>
	<a href = "https://gitlab.com/ZenithClown/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/gitlab.svg"/></a>
	<a href = "https://www.researchgate.net/profile/Debmalya_Pramanik2"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/researchgate.svg"/></a>
	<a href = "https://www.kaggle.com/dPramanik/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/kaggle.svg"/></a>
	<a href = "https://app.pluralsight.com/profile/Debmalya-Pramanik/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/pluralsight.svg"/></a>
	<a href = "https://stackoverflow.com/users/6623589/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/stackoverflow.svg"/></a>
</h1>

<p align="justify"><i>agine</i> is a Python package which have functionalities related to points in an n-dimensional space (which is defined by its <code>x, y, ...z</code> coordinates), or an actual position on the Earth (given by its <code>latitude, longitude</code>). Considering two points (<code>say P, Q</code>), apart from many other purposes, this library can also detect if the two have a clear line of sight or not.
</p>

## Basic Usage

<p align="justify">agine has <b>three</b> main functionalities: (1) Calculation of Distances, using different metrics, which is defined under <code>commons</code>, (2) Functions to Find the Nearest Neighbor and (3) Function to Find if two Geographic Point has a <i>Line-of-Sight</i> or not. All of this can be done using the following:</p>

```bash
git clone https://github.com/ZenithClown/agine.git
cd agine # as agine is currently not indexed in PyPi
```

```python
pip install agine # Installing agine with pip
import agine
>> Setting up agine-Environment...
>>   Detected OS            : "<os-name-with-version>"
>>   scikit-learn Options   : "<is-scikit-learn-available>"
>>   "etc. which Defines the Core-Capability"
```

<p align="justify">agine has a hard dependency of only <code>numpy</code> so that some of its functionalities can be used somewhere else. For options (2) and (3) it has different requirements, which can be accessed using: <code>agine.OSOptions._point_func</code> and <code>agine.OSOptions._line_of_st</code> repectively.</p>
