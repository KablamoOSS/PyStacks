PyStacks
--------

Python AWS stack creation.

N.B. this is just for modifying this code and you will need to use the latest docker image if you want to run anything

Pystacks helps with the creation of Cloudformation templates. It is assumed that you know what cloudformation is and how it works before you attempt to make changes in here https://aws.amazon.com/cloudformation/

Pystacks is a thin wrapper on top of cloudformation and the AWS API. It takes in definition YML templates (hereafter referred to as stacks) and converts them into either a cloudformation JSON file or calls the Amazon API to create/modify/delete resources. The stack files live in different projects where appropriate for each desired environment.

To see how it works have a look inside PyStacks/configs/cftemplates/resources/ and look though the JSON files that exist in there. There are different ones for each product that AWS offers. The templates are written using the Jinja template language http://jinja.pocoo.org/ which is similar to the Python Django template language.

An overview of how this works:

User Defined YML Stack File -> Pystacks -> Merged with resource template -> Cloudformation File

Where the user defined YML file is merged into the resource template which produces a cloudformation file if it is valid JSON. You can view this output by looking inside the compiled folder where you ran the command to merge the templates.

Some functionality in PyStacks such as Route 53 use direct API calls and as such there is no output. They should print what they have done to standard output for you to inspect what has happened.

If you want to trace the code start by looking inside tasks.py which is the task runner for Pystacks and as such the entry point for all actions. Most of the logic however lives inside the templates which is where you should focus your attention.



Requirements
------------
 - Python 2.7
 - pip (requirements are in requirements.txt for production and requirements_test.txt for testing)
 - git

Not required but useful

 - Docker
 - pep8 (for linting)

Before Commiting
----------------

Run the following command

	./commit_check.sh

Otherwise face the shame of having broken the build!

Run Locally
-----------

Build a local copy

	docker build -t pystacks -f Dockerfile .

Or build using proxy

	docker build -t pystacks -f Dockerfile --build-arg http_proxy=http://PROXYSERVER:PROXYPORT --build-arg https_proxy=https://PROXYSERVER:PROXYPORT .

Then to generate example templates

	docker run -v $(pwd)/Pystacks:/opt/app pystacks generateTemplate iam_policies aps2

Note: Pystacks expects a configs/user/ folder in the root directory

	docker run -v $(pwd):/opt/app/configs/user/ pystacks generateTemplate iam_policies aps2

Remove Unlinked Containers
------------

docker rmi $(docker images | awk '/<none>/ {print $3}')

Git Hash Support
------------

	docker run -v $(pwd):/opt/app/configs/user/ pystacks generateTemplate iam_policies aps2 --githash=<git shorthash>

Must be called as a named optional variable.


Unit testing
------------

Please expand on tests.

Read http://www.voidspace.org.uk/python/mock/ for details on how to use mocks

Running tests
-------------
##### To run locally (must run from root of project),

If you don't have test dependencies installed, install them first:

    pip install -t .pip -r requirements_test.txt

then run

    pytest --pyargs PyStacks -s

or

    python ./.pip/pytest.py --pyargs PyStacks -s

##### To run in docker

	docker build -t pystacks-test -f Dockerfile.test .

##### To run with proxy

	docker build -t pystacks-test -f Dockerfile.test --build-arg http_proxy=http://PROXYSERVER:PROXYPORT --build-arg https_proxy=https://PROXYSERVER:PROXYPORT .

Code Check
----------

To run in docker

	docker build -t pystacks-check -f Dockerfile.check .

To run with proxy

	docker build -t pystacks-check -f Dockerfile.check --build-arg http_proxy=http://PROXYSERVER:PROXYPORT --build-arg https_proxy=https://PROXYSERVER:PROXYPORT .


Code Coverage
-------------

To run in docker

	docker build -t pystacks-coverage -f Dockerfile.coverage .

To run with proxy

	docker build -t pystacks-coverage -f Dockerfile.coverage --build-arg http_proxy=http://PROXYSERVER:PROXYPORT --build-arg https_proxy=https://PROXYSERVER:PROXYPORT .

To generate a coverage report run

	make coverageLocal


Python 3 Conversion
-------------------

Please write code which allows an easy conversion to Python 3. This is still work in progress but to do so run the following,

	docker build -t pystacks-test -f Dockerfile.test . && docker build -t pystacks-test -f Dockerfile.Python3.test .

Or

	docker build -t pystacks-test -f Dockerfile.test --build-arg http_proxy=http://PROXYSERVER:PROXYPORT --build-arg https_proxy=https://PROXYSERVER:PROXYPORT . && docker build -t pystacks-test -f Dockerfile.Python3.test --build-arg http_proxy=http://PROXYSERVER:PROXYPORT --build-arg https_proxy=https://PROXYSERVER:PROXYPORT .


Pipeline
--------

Look at bitbucket-pipelines.yml

Generate Template
-----------------

