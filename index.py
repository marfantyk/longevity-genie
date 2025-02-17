import os
import click
import dotenv

from click import Context
from dotenv import load_dotenv

from genie.config import Locations
from genie.calls import longevity_gpt
from genie.indexing import *

e = dotenv.find_dotenv()
print(f"environment found at {e}")
has_env: bool = load_dotenv(e, verbose=True)
if not has_env:
    print("Did not found environment file, using system OpenAI key (if exists)")
openai_key = os.getenv('OPENAI_API_KEY')
#print(f"OPENAI key is {openai_key}")

@click.group(invoke_without_command=False)
@click.pass_context
def app(ctx: Context):
    #if ctx.invoked_subcommand is None:
    #    click.echo('Running the default command...')
    #    test_index()
    pass

@app.command("write")
@click.option('--model', default='gpt-3.5-turbo', help='model to use, gpt-3.5-turbo by default')
@click.option('--base', default='.', help='base folder')
def write(model: str, base: str):
    load_dotenv()
    locations = Locations(Path(base))
    index = Index(locations, model)
    print("saving modules and papers")
    index.with_modules().with_papers().persist()

@app.command("longevity_gpt")
@click.option('--question', default='What is aging?', help='Question to be asked')
def longevity_gpt_command(question: str):
    return longevity_gpt(question, [])


@app.command("test")
@click.option('--chain', default="map_reduce", type=click.Choice([ "stuff", "map_reduce", "refine", "map_rerank"], case_sensitive=True), help="chain type")
@click.option('--process', default="split", help="preprocessing type")
@click.option('--search', default='similarity', help='search type')
@click.option('--base', default='.', help='base folder')
def test_index(chain: str, process: str,  search: str, base: str):
    locations = Locations(Path(base))
    index = Index(locations.paper_index, "gpt-3.5-turbo", chain_type=chain, search_type=search) #Index(locations, "gpt-4")
    question1 = f"There are rs4946936, rs2802290, rs9400239, rs7762395, rs13217795 genetic variants in FOXO gene, explain their connection with aging and longevity"
    print(f"Q1: {question1}")
    answer1 = index.query_with_sources(question1, [])
    print(f"A1: {answer1}")

#prompt=PromptTemplate.from_template('tell us a joke about {topic}')
if __name__ == '__main__':
    app()