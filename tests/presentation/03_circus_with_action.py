from datagenerator.core import circus
from datagenerator.core.circus import *
from datagenerator.core.actor import *
import datagenerator.core.util_functions as util_functions
from tabulate import tabulate


util_functions.setup_logging()

logging.info("building circus")


def create_circus_with_actor():
    example_circus = circus.Circus(
        name="example",
        master_seed=12345,
        start=pd.Timestamp("1 Jan 2017 00:00"),
        step_duration=pd.Timedelta("1h"))

    person = example_circus.create_actor(
        name="person", size=1000,
        ids_gen=SequencialGenerator(prefix="PERSON_"))

    person.create_attribute(
        "NAME",
        init_gen=FakerGenerator(method="name",
                                seed=example_circus.seeder.next()))

    person.create_attribute(
        "age",
        init_gen=NumpyRandomGenerator(
            method="normal", loc="35", scale="5",
            seed=example_circus.seeder.next()))

    return example_circus


example = create_circus_with_actor()

hello_world = example.create_action(
    name="hello_world",
    initiating_actor=example.actors["person"],
    actorid_field="PERSON_ID",

    timer_gen=ConstantDependentGenerator(value=1)
)

hello_world.set_operations(

    ConstantGenerator(value="hello world")
        .ops
        .generate(named_as="MESSAGE"),

    FieldLogger(log_id="hello")

)

example.run(
    duration=pd.Timedelta("48h"),
    log_output_folder="output/example3",
    delete_existing_logs=True
)

with open("output/example3/hello.csv") as log:
    logging.info("some produced logs: \n\n" + "".join(log.readlines(10)[:10]))






