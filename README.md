# Doc Tagger
## Installation

Create environment if not already present:

`conda create <env name>`

Activate environment:

`source activate <env name>`

Install dependencies:

`pip install -r requirements.txt`

`python -m spacy download en_core_web_lg`

Download and install Neo4j Desktop. See asset/demo.mp4 for demonstration of this feature in action.

Run app on the flask test server `python app.py`

### Test inputs for curl:

Test the schema object generator for knowledge snippets

`curl -H "Content-Type: application/json" -X POST -d '{"schema": "Generative adversarial networks (GANs) are an expressive class of neural generative models with tremendous success in modeling high-dimensional continuous measures. In this paper, we present a scalable method for unbalanced optimal transport (OT) based on the generative-adversarial framework. We formulate unbalanced OT as a problem of simultaneously learning a transport map and a scaling factor that push a source measure to a target measure in a cost-optimal manner. In addition, we propose an algorithm for solving this problem based on stochastic alternating gradient updates, similar in practice to GANs. We also provide theoretical justification for this formulation, showing that it is closely related to an existing static formulation by Liero et al. (2018), and perform numerical experiments demonstrating how this methodology can be applied to population modeling."}' http://0.0.0.0:5000/`

Test the regular tagger for node compatible nouns and named entities

`curl -H "Content-Type: application/json" -X POST -d '{"tags": "Generative adversarial networks (GANs) are an expressive class of neural generative models with tremendous success in modeling high-dimensional continuous measures. In this paper, we present a scalable method for unbalanced optimal transport (OT) based on the generative-adversarial framework. We formulate unbalanced OT as a problem of simultaneously learning a transport map and a scaling factor that push a source measure to a target measure in a cost-optimal manner. In addition, we propose an algorithm for solving this problem based on stochastic alternating gradient updates, similar in practice to GANs. We also provide theoretical justification for this formulation, showing that it is closely related to an existing static formulation by Liero et al. (2018), and perform numerical experiments demonstrating how this methodology can be applied to population modeling."}' http://0.0.0.0:5000/`